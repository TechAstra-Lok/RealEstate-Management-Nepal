let map;
let markers = [];

// Using OpenStreetMap with Leaflet (free alternative to Google Maps)
function initMap() {
  map = L.map('map').setView([27.7172, 85.3240], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: ' OpenStreetMap contributors'
  }).addTo(map);

  // Initialize search functionality
  initializeSearch();
}

function initializeSearch() {
  const searchInput = document.getElementById("location-search");
  if (!searchInput) return;

  searchInput.addEventListener('input', debounce(async (e) => {
    const query = e.target.value;
    if (query.length < 3) return;

    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}+Nepal`);
      const data = await response.json();
      showSearchResults(data);
    } catch (error) {
      console.error('Search error:', error);
    }
  }, 500));
}

function showSearchResults(results) {
  clearMarkers();
  const bounds = L.latLngBounds();

  results.forEach(place => {
    const position = [place.lat, place.lon];
    addMarker(position, place.display_name);
    bounds.extend(position);
  });

  if (!bounds.isEmpty()) {
    map.fitBounds(bounds);
  }
}

function addMarker(position, title) {
  const marker = L.marker(position).addTo(map);
  markers.push(marker);

  marker.bindPopup(`
    <div class="info-window">
      <h5>${title}</h5>
      <p>Click to view properties in this area</p>
    </div>
  `);

  marker.on('click', () => {
    marker.openPopup();
  });

  return marker;
}

function clearMarkers() {
  markers.forEach(marker => map.removeLayer(marker));
  markers = [];
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function addPropertyMarkers(properties) {
  clearMarkers();
  const bounds = L.latLngBounds();

  properties.forEach(property => {
    const position = [property.location.lat, property.location.lng];
    const marker = addMarker(position, property.title);
    
    marker.bindPopup(`
      <div class="map-popup">
        <img src="${property.image}" alt="${property.title}" style="width: 100%; max-width: 200px;">
        <h6>${property.title}</h6>
        <p><strong>${formatPrice(property.price)}</strong></p>
        <p>${property.area.value} ${property.area.unit}</p>
        <button class="btn btn-sm btn-primary" onclick="viewProperty('${property.id}')">
          View Details
        </button>
      </div>
    `);

    bounds.extend(position);
  });

  if (!bounds.isEmpty()) {
    map.fitBounds(bounds);
  }
}

function formatPrice(price) {
  if (price >= 10000000) {
    return `₹${(price / 10000000).toFixed(2)} Cr`;
  } else if (price >= 100000) {
    return `₹${(price / 100000).toFixed(2)} Lakhs`;
  }
  return `₹${price.toLocaleString()}`;
}

// Initialize map when the page loads
if (document.getElementById('map')) {
  window.addEventListener("load", initMap);
}