from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
from dotenv import load_dotenv
load_dotenv('.env')
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')       #Puxa do .env as variaveis
app.config['UPLOAD_FILES'] = r'static/data'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'
bcrypt = Bcrypt(app)

#---------------------------------------------------------------

from app.views import homepage
from app.models import Aluno