from flask import Flask, render_template, redirect, session, get_flashed_messages
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
# from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "girlslovebeyonce"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template('users/register.html')