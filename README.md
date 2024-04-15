# FitFeasters
Nutritional info and recipes for foodies at home.

Welcome to Fit Feasters! FitFeasters is a web application built with Flask, designed to help users discover recipes based on their dietary preferences and ingredients they have on hand. User has inputs for the food name, any food intolerances (optional), and any ingredients which should be included (optional). That avocado is perfectly ripe, time to get recipes! User can also look up food recipe in the search box. After searching, the user is given 5 food images, clicking on one of the food links, the user is brought to a new page and given:
- Time to prepare meal
- Weight Watcher Points
- How many servings
- If the meal is gluten free
- If the meal is vegetarian
- A link to the meal's recipe 

![Opening UI page](https://private-user-images.githubusercontent.com/141876079/322639700-47f207e8-0cda-4d4b-ba7c-06318d7a0ab9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTMyMTg1NDUsIm5iZiI6MTcxMzIxODI0NSwicGF0aCI6Ii8xNDE4NzYwNzkvMzIyNjM5NzAwLTQ3ZjIwN2U4LTBjZGEtNGQ0Yi1iYTdjLTA2MzE4ZDdhMGFiOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNDE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDQxNVQyMTU3MjVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hMTFlYTM1NDBmN2Q1NzI5MWEyNmFlMWY4ODcyZjdlZWY5YTY0ZGRkY2JkYTZiMmRjNTVkZjNjZDdhNjE5MTg4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.cYU7ejdUx9TK80KS21pz3l2tjH1mVH9KX3yq6R7T84U)


link to api---> https://api.spoonacular.com

Getting Started:
To get started with FitFeasters locally, follow these steps in the terminal:

Prerequisites:
Make sure you have the following installed on your machine:

-Python (3.6 or higher)
-Flask
-Jinja
-SQLAlchemy

Installation:
-Clone this repository to your local machine:

    git clone https://github.com/yourusername/fitfeasters.git

Navigate to the project directory:

    cd fitfeasters

Install the required Python packages:

    pip install -r requirements.txt

Configuration:
Obtain an API key from Spoonacular by signing up ![here](https://spoonacular.com/food-api/pricing).

Replace API_KEY in app.py with your Spoonacular API key.


Run the Flask application:

    python app.py

Open your web browser and navigate to http://localhost:5000 to access FitFeasters.

Usage:

Signup/Login: Create an account or login with existing credentials to start using the app.
Search for Recipes: Use the search form to find recipes based on titles, ingredients, and dietary preferences.
Update Profile: Update your profile information, including username, email, and profile picture.
Logout: Logout from your account when you're done using the app.

Future Features:

Save Recipes: Save your favorite recipes to your profile for easy access later.