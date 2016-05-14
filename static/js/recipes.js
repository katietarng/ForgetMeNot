"use strict";

function addUsedRecipe(evt) {

    var apiId = {
        "api_id": $(this).parent().attr("id"),
        "image": $(this).data("image"),
        "source": $(this).data("link"),
        "title": $(this).data("name")
    };

    $.get("/used-recipe",
            apiId,
            function (result) {
                $('.cook').html(result);
                console.log("Inserted into db.");
          }
);}

$('.cook').on('click', addUsedRecipe);


// function addToFavorites(evt) {

// }

// $('.favorites').on('click', addToFavorites);