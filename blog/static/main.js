
// $(document).ready(function () {
//     $('.year, .month').click(function (event) {
//         event.stopPropagation();
//         $(this).toggleClass('reveal');
//         $(this).children('ul').toggle();
//     });

//     $('.date').click(function (event) {
//         event.stopPropagation();
//     });
// });


document.addEventListener("DOMContentLoaded", function () {
    const yearMonthElements = document.querySelectorAll(".year, .month");

    yearMonthElements.forEach(function (element) {
        element.addEventListener("click", function (event) {
            event.stopPropagation();
            element.classList.toggle("reveal");

            const datesUl = element.querySelector(".dates");
            if (datesUl) {
                datesUl.style.display = datesUl.style.display === "none" ? "block" : "none";
            }
        })
    });

    const dateElements = document.querySelectorAll(".date");

    dateElements.forEach(function (element) {
        element.addEventListener("click", function (event) {
            event.stopPropagation();
        })
    })
});

const menuButton = document.querySelector(".menu-button");
const headerMenu = document.querySelector(".header-menu");

window.addEventListener("scroll", () => {
    const banner = document.querySelector(".banner");
    const bannerScroll = banner.clientHeight - (menuButton.clientHeight * 1.33);

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

document.addEventListener("click", function (event) {
    if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
        menuButton.classList.remove("active");
        headerMenu.classList.remove("active");
    }
});