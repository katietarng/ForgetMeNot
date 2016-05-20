from model import *
import pint 

p = pint.UnitRegistry(system="US")

# ~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~


def return_current_ingredients(current_ingredients):
    """Return a list of dictionaries containing ingredients."""

    ings = []
    for ingredient in current_ingredients:
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


def calculate_amount():
    """Calculate new ingredient amount after ingredient has been used."""

    # user_id = session.get('user_id', None)
    user_id = 1
    used_ings = UsedIngredient.query.filter_by(user_id=user_id).all()

    for used_ing in used_ings:
        ingredient = Ingredient.query.filter_by(name=used_ing.name, user_id=user_id).first()
        ing_unit = ingredient.unit

        if used_ing.unit != ing_unit:
            used_amount = convert_units(used_ing, ing_unit)
            amount = float("%0.2f" % (ingredient.amount - used_amount))
            print amount
        else:
            amount = ingredient.amount - used_ing.amount
            print amount
        db.session.query(Ingredient).filter_by(name=ingredient.name, user_id=user_id).update({Ingredient.amount: amount})

    db.session.commit()


def convert_units(used_ing, ing_unit):
    """Convert used ingredient unit to current ingredient unit."""

    measurement = IngMeasurement.query.filter_by(name=used_ing.name).first()  # Query to see if ingredient is in measurements library

    # If volume to weight conversion exists in measurements table, run the calculation below
    if measurement:
        used_amount = str(used_ing.amount * measurement.gram)
        used_amount += "gram"
        used_amount = p(used_amount).to(ing_unit)
        used_amount = used_amount.m  # Using the m method from the pint library to grab the value
        return used_amount
    # If ingredient does not exist in measurements table, convert units
    else:
        used_amount = str(used_ing.amount + used_ing.unit)
        used_amount = p(used_amount).to(ing_unit)
        used_amount = used_amount.m
        return used_amount


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."














