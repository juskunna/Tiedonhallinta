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
    print(f"Lisätty opiskelija ID:llä {student_id}")

    # Tehdään muutoksista pysyviä
    db_conn.commit()

# Opiskelijan haun funktio
def student_search():
    # Kysytään käyttäjältä haettavan opiskelijan tiedot
    f_name = input("Anna opiskelijan etunimi ")
    l_name = input("Anna opiskelijan sukunimi ")

    try:
        # Haetaan students-taulusta opiskelijan ID ja nimi
        cursor.execute("SELECT * FROM students WHERE first_name=%s AND last_name=%s ", (f_name, l_name))
        student_data = cursor.fetchall()

        # Käsitellään haettu tieto.
        student_ids = []
        # Tulostetaan ensin oppilaan ID ja nimi.
        for student in student_data:
            print(f"\n{student['id']:5} {student['first_name']} {student['last_name']}")
            student_ids.append(student['id'])

        # Haetun oppilaan ID:n perusteella tulostetaan kurssisuoritukset.
        for student_id in student_ids:
            cursor2.execute("SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON students.id = grades.student_id WHERE students.id = %s", (student_id,))
            course_data = cursor2.fetchall()

        # Muotoiltu tuloste näyttämään siistiltä.
        print("--Kurssisuoritukset--")
        print("{:20} {:5} {:20} {}".format("Kurssi", "Arvosana", "Suorituspäivä", "Opettaja"))
        for course in course_data:
            print("{:20} {:>5} {:>15} {:>20}".format(course['name'], course['grade'], course['completion_date'].strftime('%d.%m.%Y'), course['teacher']))


    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

# Opiskelijan tietojen päivityksen funktio
def student_update():
    pass

# ---- Toiminnon valinta

while True:
    choose_action = input("Haluatko\nL: Lisätä opiskelijan\nH: Hakea opiskelijan tiedot\nP: Päivittää opiskelijan suorituksia\nQ: Lopettaa ohjelman?\n[L/H/P/Q] ")
    choose_action = choose_action.lower()

    if choose_action == "l":
        # Opiskelijan lisäys
        student_add()
    elif choose_action == "h":
        # Opiskelijan haku
        student_search()
    elif choose_action == "p":
        # Opiskelijan tietojen päivitys
        student_update()
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