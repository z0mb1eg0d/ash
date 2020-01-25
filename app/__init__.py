from flask import Flask
from config import Config
from flask_login import LoginManager
import psycopg2

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
con  = psycopg2.connect(
    host="ec2-34-196-180-38.compute-1.amazonaws.com",
    port="5432",
    database="dbf9vo1gnasv5r",
    user="ofkbtrwtokulrj",
    password="9317df662346c8c6bba272688a69dfb89977841e35c39465e6578215f6ea17d6"
    )


from app import routes