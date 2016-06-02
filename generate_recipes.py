import os
import unirest
from model import *
import inflect
import json
from datetime import datetime

# ~~~~~~~~~~~~Spoonacular API request and responses~~~~~~~~~~~~~~

# Initiate w as an object of the inflect module
w = inflect.engine()


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

    suggested_recipes = return_suggested_recipes(responses, user_id)

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


def return_suggested_recipes(responses, user_id):
    """Return a list of suggested recipes that are not stored in the database."""

    suggested_recipes = []

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

        suggested_recipes.append(recipe)

    return suggested_recipes


def return_ingredient_list(ingredients, used_ingredients):
    """Return ingredient list with name, amount, and unit."""

    ings = []

    for ingredient in ingredients:
        ing = {}
        name = ingredient[0].split()  # Split the ingredient name if it is two words and grab the ingredient name

        if name[-1] in used_ingredients:
            ing["name"] = name[-1]
            ing["amount"] = ingredient[1]
            ing["unit"] = ingredient[2]
            ings.append(ing)

    return ings


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


def return_singular_form(ingredients):
    """Return singular form of ingredient."""

    ing = []
    for ingredient in ingredients:
        name = ingredient["name"]
        unit = ingredient["unit"].lower()

        # Using the inflect module, change any plural units into singular units - for consistency purposes
        if unit == "":
            pass
        elif unit[-1] == "s":
            unit = w.singular_noun(unit)

        # Using the inflect module, change any plural ingredients into singular ingredients
        # Singular ingredients are needed to match used ingredients in recipe request function
        if name[-1] == "s":
            name = w.singular_noun(name, count=1)  # Setting count=1, allows it to return the singular form
        else:
            name = w.singular_noun(name, count=0)  # Setting count=0, allows nouns that are already singular to return as is

        ingredient = (name, ingredient["amount"], unit)
        ing.append(ingredient)

    return ing


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
