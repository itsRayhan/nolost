/**
 * Nolost maps - Frontend Visualization & API Controller
 * Supports Google Maps JavaScript API natively, with automatic Leaflet fallback
 * when no Google Maps API key is configured yet.
 */

let mapMode = null; // "google" or "leaflet"
let gMap = null;
let gRoutePolyline = null;

let lMap = null;
let lRoutePolyline = null;

const DHAKA_CENTER = { lat: 23.7465, lng: 90.4110 };

/**
 * Initialize Google Maps JavaScript API (called via Google Maps script callback)
 */
function initGoogleMap() {
    mapMode = "google";
    const { nodes, edges, defaultResult } = window.NOLOst_DATA;

    gMap = new google.maps.Map(document.getElementById("map"), {
        center: DHAKA_CENTER,
        zoom: 14,
        mapTypeControl: true,
        streetViewControl: false,
        fullscreenControl: true,
    });

    // Draw all static graph edges in muted gray
    edges.forEach((edge) => {
        new google.maps.Polyline({
            path: [edge.from_coords, edge.to_coords],
            geodesic: true,
            strokeColor: "#8c96a5",
            strokeOpacity: 0.75,
            strokeWeight: 3,
            map: gMap,
        });
    });

    // Place red teardrop markers with letter labels (A, B, C, ...)
    const infoWindow = new google.maps.InfoWindow();
    nodes.forEach((node) => {
        const marker = new google.maps.Marker({
            position: { lat: node.lat, lng: node.lng },
            map: gMap,
            title: `${node.label} - ${node.landmark}`,
            label: {
                text: node.id,
                color: "#111827",
                fontWeight: "bold",
                fontSize: "13px",
            },
        });

        marker.addListener("click", () => {
            infoWindow.setContent(
                `<div style="font-family: Inter, sans-serif; padding: 2px 4px;">
                    <strong>${node.label}</strong>: ${node.landmark}<br/>
                    <small style="color:#4b5563;">(${node.lat.toFixed(4)}, ${node.lng.toFixed(4)})</small>
                </div>`
            );
            infoWindow.open(gMap, marker);
        });
    });

    // Render initial default path
    renderResults(defaultResult);
}

/**
 * Initialize Fallback Leaflet Map (used only if GOOGLE_MAPS_API_KEY is not set yet)
 */
function initFallbackLeafletMap() {
    mapMode = "leaflet";
    const { nodes, edges, defaultResult } = window.NOLOst_DATA;

    lMap = L.map("map").setView([DHAKA_CENTER.lat, DHAKA_CENTER.lng], 14);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(lMap);

    edges.forEach((edge) => {
        L.polyline(
            [
                [edge.from_coords.lat, edge.from_coords.lng],
                [edge.to_coords.lat, edge.to_coords.lng],
            ],
            {
                color: "#8c96a5",
                weight: 3,
                opacity: 0.75,
            }
        ).addTo(lMap);
    });

    nodes.forEach((node) => {
        const icon = L.divIcon({
            className: "custom-pin-icon",
            html: `<div class="pin-badge"><span>${node.id}</span></div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 28],
        });

        L.marker([node.lat, node.lng], { icon })
            .addTo(lMap)
            .bindPopup(`<strong>${node.label}</strong>: ${node.landmark}`);
    });

    renderResults(defaultResult);
}

/**
 * Draw the calculated route polyline on the active map
 */
function drawCalculatedRoute(coordinates) {
    if (mapMode === "google" && gMap) {
        if (gRoutePolyline) {
            gRoutePolyline.setMap(null);
        }
        const pathCoords = coordinates.map((c) => ({ lat: c.lat, lng: c.lng }));
        gRoutePolyline = new google.maps.Polyline({
            path: pathCoords,
            geodesic: true,
            strokeColor: "#2563eb",
            strokeOpacity: 0.95,
            strokeWeight: 5.5,
            zIndex: 10,
            map: gMap,
        });
    } else if (mapMode === "leaflet" && lMap) {
        if (lRoutePolyline) {
            lMap.removeLayer(lRoutePolyline);
        }
        const latLngs = coordinates.map((c) => [c.lat, c.lng]);
        lRoutePolyline = L.polyline(latLngs, {
            color: "#2563eb",
            weight: 5.5,
            opacity: 0.95,
        }).addTo(lMap);
    }
}

/**
 * Update Pathfinding Results cards, route pills, and comparison table
 */
function renderResults(data) {
    const selected = data.selected;
    const comparison = data.comparison || [];

    // Update metric cards
    document.getElementById("res-algorithm").textContent = selected.algorithm;
    document.getElementById("res-distance").textContent = `${selected.distance_km} km`;
    document.getElementById("res-explored").textContent = `${selected.nodes_explored} nodes`;
    document.getElementById("res-time").textContent = `${selected.execution_time_ms} ms`;

    // Update route pills
    const seqContainer = document.getElementById("res-path-sequence");
    seqContainer.innerHTML = "";
    if (selected.coordinates && selected.coordinates.length > 0) {
        selected.coordinates.forEach((node, idx) => {
            const pill = document.createElement("span");
            pill.className = "route-node-pill";
            pill.textContent = `${node.label} (${node.landmark})`;
            seqContainer.appendChild(pill);

            if (idx < selected.coordinates.length - 1) {
                const arrow = document.createElement("span");
                arrow.className = "route-arrow";
                arrow.textContent = "→";
                seqContainer.appendChild(arrow);
            }
        });
    } else {
        seqContainer.textContent = "No path found between selected nodes.";
    }

    // Update comparison table
    const tbody = document.getElementById("comparison-tbody");
    tbody.innerHTML = "";
    comparison.forEach((row) => {
        const tr = document.createElement("tr");
        if (row.algorithm === selected.algorithm) {
            tr.className = "active-row";
        }
        tr.innerHTML = `
            <td>${row.algorithm}</td>
            <td>${row.path.join(" → ")}</td>
            <td>${row.hops}</td>
            <td>${row.distance_km} km</td>
            <td>${row.nodes_explored}</td>
            <td>${row.execution_time_ms} ms</td>
        `;
        tbody.appendChild(tr);
    });

    // Draw polyline on map
    drawCalculatedRoute(selected.coordinates || []);
}

/**
 * Handle "Find Path" form submission via Fetch API
 */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("pathfinder-form");
    const btn = document.getElementById("find-path-btn");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const source = document.getElementById("source-select").value;
        const destination = document.getElementById("destination-select").value;
        const algorithm = document.getElementById("algorithm-select").value;

        btn.disabled = true;
        btn.textContent = "Finding...";

        try {
            const params = new URLSearchParams({ source, destination, algorithm });
            const response = await fetch(`${window.NOLOst_DATA.apiUrl}?${params.toString()}`);
            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Failed to calculate path.");
                return;
            }

            renderResults(data);
        } catch (err) {
            console.error(err);
            alert("Network error while calculating route.");
        } finally {
            btn.disabled = false;
            btn.textContent = "Find Path";
        }
    });
});
