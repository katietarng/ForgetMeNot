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

    if ($(this).attr("class") === "btn btn-default cook") {
        window.open($(this).data("link"), "_blank");
    }

    sendServerRequest(recipe);
}

function sendServerRequest(recipe) {
        
    $.get("/add-recipe.json",
        recipe,
        function (result) {
              if (result.button === "btn btn-default cook") {
                $("#" + result.id).find(".cook").html("Cooked");
            } else if (result.button === "btn btn-default bookmarks") {
                $("#" + result.id).find(".bookmarks").html("Bookmarked");
            }
        });
}


$('.cook').on('click', addRecipe);
$('.bookmarks').on('click', addRecipe);





