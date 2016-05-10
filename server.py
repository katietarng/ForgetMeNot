import os

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import *


app = Flask(__name__)

app.secret_key = os.environ['APP_KEY']

# Raises an error if there is an undefined variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage with login and sign-up functionality."""

    return render_template("homepage.html")

@app.route('/register')
def register_form():
    """Show registration form for new user."""

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def process_new_user():
    """Process new user from registration form."""

    

@app.route('/login', methods=['POST'])
def process_login():
    """Process login form."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).one()

    if not user:
        flash("No such email. Please sign up or try again.")
        return redirect("/")

    if user.password != password:
        flash("Your password is incorrect.")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("You are now logged in.")
    return redirect("/profile/{}".format(user.user_id))




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()