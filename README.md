# Waterpolo Scoreboard
Strumento utile per la raccolta e l'analisi di dati all'interno di una partita di pallanuoto.
Realizzato con l'uso del framework Python Flask l'applicazione si presenta come un sito web sul localhost e fa uso di un database sqlite.
Testato e sviluppato con Ubuntu 22 ma teoricamente con qualche accorgimento funziona sia su Windows che su MacOS.

## Guida utente
- Lanciare su terminale Linux il comando:
        bash run.sh
- Si aprirà la pagina principale sul browser: http://localhost:5000/wp
- Dal menù è possibile scegliere tra 3 diverse voci:
1. *Inserisci dati partita*: permette attraverso un form di inserire i dati raccolti durante la partita e salvarli nel database
2. *Vedi statistiche personali*: mostra le statistiche più o meno elaborate di tutti i giocatori
3. *Vedi statistiche di squadra*: mostra le statistiche che riguardano lo squadra

## Struttura del codice
Il file *main.py* contiene il frontend dell'applicazione, infatti tramite Flask gestisce tutta la parte delle pagine web contenute in *./templates* e con i file CSS nella cartella *./static*, inoltre si occupa anche di salvare nel database (contenuto nel file *./instance/stats.db*) i dati raccolti per ogni partita.
Per interrogare il database si utilizzano le funzioni presenti nel file *analytics_wp.py* .
Infine il file *manage_db.py* viene lanciato a parte qual'ora ci sia la necessità di intervenire sul database:
        python3 manage_db.py