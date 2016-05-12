import os

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import *
from datetime import datetime
from generaterecipes import recipe_request, recipe_info


app = Flask(__name__)

app.secret_key = os.environ['APP_KEY']

# Raises an error if there is an undefined variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage with login and sign-up functionality."""

    user_id = session.get('user_id', None)

    if user_id:
        user = User.query.get(user_id)
        name = user.fname
        date = datetime.now()
        date = date.strftime("%B %d, %Y")
        return render_template("profile.html", name=name, date=date)

    return render_template("homepage.html")


@app.route('/register')
def register_form():
    """Show registration form for new user."""

    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def process_new_user():
    """Process new user from registration form."""

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    phone = request.form["phone"]

    user = db.session.query(User).filter_by(username=username).first()

    if user:
        flash("This username is taken.")
        return render_template("registration.html")
    else:
        new_user = User(username=username,
                        email=email,
                        password=password,
                        fname=first_name,
                        lname=last_name,
                        phone=phone)

        db.session.add(new_user)
        db.session.commit()

        flash("You have successfully signed up for an account!")
        return redirect('/profile/{}'.format(new_user.username))


@app.route('/login', methods=['POST'])
def process_login():
    """Process login form."""

    email = request.form["email"]
    password = request.form["password"]

    #Want to use .first() so that it can return None type object
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("This email does not exist. Please sign up or try again.")
        return redirect("/")

    if user.password != password:
        flash("Your password is incorrect.")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("You are now logged in.")
    return redirect("/profile/{}".format(user.username))


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have successfully logged out.")
    return redirect("/")


@app.route('/profile/<username>')
def show_user_profile(username):
    """Show user profile."""

    user = db.session.query(User).filter_by(username=username).one()
    name = user.fname
    date = datetime.now()
    date = date.strftime("%B %d, %Y")

    return render_template("profile.html", name=name, date=date)


@app.route('/recipes', methods=['POST'])
def suggest_recipes():
    """Show user a list of suggested recipes."""

    ingredients = request.form.getlist("ingredient")
    ingredients = ",".join(ingredients)  # Creating a comma separated string (required for API argument)

    recipes = recipe_request(ingredients)  # Returns a list of tuples (id, image_url, recipe name, source, ingredients)

    return render_template("recipes.html", recipes=recipes)


@app.route('/recipe-source.json')
def get_source_urls():
    """Get source urls for each recipe."""

    recipe_ids = request.form.getlist["recipe_id"]  # Returns a list of recipe IDs

    sources = {}

    #Iterate through each recipe id and grab the s
    for recipe_id in recipe_ids:
        info = recipe_info(recipe_id)  # Returns a tuple
        id = info[0]
        source = info[1]

        sources[id] = source

    return jsonify(sources)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()