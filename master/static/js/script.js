$(document).ready(function(){
    $('.form-add-product').on('submit', function(e){
         e.stopPropagation();
         e.preventDefault();

         var __loader__ = $('#loader');
         var parent =  $(this).parent().parent();
         var element = $('img', $(parent));
         var oldOffset = element.offset();
         var img = element.clone().appendTo('body');
         var newOffset = $('#aliments').offset();
         var width = $(img).css('width');
         var height = $(img).css('height');

         var form_data = new FormData(this);
         var _url = $(this).attr('action');
         var form = $(this);
         // active loader
         __loader__.show();
         $.ajax({
            url: _url,
            type: 'POST',
            data: {'id':form_data.get('id'),
                'sub_id':form_data.get('sub_id'),
                'csrfmiddlewaretoken':form_data.get('csrfmiddlewaretoken')
            },
            dataType : 'json'
         }).done(function (data) {


            if(data) {
                if(data.status == "success") {

                    $(img).css({
                        'position': 'absolute',
                        'left': oldOffset.left,
                        'top': oldOffset.top,
                        'width': width,
                        'height': height,
                        'zIndex': 1000
                    });

                    $(img).animate({
                        'top': newOffset.top,
                        'left': newOffset.left,
                        'width': 0,
                        'height': 0,
                    }, 'slow', function () {
                        $(img).remove();
                    });
                }
            }

         }).always(function () {
            __loader__.hide();
         });


    });

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {scrollFunction()};

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("btn-top").style.display = "block";
        } else {
            document.getElementById("btn-top").style.display = "none";
        }
    }

    // When the user clicks on the button, scroll to the top of the document
    $('#btn-top').on('click',function() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    });

    // autocomplete search
    $('#autocomplete-product').autocomplete({
       minLength:4,
       source: function (req, response) {
           var search = $('#autocomplete-product').val();
           var url = $('#autocomplete-product').attr("data-href");
           $.ajax({
               url : url,
               async : false,
               dataType : 'json',
               type : 'GET',
               data : {term : search},
               success: function(data){
                   response(data)
               }

           });
       } 
    });
    // autocomplete search
    $('#autocomplete-product-2').autocomplete({
       minLength:4,
       source: function (req, response) {
           var search = $('#autocomplete-product-2').val();
           var url = $('#autocomplete-product-2').attr("data-href");
           $.ajax({
               url : url,
               async : false,
               dataType : 'json',
               type : 'GET',
               data : {term : search},
               success: function(data){
                   response(data)
               }

           });
       }
    });

    var checkImage = function(url, callback) {
        var res = url.substring(0, 4);
        if(res == 'http') {
            var img = new Image();
            img.onerror = function () {
                callback();
            };
            img.src = url;
        }

    }



    $('img').each(function(idx, item){
        var img_src = $(item);
        checkImage($(item).attr('src'), function(){
            img_src.attr('src', '/static/img/noimage.png');
        });
    });
});