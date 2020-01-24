from flask import Flask
from config import Config
from flask_login import LoginManager
import psycopg2

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
con  = psycopg2.connect(
    host="ec2-35-175-170-131.compute-1.amazonaws.com",
    port="5432",
    database="dfoaqrqntpbkuq",
    user="buhktexwpqtxcd",
    password="436c1c1c9db17b72c8d4042cc306076740079714afd5fe7351f31bc0b2576d2e"
    )


from app import routes