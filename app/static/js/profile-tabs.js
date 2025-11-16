document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".tab-btn");
    const tabs = document.querySelectorAll(".tab-content");

    let activeTab = document.querySelector(".active-tab");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            const target = btn.dataset.tab;
            const newTab = document.querySelector(`#tab-${target}`);

            if (newTab === activeTab) return;

            // Switch active button
            document.querySelector(".tab-btn.active")?.classList.remove("active");
            btn.classList.add("active");

            // Animate old tab
            activeTab.classList.remove("active-tab");
            activeTab.classList.add("slide-out-left");

            activeTab.addEventListener("animationend", () => {
                activeTab.classList.remove("slide-out-left");
            }, { once: true });

            // Animate new tab
            newTab.classList.add("slide-in-right");
            newTab.classList.add("active-tab");

            newTab.addEventListener("animationend", () => {
                newTab.classList.remove("slide-in-right");
            }, { once: true });

            activeTab = newTab;
        });
    });
});
