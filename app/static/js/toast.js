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

async function joinProject(projectId) {
    try {
        const response = await fetch(`/projects/join/${projectId}`, {
            method: "POST"
        });

        const data = await response.json();
        showToast(data.message);

    } catch (err) {
        showToast("Error joining project.");
    }
}
