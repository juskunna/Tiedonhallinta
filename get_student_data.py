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
            print(f"\n{student['id']:5} {student['first_name']} {student['last_name']}")

        return student_data
    except mysql.connector.Error as err:
        print(f"Virhe opiskelijahaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

