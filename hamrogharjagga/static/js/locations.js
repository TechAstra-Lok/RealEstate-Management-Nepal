const nepalLocations = {
    provinces: {
      "Bagmati": {
        districts: {
          "Kathmandu": {
            municipalities: [
              "Kathmandu Metropolitan",
              "Kirtipur",
              "Budhanilkantha",
              "Tokha",
              "Tarakeshwar",
              // Add more municipalities in Kathmandu
            ]
          },
          "Lalitpur": {
            municipalities: [
              "Lalitpur Metropolitan",
              "Godawari",
              "Mahalaxmi",
              // Add more municipalities in Lalitpur
            ]
          },
          "Bhaktapur": {
            municipalities: [
              "Bhaktapur Metropolitan",
              "Changunarayan",
              "Madhyapur Thimi",
              // Add more municipalities in Bhaktapur
            ]
          }
          // Add more districts in Bagmati
        }
      },
      "Karnali": {
        districts: {
          "Surkhet": {
            municipalities: [
              "Birendranagar",
              "Khirabari",
              "Gorakhpur",
              // Add more municipalities in Surkhet
            ]
          },
          "Dailekh": {
            municipalities: [
              "Dailekh",
              "Narayan",
              "Panchapuri",
              // Add more municipalities in Dailekh
            ]
          }
          // Add more districts in Karnali
        }
      },
      "Province 1": {
        districts: {
          "Jhapa": {
            municipalities: [
              "Bhadrapur",
              "Damak",
              "Birtamod",
              // Add more municipalities in Jhapa
            ]
          },
          "Bhojpur": {
            municipalities: [
              "Bhojpur",
              "Shadananda",
              "Arun",
              // Add more municipalities in Bhojpur
            ]
          }
          // Add more districts in Province 1
        }
      },
      "Lumbini": {
        districts: {
          "Rupandehi": {
            municipalities: [
              "Bhairahawa",
              "Lumbini Sanskritik",
              "Kanchan Kawan",
              // Add more municipalities in Rupandehi
            ]
          },
          "Nawalparasi": {
            municipalities: [
              "Nawalpur",
              "Parasi",
              "Bardaghat",
              // Add more municipalities in Nawalparasi
            ]
          }
          // Add more districts in Lumbini
        }
      },
      "Sudurpashchim": {
        districts: {
          "Doti": {
            municipalities: [
              "Doti",
              "Beldandi",
              "Shikhar",
              // Add more municipalities in Doti
            ]
          },
          "Kailali": {
            municipalities: [
              "Dhangadhi",
              "Tikapur",
              "Lamkichuha",
              // Add more municipalities in Kailali
            ]
          }
          // Add more districts in Sudurpashchim
        }
      },
      "Gandaki": {
        districts: {
          "Pokhara": {
            municipalities: [
              "Pokhara Metropolitan",
              "Lekhnath",
              "Madhyapur Thimi",
              // Add more municipalities in Pokhara
            ]
          },
          "Kaski": {
            municipalities: [
              "Pokhara",
              "Gandaki",
              "Pumdi Bhumdi",
              // Add more municipalities in Kaski
            ]
          }
          // Add more districts in Gandaki
        }
      },
      "Province 2": {
        districts: {
          "Saptari": {
            municipalities: [
              "Rajbiraj",
              "Kanchan Kawan",
              "Dhanusha",
              // Add more municipalities in Saptari
            ]
          },
          "Siraha": {
            municipalities: [
              "Lahan",
              "Siraha",
              "Golbazar",
              // Add more municipalities in Siraha
            ]
          }
          // Add more districts in Province 2
        }
      }
      // Add other provinces as needed
    }
  };
  
  class LocationManager {
    constructor() {
      this.initializeLocationSelect();
      this.setupEventListeners();
    }
  
    initializeLocationSelect() {
      const select = $('#location-search');
      select.select2({
        placeholder: 'Search location...',
        minimumInputLength: 1,
        ajax: {
          delay: 250,
          transport: (params, success, failure) => {
            const query = params.data.term.toLowerCase();
            const results = this.searchLocations(query);
            success({ results });
          }
        }
      });
    }
  
    searchLocations(query) {
      const results = [];
      
      Object.entries(nepalLocations.provinces).forEach(([province, provinceData]) => {
        Object.entries(provinceData.districts).forEach(([district, districtData]) => {
          districtData.municipalities.forEach(municipality => {
            const text = `${municipality}, ${district}, ${province}`;
            if (text.toLowerCase().includes(query)) {
              results.push({
                id: text,
                text: text,
                province,
                district,
                municipality
              });
            }
          });
        });
      });
  
      return results;
    }
  
    setupEventListeners() {
      // Add any additional event listeners needed
    }
  }
  
  // Initialize when the page loads
  document.addEventListener('DOMContentLoaded', () => {
    new LocationManager();
  });
  