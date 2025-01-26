class PropertyManager {
    constructor() {
      this.properties = [];
      this.currentPage = 1;
      this.itemsPerPage = 12;
      this.loading = false;
      this.hasMore = true;
      this.filters = {
        location: '',
        minPrice: null,
        maxPrice: null,
        area: null,
        areaUnit: null,
        propertyTypes: [],
        roadTypes: []
      };
      this.init();
    }
  
    async init() {
      // Get search params from URL if any
      const params = new URLSearchParams(window.location.search);
      this.filters = {
        location: params.get('location') || '',
        minPrice: params.get('minPrice') ? parseInt(params.get('minPrice')) : null,
        maxPrice: params.get('maxPrice') ? parseInt(params.get('maxPrice')) : null,
        area: params.get('size') ? parseFloat(params.get('size')) : null,
        areaUnit: params.get('unit') || 'ropani',
        propertyTypes: params.getAll('type'),
        roadTypes: params.getAll('road')
      };
  
      await this.loadMoreProperties();
      this.setupInfiniteScroll();
      this.setupLoadMoreButton();
      this.setupEventListeners();
      this.setupSortingControls();
      this.applyFilters();
    }
  
    async loadMoreProperties() {
      if (this.loading || !this.hasMore) return;
      
      this.loading = true;
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newProperties = await this.generateDummyProperties(this.itemsPerPage);
      this.properties.push(...this.filterProperties(newProperties));
      
      this.renderProperties();
      this.loading = false;
      
      this.hasMore = this.properties.length < 100; // Total limit
      this.updateLoadMoreButton();
      this.addPropertiesToMap();
    }
  
    filterProperties(properties) {
      return properties.filter(property => {
        let matches = true;
  
        // Location filter
        if (this.filters.location) {
          matches = matches && property.address.toLowerCase().includes(this.filters.location.toLowerCase());
        }
  
        // Price filter
        if (this.filters.minPrice) {
          matches = matches && property.price >= this.filters.minPrice;
        }
        if (this.filters.maxPrice) {
          matches = matches && property.price <= this.filters.maxPrice;
        }
  
        // Area filter
        if (this.filters.area) {
          const propertyAreaInRopani = LandConverter.toRopani(property.area.value, property.area.unit);
          const filterAreaInRopani = LandConverter.toRopani(this.filters.area, this.filters.areaUnit);
          matches = matches && propertyAreaInRopani >= filterAreaInRopani;
        }
  
        // Property type filter
        if (this.filters.propertyTypes.length > 0) {
          matches = matches && this.filters.propertyTypes.includes(property.type);
        }
  
        // Road type filter
        if (this.filters.roadTypes.length > 0) {
          matches = matches && this.filters.roadTypes.includes(property.roadAccess);
        }
  
        return matches;
      });
    }
  
    applyFilters() {
      // Get filter values
      this.filters = {
        location: document.getElementById('location-search')?.value || '',
        minPrice: document.getElementById('min-price')?.value ? parseInt(document.getElementById('min-price').value) : null,
        maxPrice: document.getElementById('max-price')?.value ? parseInt(document.getElementById('max-price').value) : null,
        area: document.getElementById('area-size')?.value ? parseFloat(document.getElementById('area-size').value) : null,
        areaUnit: document.getElementById('area-unit')?.value || 'ropani',
        propertyTypes: Array.from(document.querySelectorAll('input[type="checkbox"][id^="type-"]:checked')).map(cb => cb.value),
        roadTypes: Array.from(document.querySelectorAll('input[type="checkbox"][id^="road-"]:checked')).map(cb => cb.value)
      };
  
      // Update URL with filters
      const searchParams = new URLSearchParams();
      for (const [key, value] of Object.entries(this.filters)) {
        if (value) {
          if (Array.isArray(value)) {
            value.forEach(v => searchParams.append(key, v));
          } else {
            searchParams.set(key, value);
          }
        }
      }
      window.history.replaceState({}, '', `${window.location.pathname}?${searchParams.toString()}`);
  
      // Reset and reload properties
      this.properties = [];
      this.currentPage = 1;
      this.hasMore = true;
      this.loadMoreProperties();
      this.clearMarkers();
    }
  
    setupEventListeners() {
      // Add event listener for the apply filters button
      document.getElementById('apply-filters')?.addEventListener('click', () => this.applyFilters());
  
      // Add event listeners for instant filtering
      document.querySelectorAll('.filter-control').forEach(control => {
        control.addEventListener('change', () => this.applyFilters());
      });
  
      // Location search event listener
      document.getElementById('location-search')?.addEventListener('change', () => this.applyFilters());
  
      // Sort controls
      document.getElementById('sort-select')?.addEventListener('change', (e) => {
        this.currentSort = e.target.value;
        this.renderProperties();
      });
    }
  
    setupSortingControls() {
      const sortSelect = document.getElementById('sort-select');
      if (!sortSelect) return;
  
      const options = [
        { value: 'price-asc', text: 'Price: Low to High' },
        { value: 'price-desc', text: 'Price: High to Low' },
        { value: 'area-asc', text: 'Area: Small to Large' },
        { value: 'area-desc', text: 'Area: Large to Small' },
        { value: 'date-desc', text: 'Newest First' },
        { value: 'date-asc', text: 'Oldest First' }
      ];
  
      sortSelect.innerHTML = options.map(opt => 
        `<option value="${opt.value}">${opt.text}</option>`
      ).join('');
    }
  
    generateDummyProperties(count) {
      const districts = [
        { name: 'Kathmandu', center: [27.7172, 85.3240] },
        { name: 'Lalitpur', center: [27.6588, 85.3247] },
        { name: 'Bhaktapur', center: [27.6710, 85.4298] },
        // Add more districts
      ];
  
      const propertyTypes = ['residential', 'commercial', 'agricultural'];
      const roadTypes = ['pitched', 'gravel', 'soil'];
      
      return Array.from({ length: count }, (_, i) => {
        const district = districts[Math.floor(Math.random() * districts.length)];
        const lat = district.center[0] + (Math.random() - 0.5) * 0.1;
        const lng = district.center[1] + (Math.random() - 0.5) * 0.1;
        
        return {
          id: i + 1,
          title: `${propertyTypes[Math.floor(Math.random() * propertyTypes.length)]} Land in ${district.name}`,
          price: Math.floor(Math.random() * 500 + 50) * 100000, // 5L to 5Cr
          location: { lat, lng },
          address: `${district.name}, Nepal`,
          type: propertyTypes[Math.floor(Math.random() * propertyTypes.length)],
          area: {
            value: Math.floor(Math.random() * 20 + 1),
            unit: 'ropani'
          },
          roadAccess: roadTypes[Math.floor(Math.random() * roadTypes.length)],
          image: `https://source.unsplash.com/800x600/?land,property&sig=${i}`,
          features: this.generateRandomFeatures(),
          description: this.generatePropertyDescription(),
          verified: Math.random() > 0.3,
          createdAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000)
        };
      });
    }
  
    generateRandomFeatures() {
      const allFeatures = [
        'South Facing', 'Corner Plot', 'Plain Land', 'Near Highway',
        'River View', 'Mountain View', 'Near School', 'Near Hospital',
        'Public Transportation', 'Electricity', 'Water Supply'
      ];
      
      return allFeatures
        .sort(() => Math.random() - 0.5)
        .slice(0, Math.floor(Math.random() * 5 + 3));
    }
  
    generatePropertyDescription() {
      const descriptions = [
        'Prime location with excellent connectivity.',
        'Perfect for residential development.',
        'Ideal for commercial construction.',
        'Fertile agricultural land with irrigation facility.',
        'Strategic location with high appreciation potential.'
      ];
      return descriptions[Math.floor(Math.random() * descriptions.length)];
    }
  
    setupInfiniteScroll() {
      window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
          this.loadMore();
        }
      });
    }
  
    setupLoadMoreButton() {
      const container = document.querySelector('.load-more-container');
      if (!container) return;
  
      container.innerHTML = `
        <button class="load-more-btn">
          <i class="fas fa-spinner fa-spin" style="display: none;"></i>
          Load More Properties
        </button>
      `;
  
      container.querySelector('button').addEventListener('click', () => this.loadMore());
    }
  
    async loadMore() {
      if (this.loading || !this.hasMore) return;
      this.currentPage++;
      await this.loadMoreProperties();
    }
  
    updateLoadMoreButton() {
      const btn = document.querySelector('.load-more-btn');
      if (!btn) return;
  
      const spinner = btn.querySelector('.fa-spinner');
      
      if (this.loading) {
        btn.disabled = true;
        spinner.style.display = 'inline-block';
      } else {
        btn.disabled = false;
        spinner.style.display = 'none';
      }
  
      btn.textContent = this.hasMore ? 'Load More Properties' : 'No More Properties';
    }
  
    formatPrice(price) {
      if (price >= 10000000) {
        return `₹${(price / 10000000).toFixed(2)} Cr`;
      } else if (price >= 100000) {
        return `₹${(price / 100000).toFixed(2)} Lakhs`;
      }
      return `₹${price.toLocaleString()}`;
    }
  
    createPropertyCard(property) {
      return `
        <div class="property-card animate-up">
          <div class="property-image">
            <img src="${property.image}" alt="${property.title}" loading="lazy">
            ${property.verified ? '<div class="verified-badge"><i class="fas fa-check-circle"></i> Verified</div>' : ''}
            <div class="property-type">${property.type}</div>
          </div>
          <div class="card-body">
            <h5 class="property-title">${property.title}</h5>
            <div class="price">
              <i class="fas fa-tag"></i> ${this.formatPrice(property.price)}
            </div>
            <div class="property-details">
              <span><i class="fas fa-ruler-combined"></i> ${property.area.value} ${property.area.unit}</span>
              <span><i class="fas fa-road"></i> ${property.roadAccess}</span>
            </div>
            <div class="location">
              <i class="fas fa-map-marker-alt"></i> ${property.address}
            </div>
            <div class="property-features">
              ${property.features.map(feature => `
                <span class="feature-tag"><i class="fas fa-check"></i> ${feature}</span>
              `).join('')}
            </div>
            <div class="action-buttons">
              <button class="btn btn-primary" onclick="viewProperty(${property.id})">
                <i class="fas fa-info-circle"></i> View Details
              </button>
              <button class="btn btn-outline-primary add-to-wishlist" data-id="${property.id}">
                <i class="fas fa-heart"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }
  
    renderProperties() {
      const container = document.getElementById("property-list");
      if (!container) return;
  
      const sortedProperties = this.sortProperties(this.properties);
  
      container.innerHTML = sortedProperties.map(property => 
        this.createPropertyCard(property)
      ).join("");
    }
  
    sortProperties(properties) {
      const currentSort = 'price-asc';
      const [field, order] = currentSort.split('-');
      return [...properties].sort((a, b) => {
        let comparison = 0;
        switch (field) {
          case 'price':
            comparison = a.price - b.price;
            break;
          case 'area':
            comparison = a.area.value - b.area.value;
            break;
          case 'date':
            comparison = new Date(a.createdAt) - new Date(b.createdAt);
            break;
        }
        return order === 'asc' ? comparison : -comparison;
      });
    }
  
    addPropertiesToMap() {
      if (!window.map) return;
      this.properties.forEach(property => {
        const position = [property.location.lat, property.location.lng];
        const marker = addMarker(position, property.title);
        
        marker.bindPopup(`
          <div class="map-popup">
            <img src="${property.image}" alt="${property.title}">
            <h5>${property.title}</h5>
            <p>${this.formatPrice(property.price)}</p>
            <p>${property.area.value} ${property.area.unit}</p>
            <button class="btn btn-sm btn-primary" onclick="viewProperty(${property.id})">
              View Details
            </button>
          </div>
        `);
      });
    }
  
    clearMarkers() {
      if (!window.map) return;
      // window.map.eachLayer((layer) => {
      //   if (layer instanceof L.Marker) {
      //     window.map.removeLayer(layer);
      //   }
      // });
    }
  }
  
  function viewProperty(id) {
    window.location.href = `property-detail.html?id=${id}`;
  }
  
  // Initialize when the page loads
  const propertyManager = new PropertyManager();