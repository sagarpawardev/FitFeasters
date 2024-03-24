from flask import Flask, request, render_template,  redirect, flash, session, requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, user


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fitfeasters_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "food4thesoul"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
debug = DebugToolbarExtension(app)

connect_db(app)


app.app_context().push()
db.create_all()


API_KEY = 'Y43cb4f5704da4cfe9d4d261fbb40c746'
endpoint = 'https://api.spoonacular.com/recipes/random'

params = {
    'number': 10,  # Number of random recipes to fetch
    'apiKey': API_KEY
}

# Make GET request to Spoonacular API
response = requests.get(endpoint, params=params)

# Check if request was successful (status code 200)
if response.status_code == 200:
    # Extract data from response (assuming JSON format)
    data = response.json()
    
    # Process and store data in your database
    for recipe in data['recipes']:
        # Example: Store recipe information in your database
        recipe_id = recipe['id']
        recipe_title = recipe['title']
        # Store other relevant recipe information...
        print(f"Recipe ID: {recipe_id}, Title: {recipe_title}")
else:
    print(f"Failed to fetch data: {response.status_code}")
