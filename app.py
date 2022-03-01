from flask import Flask, render_template, redirect, session, get_flashed_messages
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
from forms import LoginForm, RegisterForm

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
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    "Registers user and produces form to handle registration"
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        return redirect("/show")
        
    else:
        return render_template("users/register.html", form=form)
 