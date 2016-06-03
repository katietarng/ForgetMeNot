import inflect
import pint
from datetime import datetime
from model import User, IngMeasurement, Ingredient, UsedRecipe, BookmarkedRecipe, Recipe, connect_to_db, db

w = inflect.engine()
p = pint.UnitRegistry(system="US")


################################################################################
#                                RETURN INGREDIENTS                            #
# Use functions to return ingredients to server                                #
################################################################################


def return_ingredient_list(ingredients, used_ingredients):
    """Return ingredient list with name, amount, and unit."""

    ings = []

    for ingredient in ingredients:
        ing = {}
        name = ingredient[0].split()

        if name[-1] in used_ingredients:
            ing["name"] = name[-1]
            ing["amount"] = ingredient[1]
            ing["unit"] = ingredient[2]
            ings.append(ing)

    return ings


def return_db_ingredients(db_ingredients):
    """Return a list of dictionaries containing ingredients."""

    ings = []
    for ingredient in db_ingredients:
        ingredients = {}

        if ingredient.amount > 1 and ingredient.unit != "none":
            ingredients["unit"] = w.plural(ingredient.unit)
        else:
            ingredients["unit"] = ingredient.unit

        ingredients["name"] = ingredient.name
        ingredients["amount"] = ingredient.amount

        ings.append(ingredients)

    return ings


def return_avail_ingredients(user_id):
    """Return ingredients that are not depleted."""

    avail_ing = Ingredient.query.filter(Ingredient.user_id == user_id, Ingredient.amount > 0).all()
    return avail_ing


def ingredient_names(user_id):
    """Return the names of ingredients that are not depleted."""

    ingredient_names = db.session.query(Ingredient.name).filter(Ingredient.user_id == user_id, Ingredient.amount > 0).all()
    return ingredient_names


def return_depleted_ingredients(user_id):
    """Return depleted ingredients."""

    depleted_ing = db.session.query(Ingredient.name).filter_by(user_id=user_id, amount=0).all()
    return depleted_ing


################################################################################
#                      UPDATES INGREDIENTS TABLE IN DATABASE                   #
# Used to update ingredients table                                             #
################################################################################


def add_ingredients(ingredients, amounts, units, user_id):
    """Add new ingredients into Ingredients table in database."""
    # Map function applies the int() function to the amounts list
    # which changes the amounts from a list of strings to a list of integers
    amounts = map(float, amounts)
    ingredients = zip(ingredients, amounts, units)

    if ingredients:
        input_date = datetime.utcnow()

        for ingredient in ingredients:
            name = ingredient[0]
            amount = ingredient[1]
            unit = ingredient[2]

            db_ingredient = db.session.query(Ingredient).filter_by(user_id=user_id, name=name).first()

            if db_ingredient:
                amount += db_ingredient.amount
                db.session.query(Ingredient).filter_by(user_id=user_id, name=name).update({Ingredient.amount: amount,
                                                                                           Ingredient.unit: unit})
            else:
                new_ingredient = Ingredient(user_id=user_id,
                                            name=ingredient[0],
                                            amount=ingredient[1],
                                            unit=ingredient[2],
                                            input_date=input_date)

                db.session.add(new_ingredient)

            db.session.commit()


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


################################################################################
#                          PROCESS INGREDIENT ATTRIBUTES                       #
#                                                                              #
################################################################################



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
