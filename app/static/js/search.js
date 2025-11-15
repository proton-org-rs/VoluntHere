let searchTimeout = null;

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const resultsBox = document.getElementById("search-results");

    if (!input) return;

    input.addEventListener("input", () => {
        clearTimeout(searchTimeout);
        const q = input.value.trim();

        if (q.length < 2) {
            resultsBox.style.display = "none";
            return;
        }

        searchTimeout = setTimeout(() => {
            fetch(`/search/ajax?q=${encodeURIComponent(q)}`)
                .then(res => res.json())
                .then(data => showResults(data));
        }, 200);
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", (e) => {
        if (!resultsBox.contains(e.target) && e.target !== input) {
            resultsBox.style.display = "none";
        }
    });

    function showResults(data) {
        let html = "";

        if (data.users.length === 0 && data.projects.length === 0) {
            resultsBox.style.display = "none";
            return;
        }

        // USERS
        if (data.users.length > 0) {
            html += `<div class="category">Users</div>`;
            data.users.forEach(u => {
                html += `
                    <a href="/profile/${u.id}" class="result-item">
                        <strong>${u.username}</strong>
                        <span>${u.name}</span>
                    </a>
                `;
            });
        }

        // PROJECTS
        if (data.projects.length > 0) {
            html += `<div class="category">Projects</div>`;
            data.projects.forEach(p => {
                html += `
                    <a href="/projects/${p.id}" class="result-item">
                        <strong>${p.title}</strong>
                        <span>${p.desc || ""}</span>
                    </a>
                `;
            });
        }

        resultsBox.innerHTML = html;
        resultsBox.style.display = "block";
    }
});
