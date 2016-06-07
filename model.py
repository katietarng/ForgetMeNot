from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################


class User(db.Model):
    """User information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(65), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Print user information."""

        return "<user_id={} username={} email={}, password={}, fname={}, lname={}, phone={}>".format(self.user_id,
                                                                                                     self.username,
                                                                                                     self.email,
                                                                                                     self.password,
                                                                                                     self.fname,
                                                                                                     self.lname,
                                                                                                     self.phone)


class IngMeasurement(db.Model):
    """Ingredient measurements for various ingredients."""

    __tablename__ = "measurements"

    weight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    volume = db.Column(db.Float, nullable=False)
    vol_unit = db.Column(db.String(20), nullable=False)
    ounce = db.Column(db.Float, nullable=True)
    gram = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Print ingredient measurements."""

        return "<Ingredient measurement weight_id={}, name={}, volume={}, vol_unit={}, ounce={} gram={}>".format(self.weight_id,
                                                                                                                 self.name,
                                                                                                                 self.volume,
                                                                                                                 self.vol_unit,
                                                                                                                 self.ounce,
                                                                                                                 self.gram)


class Ingredient(db.Model):
    """Ingredient in fridge or pantry."""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(70), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=True)  # Units of measurement (ounces,liters,etc.)
    input_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User",
                           backref=db.backref("ingredients", order_by=ingredient_id))

    def __repr__(self):
        """Print ingredients in fridge or pantry."""

        return "<Ingredient user_id={} ingredient_id={}, name={}, amount={}, unit={}, input_date={}>".format(self.user_id,
                                                                                                             self.ingredient_id,
                                                                                                             self.name,
                                                                                                             self.amount,
                                                                                                             self.unit,
                                                                                                             self.input_date)


class UsedRecipe(db.Model):
    """Recipe that has been cooked before."""

    __tablename__ = "used_recipes"

    used_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)

    user = db.relationship("User",
                           backref=db.backref("used_recipes", order_by=used_recipe_id))

    recipe = db.relationship("Recipe",
                             backref=db.backref("used_recipes", order_by=used_recipe_id))


class BookmarkedRecipe(db.Model):
    """Recipe that has been saved to cook later."""

    __tablename__ = "bookmarked_recipes"

    bookmarked_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False, unique=True)

    user = db.relationship("User",
                           backref=db.backref("saved_recipes", order_by=bookmarked_recipe_id))

    recipe = db.relationship("Recipe",
                             backref=db.backref("saved_recipes", order_by=bookmarked_recipe_id))


class Recipe(db.Model):
    """Recipe that has been saved, used, or favorited."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(70), nullable=False, unique=True)
    image_url = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String(200), nullable=False)

    user = db.relationship("User",
                           backref=db.backref("recipes", order_by=recipe_id))

    def __repr__(self):
        """Print user information."""

        return "<Recipe user_id={} recipe_id={} title={}, image_url={} source={}>".format(self.user_id,
                                                                                          self.recipe_id,
                                                                                          self.title,
                                                                                          self.image_url,
                                                                                          self.source_url)


##############################################################################

def connect_to_db(app, db_uri='postgresql:///recipes'):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
