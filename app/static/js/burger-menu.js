document.addEventListener("DOMContentLoaded", () => {
    const burgerBtn = document.getElementById("burger-btn");
    const burgerMenu = document.getElementById("burger-menu");

    if (burgerBtn && burgerMenu) {
        burgerBtn.addEventListener("click", () => {
            burgerBtn.classList.toggle("open");
            burgerMenu.classList.toggle("open");
        });

        // opciono: zatvaranje menija klikom van njega
        document.addEventListener("click", (e) => {
            if (!burgerMenu.contains(e.target) && !burgerBtn.contains(e.target)) {
                burgerBtn.classList.remove("open");
                burgerMenu.classList.remove("open");
            }
        });
    }
});
