#ForgetMeNot

![ForgetMeNot](/static/images/Readme/screenshot-login.png)

ForgetMeNot is a helpful web app created with the home cook in mind. Built to keep track of ingredient amounts a user has within their fridge or pantry, this web application keeps users aware of ingredients that are depleted. ForgetMeNot will also generate recipes for any given set of ingredients. Users have the functionality to bookmark or cook a recipe. Once a recipe is cooked, the ingredient amounts are automatically updated in the user’s profile to show how much of an ingredient is left. 

## Table of Contents
* [Technologies Used](#technologiesused)
* [How to use ForgetMeNot](#use)
* [Local Installation and Running the Application](#install)
* [Credits](#credits)

## <a name="technologiesused"></a>Technologies Used
* Python
* Flask
* SQLAlchemy Object Relational Mapper
* Javascript/jQuery
* Jinja2
* CSS + Bootstrap
* AJAX/JSON
* HTML/CSS
* Python unittests
* Spoonacular API
* Bcrypt 

(Dependencies are listed in requirements.txt)

## <a name="use"></a>How to use ForgetMeNot
###Profile

![Profile](/static/images/Readme/screenshot-profile.png)

A user can input the ingredient name, amount, and units of the ingredients available in their fridge or pantry. Upon submission, the ingredients are updated in the database and posted into the "Current Ingredients" section. The page also contains a section with "Ingredients You Need to Buy", as the ingredient amounts are deducted each time a recipe is cooked. 

###Recipes

####Suggested Recipes

![Suggested Recipes](/static/images/Readme/screenshot-suggested-recipes.png)
-------------
![Suggested Recipes](/static/images/Readme/screenshot-recipe-details.png)

Users can view a list of suggested recipes based on the ingredients in their profile. The API minimizes the number of missing ingredients in each recipe to prevent users from having to run to the grocery store. If a user is interested in a particular recipe, they can click on the "See Details" button which shows the cooktime of a recipe, as well as, the amounts and units of the ingredients that match their profile.

####Bookmarked and Cooked Recipes

![Bookmarked Recipes](/static/images/Readme/screenshot-bookmark-cook.png)

When a user chooses to bookmark or a cook a recipe, the recipe is saved to the local database and filtered out of the suggested recipe API response. The user can then access their bookmarks and cooked recipes through the navigation bar if they want to view the recipes they've cooked or bookmarked. Note that the user is able to re-cook a recipe again.


###Ingredient Unit Conversion

![Ingredient Recipes](/static/images/Readme/screenshot-cooked.png)

When a user clicks on the "Cook" button in the overlay, an AJAX request is sent back to the server, which then queries the database to check for an existing volume to weight conversion for that ingredient. The server then converts the ingredient unit in the overlay to match the ingredient unit in their profile and deducts accordingly. If an ingredient is fully depleted, the ingredient will be shown under the "Ingredients You Need to Buy" section. If not, then the amount of the ingredient is updated in the "Current Ingredients" section.  

## <a name="use"></a>Local Installation and Running the Application

* Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
  
* Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
    * Seed data into database: `python seed.py`
    
* Now, quit interactive mode. Start up the flask server:
    * `python server.py`

* Go to localhost:5000 to see the web app

## <a name="credits"></a>Credits

* Credits to [Spoonacular's API](https://spoonacular.com/) for providing recipe information
* Credits to [King Arthur Flour](http://www.kingarthurflour.com/learn/ingredient-weight-chart.html) for ingredient volume to weight conversions.


