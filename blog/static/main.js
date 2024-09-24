document.addEventListener("DOMContentLoaded", () => {
    const postTrees = document.querySelectorAll(".post-tree");
    const yearMonthLis = document.querySelectorAll(".year, .month");
    const menuButton = document.querySelector(".menu-button");
    const headerMenu = document.querySelector(".header-menu");
    const overlapElements = document.querySelectorAll(".menu-button, .menu-button span");

    function findMostRecentLi(lis, getValue) {
        return Array.from(lis).reduce((mostRecentLi, currentLi) => {
            const currentValue = getValue(currentLi);
            return !mostRecentLi || currentValue > getValue(mostRecentLi)
                ? currentLi
                : mostRecentLi;
        }, null);
    }

    function getYear(li) {
        return parseInt(li.dataset.year, 10);
    }

    function getMonth(li) {
        return parseInt(li.dataset.month, 10);
    }

    function revealElement(li, className) {
        li.classList.add(className);
        const childUl = li.querySelector("ul");
        if (childUl) {
            childUl.style.display = "block";
            childUl.style.opacity = "1";
        }
    }

    function revealMostRecentMonth(postTree) {
        const yearLis = postTree.querySelectorAll(".year");
        const mostRecentYearLi = findMostRecentLi(yearLis, getYear);

        if (mostRecentYearLi) {
            const monthLis = mostRecentYearLi.querySelectorAll(".month");
            const mostRecentMonthLi = findMostRecentLi(monthLis, getMonth);

            if (mostRecentMonthLi) {
                revealElement(mostRecentYearLi, "reveal");
                revealElement(mostRecentMonthLi, "reveal");
            }
        }
    }

    function checkOverlap(element) {
        const overlapPercent = getOverlapMetrics(element);
        const isButton = element.tagName === "BUTTON";
        const gradientStyle = getGradientStyle(overlapPercent);
        applyGradientStyle(element, isButton, gradientStyle);
    }

    function getOverlapMetrics(element) {
        const headerBottom = document.querySelector(".page-header").getBoundingClientRect().bottom;
        const elementBottom = element.getBoundingClientRect().bottom;
        const elementHeight = element.getBoundingClientRect().height;

        const overlapPixels = elementBottom - headerBottom;
        const overlapPercent = Math.round((overlapPixels / elementHeight) * 100);

        return overlapPercent;
    }

    function getGradientStyle(overlapPercent) {
        if (overlapPercent <= 0) {
            return "linear-gradient(white 100%, black 0%)";
        } else if (overlapPercent >= 100) {
            return "linear-gradient(white 0%, black 0%)";
        } else {
            return `linear-gradient(white ${100 - overlapPercent}%, black 0%)`;
        }
    }

    function applyGradientStyle(element, isButton, gradientStyle) {
        if (isButton) {
            element.style.borderImageSource = gradientStyle;
        } else {
            element.style.background = gradientStyle;
        }
    }

    function buttonOverlapColours() {
        overlapElements.forEach((element) => checkOverlap(element));
    }

    function toggleNode(event) {
        event.stopPropagation();
        const li = event.currentTarget;
        li.classList.toggle("reveal");
        const childUl = li.querySelector("ul");
        if (childUl) {
            childUl.style.display =
                childUl.style.display === "none"
                    ? "block"
                    : setTimeout(() => (childUl.style.display = "none"), 100);
            setTimeout(
                () => (childUl.style.opacity = childUl.style.opacity === "0" ? "1" : "0"),
                0
            );
        }
    }

    function toggleMenuButton() {
        menuButton.classList.toggle("active");
        headerMenu.classList.toggle("active");
    }

    function menuOffClick(event) {
        if (!menuButton.contains(event.target) && !headerMenu.contains(event.target)) {
            menuButton.classList.remove("active");
            headerMenu.classList.remove("active");
        }
    }

    postTrees.forEach(revealMostRecentMonth);

    yearMonthLis.forEach((li) => li.addEventListener("click", toggleNode));

    menuButton.addEventListener("click", toggleMenuButton);
    window.addEventListener("scroll", buttonOverlapColours);
    document.addEventListener("click", menuOffClick);
});
