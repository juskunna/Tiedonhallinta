"""
Toteuta tehtävässä annetun tietokannan päälle ohjelma, joka toteuttaa alla pyydetyt toiminnot.
Tässä tehtävässä käytettävä tietokantarakenne ja data on sama kuin tehtävässä 2, joten voit käyttää
sen kaaviota apuna.
1. Opiskelijan lisääminen tietokantaan käyttäjän syötteen perusteella
a. Kysy tarvittavat tiedot ja lisää opiskelija tietokantaan. Tulosta onnistuneen
lisäämisen jälkeen opiskelijan ID
2. Opiskelijan haku etunimellä ja sukunimellä käyttäjän syötteen perusteella
a. Tulosta opiskelijan tiedot (nimi, id, kurssisuoritukset)
b. Tulosta opiskelijan kurssisuoritukset, näytä kurssin nimi, arvosana ja suorituspäivä ja
opettaja
3. Anna opiskelijan tiedoissa mahdollisuus lisätä kurssisuoritus tietokantaan
a. Riittää että annetaan kurssin koodi (ID) ja arvosana sekä opiskelijan tunniste. Jos
opiskelijan tiedot ovat avoinna, voidaan hyödyntää suoraan valitun opiskelijan
tunnistetta.
i. Käytä tätä hetkeä suorittamisajankohtana (now)
ii. Voit halutessasi tulostaa vaihtoehdot ruudulle
b. Jos opiskelijalla on olemassa oleva suoritus, päivitä se uusilla tiedoilla sekä tämän
hetken aikaleimalla.
4. Toteuta kaikki kyselyt siten, että SQL-injektiot eivät ole mahdollisia
"""

# Otetaan käyttöön mysql-kirjasto
import mysql.connector

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


# ---- Funktiot

# Opiskelijan lisäyksen funktio
def student_add():
    # first_name, last_name, location
    f_name = input("Anna etunimi ")
    l_name = input("Anna sukunimi ")
    location = input("Anna paikkakunta ")

    # Lisätään opiskelija tietokantaan
    cursor.execute("INSERT INTO students (first_name, last_name, location) VALUES (%s, %s, %s)", (f_name, l_name, location))

    # Haetaan viimeisen lisäyksen ID
    student_id = cursor.lastrowid
    print(f"Lisätty opiskelija ID:llä {student_id}")

    # Tehdään muutoksista pysyviä
    db_conn.commit()

def student_search():
    pass

def student_update():
    pass

# ---- Toiminnon valinta

choose_action = ""
while choose_action not in ("l", "h", "p" ):
    choose_action = input("L: Opiskelijan lisäys\nH: Opiskelijan haku\nP: Opiskelijan tietojen päivitys?\n [L/H/P] ")
    choose_action = choose_action.lower()

    if choose_action == "l":
        # Opiskelijan lisäys
        student_add()
    elif choose_action == "h":
        # Elokuvan haku
        student_search()
    elif choose_action == "p":
        student_update()
    else:
        # Tuntematon haku
        print("Tuntematon valinta")
