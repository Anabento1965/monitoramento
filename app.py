from flask import Flask, render_template, request, url_for, flash, redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config["SECRET_KEY"] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from datetime import datetime




@app.route('/')
def index():
    posts = Posts.query.order_by(Posts.created.asc()).all()
    return render_template('index.html', posts=posts)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    ocorrencia = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    adesao = db.Column(db.String(255))
    rua = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self, title, content, ocorrencia, tipo, adesao, rua, cidade, estado):
        self.title = title
        self.content = content
        self.ocorrencia = ocorrencia
        self.tipo = tipo
        self.adesao = adesao
        self.rua = rua
        self.cidade = cidade
        self.estado = estado


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        ocorrencia = request.form['ocorrencia']
        tipo = request.form['tipo']
        adesao = request.form['adesao']
        rua = request.form['rua']
        cidade = request.form['cidade']
        estado = request.form['estado']

        if not title:
            flash('O título é obrigatório')
        else:
            post = Posts(title=title, content=content, ocorrencia=ocorrencia, tipo=tipo, adesao=adesao, rua=rua, cidade=cidade, estado=estado)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

def get_post(id):
    post = Posts.query.get(id)
    if post is None:
        abort(404)
    return post

@app.route('/<int:id>/edit' , methods=('GET' , 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form ['title']
        content = request.form['content']
        ocorrencia = request.form['ocorrencia']
        tipo = request.form['tipo']
        adesao = request.form['adesao']
        rua = request.form['rua']
        cidade = request.form['cidade']
        estado = request.form['estado']

        if not title:
            flash('Titulo é obrigatório!')
        else:
            post.title = title
            post.content = content
            post.ocorrencia = ocorrencia
            post.tipo = tipo
            post.adesao = adesao
            post.rua = rua
            post.cidade = cidade
            post.estado = estado
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    post = get_post(id)
    post_title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'A postagem "{post_title}" foi apagada com sucesso!')
    return redirect(url_for('index'))


@app.route('/sobre')
def sobre():
    # Lógica da rota sobre
    return render_template('sobre.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.get(post_id)
    if post is None:
        abort(404)
    return render_template('post.html', post=post)


from sqlalchemy import or_


@app.route('/search')
def search():
    query = request.args.get('q')

    if query:
        posts = Posts.query.filter(or_(
            Posts.title.ilike(f'%{query}%'),
            Posts.content.ilike(f'%{query}%'),
            Posts.ocorrencia.ilike(f'%{query}%'),
            Posts.tipo.ilike(f'%{query}%'),
            Posts.adesao.ilike(f'%{query}%'),
            Posts.rua.ilike(f'%{query}%'),
            Posts.cidade.ilike(f'%{query}%'),
            Posts.estado.ilike(f'%{query}%')
        )).all()
    else:
        posts = []

    return render_template('search.html', posts=posts, query=query)


