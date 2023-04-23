# Otetaan käyttöön mysql tietokantakirjasto
import mysql.connector
from mysql.connector import errorcode

# Luodaan yhteys tietokantaan, tässä esimerkkinä tunneilla käytetty sakila
try:
    db_conn = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        database='sakila'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Ei pääsyä")
    else:
        print(f"MySQL-yhdistämisessä virhe: {err.errno}")
    exit()

# Kysely tietokannasta tehtään kursorilla joka saadaan tietokannan yhteys-objektista
# cursor = db_conn.cursor()

# Jos halutaan helpottaa tulosten käsittelyä voidaan tulos ottaa ulos myös dictionaryna

cursor = db_conn.cursor(dictionary=True)

# Suoritetaan kysely
try:

    cursor.execute("SELECT * FROM actor ORDER BY last_update DESC LIMIT 10")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_SYNTAX_ERROR:
        print("Syntaksivirhe!")
    else:
        print(f"Virhe suoritettaessa kyselyä: {err.errno}")
        print(f"Virheviesti: {err.msg}")
    exit()

# for result in cursor:
#     # tulostetaan yksittäinen result-objekti komentoriville
#     print(result['title'], result['release_year'])
#
# # Käydään tulokset läpi yksitellen
# for result in cursor:
#     # Tulostetaan yksittäiset tulokset komentoriville, [*] indexillä voidaan tulostaa vain haluttu sarake.
#     print(result)


# Haetaan kaikki tulokset kerralla yhteen muuttujaan
data = cursor.fetchall()
for row in data:
    print(row['actor_id'], row['first_name'], row['last_name'])

# Tulostetaan vielä rivimäärä
print("Yhteensä: ", cursor.rowcount)

# Lisätään itsemme näyttelijäksi
print("Anna lisättävän näyttelijän nimi")
etunimi = input("Etunimi: ")
sukunimi = input("Sukunimi: ")

# sql = "INSERT INTO actor (first_name, last_name) VALUES ('%s', '%s');" % (etunimi, sukunimi)
# print(sql)

try:
    #    db_conn.start_transaction()
    cursor.execute("INSERT INTO actor (first_name, last_name) VALUES (%s, %s);" , (etunimi, sukunimi))
except mysql.connector.Error as err:
    print(f"Virhe lisättäessä tietoa: {err.errno}")
    print(f"Virheviesti: {err.msg}")
    db_conn.rollback()
else:
    # Suoritetaan vain jos virhettä ei tapahdu

    print(f"Viimeisin lisätty ID: {cursor.lastrowid}")
    db_conn.commit()

# Suljetaan yhteys tietokantaan
db_conn.close()

# Kysely voidaan muodostaa myös yhdistämällä ohjelmallisesti kyselyn lausekkeen
# osia merkkijonoksi, joka muodostaa halutun kyselyn
# query = "SELECT * FROM actor WHERE first_name = '%s' AND last_name = '%s;" % (firstname, lastname)

# query = f"SELECT * FROM actor WHERE first_name = '{firstname}' AND last_name = '{lastname}'"



def get_student_data():
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

        # Palautetaan opiskelijan ID:t, jotta niitä voidaan käyttää kurssisuoritusten haussa.
        return student_ids

    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

def show_student_data(student_ids):
    try:
        for student_id in student_ids:
            # Haetun oppilaan ID:n perusteella tulostetaan kurssisuoritukset.
            cursor2.execute("SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON students.id = grades.student_id WHERE students.id = %s", (student_id,))
            course_data = cursor2.fetchall()

            # Muotoiltu tuloste näyttämään siistiltä.
            print(f"\n--Opiskelijan {student_id} kurssisuoritukset--")
            print("{:20} {:5} {:20} {}".format("Kurssi", "Arvosana", "Suorituspäivä", "Opettaja"))
            for course in course_data:
                print("{:20} {:>5} {:>15} {:>20}".format(course['name'], course['grade'], course['completion_date'].strftime('%d.%m.%Y'), course['teacher']))

            add_course = input("\nHaluatko lisätä uuden kurssisuorituksen tälle opiskelijalle? (K/E) ")
            if add_course.lower() == 'k':
                course_add(student_id)
            elif add_course.lower() == 'e':
                return

    except mysql.connector.Error as err:
        print(f"Virhe kurssisuoritusten haussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")





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

        add_course = input("\nHaluatko lisätä uuden kurssisuorituksen tälle opiskelijalle? (K/E) ")
        if add_course.lower() == 'k':
            course_add(student_id)
        elif add_course.lower() == 'e':
            return

    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

        def student_update():

            new_date = datetime.datetime.now().strftime('%Y-%m-%d')

            # Pyydetään käsiteltävän opiskelijan nimi
            f_name = input("Anna oppilaan etuimi: ")
            l_name = input("Anna oppilaan sukunimi: ")

            try:
                # Haetaan students-taulusta opiskelijan ID ja nimi
                cursor.execute("SELECT * FROM students WHERE first_name=%s AND last_name=%s", (f_name, l_name))
                student_data = cursor.fetchall()

                # Tulostetaan ensin oppilaan ID ja nimi.
                for student in student_data:
                    print(f"\n{student['id']:5} {student['first_name']} {student['last_name']}\n")
                    # Tallennetaan oppilaan id muuttujaan kurssin hakua varten.
                    selected_student = student_data[0]['id']

            except mysql.connector.Error as err:
                print(f"Virhe opiskelijahaussa: {err.errno}")
                print(f"Virheviesti: {err.msg}")

            # Pyydetään käyttäjältä käsiteltävän kurssin id.
            print(f"Kurssit:\n1: {courses[0]}\n2: {courses[1]}\n3: {courses[2]}\n4: {courses[3]}\n5: {courses[4]}\n")
            course_id = int(input("Anna kurssin ID: "))

            course_name = courses[course_id]

            # Haetaan tietokannasta annetun kurssin tiedot valitun oppilaan osalta.
            cursor.execute("SELECT * FROM grades WHERE student_id = %s AND course_id = %s",
                           (selected_student, course_id))
            student_course = cursor.fetchall()

            # Tarkistetaan haettujen rivien määrä
            lkm = cursor.rowcount

            # Jos haettuja rivejä löytyy, tarkoittaa se että oppilaalla on jo olemassa oleva suoritus kurssista, jota voidaan päivittää. Muuten lisätään uusi.
            if lkm >= 1:

                # Ilmoitetaan löyvyvästä suorituksesta käyttäjälle arvosanan kera.
                print(
                    f"Oppilaalta {student['first_name']} {student['last_name']} löytyy kurssin {course_name} suoritus arvosanalla {student_course[0]['grade']}'.\n")
                # Tiedustellaan halutaanko suoritusta päivittää.
                update_grade = input("Haluatko päivittää suorituksen? [K/E] ")

                # Jos päivitetään, pyydetään antamaan uusi arvosana.
                if update_grade.lower() == 'k':
                    # Tallennetaan uusi arvosana sekä tämän hetken aikaleimat muuttujiin
                    new_grade = input("Anna uusi arvosana (0-5): ")

                    cursor2.execute(
                        "UPDATE grades SET grade = %s AND completion_date = %s WHERE student_id = %s AND course_id = %s",
                        (new_grade, new_date, selected_student, course_id))

                    print(
                        f"Opiskelijan {student['first_name']} {student['last_name']}, {course_name}-kurssin arvosana on päivitetty.\n")

                elif update_grade.lower() == 'e':
                    return
            else:
                new_grade2 = input("Anna Kurssin arvosana (0-5): ")
                cursor2.execute(
                    "INSERT INTO grades (student_id, course_id, grade, completion_date) VALUES (%s, %s, %s, %s)",
                    (selected_student, course_id, new_grade2, new_date))
                grade_id = cursor2.lastrowid

            db_conn.commit()
            print(
                f"Opiskelijalle {student['first_name']} {student['last_name']} lisätty suoritus kurssille: {course_name} tunnuksella: {grade_id}\n")
