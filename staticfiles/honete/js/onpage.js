$(document).ready(function()
{
    $('.drop').hover(function() {
        if ($(this).hasClass('com'))
            $(this).parent('.mNav').find('.com').addClass('hovering');

        if ($(this).hasClass('gui'))
            $(this).parent('.mNav').find('.gui').addClass('hovering');

        if ($(this).hasClass('sto'))
            $(this).parent('.mNav').find('.sto').addClass('hovering');

        if ($(this).hasClass('med'))
            $(this).parent('.mNav').find('.med').addClass('hovering');

        if ($(this).hasClass('for'))
            $(this).parent('.mNav').find('.for').addClass('hovering');

        if ($(this).hasClass('ser'))
            $(this).parent('.mNav').find('.ser').addClass('hovering');
    }, function() {
        if ($(this).hasClass('com') && $(this).parent('.mNav').find('.com').hasClass('hovering'))
            $(this).parent('.mNav').find('.com').removeClass('hovering');

        if ($(this).hasClass('gui') && $(this).parent('.mNav').find('.gui').hasClass('hovering'))
            $(this).parent('.mNav').find('.gui').removeClass('hovering');

        if ($(this).hasClass('sto') && $(this).parent('.mNav').find('.sto').hasClass('hovering'))
            $(this).parent('.mNav').find('.sto').removeClass('hovering');

        if ($(this).hasClass('med') && $(this).parent('.mNav').find('.med').hasClass('hovering'))
            $(this).parent('.mNav').find('.med').removeClass('hovering');

        if ($(this).hasClass('for') && $(this).parent('.mNav').find('.for').hasClass('hovering'))
            $(this).parent('.mNav').find('.for').removeClass('hovering');

        if ($(this).hasClass('ser') && $(this).parent('.mNav').find('.ser').hasClass('hovering'))
            $(this).parent('.mNav').find('.ser').removeClass('hovering');
    });

    $('body').css("min-height", $(window).height() - 300 + "px");
    $('#mainContent').css("min-height", $(window).height() - 300 + "px");

    //START Smooth Scroll Anchors
    //console.log($(".scroll").length);
    $(".scroll").click(function(event) {
        event.preventDefault();
        var $anchor = $('#' + this.hash.substring(1));

        //Mobile
        if ($('body').hasClass('mobile')) {
            $('html,body').animate({
                scrollTop: $anchor.offset().top - 20
            }, 600);
        }
        else {
            $('html,body').animate({
                scrollTop: $anchor.offset().top - 50
            }, 600);
        }
    });
    //END Smooth Scroll Anchors
});

var hideTimer = null;

// Resize Window Effects
$(window).resize(function()
{
    $('body').css("min-height", $(window).height() - 300 + "px");
    $('#mainContent').css("min-height", $(window).height() - 300 + "px");
});

// Dropdown Menu
function showMenu(div)
{
    $('#' + div).stop().fadeTo("fast", 1).show();

    if (hideTimer != null) {
        clearTimeout(hideTimer);
        hideTimer = null;
    }

    if (div != "news")
        hideIt("news");

    if (div != "guides")
        hideIt("guides");

    if (div != "community")
        hideIt("community");

    if (div != "store")
        hideIt("store");

    if (div != "services")
        hideIt("services");

    if (div != "forums")
        hideIt("forums");

    if (div != "media")
        hideIt("media");
}

function hideMenu(div)
{
    hideTimer = setTimeout(function()
    {
        $("#" + div).fadeTo("fast", 0, function()
        {
            $(this).hide();
        });
    }, 200);
}

function showIt(div)
{
    $('#' + div).show();
}

function hideIt(div)
{
    $('#' + div).hide();
}
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));