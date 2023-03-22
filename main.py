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
    cursor.execute("SELECT * FROM film LIMIT 3")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_SYNTAX_ERROR
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
#     # Tulostetaan yskittäiset tulokset komentoriville, [*] indexillä voidaan tulostaa vain haluttu sarake.
#     print(result)


# Haetaan kaikki tulokset kerralla yhteen muuttujaan
data = cursor.fetchall()
for row in data:
    print(row['title'], row['release_year'])

# Tulostetaan vielä rivimäärä
print("Yhteensä: ", cursor.rowcount)

# Suljetaan yhteys tietokantaan
db_conn.close()


# Kysely voidaan muodostaa myös yhdistämällä ohjelmallisesti kyselyn lausekkeen
# osia merkkijonoksi, joka muodostaa halutun kyselyn
#query = "SELECT * FROM actor WHERE first_name = '%s' AND last_name = '%s;" % (firstname, lastname)

#query = f"SELECT * FROM actor WHERE first_name = '{firstname}' AND last_name = '{lastname}'"
