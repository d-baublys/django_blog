document.addEventListener("DOMContentLoaded", function () {
    const yearMonthElements = document.querySelectorAll(".year, .month");
    const yearElements = document.querySelectorAll(".year");
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth();

    yearElements.forEach(function(yearElement) {
        const year = parseInt(yearElement.textContent.trim(), 10);

        if (year === currentYear) {
            yearElement.classList.add("reveal");
            const monthsUl = yearElement.querySelector("ul.months");
            
            monthsUl.style.display = "block";
            const monthLis = monthsUl.querySelectorAll('li.month');
            
            monthLis.forEach(function(monthLi) {
                monthLi.classList.add("reveal");
                const datesUl = monthLi.querySelector("ul.dates");
                datesUl.style.display = "block";
            })
        }
    });

    yearMonthElements.forEach(function (element) {
        element.addEventListener("click", function (event) {
            event.stopPropagation();
            element.classList.toggle("reveal");
            const childUl = element.querySelector("ul");
            
            if (childUl) {
                childUl.style.display = childUl.style.display === "none" ? "block" : "none";
            }
        })
    });
});

const menuButton = document.querySelector(".menu-button");
const headerMenu = document.querySelector(".header-menu");
const banner = document.querySelector(".banner");
const bannerScroll = banner.clientHeight - (menuButton.clientHeight * 1.33);

window.addEventListener("scroll", () => {
    if (window.scrollY > bannerScroll) {
        menuButton.classList.add("sticky");
    } else if (!menuButton.classList.contains("active")) {
        menuButton.classList.remove("sticky");
    }
});

menuButton.addEventListener("click", () => {
    menuButton.classList.toggle("active");
    headerMenu.classList.toggle("active");
    menuButton.classList.toggle("sticky");
});

document.addEventListener("click", function (event) {
    if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
        menuButton.classList.remove("active");
        headerMenu.classList.remove("active");
        menuButton.classList.remove("sticky");
    }
});