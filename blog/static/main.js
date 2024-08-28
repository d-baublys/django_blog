
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

const menuButton = document.querySelector(".menu-button");
const headerMenu = document.querySelector(".header-menu");
const banner = document.querySelector(".banner");
const bannerScroll = banner.clientHeight - (menuButton.clientHeight * 1.33);

window.addEventListener("scroll", () => {
    if (window.scrollY > bannerScroll) {
        menuButton.classList.add("sticky");
    } else {
        menuButton.classList.remove("sticky");
    }
});

menuButton.addEventListener("click", () => {
    menuButton.classList.toggle("active");
    headerMenu.classList.toggle("active");
});

document.addEventListener("click", function(event) {
    if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
        menuButton.classList.remove("active");
        headerMenu.classList.remove("active");
    }
});