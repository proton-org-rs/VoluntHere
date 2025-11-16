document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".tag-filter-btn");
    const projectContainer = document.querySelector(".projects");

    let activeFilters = [];
    let originalProjects = []; // ovde čuvamo sve projekte

    // FIRST LOAD – sačuvaj sve projekte iz DOM-a
    // -------------------------------------------
    document.querySelectorAll(".project-card").forEach(card => {
        originalProjects.push({
            id: card.querySelector("a").getAttribute("href").split("/").pop(),
            title: card.querySelector("h2").innerText,
            short_description: card.querySelector("p").innerText
        });
    });

    // --------------------------------------
    // CLICK HANDLER ZA FILTER DUGMICE
    // --------------------------------------
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            const tag = btn.dataset.tag;

            // TOGGLE
            if (activeFilters.includes(tag)) {
                activeFilters = activeFilters.filter(t => t !== tag);
                btn.classList.remove("active");
            } else {
                activeFilters.push(tag);
                btn.classList.add("active");
            }

            applyFilters(); // uvek osveži nakon svakog klika
        });
    });


    // --------------------------------------
    // GLAVNA LOGIKA FILTRIRANJA
    // --------------------------------------
    function applyFilters() {

        // -----------------------------------
        // 0 FILTERA → prikaz svih projekata
        // -----------------------------------
        if (activeFilters.length === 0) {
            updateProjects(originalProjects);
            return;
        }

        // -----------------------------------
        // Inače → fetch za svaki tag
        // -----------------------------------
        const requests = activeFilters.map(tag =>
            fetch(`/projects/filter/tag/${tag}`).then(res => res.json())
        );

        Promise.all(requests).then(results => {

            // INTERSECTION svih setova projekata
            const intersection = intersect(results);

            updateProjects(intersection);
        });
    }


    // --------------------------------------
    // FUNKCIJA ZA PRESEK REZULTATA
    // projekat mora biti u SVIM listama
    // --------------------------------------
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


    // --------------------------------------
    // TVOJA ORIGINALNA FUNKCIJA — NE DIRAM
    // --------------------------------------
    function updateProjects(projects) {

        projectContainer.innerHTML = ""; // očisti stare

        if (projects.length === 0) {
            projectContainer.innerHTML = `
                <p class="no-results">No active projects found for selected tags.</p>
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
