from model import User, db
from datetime import datetime


def query_user_email(email):
    """Check if user email exists in database."""

    user = User.query.filter_by(email=email).first()
    return user


def query_username(username):
    """Check if username exists in database."""

    user = db.session.query(User).filter_by(username=username).first()
    return user


def user_info(user_id):
    """Return user to profile page if logged in."""

    user = User.query.get(user_id)
    name = user.fname
    date = datetime.now()
    date = date.strftime("%B %d, %Y")

    return name, date


def add_new_user(username, email, password, fname, lname, phone):
    """Add new user into database."""

    new_user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    phone=phone)

    db.session.add(new_user)
    db.session.commit()

    return new_user
