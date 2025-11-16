document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("tagInput");
    const dropdown = document.getElementById("tagDropdown");
    const chips = document.getElementById("selectedTags");
    const hidden = document.getElementById("tagsHidden");

    let selected = [];

    input.addEventListener("input", async () => {
        const query = input.value.trim();
        if (query.length === 0) {
            dropdown.classList.add("hidden");
            return;
        }

        const response = await fetch(`/projects/api/tags/search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            console.error("Tag search failed:", response.status);
            dropdown.classList.add("hidden");
            return;
        }

        let data;
        try {
            data = await response.json();
        } catch (err) {
            console.error("Invalid JSON:", err);
            dropdown.classList.add("hidden");
            return;
        }

        dropdown.innerHTML = "";
        dropdown.classList.remove("hidden");

        data.forEach(tag => {
            const div = document.createElement("div");
            div.textContent = tag.name;
            div.classList.add("dropdown-item");
            div.addEventListener("click", () => {
                if (!selected.includes(tag.name)) {
                    selected.push(tag.name);
                    updateChips();
                }
                dropdown.classList.add("hidden");
                input.value = "";
            });
            dropdown.appendChild(div);
        });
    });

    function updateChips() {
        chips.innerHTML = "";
        selected.forEach(name => {
            const chip = document.createElement("div");
            chip.classList.add("chip");
            chip.innerHTML = `${name} <span data-name="${name}">✕</span>`;
            chips.appendChild(chip);
        });

        hidden.value = JSON.stringify(selected);
    }

    chips.addEventListener("click", (e) => {
        if (e.target.tagName === "SPAN") {
            const name = e.target.getAttribute("data-name");
            selected = selected.filter(t => t !== name);
            updateChips();
        }
    });

    const form = document.getElementById("projectForm");
    form.addEventListener("submit", () => {
        setTimeout(() => showToast("Your project has been successfully submitted and is now awaiting administrator review."), 300);
    });
});

function showToast(message) {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.textContent = message;

    container.appendChild(toast);

    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.add("hide");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    const msgDiv = document.getElementById("toast-message");

    if (msgDiv) {
        const code = msgDiv.dataset.msg;

        let message = "";
        if (code === "created") {
            message = "Your project has been successfully submitted and is now awaiting administrator review.";
        }

        if (message) {
            showToast(message);
        }
    }
});