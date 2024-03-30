import os

from flask import Flask, request, render_template,  redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError

from forms import SignUpForm, LoginForm, DeleteForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"
API_KEY = 'Y43cb4f5704da4cfe9d4d261fbb40c746'
BASE_URL= 'https://api.spoonacular.com/recipes/'
endpoint = 'https://api.spoonacular.com/recipes/findByIngredients/'
params = {
    'number': 5,  # Number of recipes to fetch
    'apiKey': API_KEY
}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fitfeasters_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "food4thesoul"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.drop_all()
db.create_all()

#################################### User Sign up/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# API_KEY = 'Y43cb4f5704da4cfe9d4d261fbb40c746'
# endpoint = 'https://api.spoonacular.com/recipes/findByIngredients/'

# params = {
#     'number': 5,  # Number of recipes to fetch
#     'apiKey': API_KEY
# }

# # Make GET request to Spoonacular API
# response = request.get(endpoint, params=params)

# # Check if request was successful (status code 200)
# if response.status_code == 200:
#     # Extract data from response 
#     data = response.json()
    
#     # Process and store data in your database
#     for recipe in data['recipes']:
#         # Example: Store recipe information in your database
#         recipe_id = recipe['id']
#         recipe_title = recipe['title']
#         # Store other relevant recipe information...
#         print(f"Recipe ID: {recipe_id}, Title: {recipe_title}")
# else:
#     print(f"Failed to fetch data: {response.status_code}")


@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return render_template("users/homepage.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            image_url = form.image_url.data

            user = User.signup(username, password, first_name, last_name, email, image_url)

            db.session.commit()
            
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("curr_user")
    flash("You have been logged out.", "success")
    return redirect("/login")



############################ General User routes


@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("/homepage.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")