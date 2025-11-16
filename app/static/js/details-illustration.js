document.addEventListener("DOMContentLoaded", () => {

    const box = document.querySelector(".details-illustration");
    if (!box) return;

    const illustrations = [
        "/static/images/ecology_image.png",
        "/static/images/Education_Image.png",
        "/static/images/Elderly_Image.png"
    ];

    const randomIllustration = illustrations[Math.floor(Math.random() * illustrations.length)];

    box.style.backgroundImage = `url("${randomIllustration}")`;
});
