$(function () {
    //slide part js
    $('.late').textillate({
        loop: true,
        minDisplayTime: 3000,
        initialDelay: 1000,
        in: {
            effect: 'bounceInDown',
            delayScale: 2,
        },
        out: {
            effect: 'bounce',
            delayScale: 1,
            shuffle: true,
        },
    });
    
    //slide part js
    $('#slider').slick({
        dots: false,
        autoplay: true,
        autoplaySpeed: 5000,
        prevArrow: '.pre_btn',
        nextArrow: '.next_btn',
    });

    //Book A Table Area js
    $('.Check_in ').datetimepicker({
        formatTime: 'H:i:i',
        formatDate: 'd.m.Y',
        theme: 'dark',
        step: 30,
        hours12: false,
    });
    $('.open').click(function () {
        $('.Check_in').datetimepicker('show');
    });
 
    $('.Check_out ').datetimepicker({
        formatTime: 'H:i:i',
        formatDate: 'd.m.Y',
        theme: 'dark',
        step: 30,
        hours12: false,
        
    });
    $('.open1').click(function () {
        $('.Check_out').datetimepicker('show');
    });
  // EXPLOR OUR ROOMS js
    $('.room_slide').slick({
        autoplay: true,
        autoplaySpeed:2000,
        slidesToShow:3,
        slidesToScroll:2,
        dots: true,
        arrows:false
    });
    // Udogodnienia — przełączanie zdjęć
    $('.aladu-service-item').on('click', function () {
        var $btn = $(this);
        var img = $btn.data('img');
        var label = $btn.data('label');
        $('.aladu-service-item').removeClass('is-active').attr('aria-selected', 'false');
        $btn.addClass('is-active').attr('aria-selected', 'true');
        $('#aladu-service-img').attr('src', img).attr('alt', label);
    });

   //OUR GALLERY js
    $('.gallary_overly').magnificPopup({
    type: 'image',
    gallery: {
      enabled: true,
      tPrev: 'Gallery_pre', 
      tNext: 'Gallery_next', 
    },
    });

    $('.GALLERY_slider').slick({
        autoplay: true,
        autoplaySpeed: 4000,
        slidesToShow: 4,
        slidesToScroll: 1,
        dots: false,
        arrows: true,
        prevArrow: $('.gallery-prev'),
        nextArrow: $('.gallery-next'),
        responsive: [
            { breakpoint: 992, settings: { slidesToShow: 2 } },
            { breakpoint: 576, settings: { slidesToShow: 1 } }
        ]
    });

      // Nasz zespół
     $('.Staff_slider').slick({
        autoplay: true,
        autoplaySpeed: 4500,
        slidesToShow: 4,
        slidesToScroll: 1,
        dots: false,
        arrows: true,
        prevArrow: $('.staff-prev'),
        nextArrow: $('.staff-next'),
        infinite: true,
        responsive: [
            { breakpoint: 1200, settings: { slidesToShow: 3 } },
            { breakpoint: 992, settings: { slidesToShow: 2 } },
            { breakpoint: 576, settings: { slidesToShow: 1 } }
        ]
    });
   
   //counter part js
    $('.counter').counterUp({
      delay:5,
      time: 1000,
      });  
 
 
});