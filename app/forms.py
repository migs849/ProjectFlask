from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db, bcrypt, app
from app.models import Aluno, User, Post, ClasseComentario

import os
from werkzeug.utils import secure_filename


class AlunoForm(FlaskForm): 
    nome = StringField('Nome', validators=[DataRequired()])
    idade = StringField('Idade', validators=[DataRequired()])
    matricula = StringField('Matricula', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        aluno = Aluno(  #o Aluno, precisa ser o mesmo do Model, que é a banco de dados
            nome = self.nome.data,
            idade = self.idade.data,
            matricula = self.matricula.data,
            descricao = self.descricao.data
        )
        db.session.add(aluno)   #não importa oque coloca aqui
        db.session.commit()

class Userform(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('SobreNome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confrime a Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self,email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já está cadastrado neste E-Mail')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )    
        db.session.add(user)
        db.session.commit()
        return user
    
class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
         #Recupera o usuario do email
        user= User.query.filter_by(email=self.email.data).first()
        #senha é verdadeira?
        if user:
            if bcrypt.check_password_hash(user.senha , self.senha.data.encode('utf-8')):
                return user
            else:
                 raise Exception('Senha Incorreta!!!!!!!')
        else:
            raise Exception('Usuário inexistente!!!!!!!!!')
        
class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
       imagem = self.imagem.data
       nome_seguro = secure_filename(imagem.filename)
       post= Post(
           mensagem = self.mensagem.data,
           user_id = user_id,
           imagem=nome_seguro
       )
       caminho = os.path.join(
       os.path.abspath(os.path.dirname(__file__)),
       app.config['UPLOAD_FILES'],
       'post',
       nome_seguro   
       )
       imagem.save(caminho)
       db.session.add(post)
       db.session.commit()

class PostComentarioForm(FlaskForm):
    comentario = StringField('Comentário:', validators=[DataRequired()])
    btnSubmit2 = SubmitField('Enviar Comentário')

    def save(self, Post):
       add2= ClasseComentario(
           comentario = self.comentario.data,
           post_id = Post
       )
       db.session.add(add2)
       db.session.commit()