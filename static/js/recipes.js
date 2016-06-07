"use strict";

function showDetails(e) {

    var details = {
        "api_id": $(this).parent().attr("id"),
        "ingredients": $(this).siblings(".ingredients").html(),
        "image": $(this).data("image"),
        "title": $(this).data("title")
    };

    $.get("/recipe-details.json",
        details,
        function (result) {
            var cooktimeHtml = '<b class="ing-label">Cook Time:</b> ' + result.info.cooktime +
                             ' minutes';
            var ingHtml = '<b class="ing-label">Matched Ingredients:</b> ' +
                             '<br>';

            $("#modal-" + result.id).find(".modal-title").html(result.title);
            $("#modal-" + result.id).find(".modal-body .modal-image").css("background-image", "url('" + result.image + "')");
            $("#modal-" + result.id).find(".modal-body .cooktime").html(cooktimeHtml);
            $("#modal-" + result.id).find(".modal-body .matched-ing").html(ingHtml);

            $("#modal-" + result.id).find(".cook").attr("data-source", result.info.source);
            $("#modal-" + result.id).find(".cook").attr("data-ing", result.info.ingredients);
            $("#modal-" + result.id).find(".cook").attr("data-image", result.image);

            $("#modal-" + result.id).find(".bookmarks").attr("data-ing", result.info.ingredients);
            $("#modal-" + result.id).find(".bookmarks").attr("data-source", result.info.source);
            $("#modal-" + result.id).find(".bookmarks").attr("data-image", result.image);
            
            var ingredients = (JSON.parse(result.info.ingredients)).used_ings;
                              $.each(ingredients, function (key, value) {
                                $("#modal-" + result.id).find(".modal-body .matched-ing")
                                .append('<i class="fa fa-square-o" aria-hidden="true" style="font-size: x-small"></i>  ' + value.name + ' ' + (value.amount).toFixed(1) + ' ' + value.unit + '<br>');
                            });

            $('#modal-' + result.id).modal();
        }
    );         
}

function addRecipe(evt) {
    
    var recipe = {
        "button": $(this).attr("class"),
        "api_id": $(this).closest('.recipe').attr('id'),
        "ing": JSON.stringify($(this).data("ing")),
        "image": $(this).data("image"),
        "title": $(this).parent().siblings(".modal-header").find(".modal-title").html(),
        "source": $(this).data("source")
    };

    if ($(this).attr("class") === "btn btn-default cook") {
        window.open($(this).data("source"), "_blank");
    }

    sendServerRequest(recipe);
}


function sendServerRequest(recipe) {
        
    $.get("/add-recipe.json",
        recipe,
        function (result) {
              if (result.button[2] === "cook") {
                $("#" + result.id).find(".cook").html("Cooked");
            } else if ((result.button)[2] === "bookmarks") {
                $("#" + result.id).find(".bookmarks").html("Bookmarked");
            }
        });
}

$(function () {

    $('.details')
        .on('click', showDetails);
    $('.bookmarks')
        .on('click', addRecipe);
    $('.cook')
        .on('click', addRecipe);

    $(".recipe").slice(0, 6).css("display", "inline-block");
    $("#load").click(function(e){
        e.preventDefault();
        $(".recipe:hidden").slice(0, 6).css("display", "inline-block");
        if($(".recipe:hidden").length === 0){
            $("#load").hide();
        }
    });


});





