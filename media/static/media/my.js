$(document).ready(function() {

        $('.likes').click(function(){
            var tag_id;
            tag_id = $(this).attr("data-tag_id");
             $.get('like_tag/', {tag_id: tag_id}, function(data){
                       $('#like_count_'+tag_id.toString()).html(data); //# - доступ по id, . - доступ по классу, id уникален, класс нет
                       //$('#likes').hide();
                   });
        });

        $('#suggestion').keyup(function(){
            var query;
            query = $(this).val();
            $.get('suggest_song/', {suggestion: query}, function(data){
                $('#songs').html(data);
            });
        });

        $('#artist_selector').on("select2-selecting", function(e) {
            var artist = e.val;
            var albums = jQuery.getJSON('albums.json',{artist:artist});
            alert("selected: "+JSON.stringify(albums));
        })

});