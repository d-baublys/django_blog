
$(document).ready(function () {
    $('.year, .month').click(function (event) {
        event.stopPropagation();
        $(this).toggleClass('revealed');
        $(this).children('ul').toggle();
    });

    $('.date').click(function (event) {
        event.stopPropagation();
    });
});
