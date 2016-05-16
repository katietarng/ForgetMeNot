import os
import unirest
from model import *
import inflect

# Initiate w as an object of the inflect module
w = inflect.engine()


#Dynamically pass in ingredients
def recipe_request(ingredients):
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
            "number": 15,  # Maximal number of recipes to return
            "ranking": 1  # Minimizes missing ingredients
        }
    )

    responses = request.body  # Returns a list of dictionaries that are recipes
    recipes = []
    used_ingredients = []

    # Within one recipe starting from line 30
    for response in responses:
        recipe_id = response['id']
        image_url = response['image']
        title = response['title']
        used_ingredients = response.get("usedIngredients")  # Used ingredients is a list of dictionaries
        used_ingredients = [used_ingredient['name'] for used_ingredient in used_ingredients]

        # Call recipe_info function below to return source URL and ingredients
        info = recipe_info(recipe_id)
        source = info[0]
        ingredients = info[1]

        ing = []

        # Grab the ingredients that are used in the recipe and return the amount, unit used for that ingredient in the recipe
        for ingredient in ingredients:     # Within a recipe within a single ingredient
            if ingredient[0] in used_ingredients:
                ingredient = (ingredient[0], ingredient[1], ingredient[2])
                ing.append(ingredient)
            else:
                pass

        recipe = (recipe_id, image_url, title, source, ing)
        recipes.append(recipe)

    print recipes


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

    ing = []

    for ingredient in ingredients:
        name = ingredient['name']

        # Using the inflect module, change any plural ingredients into singular ingredients
        # Singular ingredients are needed to match used ingredients in recipe request function
        if name[-1] == "s":
            name = w.singular_noun(name, count=1)  # Setting count=1, allows it to return the singular form
        else:
            name = w.singular_noun(name, count=0)  # Setting count=0, allows nouns that are already singular to return as is

        ingredient = [name, ingredient['amount'], ingredient['unit']]
        ing.append(ingredient)

    recipe = (source, ing)
    return recipe
