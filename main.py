from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import analytics_wp 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
db = SQLAlchemy(app)
db.init_app(app)

# CLASSI DEL DATABASE
class TeamStats(db.Model):
    __tablename__ = "PARTITA"
    id = db.Column(db.Integer, primary_key=True)
    avversario = db.Column(db.String(255))
    location = db.Column(db.String(255))
    data_partita = db.Column(db.String(255))
    gol_subiti = db.Column(db.Integer())
    piu_tentati = db.Column(db.Integer())
    piu_realizzati = db.Column(db.Integer())
    ritmo_att = db.Column(db.Integer())
    ritmo_def = db.Column(db.Integer())
    meno_tentati = db.Column(db.Integer())
    meno_subiti = db.Column(db.Integer())
class Player(db.Model):
    __tablename__ = "GIOCATORE"
    nome = db.Column(db.String(255), primary_key=True)
class PersonalStats(db.Model):
    __tablename__ = "PERSONALI"
    nome_giocatore = db.Column(db.Integer, primary_key=True)
    id_partita = db.Column(db.Integer, primary_key=True)
    gol = db.Column(db.Integer())
    tiri = db.Column(db.Integer())
    assist = db.Column(db.Integer())
    espulsioni = db.Column(db.Integer())
    recuperi = db.Column(db.Integer())
    stoppate = db.Column(db.Integer())
    plusminus = db.Column(db.Integer())
    palle_perse = db.Column(db.Integer())
    
def salva_partita(request):
    team_stats = TeamStats(avversario=request.form['avversaria'], location=request.form["location"], data_partita=request.form['data'], gol_subiti=request.form["gol subiti"], piu_tentati=request.form['+ tentati'], piu_realizzati=request.form['+ realizzati'], ritmo_att=request.form['ritmo_att'], ritmo_def=request.form['ritmo_def'], meno_tentati=request.form["- tentati"], meno_subiti=request.form["- subiti"])
    # controllino
    if team_stats.avversario == "" or team_stats.data_partita == "" or team_stats.location == "":
        return redirect("http://localhost:5000/stats_partita")
    # salvo stats squadra
    db.session.add(team_stats)
    db.session.flush()
    id_partita = team_stats.id
    db.session.commit()
    # salvo giocatori e stats personali
    for i in range(1,14):
        # nomi
        player_name = request.form["nome"+str(i)]
        if player_name == "0":
            continue
        existing_player = Player.query.filter_by(nome=player_name).first()
        if existing_player is None:
            new_player = Player(nome=player_name)
            db.session.add(new_player)
            db.session.commit()
        else:
            existing_player.nome = player_name
            db.session.commit()
        # stats personali
        player_stats = PersonalStats(nome_giocatore=request.form['nome'+str(i)], id_partita=id_partita, gol=request.form['gol'+str(i)], tiri=request.form['tiri'+str(i)], plusminus=request.form['plusminus'+str(i)], palle_perse=request.form['palleperse'+str(i)], assist=request.form['assist'+str(i)], espulsioni=request.form['espulsioni'+str(i)], recuperi=request.form['recuperi'+str(i)], stoppate=request.form['stoppate'+str(i)])
        db.session.add(player_stats)
        db.session.commit()
# **************************************************

@app.route('/wp')
def index():
    return render_template("index.html")

@app.route('/wp/stats_partita')
def stats_partita():
    return render_template('partita.html')

@app.route('/wp/db')
def stampa_db():
    team_stats = TeamStats.query.all()
    giocatori = Player.query.all()
    personal_stats = PersonalStats.query.all()
    return render_template('stampa_db.html', team_stats=team_stats, giocatori=giocatori, personal_stats=personal_stats)    

@app.route('/wp/stats_partita/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        salva_partita(request)
        return render_template("personali.html", classifica_grezza=analytics_wp.classifica_grezza(), classifica_partita=analytics_wp.classifica_partita(), avanzate=analytics_wp.avanzate())

@app.route('/wp/personali',methods = ['POST', 'GET'])
def personali():
    return render_template("personali.html", classifica_grezza=analytics_wp.classifica_grezza(), classifica_partita=analytics_wp.classifica_partita(), avanzate=analytics_wp.avanzate())

@app.route('/wp/squadra',methods = ['POST', 'GET'])
def squadra():
    return render_template("squadra.html", squadra_grezza=analytics_wp.squadra_grezza(), medie_squadra=analytics_wp.medie_squadra())

if __name__=="__main__":
    app.run("127.0.0.1", 5000, True)

