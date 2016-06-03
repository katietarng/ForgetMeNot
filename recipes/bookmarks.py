def add_bookmark(user_id, recipe_id):
    """Add bookmarked recipe to bookmarked_recipes table if it does not exist."""

    bookmarked_recipe = BookmarkedRecipe(user_id=user_id,
                                         recipe_id=recipe_id)
    db.session.add(bookmarked_recipe)
    db.session.commit()