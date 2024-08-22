
$(document).ready(function () {
    $('.year, .month').click(function (event) {
        event.stopPropagation();
        $(this).toggleClass('reveal');
        $(this).children('ul').toggle();
    });

    $('.date').click(function (event) {
        event.stopPropagation();
    });
});


const header = document.querySelector(".b-header");
const banner = document.querySelector(".banner");
const bannerScroll = banner.clientHeight - header.clientHeight;

window.addEventListener("scroll", () => {
    if (window.scrollY > bannerScroll) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
});

