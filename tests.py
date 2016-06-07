import recipes

from unittest import TestCase, main
from recipes import process_recipes
from recipes import process_ingredients
from model import User, IngMeasurement, Ingredient, UsedRecipe, BookmarkedRecipe, Recipe, db


class ProcessRecipes(TestCase):

    def setUp(self):

        def _mock_recipe_request(ingredients, user_id):

            return [{'title': 'Apricot Glazed Apple Tart',
                     'image': 'https://spoonacular.com/recipeImages/Apricot-Glazed-Apple-Tart-632660.jpg',
                     'missedIngredientCount': 1,
                     'usedIngredients': [{'aisle': 'Produce',
                                          'image': 'https://spoonacular.com/cdn/ingredients_100x100/apple.jpg',
                                          'name': 'apple'},
                                         {'aisle': 'Baking',
                                          'image': 'https://spoonacular.com/cdn/ingredients_100x100/white-sugar.jpg',
                                          'name': 'sugar'},
                                         {'aisle': 'Baking',
                                          'image': 'https://spoonacular.com/cdn/ingredients_100x100/flour.png',
                                          'name': 'flour'}],
                     'likes': 3,
                     'missedIngredients': [{'aisle': 'Nut butters, Jams, and Honey',
                                            'image': 'https://spoonacular.com/cdn/ingredients_100x100/apricot-jam.jpg',
                                            'name': 'apricot preserves'},
                                           {'aisle': 'Spices and Seasonings',
                                            'image': 'https://spoonacular.com/cdn/ingredients_100x100/cinnamon.jpg',
                                            'name': 'cinnamon'},
                                           {'aisle': 'Milk, Eggs, Other Dairy',
                                            'image': 'https://spoonacular.com/cdn/ingredients_100x100/butter.png',
                                            'name': 'butter'}],
                     'usedIngredientCount': 3,
                     'id': 632660,
                     'imageType': 'jpg'
                     }]

        # def _mock_recipe_info(recipe_id, used_ing=None):

        #     return {'source': 'http://www.foodista.com/recipe/JVKTLG23/apricot-glazed-apple-tart',
        #             'cooktime': 45,
        #             'ingredients': '{"used_ings": [{"amount": 4.0, "name": "apple", "unit": ""}, {"amount": 1.5, "name": "flour", "unit": "cup"}, {"amount": 3.5, "name": "sugar", "unit": "tablespoon"}]}'
        #             }

        self._old_recipe_request = process_recipes.recipe_request
        process_recipes.recipe_request = _mock_recipe_request

        # self._old_recipe_info = process_recipes.recipe_info
        # process_recipes.recipe_info = _mock_recipe_info

    def tearDown(self):

        process_recipes.recipe_request = self._old_recipe_request
        # process_recipes.recipe_info = self._old_recipe_info

    def test_return_suggested_recipes(self):
        INGREDIENTS = "apple,flour,sugar"
        USER_ID = 1

        response = process_recipes.recipe_request(INGREDIENTS, USER_ID)
        self.assertEqual(process_recipes.return_suggested_recipes(response, USER_ID), [{'bookmarked': False,
                                                                                        'image': 'https://spoonacular.com/recipeImages/Apricot-Glazed-Apple-Tart-632660.jpg',
                                                                                        'recipe_id': 632660,
                                                                                        'ingredients': '{"used_ings": ["apple", "sugar", "flour"]}',
                                                                                        'title': 'Apricot Glazed Apple Tart'
                                                                                        }])


class Process_Ingredients(TestCase):

    def test_return_singular_form(self):
        INGREDIENTS = [{"name": "apples", "amount": 5, "unit": ""},
                       {"name": "sugar", "amount": 4, "unit": "cups"}]

        self.assertEqual(process_ingredients.return_singular_form(INGREDIENTS), [("apple", 5, ""),
                                                                                 ("sugar", 4, "cup")])


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        connect_to_db(app)

        # db.drop_all()
        # db.create_all()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_homepage(self):
        """Test profile page."""

        result = self.client.get("/")
        self.assertIn("Current Ingredients", result.data)
        self.assertNotIn("Login", result.data)






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
    main()
