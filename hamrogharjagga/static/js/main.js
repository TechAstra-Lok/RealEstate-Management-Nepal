class LandConverter {
    static toRopani(value, fromUnit) {
      const conversions = {
        ropani: 1,
        dhur: 1 / 30,
        kattha: 1 / 20,
        bigha: 13.31
      };
      return value * conversions[fromUnit];
    }
  }
  
  function showLoginPrompt() {
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    loginModal.show();
  }
  
  function updateNavbar() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const navbar = document.querySelector('.navbar-nav');
  
    if (!navbar) return;
  
    if (isLoggedIn) {
      navbar.innerHTML = `
        <a class="nav-link" href="${window.dashboardUrl}">
          <i class="fas fa-tachometer-alt"></i> Dashboard
        </a>

        <a class="nav-link" href="${window.propertiesUrl}">
          <i class="fas fa-search"></i> Find Land
        </a>
        <a class="nav-link" href="sell.html">
          <i class="fas fa-plus-circle"></i> Sell Land
        </a>
        <a class="nav-link" href="wishlist.html">
          <i class="fas fa-heart"></i> Wishlist
        </a>
        <a class="nav-link" href="#" onclick="logout()">
          <i class="fas fa-sign-out-alt"></i> Logout
        </a>
      `;
    } else {
      // Only show login/register on home page
      if (window.location.pathname === '/home/') {
        navbar.innerHTML = `
          <a class="nav-link" href="#" data-bs-toggle="modal" data-bs-target="#loginModal">
            <i class="fas fa-sign-in-alt"></i> Login
          </a>
          <a class="nav-link" href="#" data-bs-toggle="modal" data-bs-target="#registerModal">
            <i class="fas fa-user-plus"></i> Register
          </a>
        `;
      }
    }
  }
  
  function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'home.html'; // Redirect to home.html after logout
  }
  
  function showRegisterModal() {
    const loginModal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
    if (loginModal) loginModal.hide();
  
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
  }
  
  class UserProfile {
    constructor() {
      this.user = this.loadUserData();
      this.init();
    }
  
    init() {
      this.updateUI();
      this.setupEventListeners();
    }
  
    loadUserData() {
      const userData = localStorage.getItem('userData');
      return userData ? JSON.parse(userData) : null;
    }
  
    saveUserData(userData) {
      localStorage.setItem('userData', JSON.stringify(userData));
      this.user = userData;
      this.updateUI();
    }
  
    updateUI() {
      const userAvatars = document.querySelectorAll('.user-avatar img, #profile-picture-preview, #profilePreview');
      const usernames = document.querySelectorAll('.user-name, #welcome-name, #user-name');
      const userEmails = document.querySelectorAll('.user-email, #user-email');
  
      if (this.user) {
        userAvatars.forEach(avatar => {
          avatar.src = this.user.avatar || 'https://via.placeholder.com/150'; // Placeholder image
          avatar.alt = this.user.fullName;
        });
  
        usernames.forEach(elem => {
          elem.textContent = this.user.fullName;
        });
  
        userEmails.forEach(elem => {
          elem.textContent = this.user.email;
        });
  
        const profileForm = document.getElementById('profile-settings-form');
        if (profileForm) {
          profileForm.querySelector('[name="fullName"]').value = this.user.fullName;
          profileForm.querySelector('[name="email"]').value = this.user.email;
          profileForm.querySelector('[name="phone"]').value = this.user.phone || '';
          profileForm.querySelector('[name="address"]').value = this.user.address || '';
        }
      }
    }
  
    setupEventListeners() {
      const profilePictureInput = document.getElementById('profile-picture-input');
      if (profilePictureInput) {
        profilePictureInput.addEventListener('change', async (e) => {
          const file = e.target.files[0];
          if (file) {
            try {
              const imageUrl = await this.uploadImage(file);
              this.saveUserData({
                ...this.user,
                avatar: imageUrl
              });
            } catch (error) {
              console.error('Error uploading image:', error);
            }
          }
        });
      }
  
      const profileForm = document.getElementById('profile-settings-form');
      if (profileForm) {
        profileForm.addEventListener('submit', async (e) => {
          e.preventDefault();
          const formData = new FormData(profileForm);
          await this.updateProfile(formData);
        });
      }
    }
  
    async uploadImage(file) {
      try {
        const url = await this.uploadToServer(file); // Placeholder method for uploading
        return url;
      } catch (error) {
        console.error('Error uploading image:', error);
        throw error;
      }
    }
  
    async updateProfile(formData) {
      try {
        let avatarUrl = this.user?.avatar;
        const avatarFile = formData.get('avatar');
  
        if (avatarFile instanceof File) {
          avatarUrl = await this.uploadImage(avatarFile);
        }
  
        const updatedUser = {
          ...this.user,
          fullName: formData.get('fullName'),
          email: formData.get('email'),
          phone: formData.get('phone'),
          address: formData.get('address'),
          avatar: avatarUrl
        };
  
        this.saveUserData(updatedUser);
        this.showAlert('Profile updated successfully!', 'success');
      } catch (error) {
        console.error('Error updating profile:', error);
        this.showAlert('Failed to update profile', 'error');
      }
    }
  
    showAlert(message, type) {
      const alertDiv = document.createElement('div');
      alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
  
      const container = document.querySelector('.dashboard-main') || document.body;
      container.insertBefore(alertDiv, container.firstChild);
  
      setTimeout(() => alertDiv.remove(), 5000);
    }
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    window.userProfile = new UserProfile();
  });
  
  // Register form submission
  document.getElementById('registerForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
  
    if (formData.get('password') !== formData.get('confirmPassword')) {
      alert('Passwords do not match');
      return;
    }
  
    const userData = {
      fullName: formData.get('fullName'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      address: formData.get('address'),
      avatar: 'https://via.placeholder.com/150' // Placeholder avatar
    };
  
    // Store user data in localStorage and log them in
    localStorage.setItem('isLoggedIn', 'true');
    window.userProfile.saveUserData(userData);
  
    // Redirect to the login modal for the user to log in
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    loginModal.show();
  });
  
  // Login form submission
  document.getElementById('loginForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = this.querySelector('input[type="email"]').value;
    const password = this.querySelector('input[type="password"]').value;
  
    if (!email || !password) {
      alert('Please fill in all fields');
      return;
    }
  
    // Simulate login
    localStorage.setItem('isLoggedIn', 'true');
    const userData = {
      fullName: 'Test User',
      email: email,
      avatar: 'https://via.placeholder.com/150' // Placeholder avatar
    };
    window.userProfile.saveUserData(userData);
    window.location.href = 'dashboard.html';
  });
  
  document.addEventListener("DOMContentLoaded", () => {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
  
    if (navbarToggler && navbarCollapse) {
      navbarToggler.addEventListener('click', () => {
        navbarCollapse.classList.toggle('show');
      });
    }
  
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const isProtectedPage = window.location.pathname.match(/\/(dashboard|properties|wishlist|sell)\.html/);
  
    if (isProtectedPage && !isLoggedIn) {
      window.location.href = 'home.html'; // Redirect to home page if not logged in
    }
  
    updateNavbar();
  
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
  
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
        const scrolled = window.pageYOffset;
        hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
      });
    }
  
    // Handle mobile responsiveness
    if (window.innerWidth <= 768) {
      const mapDiv = document.getElementById("map");
      const listDiv = document.getElementById("property-list");
  
      // Add toggle button for map/list view on mobile
      const toggleBtn = document.createElement("button");
      toggleBtn.className = "btn btn-primary position-fixed";
      toggleBtn.style.bottom = "20px";
      toggleBtn.style.right = "20px";
      toggleBtn.style.zIndex = "1000";
      toggleBtn.innerHTML = "Toggle Map/List";
  
      document.body.appendChild(toggleBtn);
  
      let showingMap = true;
      toggleBtn.addEventListener("click", () => {
        if (showingMap) {
          mapDiv.style.display = "none";
          listDiv.style.display = "block";
        } else {
          mapDiv.style.display = "block";
          listDiv.style.display = "none";
        }
        showingMap = !showingMap;
      });
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
  });