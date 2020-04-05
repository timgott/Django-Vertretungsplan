// custom ja functions
function show_field(value){
    if (value >= 11 && value <= 13) {
        $(".show-field").removeClass('hidden');
    } else if (value < 11 || value > 13){
        $(".show-field").addClass('hidden');
    }
};

$(document).ready(function() {
    // from stackoverflow
    $(".add-more").click(function(){ 

        var html = $(".copy").html();

        $(".after-add-more").after(html);

    });

    $("body").on("click",".remove",function(){ 

        $(this).parents(".control-group").remove();

    });

    // custom jQuery script
    show_field($(".show-control").val());

    $(".show-control").on("input", function(){
        show_field($(this).val());
    });
});
