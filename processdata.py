from model import *
import pint

p = pint.UnitRegistry(system="US")

# ~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~


def return_db_ingredients(db_ingredients):
    """Return a list of dictionaries containing ingredients."""

    ings = []
    for ingredient in db_ingredients:
        ingredients = {}

        if ingredient.amount > 1 and ingredient.unit != "none":  # Pluralize the units
            unit = ingredient.unit + "s"
            ingredients["unit"] = unit
        else:
            ingredients["unit"] = ingredient.unit

        ingredients["name"] = ingredient.name
        ingredients["amount"] = ingredient.amount

        ings.append(ingredients)

    return ings


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


def update_ingredient_amount(user_id, name, unit, amount):
    """Update new ingredient amount after ingredient has been used."""

    ingredient = Ingredient.query.filter_by(name=name, user_id=user_id).first()
    db_ing_unit = ingredient.unit

    used_amount = convert_units(name, unit, amount, db_ing_unit)

    if used_amount:
        amount = float("%0.2f" % (max(ingredient.amount - used_amount, 0)))  # If the ingredient goes negative, make the ingredient = 0
        db.session.query(Ingredient).filter_by(name=ingredient.name, user_id=user_id).update({Ingredient.amount: amount})
        db.session.commit()
    else:
        pass


def convert_units(name, unit, amount, db_ing_unit):
    """Convert used ingredient unit to database ingredient unit."""

    measurement = IngMeasurement.query.filter_by(name=name).first()  # Query to see if ingredient is in measurements library
    used_amount = str(amount) + unit  # Setting integer amount into a string and combining with the unit

    # If unit of used ingredient in recipe matches the ingredient unit in fridge
    if unit == db_ing_unit:
        return amount

    # If ingredient does not exist in the measurements table
    if not measurement:
        try:
            used_amount = p(used_amount).to(db_ing_unit).m
            return used_amount
        except (pint.DimensionalityError, pint.UndefinedUnitError):  # If the units are incompatible, do not update and return boolean
            return None

    # If measurement unit does match used ingredient unit
    if (measurement.vol_unit != unit) and (unit != "g" or "gram" or "grams"):
        used_amount = p(used_amount).to(measurement.vol_unit)

    if name == "milk":
        amount *= measurement.volume
        used_amount = str(amount) + unit
        used_amount = p(used_amount).to(db_ing_unit).m
        return used_amount

    used_amount = str(amount * (float(measurement.gram)/measurement.volume)) + "gram"
    used_amount = p(used_amount).to(db_ing_unit).m  # Using the m method from the pint library to grab the value

    return used_amount


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    import doctest
    print
    result = doctest.testmod()
    if not result.failed:
        print "All tests passed."
    print

