from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.sqlite3'
app.config['SECRET_KEY'] = "secret"

db = SQLAlchemy(app)


class Colaborador(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    gmid = db.Column(db.Integer)

    def __init__(self, nome, gmid):
        self.nome = nome
        self.gmid = gmid


@app.route('/')
def index():
    colaboradores = Colaborador.query.all()
    return render_template('index.html', colaboradores=colaboradores)



@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        colaboradores = Colaborador(request.form['nome'], request.form['gmid'])
        db.session.add(colaboradores)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('adicionar.html')


@app.route('/deletar/<int:id>')
def deletar(id):
    flash('Colaborador excluído com sucesso!')
    colaborador = Colaborador.query.get(id)
    db.session.delete(colaborador)
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    colaborador = Colaborador.query.get(id)
    if request.method == 'POST':
        colaborador.nome = request.form['nome']
        colaborador.gmid = request.form['gmid']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', colaborador=colaborador)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
