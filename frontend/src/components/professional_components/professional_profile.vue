<!-- <template>
    <div>
      <nav class="navbar bg-body-tertiary fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">The Helper!</a>
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
              <router-link to="/client_logout">
                <button class="btn btn-primary">Logout</button>
              </router-link>
            </div>
          </div>
        </div>
      </nav>
      
      <br>
      <br>
      <br>
      <div class="container mt-4">
        <h1 class="text-center mb-4">Professional Profile</h1>
  
        <div class="profile-card shadow-lg rounded-circle p-4 mx-auto">
          <div class="card-body text-center">
            <h5 class="card-title">{{ profile.professional_name }}</h5>
            <p><strong>Description:</strong> {{ profile.professional_description }}</p>
            <p><strong>Experience:</strong> {{ profile.professional_experience }} years</p>
            <p><strong>Rating:</strong> {{ profile.professional_rating }}</p>
            <p><strong>Service Type:</strong> {{ profile.professional_service_type }}</p>
            <p><strong>Date Created:</strong> {{ profile.professional_date_created }}</p>
    
            <button class="btn btn-primary mt-3" @click="openEditModal">Edit Profile</button>
          </div>
        </div>
      </div>
  
      <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editProfileModalLabel">Edit Your Profile Details</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label for="professional_name" class="form-label">Name</label>
                  <input type="text" id="professional_name" class="form-control" v-model="profileEdit.professional_name" required />
                </div>
                <div class="mb-3">
                  <label for="professional_description" class="form-label">Description</label>
                  <input type="text" id="professional_description" class="form-control" v-model="profileEdit.professional_description" required />
                </div>
                <div class="mb-3">
                  <label for="professional_experience" class="form-label">Experience (years)</label>
                  <input type="number" id="professional_experience" class="form-control" v-model="profileEdit.professional_experience" required />
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ProfessionalProfile",
    data() {
      return {
        profile: {},
        profileEdit: {},
        loading: true,
        errorMsg: ""
      };
    },
    methods: {
      async fetchProfile() {
        try {
          const response = await fetch("http://127.0.0.1:8000/professional_profile", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("JWTToken")}`
            }
          });
  
          if (!response.ok) {
            throw new Error("Failed to fetch profile data.");
          }
  
          const data = await response.json();
          this.profile = data;
          this.profileEdit = { ...data };  // Copy the fetched data to the editable profile
        } catch (error) {
          this.errorMsg = error.message;
        } finally {
          this.loading = false;
        }
      },
  
      openEditModal() {
        // Show the modal
        const editModal = new bootstrap.Modal(document.getElementById("editProfileModal"));
        editModal.show();
      },
  
      async updateProfile() {
        try {
          const response = await fetch("http://127.0.0.1:8000/professional_profile/update", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("JWTToken")}`
            },
            body: JSON.stringify(this.profileEdit)
          });
  
          if (!response.ok) {
            throw new Error("Failed to update profile.");
          }
  
          const data = await response.json();
          alert(data.message);  // Show success message
          this.fetchProfile();  // Reload the updated profile data
        } catch (error) {
          this.errorMsg = error.message;
        }
      }
    },
    created() {
      this.fetchProfile();  // Fetch profile data on page load
    }
  };
  </script>
  
  <style>
  .profile-card {
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .card-body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
  
  .card-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .modal-dialog {
    max-width: 500px;
  }
  </style>
   -->

   <template>
    <div>
      <!-- Navigation Bar -->
      <nav class="navbar bg-body-tertiary fixed-top" style="background-color: #AC9FBB;">
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
      
      <!-- Profile Section -->
      <br><br><br>
      <div class="container mt-4">
        <h1 class="text-center mb-4">Professional Profile</h1>
      
        <!-- Circular Profile Card -->
        <div class="profile-card shadow-lg rounded-circle p-4 mx-auto" style="background-color: #DDBDD5;">
          <div class="card-body text-center">
            <h5 class="card-title">{{ profile.professional_name }}</h5>
            <p><strong>Description:</strong> {{ profile.professional_description }}</p>
            <p><strong>Experience:</strong> {{ profile.professional_experience }} years</p>
            <p><strong>Rating:</strong> {{ profile.professional_rating }}</p>
            <p><strong>Service Type:</strong> {{ profile.professional_service_type }}</p>
            <p><strong>Date Created:</strong> {{ profile.professional_date_created }}</p>
      
            <button class="btn btn-primary mt-3" @click="openEditModal">Edit Profile</button>
          </div>
        </div>
      </div>
      
      <!-- Edit Profile Modal (unchanged) -->
      <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editProfileModalLabel">Edit Your Profile Details</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <!-- Profile Edit Form (unchanged) -->
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label for="professional_name" class="form-label">Name</label>
                  <input type="text" id="professional_name" class="form-control" v-model="profileEdit.professional_name" required />
                </div>
                <div class="mb-3">
                  <label for="professional_description" class="form-label">Description</label>
                  <input type="text" id="professional_description" class="form-control" v-model="profileEdit.professional_description" required />
                </div>
                <div class="mb-3">
                  <label for="professional_experience" class="form-label">Experience (years)</label>
                  <input type="number" id="professional_experience" class="form-control" v-model="profileEdit.professional_experience" required />
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </form>
            </div>
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
    name: "ProfessionalProfile",
    data() {
      return {
        profile: {},
        profileEdit: {},
        loading: true,
        errorMsg: "",
        showLogoutModal: false, // Tracks the visibility of the logout confirmation modal
      };
    },
    methods: {
      async fetchProfile() {
        try {
          const response = await fetch("http://127.0.0.1:8000/professional_profile", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            },
          });
  
          if (!response.ok) {
            throw new Error("Failed to fetch profile data.");
          }
  
          const data = await response.json();
          this.profile = data;
          this.profileEdit = { ...data }; // Copy the fetched data to the editable profile
        } catch (error) {
          this.errorMsg = error.message;
        } finally {
          this.loading = false;
        }
      },
  
      openEditModal() {
        // Show the modal
        const editModal = new bootstrap.Modal(document.getElementById("editProfileModal"));
        editModal.show();
      },
  
      async updateProfile() {
        try {
          const response = await fetch("http://127.0.0.1:8000/professional_profile/update", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            },
            body: JSON.stringify(this.profileEdit),
          });
  
          if (!response.ok) {
            throw new Error("Failed to update profile data.");
          }
  
          alert("Profile updated successfully!");
          this.fetchProfile(); // Reload the profile after updating
        } catch (error) {
          this.errorMsg = error.message;
        }
      },
  
      logout() {
        // Clear the JWT token
        localStorage.removeItem("JWTToken");
        // Redirect to home panel
        window.location.href = "http://localhost:8080/";
      },
    },
    created() {
      this.fetchProfile();
    },
  };
  </script>
  
  <style scoped>
  /* Additional styling */
  .profile-card {
    border-radius: 20px; /* Slightly more circular */
  }
  </style>
  