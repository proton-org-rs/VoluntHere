document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".tag-filter-btn");
    const projectContainer = document.querySelector(".projects");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            const tag = btn.dataset.tag;

            fetch(`/projects/filter/tag/${tag}`)
                .then(res => res.json())
                .then(data => updateProjects(data));
        });
    });

    function updateProjects(projects) {

        projectContainer.innerHTML = ""; // očisti stare

        if (projects.length === 0) {
            projectContainer.innerHTML = `
                <p class="no-results">No active projects found for this tag.</p>
            `;
            return;
        }

        projects.forEach(p => {
            projectContainer.innerHTML += `
                <div class="project-card">
                    <h2>${p.title}</h2>
                    <p>${p.short_description}</p>
                    <a href="/projects/${p.id}" class="btn-secondary">View Details</a>
                </div>
            `;
        });
    }
});
