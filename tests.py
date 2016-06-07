import recipes
import server

from unittest import TestCase
from server import app
from recipes import process_recipes
from recipes import process_ingredients
from model import User, IngMeasurement, Ingredient, UsedRecipe, BookmarkedRecipe, Recipe, connect_to_db, db


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

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        self.client = app.test_client()
        connect_to_db(app, "postgresql:///examplerecipes")

        # Create tables and add sample data
        db.drop_all()
        db.create_all()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):

        db.session.close()
        db.drop_all()

    print "tearDown successfull"






##############################################################################

if __name__ == "__main__":
    main()
