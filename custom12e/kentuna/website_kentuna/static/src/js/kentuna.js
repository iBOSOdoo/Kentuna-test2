odoo.define('website_kentuna.kentuna', function (require) {
"use strict";
var rpc=require('web.rpc');
$(document).ready(function(){
    var ajax = require('web.ajax');
    var session = require('web.session');


    if(session['user_id']==4){
        $(".navbar-light.bg-light").css('top','0%');
    }
//    else{
//        $(".navbar-light").css('top','6%');
//    }
    if(screen.width == 768){
        $('body').addClass("height_kentuna_content");
    }
    else{
        $('body').removeClass("height_kentuna_content");
    }
    console.log(".........session/......",session['user_id'])
    if(session['user_id']==4){
        $(".navbar-light").css('top','0%');
    }
//    else{
//        $(".navbar-light").css('top','6%');
//    }

     $(".description_tab").click(function(){
        $("#tab-description").css('display','block');
        $(".review_rating_class").css('display','none');
        $('body').addClass("tab_description");
        $('.review_color').css('color','#515151');
        $(".Des_color").css('border-top','2px solid Blue');
        $('body').removeClass("review_rate_tag");
    });

    $(".reviews_tab").click(function(){
        $("#tab-description").css('display','none');
        $(".review_rating_class").css('display','block');
        $('body').removeClass("tab_description");
        $('body').addClass("review_rate_tag");
        $(".Des_color").css('border-top','none');
        $('.Des_color').css('color','#515151');
    });


    window.onscroll = function() {scrollFunction()};
        function scrollFunction()
        {
            if (document.body.scrollTop > 20|| document.documentElement.scrollTop > 20)
            {
                $("body").addClass("navbar_scroll");

            }
            else{
                $("body").removeClass("navbar_scroll");

            }
        }

        $('#send_message').click(function(){
            $('.thanks_page').css('display','block');
            $('.s_website_form').css('display','none');
         });

});


});




