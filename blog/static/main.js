document.addEventListener("DOMContentLoaded", () => {
    const yearMonthLis = document.querySelectorAll(".year, .month");
    const yearLis = document.querySelectorAll(".year");
    let mostRecentYear = 0;
    let mostRecentYearLi = null;
    let mostRecentMonth = 0;
    let mostRecentMonthLi = null;
    
    yearLis.forEach((yearLi) => {
        const year = parseInt(yearLi.textContent.trim(), 10);

        if (year > mostRecentYear) {
            mostRecentYear = year;
            mostRecentYearLi = yearLi;
        }
    });

    if (mostRecentYearLi) {
        const monthLis = mostRecentYearLi.querySelectorAll("li.month");

        monthLis.forEach((monthLi) => {
            const month = parseInt(monthLi.dataset.month, 10);

            if (month > mostRecentMonth) {
                mostRecentMonth = month;
                mostRecentMonthLi = monthLi;
            }
        })
    };

    if (mostRecentMonthLi) {
        mostRecentYearLi.classList.add("reveal");
        const monthsUl = mostRecentYearLi.querySelector("ul.months");
        
        monthsUl.style.display = "block";
    
        mostRecentMonthLi.classList.add("reveal");
        const datesUl = mostRecentMonthLi.querySelector("ul.dates");
        datesUl.style.display = "block";
    };

    yearLis.forEach((yearLi) => {
        const year = parseInt(yearLi.textContent.trim(), 10);

        if (year === mostRecentYear) {
            yearLi.classList.add("reveal");
            const monthsUl = yearLi.querySelector("ul.months");
            
            monthsUl.style.display = "block";
            const monthLis = monthsUl.querySelectorAll('li.month');
            
            monthLis.forEach((monthLi) => {
                const month = parseInt(monthLi.dataset.month, 10);
                if (month === mostRecentMonth) {
                    monthLi.classList.add("reveal");
                    const datesUl = monthLi.querySelector("ul.dates");
                    datesUl.style.display = "block";
                }
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