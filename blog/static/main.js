
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
const banner = document.querySelector(".banner");
const bannerScroll = banner.clientHeight - (menuButton.clientHeight * 1.33);

window.addEventListener("scroll", () => {
    if (window.scrollY > bannerScroll) {
        menuButton.classList.add("sticky");
    } else {
        menuButton.classList.remove("sticky");
    }
});

const headerMenu = document.querySelector(".header-menu");

menuButton.addEventListener("click", () => {
    headerMenu.classList.toggle("active");
    menuButton.classList.toggle("active");
})