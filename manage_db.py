import sqlite3
import os
from datetime import date

def crea_db(conn):
    conn.execute("""CREATE TABLE GIOCATORE
            (NOME  TEXT     PRIMARY KEY         
            );""")
    conn.execute("""CREATE TABLE PARTITA
            (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
            AVVERSARIO     TEXT   ,
            LOCATION        TEXT,
            DATA_PARTITA    DATE   ,
            GOL_SUBITI      INT,
            PIU_TENTATI     INT,
            PIU_REALIZZATI  INT,
            RITMO_ATT           INT,
            RITMO_DEF           INT,
            MENO_TENTATI           INT,
            MENO_SUBITI           INT
            );""")
    conn.execute("""CREATE TABLE PERSONALI
            (NOME_GIOCATORE INT,
            ID_PARTITA INT,
            GOL             INT,
            TIRI            INT,
            ASSIST          INT,
            ESPULSIONI      INT,
            RECUPERI        INT,
            STOPPATE        INT,
            PLUSMINUS       INT,    
            PALLE_PERSE     INT,
            FOREIGN KEY(NOME_GIOCATORE) REFERENCES GIOCATORE(NOME),
            FOREIGN KEY(ID_PARTITA) REFERENCES PARTITA(ID)
            );""")
    print("Tables created successfully")

def mostra_db(conn):
    cursor = conn.execute("SELECT * from GIOCATORE")
    print(cursor.fetchall())
    cursor = conn.execute("SELECT * from PARTITA")
    print(cursor.fetchall())
    cursor = conn.execute("SELECT * from PERSONALI")
    print(cursor.fetchall())

def delete_all_data(conn):
    c = conn.cursor()
    # delete all rows from table
    c.execute('DELETE FROM giocatore;',);
    print('We have deleted', c.rowcount, 'records from the table.')
    conn.commit()
    c.execute('DELETE FROM partita;',);
    print('We have deleted', c.rowcount, 'records from the table.')
    conn.commit()
    c.execute('DELETE FROM personali;',);
    print('We have deleted', c.rowcount, 'records from the table.')
    conn.commit()

def delete_personal_stats(conn):
    c = conn.cursor()
    c.execute('DELETE FROM personali;',);
    print('We have deleted', c.rowcount, 'records from the table.')
    conn.commit()

def delete_partite_stats(conn):
    c = conn.cursor()
    c.execute('DELETE FROM partita;',);
    print('We have deleted', c.rowcount, 'records from the table.')
    conn.commit()

def dump():
    today = str(date.today())
    os.system("cp instance/stats.db instance/stats_dump"+today+".db")

conn = sqlite3.connect('instance/stats.db')
print("Opened database successfully")

while 1:
    i = input("1: crea\n2: mostra\n3: elimina tutti i dati\n4: elimina personal stats\n5: elimina partite\n6: dump\n")
    match i:
        case "1":
            crea_db(conn)
        case "2": 
            mostra_db(conn) 
        case "3": 
            delete_all_data(conn)   
        case "4":
            delete_personal_stats(conn)         
        case "5":
            delete_partite_stats(conn)   
        case "6":
            dump()      


conn.close()

