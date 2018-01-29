(function($) { $(function() {
    // Allow whole list item to post to be clickable
    $("#posts li").click(function(){
        location.assign($(this).attr("data-url"));
    });
    
    // Add Title placeholder
    $("#id_title").attr("placeholder", "Title your post");
    
    // set sidebar height
    $('#sidebar').css("height", window.innerHeight - 55 );


    $(document).ready(function(){
       $("#delete-post").click(function(e){
            e.preventDefault();
            if (window.confirm("Are you sure?")) {
               $("#delete-post-form").submit();
           }
       });
    });

}); })(jQuery);
