import os
import unirest


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
            "number": 10,  # Maximal number of recipes to return
            "ranking": 2  # Minimizes missing ingredients
        }
    )

    responses = request.body  # Returns a list of dictionaries that are recipes

    for response in responses:
        recipe_id = response['id']
        image = response['image']
        title = response['title']
        ingredients = response['usedIngredients'] + response['missedIngredients']

        ingredients = [ingredient['name'] for ingredient in ingredients]

        recipes = {title: ingredients}

        return recipes


def recipe_info(recipe_id):
    """Return individual recipe information."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information".format(recipe_id)

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"]
        }
    )

    response = request.body  # Returns one dictionary with a list of dictionary ingredients

    #Need to link source URL from response body

    ingredients = response.get('extendedIngredients')

    # List of ingredients as tuples
    ingredients = [(ingredient['name'], ingredient['amount'], ingredient['unit']) for ingredient in ingredients]

    return ingredients


