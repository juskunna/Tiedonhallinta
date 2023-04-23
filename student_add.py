def student_add():
    # first_name, last_name, location
    f_name = input("Anna etunimi ")
    l_name = input("Anna sukunimi ")
    location = input("Anna paikkakunta \n")

    # Lisätään opiskelija tietokantaan
    cursor.execute("INSERT INTO students (first_name, last_name, location) VALUES (%s, %s, %s)", (f_name, l_name, location))

    # Haetaan viimeisen lisäyksen ID
    student_id = cursor.lastrowid
    print(f"Lisätty opiskelija ID:llä {student_id}\n")

    # Tehdään muutoksista pysyviä
    db_conn.commit()