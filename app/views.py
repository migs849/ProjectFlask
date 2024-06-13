from app import app
from flask import render_template, url_for, request, redirect
from app import db

from app.forms import AlunoForm, Userform, LoginForm, PostForm, PostComentarioForm
from app.models import Aluno, Post, ClasseComentario
from flask_login import login_user, logout_user, current_user, login_required

#--- Tudo para rodar o html ou aparecer ou mandar para o html

@app.route('/', methods=['GET','POST'])
def homepage():
    form = LoginForm()

    if form.validate_on_submit():
        user=form.login()
        login_user(user, remember=True)
    context = {  }
    return render_template('index.html',context=context, form=form)

@app.route('/cadastro/', methods={'GET','POST'})
def cadastro():
    form = Userform()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

@app.route('/post/novo',  methods={'GET','POST'})
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))
    return render_template('post_novo.html', form=form)

@app.route('/post/lista')
@login_required
def PostLista():
    posts = Post.query.all()
    return render_template('post_lista.html', posts = posts)

@app.route('/post/<int:id>', methods={'GET','POST'})
def PostDetail(id):
    obj= Post.query.get(id)
    post= Post.query.get(id)

    form = PostComentarioForm()

    if form.validate_on_submit():
        form.save(id)
        return redirect(url_for('PostLista'))
    
    #comentario = ClasseComentario.query.all()
    comentario = ClasseComentario.query.filter_by(post_id=id).all()
    return render_template('post_detail.html',post=post,obj=obj, form=form, comentario=comentario)

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))













@app.route('/contato/', methods=['GET','POST'])
@login_required
def contato():      #O route, def contato, é definido no index para poder ser linkado.
    form = AlunoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
@login_required
def contato_lista():
    if current_user.id == 17: return redirect(url_for('homepage'))
    if request.method =='GET':
        pesquisa = request.args.get('pesquisa','')
    dados = Aluno.query.order_by('nome')
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
    context = {'dados' : dados.all()}

    return render_template('contato_lista.html', context=context)

@app.route('/contato/<int:id>')
@login_required
def contatoDetail(id):
    obj= Aluno.query.get(id)
    
    return render_template('contato_detail.html',obj=obj,)