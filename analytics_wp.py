import sqlite3

# classifica dati grezzi
def classifica_grezza():
    conn = sqlite3.connect('instance/stats.db')
    cursor = conn.execute("""
    SELECT nome_giocatore, count(*) as partite, sum(gol), sum(tiri), sum(assist), sum(recuperi), sum(stoppate), sum(espulsioni), sum(palle_perse), sum(plusminus)
    FROM personali
    GROUP BY nome_giocatore
    ORDER BY sum(gol) DESC""")
    ris = cursor.fetchall()
    conn.close()
    return ris

# classifica stats per partita
def classifica_partita():    
    conn = sqlite3.connect('instance/stats.db')
    cursor = conn.execute("""
    SELECT nome_giocatore, count(*), round(sum(gol)*1.0/count(*), 2), round(sum(tiri)*1.0/count(*), 2), round(sum(assist)*1.0/count(*), 2), round(sum(recuperi)*1.0/count(*), 2), round(sum(stoppate)*1.0/count(*), 2), round(sum(espulsioni)*1.0/count(*), 2), round(sum(palle_perse)*1.0/count(*), 2), round(sum(plusminus)*1.0/count(*), 2)
    FROM personali
    GROUP BY nome_giocatore
    ORDER BY sum(gol) DESC""")
    ris = cursor.fetchall()
    conn.close()
    return ris

# stats avanzate
def avanzate():
    conn = sqlite3.connect('instance/stats.db')
    cursor = conn.execute("""
    SELECT nome_giocatore, 
        round(sum(plusminus)*100.0/sum(ritmo), 2) as net_rating,
        round(sum(gol)*100.0/sum(tiri), 2) as goal_perc,
        round((sum(gol)+sum(assist)+sum(recuperi)+sum(stoppate)-sum(espulsioni)-sum(palle_perse))*1.0/count(*), 2) as eff,
        round((sum(gol)+sum(assist))*100.0/sum(ritmo), 2) as att,
        round((sum(stoppate)+sum(recuperi))*100.0/sum(ritmo), 2) as def,
        round(sum(assist)*1.0/sum(palle_perse), 2) as pm
    FROM personali INNER JOIN partita ON partita.id = personali.id_partita
    GROUP BY nome_giocatore
    ORDER BY net_rating DESC""")
    ris = cursor.fetchall()
    conn.close()
    return ris

# tutte le statistiche di squadra per partita
def squadra_grezza():
    conn = sqlite3.connect('instance/stats.db')
    cursor = conn.execute("""
    SELECT avversario, location, data_partita, sum(gol), gol_subiti, round(piu_realizzati*100.0/piu_tentati, 2), round(meno_subiti*100.0/meno_tentati, 2), ritmo
    FROM personali INNER JOIN partita ON partita.id = personali.id_partita
    GROUP BY partita.id
    ORDER BY data_partita DESC""")
    ris = cursor.fetchall()
    conn.close()
    return ris

# stats di squadra per partita
def medie_squadra():
    conn = sqlite3.connect('instance/stats.db')
    cursor = conn.execute("""
    SELECT round(avg(gol_fatti), 2), round(avg(gol_subiti), 2), round(avg(perc_piu), 2), round(avg(perc_meno), 2), round(avg(ritmo), 2)
    FROM (
        SELECT sum(gol) as gol_fatti, gol_subiti, 
                round(piu_realizzati*100.0/piu_tentati, 2) as perc_piu, 
                round(meno_subiti*100.0/meno_tentati, 2) as perc_meno, ritmo
        FROM personali INNER JOIN partita ON partita.id = personali.id_partita
        GROUP BY partita.id
    )
    """)
    ris = cursor.fetchall()
    conn.close()
    return ris

