import json
import os
import unirest
from model import User, IngMeasurement, Ingredient, UsedRecipe, BookmarkedRecipe, Recipe, connect_to_db, db
from process_ingredients import update_ingredient_amount, return_ingredient_list, return_singular_form

################################################################################
#                           SPOONACULAR API REQUESTS                           #
#                                                                              #
################################################################################


def recipe_request(ingredients, user_id):
    """Return a list of recipes that matches ingredient list."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"],
            "Accept": "application/json"
        },
        params={
            "fillIngredients": True,  # Adds information about used ingredients
            "ingredients": ingredients,  # List of ingredients as a string
            "number": 30,  # Maximal number of recipes to return
            "ranking": 1  # Minimizes missing ingredients
        }
    )

    responses = request.body  # Returns a list of dictionaries that are recipes

    suggested_recipes = parse_api_recipes(responses, user_id)

    return suggested_recipes


def recipe_info(recipe_id, used_ing=None):
    """Return recipe information for a single recipe."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information".format(recipe_id)

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"]
        }
    )

    response = request.body

    recipe = {}
    source = response.get("sourceUrl")
    cooktime = response.get("readyInMinutes")

    # Check to see if a used amount exists, if so, don't get the extended ingredients
    if used_ing:
        ingredients = response.get("extendedIngredients")
        ingredients = return_singular_form(ingredients)
        ingredients = return_ingredient_list(ingredients, used_ing)
        recipe["ingredients"] = json.dumps({"used_ings": ingredients})

    recipe["source"] = source
    recipe["cooktime"] = cooktime

    return recipe


################################################################################
#                                PROCESS RECIPES                               #
# Update, parses, and queries recipe data                                      #
################################################################################


def query_bookmarks(user_id):
    """Query for bookmarked recipes."""

    bookmarked = BookmarkedRecipe.query.filter_by(user_id=user_id).all()
    return bookmarked


def query_cooked_recipe(user_id):
    """Query for cooked recipes."""

    cooked = UsedRecipe.query.filter_by(user_id=user_id).all()
    return cooked


def return_stored_recipes(stored_recipes, avail_ingredients, user_id, bookmark=False):
    """Return recipes stored from database."""

    recipes = []

    avail_ingredients = [ingredients[0] for ingredients in avail_ingredients]
    avail_ingredients = ",".join(avail_ingredients)

    for stored_recipe in stored_recipes:
        recipe = {}

        ingredients = (recipe_info(stored_recipe.recipe_id, avail_ingredients))["ingredients"]

        recipe["recipe_id"] = stored_recipe.recipe_id
        recipe["image"] = stored_recipe.recipe.image_url
        recipe["title"] = stored_recipe.recipe.title
        recipe["source"] = stored_recipe.recipe.source_url
        recipe["ingredients"] = ingredients
        recipe["bookmarked"] = bookmark

        recipes.append(recipe)

    return recipes


def add_recipe(user_id, recipe_id, title, image, source):
    """Add recipe to recipe table."""

    db_recipe = Recipe.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()

    if db_recipe:
        pass
    else:
        recipe = Recipe(recipe_id=recipe_id,
                        user_id=user_id,
                        title=title,
                        image_url=image,
                        source_url=source)

        db.session.add(recipe)
        db.session.commit()


def add_bookmark(user_id, recipe_id):
    """Add bookmarked recipe to bookmarked_recipes table if it does not exist."""

    bookmarked_recipe = BookmarkedRecipe(user_id=user_id,
                                         recipe_id=recipe_id)
    db.session.add(bookmarked_recipe)
    db.session.commit()


def update_cooked_recipe(user_id, recipe_id, ingredients):
    """Update cooked recipe ingredient amounts and add to database if not there already."""

    db_recipe = UsedRecipe.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()

    if db_recipe:
        pass
    else:
        used_recipe = UsedRecipe(user_id=user_id,
                                 recipe_id=recipe_id)

        db.session.add(used_recipe)
        db.session.commit()

    for key, value in ingredients.items():
        for ing in ingredients["used_ings"]:
            amount = ing["amount"]
            name = ing["name"]
            unit = ing["unit"]

            if unit == "":
                unit = "none"

            update_ingredient_amount(user_id, name, unit, amount)


def return_suggested_recipes(user_id):
    """Return a list of suggested recipes from the Spoonacular API."""

    avail_ingredients = db.session.query(Ingredient.name).filter(Ingredient.user_id == user_id, Ingredient.amount > 0).all()  # Returns a list of tuples
    avail_ingredients = ",".join([ingredient[0] for ingredient in avail_ingredients])  # Creating a comma separated string (required for API argument)

    suggested_recipes = recipe_request(avail_ingredients, user_id)  # API request returns a dictionary with: id, image_url, recipe name, source, only the used ingredients and the amount

    return suggested_recipes


def parse_api_recipes(responses, user_id):
    """Return a list of recipes from the API that are not stored in the database."""

    recipes = []

    for response in responses:
        recipe = {}

        used_ingredients = response.get("usedIngredients")
        used_ingredients = [ingredient["name"] for ingredient in used_ingredients]

        recipe["recipe_id"] = response['id']
        recipe["image"] = response['image']
        recipe["title"] = response['title']
        recipe["bookmarked"] = False
        recipe["ingredients"] = json.dumps({"used_ings": used_ingredients})

        # Check if a recipe has been cooked or bookmarked before
        stored_id = Recipe.query.filter_by(user_id=user_id, recipe_id=response['id']).first()

        # If stored id is not None, continue to the next iteration
        if stored_id:
            continue

        recipes.append(recipe)

    return recipes

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
