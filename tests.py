import unittest
from generaterecipes import *
from processdata import *


class ProcessDataTestCase(unittest.TestCase):
    """Running tests on process data helper functions."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()

    def test_return_db_ingredients(self):
        DB_INGREDIENTS = Ingredient.query.filter_by(user_id=1, name="orange").all()

        self.assertEqual(return_current_ingredients(DB_INGREDIENTS), [{'amount': 7.0,
                                                                       'name': 'orange',
                                                                       'unit': 'none'}])

    def test_add_bookmark(self):
        BOOKMARKED_RECIPE = BookmarkedRecipe.query.filter_by(user_id=1, bookmarked_recipe_id=1).one()

        if BOOKMARKED_RECIPE:
            return True

        self.assertEqual(BOOKMARKED_RECIPE, True)


class GenerateRecipeTestCase(unittest.TestCase):

    def test_return_singular_form(self):
        INGREDIENTS = [{"name": "apples", "amount": 5, "unit": ""},
                       {"name": "sugar", "amount": 4, "unit": "cups"}]

        self.assertEqual(return_singular_form(INGREDIENTS), [("apple", 5, ""),
                                                             ("sugar", 4, "cup")])


##############################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///examplerecipes'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB. "
    unittest.main()
