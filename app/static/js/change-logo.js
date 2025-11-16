document.addEventListener("DOMContentLoaded", () => {

    const logoImg = document.querySelector(".logo img");

    const desktopLogo = logoImg.dataset.desktopLogo;
    const mobileLogo  = logoImg.dataset.mobileLogo;

    function updateLogo() {
        if (window.innerWidth <= 768) {
            logoImg.src = mobileLogo;
        } else {
            logoImg.src = desktopLogo;
        }
    }

    updateLogo();
    window.addEventListener("resize", updateLogo);
});
