// ==========================
// 1. GEOCODING FUNCTION
// Converting string to latitude and longitude
// ==========================
async function geocodeLocation(location) {
    if (!location || location.trim() === "") return null;

    // 1. CHECK LOCAL CACHE
    const cached = localStorage.getItem("geo_" + location);
    if (cached) {
        return JSON.parse(cached);
    }

    // 2. OTHERWISE DO REAL GEOCODING
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&limit=1`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!data || data.length === 0) return null;

        const result = {
            lat: parseFloat(data[0].lat),
            lon: parseFloat(data[0].lon),
        };

        // 3. SAVE TO CACHE
        localStorage.setItem("geo_" + location, JSON.stringify(result));

        return result;

    } catch (err) {
        console.error("Geocoding error:", location, err);
        return null;
    }
}


// ==========================
// 2. INITIALIZATION OF THE MAP
// ==========================
document.addEventListener("DOMContentLoaded", async () => {

    // Create map (centered on Timisoara)
    const map = L.map("map").setView([45.7558, 21.2322], 12);

    // Tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    console.log("Leaflet mapa pokrenuta.");

    // ==========================
    // 3. LOAD APPROVED PROJECTS
    // ==========================
    let response;

    try {
        response = await fetch("/api/projects");
    } catch (e) {
        console.error("Ne mogu da dohvatim /api/projects");
        return;
    }

    const projects = await response.json();


    // ==========================
    // 4. PARALLEL GEOCODING (FASTER)
    // ==========================
    const geocodePromises = projects.map(p =>
        geocodeLocation(p.location)
    );

    // All lookups run in parallel
    const coordsArray = await Promise.all(geocodePromises);


    // ==========================
    // 5. ADD MARKERS TO MAP
    // ==========================
    projects.forEach((project, i) => {
        const coords = coordsArray[i];

        if (!coords) return;

        const marker = L.marker([coords.lat, coords.lon]).addTo(map);

        marker.bindPopup(`
            <b>${project.title}</b><br>
            <a href="/projects/${project.id}">View project</a>
        `);
    });


    // FIX MAP IF HIDDEN IN FLEX GRID
    setTimeout(() => {
        map.invalidateSize();
    }, 150);

});


// ==========================
// 6. UPDATE MAP ON WINDOW RESIZE
// ==========================
window.addEventListener("resize", () => {
    if (window.map) {
        window.map.invalidateSize();
    }
});
