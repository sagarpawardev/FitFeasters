import os
from flask import Flask, request, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from forms import SignUpForm, LoginForm, DeleteForm, SearchForm
from models import db, connect_db, User


CURR_USER_KEY = "curr_user"
API_KEY = 'Y43cb4f5704da4cfe9d4d261fbb40c746'
BASE_URL = 'https://api.spoonacular.com/recipes/complexSearch?'

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fitfeasters_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "food4thesoul"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

# Debug toolbar
debug = DebugToolbarExtension(app)

# Database setup
connect_db(app)
app.app_context().push()
db.create_all()

#################################### User Sign up/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""
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

@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""
    return render_template("/users/homepage.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
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
        return redirect("/search_form")

    else:
        return render_template("users/signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/search_form")
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

##################### Recipe searches

@app.route('/search_form', methods=['GET', 'POST'])
def search_form():
    """Render the search form template."""
    form = SearchForm()
    return render_template('/users/search_form.html', form=form)

@app.route('/search', methods=['POST'])
def search():
    """Handle recipe search."""
    form = SearchForm()
    if form.validate_on_submit():
        title = form.name.data
        intolerances = form.intolerances.data
        include_ingrediants = form.include_ingrediants.data
        
        query = f'{title}intolerances={intolerances}includeIngrediants={include_ingrediants}'
        endpoint = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&number=5&query={query}'
        response = requests.get(endpoint)
        
        if response.status_code == 200:
            data = response.json()
            return render_template('search_results.html', recipes=data)
        else:
            return 'Failed to fetch data from Spoonacular API', 500

    return render_template('search_form.html', form=form)
    


# @app.route('/search', methods=['POST'])
# def get_query():
#     # Now 'query' contains the search query entered by the user
#     query = request.form.get('query')
    
#     return render_template('search_results.html', query=query)

# @app.route('/?<query>', methods=['GET', 'POST'])
# def search():
    
#     if request.method == 'POST':
#         query = request.form.get('query')
        
#         # Make GET request to Spoonacular API
#         endpoint = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&number=5&query={query}'
#         response = requests.get(endpoint)
        
#         if response.status_code == 200:
#             data = response.json()
#             return render_template('search_results.html', recipes=data)
#         else:
#             return 'Failed to fetch data from Spoonacular API', 500

#     # Render the search form template
#     return render_template('search_form.html')

# # API_KEY = 'Y43cb4f5704da4cfe9d4d261fbb40c746'
# # endpoint = 'https://api.spoonacular.com/recipes/findByIngredients/'

# # params = {
# #     'number': 5,  # Number of recipes to fetch
# #     'apiKey': API_KEY
# # }

# # # Make GET request to Spoonacular API
# # response = request.get(endpoint, params=params)

# # # Check if request was successful (status code 200)
# # if response.status_code == 200:
# #     # Extract data from response 
# #     data = response.json()
    
# #     # Process and store data in your database
# #     for recipe in data['recipes']:
# #         recipe_id = recipe['id']
# #         recipe_title = recipe['title']
       
# #         print(f"Recipe ID: {recipe_id}, Title: {recipe_title}")
# # else:
# #     print(f"Failed to fetch data: {response.status_code}")