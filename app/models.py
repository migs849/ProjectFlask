from app import db, login_manager
from datetime import datetime

from flask_login import UserMixin
#

#--- tudo haver com sql commands


class Aluno(db.Model):  #Nome da tabela
    id = db.Column( db.Integer, primary_key=True)
    nome = db.Column( db.String, nullable=True)
    idade = db.Column( db.Integer, nullable=True)
    matricula = db.Column( db.Integer, nullable=True)
    descricao = db.Column( db.String, nullable=True)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String, nullable = True)
    sobrenome = db.Column(db.String, nullable = True)
    email = db.Column(db.String, nullable = True)
    senha = db.Column(db.String, nullable = True)
    posts = db.relationship('Post', backref='user',lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_criação = db.Column(db.DateTime,default=datetime.now())
    mensagem = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    coms = db.relationship('ClasseComentario', backref='Post',lazy=True)
    imagem = db.Column(db.String,nullable=True, default="jax2.png")

    def msg_resumo(self):
        return f"{self.mensagem[:10]} ..."

class ClasseComentario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_criação = db.Column(db.DateTime,default=datetime.now())
    comentario = db.Column(db.String, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=True)

    def comentario_resumo(self):
        return f"{self.mensagem} ..."