document.addEventListener("DOMContentLoaded", () => {
    const postTrees = document.querySelectorAll(".post-tree");
    const yearMonthLis = document.querySelectorAll(".year, .month");
    const menuButton = document.querySelector(".menu-button");
    const headerMenu = document.querySelector(".header-menu");
    const banner = document.querySelector(".banner");
    const bannerScroll = banner.clientHeight - (menuButton.clientHeight * 1.33);

    function revealMostRecentMonth(postTree) {
        const yearLis = postTree.querySelectorAll(".year");
        let mostRecentYearLi = null;
        let mostRecentMonthLi = null;

        yearLis.forEach(yearLi => {
            const year = parseInt(yearLi.textContent.trim(), 10);
            if (!mostRecentYearLi || year > parseInt(mostRecentYearLi.textContent.trim(), 10)) {
                mostRecentYearLi = yearLi;
            }
        });
    
        if (mostRecentYearLi) {
            const monthLis = mostRecentYearLi.querySelectorAll("li.month");
            monthLis.forEach(monthLi => {
                const month = parseInt(monthLi.dataset.month, 10);
                if (!mostRecentMonthLi || month > parseInt(mostRecentMonthLi.textContent.trim(), 10)) {
                    mostRecentMonthLi = monthLi;
                }
            });
    
            if (mostRecentMonthLi) {
                mostRecentYearLi.classList.add("reveal");
                const monthsUl = mostRecentYearLi.querySelector("ul.months");
                monthsUl.style.display = "block";
            
                mostRecentMonthLi.classList.add("reveal");
                const datesUl = mostRecentMonthLi.querySelector("ul.dates");
                datesUl.style.display = "block";
            }
        }
    }

    function toggleNode(event) {
        event.stopPropagation();
        const li = event.currentTarget;
        li.classList.toggle("reveal");
        const childUl = li.querySelector("ul");
        if (childUl) {
            childUl.style.display = childUl.style.display === "none" ? "block" : "none";
        }
    }

    function stickyMenuButton() {
        if (window.scrollY > bannerScroll) {
            menuButton.classList.add("sticky");
        } else if (!menuButton.classList.contains("active")) {
            menuButton.classList.remove("sticky");
        }
    }

    function toggleMenuButton() {
        menuButton.classList.toggle("active");
        headerMenu.classList.toggle("active");
        menuButton.classList.toggle("sticky");
    }

    function menuOffClick(event) {
        if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
            menuButton.classList.remove("active");
            headerMenu.classList.remove("active");
            menuButton.classList.remove("sticky");
        }
    }

    postTrees.forEach(revealMostRecentMonth);

    yearMonthLis.forEach(li => li.addEventListener("click", toggleNode))

    menuButton.addEventListener("click", toggleMenuButton);
    window.addEventListener("scroll", stickyMenuButton);
    document.addEventListener("click", menuOffClick);
});