import datetime
# Otetaan käyttöön mysql-kirjasto
import mysql.connector
import get_student_data

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


def show_student_data(student_data):

    student_id = student_data[0]['id']

    try:
        # Haetun oppilaan ID:n perusteella tulostetaan kurssisuoritukset.
        cursor2.execute("SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON students.id = grades.student_id WHERE students.id = %s", (student_id,))
        course_data = cursor2.fetchall()

    except mysql.connector.Error as err:
        print(f"Virhe kurssisuoritusten haussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

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

