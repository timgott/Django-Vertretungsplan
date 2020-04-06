// custom ja functions
function show_field(value){
    if (value >= 11 && value <= 13) {
        $(".show-field").removeClass('hidden');
    } else if (value < 11 || value > 13){
        $(".show-field").addClass('hidden');
    }
};

var counter = 0

$(document).ready(function() {
    // from stackoverflow
    $(".add-more").click(function(){ 
        if (counter < 12) {
            var html = $(".copy").html();

            $(".after-add-more").after(html);
            counter ++;
        };
    });

    $("body").on("click",".remove",function(){ 

        $(this).parents(".control-group").remove();
        counter --;

    });

    // custom jQuery script
    show_field($(".show-control").val());

    $(".show-control").on("input", function(){
        show_field($(this).val());
    });
});
