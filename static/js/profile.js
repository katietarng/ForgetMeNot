"use strict";

function validateForm (evt) {
    event.preventDefault();
    alert("Fill out the entire form before submitting!");
}


$(document).ready(function() {

    $("#ingForm")
        .on("click", ".addButton", function() {
            $("#ingTemplate").clone()
                             .removeAttr("hidden")
                             .removeAttr("id")
                             .insertBefore("#ingTemplate");

        })
        .on("click", ".removeButton", function() {
            $(this).parents(".form-group").remove();  // Use the .parents() method to traverse up through the ancestors of the DOM tree
        });
        
});
