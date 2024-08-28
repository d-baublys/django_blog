document.addEventListener("DOMContentLoaded", function () {
    const yearMonthElements = document.querySelectorAll(".year, .month");
    const datesElements = document.querySelectorAll(".dates");

    yearMonthElements.forEach(function (element) {
        element.style.display = "block";
        element.addEventListener("click", function (event) {
            event.stopPropagation();
            element.classList.toggle("reveal");
            const childUl = element.querySelector("ul");
            
            if (childUl) {
                childUl.style.display = childUl.style.display === "none" ? "block" : "none";
            }
        })
    });

    datesElements.forEach(function (element) {
        element.style.display = "none";
    })
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

document.addEventListener("click", function (event) {
    if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
        menuButton.classList.remove("active");
        headerMenu.classList.remove("active");
    }
});