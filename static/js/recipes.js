"use strict";

function addRecipe(evt) {
    
    var recipe = {
        "button": $(this).attr("class"),
        "api_id": $(this).closest('.recipe').attr('id'),
        "ingredients": $(this).closest(".recipe").children(".ingredients").html(),
        "image": $(this).parent().siblings(".modal-body").find(".image").attr("src"),
        "title": $(this).parent().siblings(".modal-header").find(".modal-title").html(),
        "source": $(this).data("source")
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
            } else if ((result.button)[2] === "bookmarks") {
                $("#" + result.id).find(".bookmarks").html("Bookmarked");
            }
        });
}


$(document).ready(function () {

    $('.details')
        .on('click', showDetails);

    function showDetails(e) {
        e.preventDefault();

        var details = {
            "api_id": $(this).parent().attr("id"),
            "ingredients": $(this).siblings(".ingredients").html(),
            "image": $(this).data("image"),
            "title": $(this).data("title")
        };

        $.get("/recipe-details.json",
            details,
            function (result) {
                var recipeHtml = 'Cook Time: ' + result.info.cooktime +
                                 ' minutes' + '<br>Matched Ingredients: ' +
                                 '<br>';

                $("#modal-" + result.id).find(".modal-title").html(result.title);
                $("#modal-" + result.id).find(".modal-body .image").attr("src", result.image);
                $("#modal-" + result.id).find(".modal-body .description").html(recipeHtml);
                $("#modal-" + result.id).find(".cook").attr("data-source", result.info.source);
                $("#modal-" + result.id).find(".bookmarks").attr("data-source", result.info.source);
                
                var ingredients = (JSON.parse(result.info.ingredients)).used_ings;
                                  $.each(ingredients, function (key, value) {
                                    $("#modal-" + result.id).find(".modal-body .description")
                                    .append('<li> ' + value.name + ' ' + (value.amount).toFixed(1) + ' ' + value.unit + '</li>');
                                });

                $('#modal-' + result.id).modal();
            }
        );          
    }
});

$('.bookmarks').on('click', addRecipe);
$('.cook').on('click', addRecipe);




