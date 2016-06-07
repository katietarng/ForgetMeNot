"use strict";

$(document).ready(function() {
    var max_fields = 5;
    var field = 1;

    $("#ingForm")
        .on("submit", function(e){
            // .trim method trims out whitespace before and after string
            if ($.trim($(".form-control").val()) === "") {
                alert("Please fill out the entire form.");
                e.preventDefault();
            }
        })
        .on("click", ".addButton", function(e) {
            if (field < max_fields) {
                $("#ingTemplate").clone()
                                 .removeAttr("hidden")
                                 .removeAttr("id")
                                 .insertBefore("#ingTemplate");
                field++;
            }
        })
        .on("click", ".removeButton", function(e) {
            if (field > 1){
                $(this).parents(".form-group").remove();  // Use the .parents() method to traverse up through the ancestors of the DOM tree
                field--;
            }
        });
        
});

