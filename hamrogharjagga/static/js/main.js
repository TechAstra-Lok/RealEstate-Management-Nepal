
  
    // Enhanced search functionality
    const searchBtn = document.querySelector(".search-btn");
    if (searchBtn) {
      searchBtn.addEventListener("click", () => {
        const location = document.getElementById("location-search").value;
        const size = document.getElementById("land-size").value;
        const unit = document.getElementById("area-unit").value;
        const minPrice = document.getElementById("min-price").value;
        const maxPrice = document.getElementById("max-price").value;
  
        // Build search params
        const searchParams = new URLSearchParams();
        if (location) searchParams.set('location', location);
        if (size) searchParams.set('size', size);
        if (unit) searchParams.set('unit', unit);
        if (minPrice) searchParams.set('minPrice', minPrice);
        if (maxPrice) searchParams.set('maxPrice', maxPrice);
  
        // Redirect to properties page with search params
        window.location.href = `properties.html?${searchParams.toString()}`;
      });
    }
  
    // Add parallax effect to hero section
    const hero = document.querySelector('.hero-section');
    if (hero) {
      window.addEventListener('scroll', () => {
        const scrolled = window.scrollY; 
        hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
      });
    }
  
    // Handle mobile responsiveness
    if (window.innerWidth <= 768) {
      const mapDiv = document.getElementById("map");
      const listDiv = document.getElementById("property-list");
    }
  
    // Add smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
        });
      });
    });