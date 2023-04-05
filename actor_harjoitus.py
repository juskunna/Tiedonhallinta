"""
1. Toteuta komentorivisovellus, jolla voit hakea sakila-tietokannasta näyttelijöitä etunimen ja
sukunimen mukaan
2. Listaa näyttelijän elokuvat, jos näyttelijä löytyy
3. Muokkaa sovellusta siten, että sillä voidaan lisätä elokuva ja sen näyttelijät tietokantaan
a. Kysy elokuvan tiedot
b. Kysy näyttelijän tiedot
i. Alkuvaiheessa riittää yhden näyttelijän tiedot
ii. Laajenna siten että näyttelijöitä voi olla useampia
c. Lisää elokuva tietokantaan ja lisää elokuvalle näyttelijät, jos he eivät jo löydy
tietokannasta
i. Jos näyttelijän nimi on jo tietokannassa, käytä olemassa olevaa uudelleen
lisäämisen sijaan.
4. Mahdollista elokuvien hakeminen ja poistaminen
"""

import mysql.connector
from mysql.connector import errorcode

try:
    db_conn = mysql.connector.connect(
        user="root",
        password="",
        host="127.0.0.1",
        database="sakila"
    )
except mysql.connector.Error as err:
    print(f"MySQL-yhdistämisessä virhe: {err.errno}")

cursor = db_conn.cursor(dictionary=True)
cursor2 = db_conn.cursor(dictionary=True)

first_name = input("Anna näyttelijän etunimi ")
last_name = input("Anna näyttelijän sukunimi ")

try:
    cursor.execute("SELECT * FROM actor WHERE first_name=%s OR last_name=%s", (first_name, last_name))
    data = cursor.fetchall()

    for row in data:
        print(f"{row['actor_id']}: {row['first_name']} {row['last_name']}")

        # Haetaan myös näyttelijän elokuvat
        cursor2.execute("SELECT film.title FROM `film_actor` JOIN film ON film.film_id = film_actor.film_id WHERE film_actor.actor_id = %s", (row['actor_id'],))

        film_data = cursor2.fetchall()
        for film_row in film_data:
            print(f"--- {film_row['title']}")

except mysql.connector.Error as err:
    print(f"Virhe näyttelijähaussa: {err.errno}")
    print(f"Virheviesti: {err.msg}")
