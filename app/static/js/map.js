// ==========================
// 1. GEOCODING FUNKCIJA
// Pretvara string lokacije u latitude/longitude
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
// 2. INICIJALIZACIJA MAPE
// ==========================
document.addEventListener("DOMContentLoaded", async () => {

    // Kreiraj mapu i centriraj na Beograd
    const map = L.map("map").setView([44.7866, 20.4489], 12);

    // OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    console.log("Leaflet mapa pokrenuta.");

    // ==========================
    // 3. UČITAVANJE PROJEKATA IZ API-ja
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
    // 4. DODAVANJE MARKERA NA MAPU
    // ==========================
    for (let project of projects) {

        if (!project.location || project.location.trim() === "")
            continue;

        // pretvori tekst lokacije u koordinate
        const coords = await geocodeLocation(project.location);

        if (!coords) {
            console.warn("Nema koordinata za:", project.location);
            continue;
        }

        // kreiraj marker
        const marker = L.marker([coords.lat, coords.lon]).addTo(map);

        // popup sa linkom ka projektu
        marker.bindPopup(`
            <b>${project.title}</b><br>
            <a href="/projects/${project.id}">View project</a>
        `);
    }

});
