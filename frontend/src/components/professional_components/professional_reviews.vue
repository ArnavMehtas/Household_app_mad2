<!-- <template>
  <div class="professional-reviews">
    <div class="rating-container">
      <div class="stars">
        <span v-for="n in 5" :key="n" class="star">
          <span v-if="n <= fullStars" class="filled">★</span>
          <span v-else-if="n === fullStars + 1 && hasHalfStar" class="half-filled">★</span>
          <span v-else class="empty">★</span>
        </span>
      </div>
      <p class="rating-text">{{ rating }} out of 5</p>
    </div>

    <div class="reviews">
      <div v-for="review in reviews" :key="review.review_id" class="review-tile">
        <h3 class="review-client-name">{{ review.client_name }}</h3>
        <p class="review-content">{{ review.review_comment }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: 0,           // The rating value
      fullStars: 0,        // Full stars (integer part of rating)
      hasHalfStar: false,  // Whether there should be a half star
      reviews: [],         // Array to hold reviews data
      professionalId: 1    // Sample professional ID, change based on actual value
    };
  },
  created() {
    this.fetchProfessionalData();
  },
  methods: {
    // Fetch professional rating and reviews data
    fetchProfessionalData() {
      // Fetch professional rating
      fetch(`http://127.0.0.1:8000/professional/${this.professionalId}/rating`)
        .then(response => response.json())
        .then(data => {
          if (data && data.rating !== undefined) {
            this.rating = parseFloat(data.rating); // Ensure it's a number
            this.calculateStars(this.rating); // Calculate the star representation
          }
        })
        .catch(error => {
          console.error("Error fetching professional rating:", error.message);
        });

      // Fetch professional reviews
      fetch(`http://127.0.0.1:8000/professional/${this.professionalId}/reviews`)
        .then(response => response.json())
        .then(data => {
          if (data && data.reviews) {
            this.reviews = data.reviews;
          }
        })
        .catch(error => {
          console.error("Error fetching reviews:", error.message);
        });
    },

    // Method to calculate full stars, half stars, and empty stars
    calculateStars(rating) {
      this.fullStars = Math.floor(rating);  // Full stars (integer part)
      this.hasHalfStar = (rating % 1) >= 0.5; // Check if there's a half star
    }
  }
};
</script>

<style scoped>
.professional-reviews {
  text-align: center;
}

.rating-container {
  margin-bottom: 20px;
}

.stars {
  font-size: 30px;
  color: gold;
}

.star {
  margin: 0 2px;
}

.star.filled {
  color: gold;
}

.star.half-filled {
  background: linear-gradient(to right, gold 50%, lightgray 50%);
  -webkit-background-clip: text;
  color: transparent;
}

.star.empty {
  color: lightgray;
}

.rating-text {
  font-size: 16px;
  margin-top: 5px;
}

.reviews {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.review-tile {
  background-color: #f9f9f9;
  padding: 15px;
  margin: 10px 0;
  width: 80%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.review-client-name {
  font-weight: bold;
  font-size: 18px;
}

.review-content {
  font-size: 16px;
  margin-top: 10px;
  color: #555;
}
</style> -->

<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar bg-body-tertiary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">HandyHub</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasNavbar"
          aria-controls="offcanvasNavbar"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          class="offcanvas offcanvas-end"
          tabindex="-1"
          id="offcanvasNavbar"
          aria-labelledby="offcanvasNavbarLabel"
        >
          <div class="offcanvas-header">
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="offcanvas"
              aria-label="Close"
            ></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                  <router-link to="/professional_dashboard" class="nav-link active">Home</router-link>
                </li>
              <li class="nav-item">
                <router-link to="/completed_services" class="nav-link active">Completed Services</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/professional_profile" class="nav-link active">Profile</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/client_reviews" class="nav-link active">Your reviews</router-link>
              </li>
            </ul>
            <button class="btn btn-primary" @click="showLogoutModal = true">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Rating and Reviews Section -->
    <div class="professional-reviews mt-5 pt-5">
      <!-- Rating Section (Donut Chart) -->
      <div class="donut-container">
        <div class="donut" :style="donutStyle">
          <span class="rating-text">{{ rating }} out of 5</span>
        </div>
      </div>

      <!-- Reviews Section -->
      <div class="reviews">
        <div v-for="review in reviews" :key="review.review_id" class="review-tile">
          <h3 class="review-client-name">{{ review.client_name }}</h3>
          <p class="review-content">{{ review.review_comment }}</p>
        </div>
      </div>
    </div>

    <!-- Logout Confirmation Modal -->
    <div v-if="showLogoutModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Logout</h5>
            <button type="button" class="btn-close" @click="showLogoutModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to log out?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showLogoutModal = false">Cancel</button>
            <button type="button" class="btn btn-primary" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: 0,           // The rating value
      reviews: [],         // Array to hold reviews data
      professionalId: null,   // The professional ID will be fetched from localStorage
      showLogoutModal: false, // Tracks the visibility of the logout confirmation modal
    };
  },
  created() {
    this.professionalId = localStorage.getItem("professional_id"); // Get the professional ID from localStorage
    if (this.professionalId) {
      console.log(this.professionalId);
      this.fetchProfessionalData();
    } else {
      console.error("No professional ID found in localStorage");
    }
  },
  computed: {
    // Compute the donut chart style based on rating
    donutStyle() {
      // Calculate percentage for the donut fill
      const ratingPercentage = ((this.rating / 5) * 100).toFixed(2);
      return {
        background: `conic-gradient(gold ${ratingPercentage}%, lightgray ${ratingPercentage}%)`
      };
    }
  },
  methods: {
    // Fetch professional rating and reviews data
    fetchProfessionalData() {
      // Fetch professional rating
      fetch(`http://127.0.0.1:8000/professional/${this.professionalId}/rating`)
        .then(response => response.json())
        .then(data => {
          if (data && data.rating !== undefined) {
            this.rating = data.rating; // Set the rating value
          }
        })
        .catch(error => {
          console.error("Error fetching professional rating:", error.message);
        });

      // Fetch professional reviews
      fetch(`http://127.0.0.1:8000/professional/${this.professionalId}/reviews`)
        .then(response => response.json())
        .then(data => {
          if (data && data.reviews) {
            this.reviews = data.reviews;
          }
        })
        .catch(error => {
          console.error("Error fetching reviews:", error.message);
        });
    },
    logout() {
      localStorage.removeItem("JWTToken");
      localStorage.removeItem("professional_id"); // Remove professional ID on logout
      window.location.href = "http://localhost:8080/";
    }
  }
};
</script>

<style scoped>
/* Styling for the Professional Dashboard Page */
body {
  background-color: #C3C9E9;
}

.navbar {
  background-color: #AAABBC !important;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.navbar .navbar-brand {
  color: #000;
  font-weight: bold;
}

.navbar .nav-link {
  color: #000 !important;
}

.navbar .nav-link.active {
  color: #080808 !important;
}

.donut-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 20px auto;
}

.donut {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: conic-gradient(gold 0%, lightgray 0%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut:before {
  content: '';
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
  border-radius: 50%;
  background: white;
}

.rating-text {
  position: relative;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  z-index: 2; /* Ensure it's on top */
}


.rating-text {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.reviews {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.review-tile {
  background-color: #f9f9f9;
  padding: 15px;
  margin: 10px 0;
  width: 80%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.review-client-name {
  font-weight: bold;
  font-size: 18px;
}

.review-content {
  font-size: 16px;
  margin-top: 10px;
  color: #555;
}

.card {
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #8B8982;
}

.card-body {
  background-color: #8B8982;
  padding: 20px;
  border-radius: 5px;
}

.modal-content {
  background-color: #9989d9;
}

.alert-danger {
  background-color: #F8D7DA;
  color: #721C24;
}
</style>
