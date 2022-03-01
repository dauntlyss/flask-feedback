from flask import Flask, render_template, redirect, session, flash
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
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username
        flash('Welcome! You have successfully created your account')
        return redirect(f"/users/{user.username}")
        
    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form and handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)
 
@app.route("/logout")
def logout():
    """Logout route for ussers."""

    session.pop("username")
    return redirect("/login")