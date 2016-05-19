from model import *
from measurement.measures import Volume, Weight

# ~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~


def return_current_ingredients(current_ingredients):
    """Return a list of dictionaries containing ingredients."""

    ings = []
    for ingredient in current_ingredients:
        ingredients = {}

        unit = match_units(ingredient.unit)
        name = ingredient.name
        amount = ingredient.amount

        if amount > 1 and unit != "none":  # Pluralize the units
            unit = unit + "s"

        ingredients["unit"] = unit
        ingredients["name"] = name
        ingredients["amount"] = amount

        ings.append(ingredients)

    return ings


def add_bookmark(user_id, recipe_id):
    """Add bookmarked recipe to database."""

    bookmarked_recipe = BookmarkedRecipe(user_id=user_id,
                                         recipe_id=recipe_id)
    db.session.add(bookmarked_recipe)
    db.session.commit()


def add_cooked_recipe(user_id, recipe_id, ingredients):
    """Add cooked recipe and the used ingredients to database."""

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

            # Check to see if the used ingredient is already in the table
            used_ing = UsedIngredient.query.filter_by(name=name).first()

            # If so, add the amount to used_ingredient
            if used_ing:
                used_ing.amount += amount
            else:
                used_ingredient = UsedIngredient(user_id=user_id,
                                                 name=name,
                                                 amount=amount,
                                                 unit=unit)

                db.session.add(used_ingredient)
            db.session.commit()


def match_units(unit):
    """Return key or value of unit provided."""

    UNITS = {"lb": "pound",
             "ounce": "ounce",
             "gram": "gram",
             "liter": "liter",
             "us_g": "gallon",
             "quart": "quart",
             "pint": "pint",
             "us_cup": "cup",
             "us_tbsp": ["tablespoon", "tbsp"],
             "us_tsp": ["teaspooon", "tsp"],
             "serving": "ounce",
             "none": "none"
             }

    for key, value in UNITS.items():
        if key == unit:
            return UNITS[key]
        if UNITS[key] == unit:
            return key


def calculate_amount():
    """Calculate new ingredient amount after ingredient has been used."""

    user_id = session.get('user_id', None)

    ingredients = Ingredient.query.filter_by(user_id=user_id).all()

    for ingredient in ingredients:
        used_ing = UsedIngredient.query.filter_by(name=ingredient.name, user_id=user_id).first()
        unit = used_ing.unit  # Unit for used ingredient
        unit = match_units(unit)
        ing_unit = ingredient.unit

        if unit != ing_unit: 
            # Run calculation
            pass
        else: 
            amount = ingredient.amount - used_ing.amount
        
        db.session.query(Ingredient).filter_by(name=ingredient.name, user_id=user_id).update({Ingredient.amount: amount})

    db.session.commit()


def convert_units(unit):
    """Convert used ingredient unit to current ingredient unit."""

    measurement = IngMeasurement.query.filter_by(name=used_ing.name).first()

    if measurement: 
        amount = used_ing.amount * measurement.gram
        weight = Weight(grams=amount)

        # To DO: turn weight in grams to ingredient amount units

















