// Tabs
function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    $('#' + cityName).parent().find('.tabcontent').removeClass('active').css('display', 'none');
    $('#' + cityName).parent().find('.tablinks').removeClass('active');
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

// OwelSlider

$(document).ready(function() {
    var owl = $('.owl-carousel');
    owl.owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        loop: true,
        responsive: {
            0: {
                items: 2
            },
            300: {
                items: 3
            },
            600: {
                items: 4
            },
            1000: {
                items: 5
            },
            1200: {
                items: 6
            },
            1400: {
                items: 8
            }
        }
    })
})


function searchToggle(obj, evt) {
    var container = $(obj).closest('.search-wrapper');
    if (!container.hasClass('active')) {
        container.addClass('active');
        evt.preventDefault();
    } else if (container.hasClass('active') && $(obj).closest('.input-holder').length == 0) {
        container.removeClass('active');
        // clear input
        container.find('.search-input').val('');
    }
}