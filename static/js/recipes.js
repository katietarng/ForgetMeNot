"use strict";

function addRecipe(evt) {

    var recipe = {
        "button": $(this).attr("class"),
        "api_id": $(this).parent().attr("id"),
        "ingredients": $(this).siblings(".ingredients").html(),
        "image": $(this).data("image"),
        "title": $(this).data("name"),
        "source": $(this).data("link")
    };

    sendServerRequest(recipe);
}

function sendServerRequest(recipe) {
        
    $.get("/add-recipe.json",
        recipe,
        function (result) {
              if (result.button === "cook") {
                $("#" + result.id).find(".cook").html("Cooked");
            } else if (result.button === "bookmarks") {
                $("#" + result.id).find(".bookmarks").html("Bookmarked");
            } else {
                alert(result);
            }
        });
}

$('.cook').on('click', addRecipe);
$('.bookmarks').on('click', addRecipe);





