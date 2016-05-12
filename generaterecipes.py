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
            "ranking": 1  # Minimizes missing ingredients
        }
    )

    responses = request.body  # Returns a list of dictionaries that are recipes
    recipes = []

    for response in responses:
        recipe_id = response['id']
        image_url = response['image']
        title = response['title']

        info = recipe_info(recipe_id)
        source = info[0]
        ingredients = info[1]

        recipe = (recipe_id, image_url, title, source, ingredients)
        recipes.append(recipe)

    return recipes


def recipe_info(recipe_id):
    """Return recipe information for a single recipe."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information".format(recipe_id)

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"]
        }
    )

    response = request.body  # Returns a single response!!!

    source = response.get("sourceUrl")
    ingredients = response.get("extendedIngredients")

    ingredients = [(ingredient['name'], ingredient['amount'], ingredient['unit']) for ingredient in ingredients]

    recipe = (source, ingredients)

    return recipe
