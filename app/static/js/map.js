// ==========================
// 1. GEOCODING FUNCTION
// Converting string to longitude and latitude
// ==========================
async function geocodeLocation(location) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.length === 0) return null;

        return {
            lat: parseFloat(data[0].lat),
            lon: parseFloat(data[0].lon)
        };

    } catch (err) {
        console.error("Greška u geokodiranju lokacije:", location, err);
        return null;
    }
}


// ==========================
// 2. INITIALIZATION OF THE MAO
// ==========================
document.addEventListener("DOMContentLoaded", async () => {

    // Create map in the center of Timisoara
    const map = L.map("map").setView([45.7558, 21.2322], 12);

    // OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    console.log("Leaflet mapa pokrenuta.");

    // ==========================
    // LOAD PROJECT FROM API
    // ==========================
    let response;
    try {
        response = await fetch("/api/projects");
    } catch (e) {
        console.error("Ne mogu da dohvatim /api/projects!");
        return;
    }

    const projects = await response.json();

    // ==========================
    // 4. ADDING MARKERS
    // ==========================
    for (let project of projects) {

        if (!project.location || project.location.trim() === "")
            continue;

        // convert text to coordinates
        const coords = await geocodeLocation(project.location);

        if (!coords) {
            console.warn("Nema koordinata za:", project.location);
            continue;
        }

        // create marker
        const marker = L.marker([coords.lat, coords.lon]).addTo(map);

        // popup linking to the project
        marker.bindPopup(`
            <b>${project.title}</b><br>
            <a href="/projects/${project.id}">View project</a>
        `);
    }

});

setTimeout(() => {
    map.invalidateSize();
}, 200);

window.addEventListener("resize", () => {
    map.invalidateSize();
});