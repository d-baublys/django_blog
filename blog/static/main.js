document.addEventListener("DOMContentLoaded", () => {
    const yearMonthLis = document.querySelectorAll(".year, .month");
    const yearLis = document.querySelectorAll(".year");
    let mostRecentYear = 0;

    yearLis.forEach((yearLi) => {
        const year = parseInt(yearLi.textContent.trim(), 10);

        if (year > mostRecentYear) {
            mostRecentYear = year;
        }
    });

    yearLis.forEach((yearLi) => {
        const year = parseInt(yearLi.textContent.trim(), 10);

        if (year === mostRecentYear) {
            yearLi.classList.add("reveal");
            const monthsUl = yearLi.querySelector("ul.months");
            
            monthsUl.style.display = "block";
            const monthLis = monthsUl.querySelectorAll('li.month');
            
            monthLis.forEach((monthLi) => {
                monthLi.classList.add("reveal");
                const datesUl = monthLi.querySelector("ul.dates");
                datesUl.style.display = "block";
            })
        }
    });

    yearMonthLis.forEach((yearMonthLi) => {
        yearMonthLi.addEventListener("click", (event) => {
            event.stopPropagation();
            yearMonthLi.classList.toggle("reveal");
            const childUl = yearMonthLi.querySelector("ul");
            
            if (childUl) {
                childUl.style.display = childUl.style.display === "none" ? "block" : "none";
            }
        })
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

    document.addEventListener("click", (event) => {
        if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
            menuButton.classList.remove("active");
            headerMenu.classList.remove("active");
            menuButton.classList.remove("sticky");
        }
    });
});