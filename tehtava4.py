"""
Toteuta tehtävässä annetun tietokannan päälle ohjelma, joka toteuttaa alla pyydetyt toiminnot.
Tässä tehtävässä käytettävä tietokantarakenne ja data on sama kuin tehtävässä 2, joten voit käyttää
sen kaaviota apuna.
X1. Opiskelijan lisääminen tietokantaan käyttäjän syötteen perusteella
Xa. Kysy tarvittavat tiedot ja lisää opiskelija tietokantaan. Tulosta onnistuneen
Xlisäämisen jälkeen opiskelijan ID
2. Opiskelijan haku etunimellä ja sukunimellä käyttäjän syötteen perusteella
a. Tulosta opiskelijan tiedot (nimi, id, kurssisuoritukset)
b. Tulosta opiskelijan kurssisuoritukset, näytä kurssin nimi, arvosana ja suorituspäivä ja
opettaja
3. Anna opiskelijan tiedoissa mahdollisuus lisätä kurssisuoritus tietokantaan
a. Riittää että annetaan kurssin koodi (ID) ja arvosana sekä opiskelijan tunniste. Jos
opiskelijan tiedot ovat avoinna, voidaan hyödyntää suoraan valitun opiskelijan
tunnistetta.
i. Käytä tätä hetkeä suorittamisajankohtana (now)
ii. Voit halutessasi tulostaa vaihtoehdot ruudulle
b. Jos opiskelijalla on olemassa oleva suoritus, päivitä se uusilla tiedoilla sekä tämän
hetken aikaleimalla.
4. Toteuta kaikki kyselyt siten, että SQL-injektiot eivät ole mahdollisia
"""

import datetime
# Otetaan käyttöön mysql-kirjasto
import mysql.connector

# Yhdistetään tietokantaan
try:
    db_conn = mysql.connector.connect(
        user="root",
        password="",
        host="127.0.0.1",
        database="tehtava4"
    )
except mysql.connector.Error as err:
    print(f"MySQL-yhdistämisessä virhe: {err.errno}")

# Kyselyitä varten cursor
cursor = db_conn.cursor(dictionary=True)
cursor2 = db_conn.cursor(dictionary=True)

courses = ["Tiedonhallinta", "Advanced Linux", "Peliohjelmointi", "Tietokonetekniikka", "Oppimaan oppiminen"]
new_date = datetime.datetime.now().strftime('%Y-%m-%d')

# ---- Funktiot

# Opiskelijan lisäyksen funktio
def student_add():
    # first_name, last_name, location
    f_name = input("Anna etunimi ")
    l_name = input("Anna sukunimi ")
    location = input("Anna paikkakunta ")

    # Lisätään opiskelija tietokantaan
    cursor.execute("INSERT INTO students (first_name, last_name, location) VALUES (%s, %s, %s)", (f_name, l_name, location))

    # Haetaan viimeisen lisäyksen ID
    student_id = cursor.lastrowid
    print(f"Lisätty opiskelija ID:llä {student_id}\n")

    # Tehdään muutoksista pysyviä
    db_conn.commit()


# Opiskelijan haun funktio
def get_student_data():
    # Kysytään käyttäjältä haettavan opiskelijan tiedot
    f_name = input("Anna opiskelijan etunimi ")
    l_name = input("Anna opiskelijan sukunimi ")

    try:
        # Haetaan students-taulusta opiskelijan ID ja nimi
        cursor.execute("SELECT * FROM students WHERE first_name=%s AND last_name=%s ", (f_name, l_name))
        student_data = cursor.fetchall()

        # Käsitellään haettu tieto.
        # Tulostetaan ensin oppilaan ID ja nimi.
        for student in student_data:
            print(f"\n{student['id']:5} {student['first_name']} {student['last_name']}\n")

        # Palautetaan lopuksi haettu data jotta saadaan se muiden funktioiden käyttöön
        return student_data

    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

# Haetun oppilaan kurssisuoritusten näytön funktio
def show_student_data(student_data):

    # Otetaan get_student_data() hakemasta tiedosta oppilaan id
    student_id = student_data[0]['id']

    try:
        # Haetun oppilaan ID:n perusteella tulostetaan kurssisuoritukset.
        cursor.execute("SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON students.id = grades.student_id WHERE students.id = %s", (student_id,))
        course_data = cursor.fetchall()

        # Muotoiltu tuloste näyttämään siistiltä.
        print(f"\n--Opiskelijan {student_id} kurssisuoritukset--")
        print("{:20} {:5} {:20} {}".format("Kurssi", "Arvosana", "Suorituspäivä", "Opettaja"))
        for course in course_data:
            print("{:20} {:>5} {:>15} {:>20}".format(course['name'], course['grade'], course['completion_date'].strftime('%d.%m.%Y'), course['teacher']))

        add_course = input("\nHaluatko lisätä uuden kurssisuorituksen tälle opiskelijalle? (K/E) ")
        if add_course.lower() == 'k':
            student_update(student_data)
        elif add_course.lower() == 'e':
            return

    except mysql.connector.Error as err:
        print(f"Virhe kurssisuoritusten haussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")


def get_course_id(courses):
    # Pyydetään käyttäjältä käsiteltävän kurssin id.
    print(f"Kurssit:\n1: {courses[0]}\n2: {courses[1]}\n3: {courses[2]}\n4: {courses[3]}\n5: {courses[4]}\n")
    course_id = int(input("Anna kurssin ID: "))
    course_name = courses[course_id - 1]

    return course_id, course_name


# Opiskelijan tietojen päivityksen funktio
def student_update(student_data):

    student_ids = student_data[0]['id']
    student_fname = student_data[0]['first_name']
    student_lname = student_data[0]['last_name']

    selected_course_id, selected_course_name = get_course_id(courses)

    # Haetaan tietokannasta annetun kurssin tiedot valitun oppilaan osalta.
    cursor.execute("SELECT * FROM grades WHERE student_id = %s AND course_id = %s", (student_ids, selected_course_id))
    student_course = cursor.fetchone()
    if student_course is not None:
        grade = student_course['grade']

    # Tarkistetaan haettujen rivien määrä
    lkm = cursor.rowcount

    # Jos haettuja rivejä löytyy, tarkoittaa se että oppilaalla on jo olemassa oleva suoritus kurssista, jota voidaan päivittää. Muuten lisätään uusi.
    if lkm >= 1:

        # Ilmoitetaan löyvyvästä suorituksesta käyttäjälle arvosanan kera.
        print(f"Oppilaalta {student_fname} {student_lname} löytyy kurssin {selected_course_name} suoritus arvosanalla {grade}'.\n")
        # Tiedustellaan halutaanko suoritusta päivittää.
        update_grade = input("Haluatko päivittää suorituksen? [K/E] ")

        # Jos päivitetään, pyydetään antamaan uusi arvosana.
        if update_grade.lower() == 'k':
            # Tallennetaan uusi arvosana sekä tämän hetken aikaleimat muuttujiin
            new_grade = input("Anna uusi arvosana (0-5): ")

            cursor2.execute("UPDATE grades SET grade = %s, completion_date = %s WHERE student_id = %s AND course_id = %s", (new_grade, new_date, student_ids, selected_course_id))

            print(f"Opiskelijan {student_fname} {student_lname}, {selected_course_name}-kurssin arvosana on päivitetty.\n")

        elif update_grade.lower() == 'e':
            return
    else:
        new_grade2 = input("Anna Kurssin arvosana (0-5): ")
        cursor2.execute("INSERT INTO grades (student_id, course_id, grade, completion_date) VALUES (%s, %s, %s, %s)", (student_ids, selected_course_id, new_grade2, new_date))
        grade_id = cursor2.lastrowid
        print(f"Opiskelijalle {student_fname} {student_lname} lisätty suoritus kurssille: {selected_course_name} tunnuksella: {grade_id}\n")

    db_conn.commit()


# ---- Toiminnon valinta

while True:
    choose_action = input("Haluatko\nL: Lisätä opiskelijan\nH: Hakea opiskelijan tiedot\nP: Päivittää\Lisätä opiskelijan suorituksia\nQ: Lopettaa ohjelman?\n[L/H/P/Q] ")
    choose_action = choose_action.lower()

    if choose_action == "l":
        # Opiskelijan lisäys
        student_add()
    elif choose_action == "h":
        # Opiskelijan haku
        student_ids = get_student_data()
        if student_ids:
            show_student_data(student_ids)
    elif choose_action == "p":
        # Opiskelijan tietojen päivitys
        student_ids = get_student_data()
        if student_ids:
         student_update(student_ids)
    elif choose_action == "q":
        # Lopetus
        print("Ohjelma suljetaan...")
        break
    else:
        # Virheellinen syöte
        try:
            raise ValueError("Tuntematon valinta\n")
        except ValueError as e:
            print(f"Virhe: {e}")


# Suljetaan yhteys tietokantaan
db_conn.close()