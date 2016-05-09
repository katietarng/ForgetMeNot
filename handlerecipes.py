import os
import unirest


#Dynamically pass in in
def recipe_request():
    """Send a GET request for recipes."""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"

    request = unirest.get(
        url,
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_API_KEY"],
            "Accept": "application/json"
        },
        params={
            "fillIngredients": True,  # Adds information about used ingredients
            "ingredients": "apple,sugar,flour",  # List of ingredients as a string
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

        
