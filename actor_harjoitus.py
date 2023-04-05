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

# ---- Funktiot
def actor_search():
    # Kysytään käyttäjältä hakuehdot
    first_name = input("Anna näyttelijän etunimi ")
    last_name = input("Anna näyttelijän sukunimi ")

    try:
        cursor.execute("SELECT * FROM actor WHERE first_name=%s OR last_name=%s", (first_name, last_name))
        data = cursor.fetchall()

        for row in data:
            print(f"{row['actor_id']}: {row['first_name']} {row['last_name']}")

            # Haetaan myös näyttelijän elokuvat
            cursor2.execute(
                "SELECT film.film_id, film.title FROM `film_actor` JOIN film ON film.film_id = film_actor.film_id WHERE film_actor.actor_id = %s",
                (row['actor_id'],))

            film_data = cursor2.fetchall()
            for film_row in film_data:
                print(f"--- {film_row['film_id']} - {film_row['title']}")

    except mysql.connector.Error as err:
        print(f"Virhe näyttelijähaussa: {err.errno}")
        print(f"Virheviesti: {err.msg}")

def film_add():
    # title, descrition, release_year, length, language_id
    m_title = input("Elokuvan nimi: ")
    m_description = input("Elokuvan kuvaus: ")
    m_release_year = input("Elokuvan vuosi: ")
    m_length = input("Elokuvan pituus: ")

    # Tallennetaan elokuva tietokantaan
    cursor.execute("INSERT INTO film (title, description, release_year, length, language_id) VALUES (%s, %s, %s, %s, %s)", (m_title, m_description, m_release_year, m_length, 1))

    movie_id = cursor.lastrowid

    print(f"Lisätty elokuva ID:llä {movie_id}")

    # Kysytään näyttelijät, tyhjät nimet -> lopettaa
    actors = []
    f_name = ""
    l_name = ""
    print("Anna näyttelijöiden nimet. Tyhjä lopettaa")

    while True:
        f_name = input("Etunimi ")
        l_name = input("Sukunimi ")
        if f_name == "" and l_name == "":
            break
        else:
            actors.append({
                'first_name': f_name,
                'last_name': l_name
            })

    for actor in actors:
        # Tarkistetaan onko tietokannassa näyttelijää
        # jos on, niin käytetään olemassa olevaa
        # jos ei, lisätään ja käytetään sitä
        cursor.execute("SELECT actor_id FROM actor WHERE first_name = %s AND last_name = %s", (actor['first_name'], actor['last_name']))
        actor_data = cursor.fetchall()
        lkm = cursor.rowcount
        # Jos löytyy
        if lkm >= 1:
            new_actor_id = actor_data[0]['actor_id']
        # Jos ei löydy, lisätään uusi
        else:
            cursor.execute("INSERT INTO actor (first_name, last_name) VALUES (%s, %s)", (actor['first_name'], actor['last_name']))
            new_actor_id = cursor.lastrowid
            print(f"Lisättiin uusi: {new_actor_id}")

        # Lisätään näyttelijä elokuvalle
        cursor.execute("INSERT INTO film_actor (actor_id, film_id) VALUES (%s, %s)", (new_actor_id, movie_id))

    # Tehdään muutoksista pysyviä
    db_conn.commit()

def film_search():
    search_word = input("Anna hakusana: ")

    cursor.execute("SELECT * FROM film WHERE title LIKE CONCAT('%', %s '%') OR description LIKE CONCAT('%', %s '%')", (search_word, search_word))

    search_result = cursor.fetchall()

    for result in search_result:
        print(f"{result['film_id']} - {result['title']} - {result['description']}")

def movie_delete():
    movie_id = input("Anna poistettavan elokuvan ID ")

    # Poistetaan ensin viittaukset elokuvaan film_actor talusta jotta elokuva poistuu
    cursor.execute("DELETE FROM film_actor WHERE film_id = %s", (movie_id,))
    # Poistetaan itse elokuva
    cursor.execute("DELETE FROM film WHERE film_id = %s", (movie_id,))

    db_conn.commit()
    print(f"Elokuva ID:llä {movie_id} poistettu!")

# ---- Valikko
choose = ""
while choose not in ("l", "h", "p", "n" ):
    choose = input("L: Elokuvan lisäys\nH: Elokuvan haku\nP: Elokuvan poisto\nN: Näyttelijän haku?\n [L/H/P/N] ")
    choose = choose.lower()

if choose == "l":
    # Elokuvan lisäys
    film_add()
elif choose == "h":
    # Elokuvan haku
    film_search()
elif choose == "n":
    actor_search()
elif choose == "p":
    movie_delete()
else:
    # Tuntematon haku
    print("Tuntematon valinta")
