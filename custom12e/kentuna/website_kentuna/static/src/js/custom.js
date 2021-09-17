
$(document).ready(function(){
$('.features_product_caroseul').owlCarousel({
    loop:false,
    responsiveClass:true,
    autoplay: false,
    responsive:{
        0:{
            items:1,                                                                                                                                                                                                                                                                                                                
        },
        600:{
            items:2,
        },
        768:{
            items:3,
            nav:true,
        },
        1000:{
            items:4,
            nav:true,
        }
    }
});
});

