import os
import unirest
from model import *
import inflect
import json

# ~~~~~~~~~~~~Spoonacular API request and responses~~~~~~~~~~~~~~

# Initiate w as an object of the inflect module
w = inflect.engine()


def recipe_request(ingredients, user_id):
    """Return a list of recipes that matches ingredient list."""

    # Using the inflect module, change any plural ingredients into singular ingredients
    ings = []
    for ingredient in ingredients:
        if ingredient[-1] == "s":
            ingredient = w.singular_noun(ingredient, count=1)  # Setting count=1, allows it to return the singular form
        else:
            ingredient = w.singular_noun(ingredient, count=0)

        ings.append(ingredient)

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"],
            "Accept": "application/json"
        },
        params={
            "fillIngredients": True,  # Adds information about used ingredients
            "ingredients": ings,  # List of ingredients as a string
            "number": 30,  # Maximal number of recipes to return
            "ranking": 1  # Minimizes missing ingredients
        }
    )

    responses = request.body  # Returns a list of dictionaries that are recipes

    suggested_recipes = return_suggested_recipes(responses, user_id)
    return suggested_recipes


def recipe_info(recipe_id):
    """Return recipe information for a single recipe."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information".format(recipe_id)

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"]
        }
    )

    response = request.body  # Returns a single response

    source = response.get("sourceUrl")
    ingredients = response.get("extendedIngredients")
    ingredients = return_singular_form(ingredients)

    recipe = (source, ingredients)
    return recipe


def return_suggested_recipes(responses, user_id):
    """Return a list of suggested recipes that are not stored in the database."""

    suggested_recipes = []

    for response in responses:
        recipe = {}

        used_ingredients = response.get("usedIngredients")  # Used ingredients is a list of dictionaries
        used_ingredients = [(used_ingredient['name'],) for used_ingredient in used_ingredients]

        source = (recipe_info(response['id']))[0]
        ings = return_ingredient_list(response['id'], used_ingredients)

        recipe["recipe_id"] = response['id']
        recipe["image"] = response['image']
        recipe["name"] = response['title']
        recipe["source"] = source
        recipe["ingredients"] = json.dumps({"used_ings": ings})

        # Check if a recipe has been cooked or bookmarked before
        stored_id = Recipe.query.filter_by(user_id=user_id, recipe_id=response['id']).first()

        # If stored id is not None, continue to the next iteration
        if stored_id:
            continue

        suggested_recipes.append(recipe)

    return suggested_recipes


def return_ingredient_list(id, used_ingredients):
    """Return ingredient list with name, amount, and unit."""

    ingredients = (recipe_info(id))[1]

    ings = []
    # Grab the ingredients that are used in the recipe and return the amount, unit used for that ingredient in the recipe
    for ingredient in ingredients:
        ing = {}
        name = ingredient[0].split()  # Split the ingredient name if it is two words and grab the ingredient name

        for used_ingredient in used_ingredients:
            if name[-1] in used_ingredient[0]:  # Check if the ingredient is in the used ingredients list
                ing["name"] = name[-1]
                ing["amount"] = ingredient[1]
                ing["unit"] = ingredient[2]
                ings.append(ing)

    return ings


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


