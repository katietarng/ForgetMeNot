"use strict";

function addUsedRecipe(evt) {

    var used = {
        "button": $(this).attr("class"),
        "api_id": $(this).parent().attr("id"),
        "ingredients": $(this).siblings(".ingredients").html(),
        "image": $(this).data("image"),
        "title": $(this).data("name"),
        "source": $(this).data("link")
    };

    // Send AJAX post request to route with dictionary apiId
    // Success function will change cook button to "cooked" or will tepmorarily let you know that you have cooked the recipe
    $.get("/add-recipe.json",
            used,
            function (result) {
                  if (result === "You have already cooked this recipe.") {
                    alert(result);
                } else {
                    $("#" + result.id).find(".cook").html("Cooked");
                    console.log("Inserted into db.");
                }
          }
);}

$('.cook').on('click', addUsedRecipe);

function addToBookmarks (evt) {

    var bookmarked = {
        "button": $(this).attr("class"),
        "api_id": $(this).parent().attr("id"),
        "ingredients": $(this).siblings(".ingredients").html(),
        "image": $(this).data("image"),
        "title": $(this).data("name"),
        "source": $(this).data("link")
    };

    $.get("/add-recipe.json",
        bookmarked,
        function (result) {
            if (result === "You have already bookmarked this recipe") {
                alert(result);
            } else {
                $("#" + result.id).find(".bookmark").html("Bookmarked");
                console.log("Inserted into db.");
            }
        });
}

$('.bookmarks').on('click', addToBookmarks);

