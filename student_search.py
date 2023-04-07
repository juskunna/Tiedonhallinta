def student_search():
    # Kysytään käyttäjältä haettavan opiskelijan tiedot
    f_name = input("Anna opiskelijan etunimi ")
    l_name = input("Anna opiskelijan sukunimi ")

    try:
        # Haetaan students-taulusta opiskelijan ID ja nimi
        cursor.execute("SELECT * FROM students WHERE first_name=%s AND last_name=%s ", (f_name, l_name))
        student_data = cursor.fetchall()

        student_ids = []
        for student in student_data:
            print(f"{student['id']:5} {student['first_name']} {student['last_name']}")
            student_ids.append(student['id'])

        for student_id in student_ids:
            cursor.execute("SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON grades.student_id = students.id WHERE students.id = %s", (student_id,))
            course_data = cursor.fetchall()

            print("\n--Kurssisuoritukset")
            print("{:20} {:5} {:20} {}".format("Kurssi", "Arvosana", "Suorituspäivä", "Opettaja"))
            for course in course_data:
                print("{:20} {:<5} {:>15} {:>20}".format(course['name'], course['grade'], course['completion_date'].strftime('%d.%m.%Y'), course['teacher']))

    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")
