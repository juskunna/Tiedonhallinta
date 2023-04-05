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
