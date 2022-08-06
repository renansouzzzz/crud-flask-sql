from asyncio.windows_events import NULL
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.sqlite3'
app.config['SECRET_KEY'] = "secret"
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

class Colaborador(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    gmid = db.Column(db.Integer)
    feedback = db.Column(db.String(150))

    def __init__(self, nome, gmid, feedback):
        self.nome = nome
        self.gmid = gmid
        self.feedback = feedback
    
    def constructor(self, username, password):
        self.username = username
        self.password = password

@app.route('/')
def index():
    c = Colaborador
    return render_template('index.html', colaboradores=c.query.all())

@app.route('/adicionar', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        gmid = request.form['gmid']
        colaboradores = Colaborador(nome, gmid, NULL)
        db.session.add(colaboradores)
        db.session.commit()
        flash(f'Colaborador {nome} incluído com sucesso!')
        return redirect(url_for('index'))
    else:
        return render_template('adicionar.html')

@app.route('/deletar/<int:id>')
def delete(id):
    colaborador = Colaborador.query.get(id)
    db.session.delete(colaborador)
    db.session.commit()
    flash(f'Colaborador(a) excluído com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET','POST'])
def edit(id):
    colaborador = Colaborador.query.get(id)
    if request.method == 'POST':
        colaborador.nome = request.form['nome']
        colaborador.gmid = request.form['gmid']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', colaborador=colaborador)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    get = Colaborador.query.all()
    if request.method == 'POST':
        feedback = request.form['feedback']
        feedbacks = Colaborador(NULL, NULL, feedback)
        db.session.add(feedbacks)
        db.session.commit()
        flash('Feedback enviado com sucesso!')
        return redirect(url_for('index'))
    else: 
        return render_template('feedback.html', get=get)
        
class Login(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(50))

@app.route('/registrar', methods=['GET', 'POST'] )
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        acesso = Login(username, password)
        db.session.add(acesso)
        db.session.commit()
        return redirect(url_for('registrar'))
        flash(f'Usuário {username} registrado com sucesso!')
    else:
        return render_template('registrar.html') 

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
