def get_grade_data():
    student_id = student_data[0]['id']

    try:
        # Haetun oppilaan ID:n perusteella tulostetaan kurssisuoritukset.
        cursor2.execute(
            "SELECT course.name, grades.grade, grades.completion_date, CONCAT_WS(' ', teachers.first_name, teachers.last_name) AS teacher FROM course JOIN grades ON grades.course_id = course.course_id JOIN teachers ON teachers.teacher_id = course.teacher JOIN students ON students.id = grades.student_id WHERE students.id = %s",
            (student_id,))
        course_data = cursor2.fetchall()

    except mysql.connector.Error as err:
        print(f"Virhe kurssisuoritusten haussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")