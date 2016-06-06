import os
import json

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.bcrypt import Bcrypt
from recipes.process_recipes import query_bookmarks, add_bookmark, return_stored_recipes, query_cooked_recipe, add_recipe, update_cooked_recipe, recipe_request, recipe_info, return_suggested_recipes
from recipes.users import user_info, query_user_email, query_username, add_new_user
from recipes.process_ingredients import return_avail_ingredients, return_depleted_ingredients, ingredient_names, add_ingredients, return_db_ingredients
from model import User, IngMeasurement, Ingredient, UsedRecipe, BookmarkedRecipe, Recipe, connect_to_db, db


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ['APP_KEY']

# Raises an error if there is an undefined variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage with login and sign-up functionality."""

    user_id = session.get('user_id', None)

    if user_id:
        avail_ing = return_avail_ingredients(user_id)
        avail_ing = return_db_ingredients(avail_ing)
        depleted_ing = return_depleted_ingredients(user_id)
        name, date = user_info(user_id)
        return render_template("profile.html",
                               name=name,
                               date=date,
                               avail_ing=avail_ing,
                               depleted_ing=depleted_ing
                               )

    return render_template("homepage.html")


@app.route('/register')
def register_form():
    """Show registration form for new user."""

    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def process_new_user():
    """Process new user from registration form."""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone = request.form.get("phone")

    user = query_username(username)
    password = bcrypt.generate_password_hash(password)

    if user:
        flash("This username is taken.", "error")
        return render_template("registration.html")
    else:
        new_user = add_new_user(username, email, password, fname, lname, phone)
        session["user_id"] = new_user.user_id

        flash("You have successfully signed up for an account!", "success")
        return redirect('/profile/{}'.format(new_user.username))


@app.route('/login', methods=['POST'])
def process_login():
    """Process login form."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = query_user_email(email)

    if not user:
        flash("This email does not exist. Please sign up or try again.", "error")
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, password):
        flash("Your password is incorrect.", "error")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("You are now logged in.", "success")
    return redirect("/profile/{}".format(user.username))


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have successfully logged out.", "success")
    return redirect("/")


@app.route('/profile/<username>')
def show_user_profile(username):
    """Show user profile."""

    user = query_username(username)
    avail_ing = return_avail_ingredients(user.user_id)
    avail_ing = return_db_ingredients(avail_ing)
    depleted_ing = return_depleted_ingredients(user.user_id)
    name, date = user_info(user.user_id)

    return render_template("profile.html",
                           name=name,
                           date=date,
                           avail_ing=avail_ing,
                           depleted_ing=depleted_ing
                           )


@app.route('/add-ingredients', methods=["POST"])
def add_new_ingredients():
    """Add new ingredients to database."""
    #Get user ID to query the users table - need the user object to get the username attribute
    user_id = session.get('user_id', None)
    user = User.query.get(user_id)
    ingredients = request.form.getlist("ingredient", None)[:-1]  # Slice up to second to last item because of hidden form template
    amounts = request.form.getlist("amount", None)[:-1]
    units = request.form.getlist("unit", None)[:-1]

    add_ingredients(ingredients, amounts, units, user_id)

    flash("You have successfully added the ingredients.", "success")

    return redirect("/profile/{}".format(user.username))


@app.route('/recipes')
def suggest_recipes():
    """Show user a list of suggested recipes."""

    user_id = session.get('user_id', None)
    ingredients = ingredient_names(user_id)
    ingredients = ",".join([ingredient[0] for ingredient in ingredients])  # Creating a comma separated string (required for API argument)
    suggested_recipes = return_suggested_recipes(recipe_request(ingredients, user_id), user_id)
    title = "Suggested Recipes"

    return render_template("recipes.html",
                           recipes=suggested_recipes,
                           title=title)


@app.route('/bookmarks')
def show_bookmarks():
    """Show user their list of bookmarked recipes."""

    user_id = session.get('user_id', None)

    bookmarked = query_bookmarks(user_id)
    ingredients = ingredient_names(user_id)
    bookmark = True
    bookmarked_recipes = return_stored_recipes(bookmarked, ingredients, user_id, bookmark)
    title = "Bookmarked Recipes"

    return render_template("recipes.html",
                           recipes=bookmarked_recipes,
                           title=title)


@app.route('/cooked-recipes')
def show_cooked_recipes():
    """Show user their list of cooked recipes."""

    user_id = session.get('user_id', None)

    cooked = query_cooked_recipe(user_id)
    ingredients = ingredient_names(user_id)
    cooked_recipes = return_stored_recipes(cooked, ingredients, user_id)
    title = "Cooked Recipes"

    return render_template("recipes.html",
                           recipes=cooked_recipes,
                           title=title)


@app.route('/add-recipe.json', methods=["POST", "GET"])
def add_used_recipe():
    """Add used or bookmarked recipes to database."""

    user_id = session.get('user_id', None)
    button = request.args.get("button", None).split()
    recipe_id = int(request.args.get("api_id", None))
    image = request.args.get("image", None)
    source = request.args.get("source", None)
    title = request.args.get("title", None)
    ingredients = json.loads(request.args.get("ing", None))

    add_recipe(user_id, recipe_id, title, image, source)

    if button[-1] == "cook":
        update_cooked_recipe(user_id, recipe_id, ingredients)
    elif button[-1] == "bookmarks":
        add_bookmark(user_id, recipe_id)

    return jsonify(id=recipe_id, button=button)


@app.route('/recipe-details.json', methods=["POST", "GET"])
def return_recipe_details():

    recipe_id = request.args.get("api_id", None)
    ingredients = json.loads(request.args.get("ingredients", None))
    title = request.args.get("title", None)
    image = request.args.get("image", None)

    if isinstance(ingredients["used_ings"][0], unicode):
        info = recipe_info(recipe_id, ingredients["used_ings"])

    if isinstance(ingredients["used_ings"][0], dict):
        info = recipe_info(recipe_id)
        info["ingredients"] = json.dumps(ingredients)

    return jsonify(info=info,
                   id=recipe_id,
                   image=image,
                   title=title)


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
