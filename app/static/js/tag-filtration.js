document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".tag-filter-btn");
    const projectContainer = document.querySelector(".projects");

    let activeFilters = [];
    let originalProjects = [];

    // ============================================================
    // 1. LOAD PROJECTS FROM DOM (SAFE VERSION)
    // ============================================================
    document.querySelectorAll(".project-card").forEach(card => {

        originalProjects.push({
            id: card.dataset.id,
            title: card.querySelector("h2").innerText,
            short_description: card.querySelector("p").innerText,
            tags: card.dataset.tags ? card.dataset.tags.split(",") : [],
            owner_username: card.dataset.ownerUsername || "",
            owner_name: card.dataset.ownerName || ""
        });
    });

    // ============================================================
    // 2. TAG FILTER BUTTON CLICK HANDLER
    // ============================================================
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            const tag = btn.dataset.tag;

            // Toggle ON/OFF
            if (activeFilters.includes(tag)) {
                activeFilters = activeFilters.filter(t => t !== tag);
                btn.classList.remove("active");
            } else {
                activeFilters.push(tag);
                btn.classList.add("active");
            }

            applyFilters();
        });
    });

    // ============================================================
    // 3. APPLY FILTER LOGIC
    // ============================================================
    function applyFilters() {

        // No active filters → show original projects
        if (activeFilters.length === 0) {
            updateProjects(originalProjects);
            return;
        }

        // Fetch results for each filter
        const requests = activeFilters.map(tag =>
            fetch(`/projects/filter/tag/${tag}`).then(res => res.json())
        );

        Promise.all(requests).then(results => {

            // Intersection (AND logic)
            const intersection = intersect(results);

            updateProjects(intersection);
        });
    }

    // ============================================================
    // 4. INTERSECTION OF RESULT LISTS
    // ============================================================
    function intersect(lists) {

        if (lists.length === 1) return lists[0];

        const maps = lists.map(list => {
            const m = new Map();
            list.forEach(p => m.set(p.id, p));
            return m;
        });

        return lists[0].filter(p =>
            maps.every(m => m.has(p.id))
        );
    }

    // ============================================================
    // 5. RENDER PROJECT CARDS (IDENTICAL STRUCTURE)
    // ============================================================
    function updateProjects(projects) {

        projectContainer.innerHTML = "";

        if (projects.length === 0) {
            projectContainer.innerHTML = `
                <p class="no-results">No active projects found for selected tags.</p>
            `;
            return;
        }

        projects.forEach(p => {

            const tagsString = p.tags ? p.tags.join(",") : "";

            projectContainer.innerHTML += `
                <a href="/projects/${p.id}">
                    <div class="project-card"
                        data-id="${p.id}"
                        data-tags="${tagsString}"
                        data-owner-username="${p.owner_username || ""}"
                        data-owner-name="${p.owner_name || ""}">
                        
                        <h2>${p.title}</h2>

                        <h4>
                            Organized by:
                            <a href="/auth/profile/${p.owner_username || "#"}">
                                ${p.owner_name || "Unknown"}
                            </a>
                        </h4>

                        <p>${p.short_description}</p>
                    </div>
                </a>
            `;
        });
    }

});
