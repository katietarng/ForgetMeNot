import unittest
from generate_recipes import *
from process_data import *


class ProcessDataTestCase(unittest.TestCase):
    """Running tests on process data helper functions."""

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        """Stuff to do before every test."""

        super(ProcessDataTestCase, self).setUp()

        self.client = app.test_client()
        app.config['TESTING'] = True

        self.addCleanup(db.session.close)  # This method closes the session at the end of each test method and you do not need parantheses because it automatically calls the method

    def test_return_db_ingredients(self):
        DB_INGREDIENTS = Ingredient.query.filter_by(user_id=1, name="orange").all()

        self.assertEqual(return_current_ingredients(DB_INGREDIENTS), [{'amount': 7.0,
                                                                       'name': 'orange',
                                                                       'unit': 'none'}])

    def test_add_bookmark(self):
     # Use factory boy to create a test user and a recipe id
     # Check if the user has a bookmarked recipe first
     # Call the add_bookmark function 
     # Check to see if the bookmark has been added


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
