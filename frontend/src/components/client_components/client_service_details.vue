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
              <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
                Explore
              </h5>
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
                  <router-link to="/client_dashboard" class="nav-link active">Home</router-link>
                </li>
                
              <li class="nav-item">
                <router-link to="/reviews" class="nav-link active"
                  >Give a review</router-link
                >
              </li>
                <li class="nav-item">
                  <router-link to="/service_log" class="nav-link active">My Service Log</router-link>
                </li>
              </ul>
              <router-link to="/client_logout">
                <button class="btn btn-primary">Logout</button>
              </router-link>
            </div>
          </div>
        </div>
      </nav>
  
      <div class="container mt-5">
        <h1 class="text-center mb-4">Professionals for Service ID: {{ service_id }}</h1>
  
        <div class="filters mb-4 d-flex justify-content-center">
          <button
            class="btn btn-outline-primary me-2"
            @click="sortProfessionals('rating')"
          >
            Sort by Rating
          </button>
          <button
            class="btn btn-outline-primary"
            @click="sortProfessionals('experience')"
          >
            Sort by Experience
          </button>
        </div>
  
        <div class="row">
          <div
            v-for="professional in professionals"
            :key="professional.professional_id"
            class="col-md-4 mb-4 d-flex align-items-stretch"
          >
            <div class="card professional-card">
              <div class="card-body">
                <h5 class="card-title">{{ professional.name }}</h5>
                <p class="card-text">{{ professional.description }}</p>
                <p class="card-text">
                  <strong>Experience:</strong> {{ professional.experience }} years
                </p>
                <p class="card-text">
                  <strong>Rating:</strong> {{ professional.rating }} / 5
                </p>
                <button class="btn btn-primary" @click="openBookNowPopup(professional.professional_id)">
                  Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div
        v-if="isPopupVisible"
        class="modal fade show d-block"
        style="background: rgba(0, 0, 0, 0.5);"
        tabindex="-1"
        aria-labelledby="bookNowModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="bookNowModalLabel">Request Service</h5>
              <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <textarea
                v-model="requestRemarks"
                class="form-control"
                rows="4"
                placeholder="Enter your request remarks here..."
              ></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closePopup">Close</button>
              <button type="button" class="btn btn-primary" @click="submitRequest">Send Request</button>
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
        service_id: this.$route.params.service_id, 
        professionals: [],
        originalProfessionals: [],
        isPopupVisible: false,
        requestRemarks: '',
        selectedProfessionalId: null,
        client_id: localStorage.getItem("client_id"),
      };
    },
    methods: {
      async fetchProfessionals() {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/services/${this.service_id}/professionals`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch professionals.");
          }
          const data = await response.json();
          this.professionals = data;
          this.originalProfessionals = [...data];
        } catch (error) {
          console.error("Error fetching professionals:", error);
          alert("Failed to load professionals. Please try again later.");
        }
      },
      sortProfessionals(criteria) {
        if (criteria === "rating") {
          this.professionals.sort((a, b) => b.rating - a.rating);
        } else if (criteria === "experience") {
          this.professionals.sort((a, b) => b.experience - a.experience);
        }
      },

      openBookNowPopup(professionalId) {
        this.selectedProfessionalId = professionalId;
        this.isPopupVisible = true;
      },
      closePopup() {
        this.isPopupVisible = false;
        this.requestRemarks = '';  
      },
      async submitRequest() {
  const requestData = {
    professional_id: this.selectedProfessionalId,
    client_id: this.client_id,  
    remarks: this.requestRemarks,
    service_id: this.service_id,  
  };
  console.log("Sending request data:", requestData);

  try {
    const response = await fetch('http://127.0.0.1:8000/service-request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error('Failed to send request.');
    }

    alert('Request sent successfully!');
    this.closePopup();
  } catch (error) {
    console.error('Error sending request:', error);
    alert('Error sending request. Please try again.');
  }
},

    },
    mounted() {
      this.fetchProfessionals(); // call this when the component is mounted
    },
  };
  </script>
  
  <style>
  .professional-card {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 250px;
  }
  
  .modal-dialog {
    max-width: 500px;
    margin: auto;
  }
  
  .modal-content {
    padding: 20px;
  }
  </style>
   -->
   <template>
    <div>
      <nav class="navbar bg-body-tertiary fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="/client_dashboard"><strong>ComfortCrew</strong></a>
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
              <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
                Explore
              </h5>
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
                  <router-link to="/client_dashboard" class="nav-link active">Home</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/service_log" class="nav-link active">My Services</router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </nav>
  
      <div class="container mt-5">
        <br><br>
        <h1 class="text-center mb-4">Professionals for service: {{ serviceName }}</h1>
  
        <!-- Filters -->
        <div class="filters mb-4 d-flex justify-content-center">
          <button
            class="btn btn-outline-primary me-2"
            @click="sortProfessionals('rating')"
          >
            Sort by Rating
          </button>
          <button
            class="btn btn-outline-primary"
            @click="sortProfessionals('experience')"
          >
            Sort by Experience
          </button>
        </div>
  
        <!-- Professional Cards -->
        <div class="row">
          <div
            v-for="professional in professionals"
            :key="professional.professional_id"
            class="col-md-4 mb-4 d-flex align-items-stretch"
          >
            <div class="card professional-card">
              <div class="card-body">
                <h5 class="card-title">{{ professional.name }}</h5>
                <p class="card-text">{{ professional.description }}</p>
                <p class="card-text">
                  <strong>Experience:</strong> {{ professional.experience }} years
                </p>
                <p class="card-text">
                  <strong>Rating:</strong> {{ professional.rating }} / 5
                </p>
                <!-- Book Now Button -->
                <button class="btn btn-primary" @click="openBookNowPopup(professional.professional_id)">
                  Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Popup Modal -->
      <div
        v-if="isPopupVisible"
        class="modal fade show d-block"
        style="background: rgba(0, 0, 0, 0.5);"
        tabindex="-1"
        aria-labelledby="bookNowModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="bookNowModalLabel">Request Service</h5>
              <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <textarea
                v-model="requestRemarks"
                class="form-control"
                rows="4"
                placeholder="Enter your request remarks here..."
              ></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closePopup">Close</button>
              <button type="button" class="btn btn-primary" @click="submitRequest">Send Request</button>
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
        service_id: this.$route.params.service_id,
        serviceName: '',
        professionals: [],
        originalProfessionals: [],
        isPopupVisible: false,
        requestRemarks: '',
        selectedProfessionalId: null,
        client_id: localStorage.getItem("client_id"),
      };
    },
    methods: {
      async fetchProfessionals() {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/services/${this.service_id}/professionals`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch professionals.");
          }
          const data = await response.json();
          this.professionals = data;
          this.originalProfessionals = [...data];
        } catch (error) {
          console.error("Error fetching professionals:", error);
          alert("Failed to load professionals. Please try again later.");
        }
      },
  
      async fetchServiceName() {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/services/${this.service_id}`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch service name.");
          }
          const data = await response.json();
          this.serviceName = data.name; // Assuming the service name is in `data.name`
        } catch (error) {
          console.error("Error fetching service name:", error);
          alert("Failed to load service name. Please try again later.");
        }
      },
  
      sortProfessionals(criteria) {
        if (criteria === "rating") {
          this.professionals.sort((a, b) => b.rating - a.rating);
        } else if (criteria === "experience") {
          this.professionals.sort((a, b) => b.experience - a.experience);
        }
      },
  
      openBookNowPopup(professionalId) {
        this.selectedProfessionalId = professionalId;
        this.isPopupVisible = true;
      },
  
      closePopup() {
        this.isPopupVisible = false;
        this.requestRemarks = '';
      },
  
      async submitRequest() {
        const requestData = {
          professional_id: this.selectedProfessionalId,
          client_id: this.client_id,
          remarks: this.requestRemarks,
          service_id: this.service_id,
        };
        console.log("Sending request data:", requestData);
  
        try {
          const response = await fetch('http://127.0.0.1:8000/service-request', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
            },
            body: JSON.stringify(requestData),
          });
  
          if (!response.ok) {
            throw new Error('Failed to send request.');
          }
  
          alert('Request sent successfully!');
          this.closePopup();
        } catch (error) {
          console.error('Error sending request:', error);
          alert('Error sending request. Please try again.');
        }
      },
    },
    mounted() {
      this.fetchProfessionals();
      this.fetchServiceName(); // Fetch service name when the component is mounted
    },
  };
  </script>
  
  <style>
  /* Styling similar to the admin dashboard */
  body {
    background-color: #F5F5DC;
    font-family: Arial, sans-serif;
  }
  
  .navbar {
  background-color: #AF9B46 !important; /* Ensure the custom background color is applied */
  color: white !important; /* Ensure the text color is overridden */
}

.navbar-brand {
  font-weight: bold;
  color: white !important; /* Ensure the brand text is white */
}

.nav-link {
  color: rgb(4, 3, 3) !important; /* Ensure navbar links are white */
}

.nav-link:hover {
  color: #5e5603 !important; /* Add hover effect for better UX */
}

  .card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 12rem; /* Smaller width for a more rectangular look */
    height: 18rem; /* Larger vertical length */
    margin: 15px; /* Add space between cards */
    text-align: center;
    background-color: #F7B05B; /* Tertiary color */
    color: rgb(7, 7, 7);
  }
  .card-body {
    display: flex;
    flex-direction: column; /* Stack the content vertically */
    justify-content: center; /* Vertically center the body content */
    padding: 10px; /* Add padding inside the body for spacing */
    height: calc(100% - 40px); /* Ensure the body takes up the remaining height after the header */
    overflow: hidden; /* Avoid content overflow */
  }
  .card-header {
    background-color: #AF9B46;
    color: black;
    font-weight: bold;
  
  }
  
  .modal-content {
    background-color: #AF9B46;
  }
  
  .card {
    flex: 0 0 30%; /* Make each card take up 30% of the row width */
  }
  
  /* Service Cards - Layout */
  .row {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between; /* Space between cards */
    margin: 0 auto; /* Center the content */
    max-width: 100%; /* Ensure it uses the full available width */
  }
  
  .card {
    flex: 0 0 12rem; /* Ensure cards have a fixed width and wrap */
  }
  
  /* Responsive Layout - Adjust the layout for different screen sizes */
  @media (max-width: 10991px) {
    .card {
      width: 25rem; /* Slightly larger for medium screens */
      height: 20rem; /* Slightly larger for medium screens */
    }
  }
  
  @media (max-width: 768px) {
    .card {
      width: 100%; /* Full width for smaller screens */
      height: auto; /* Auto height for smaller screens */
    }
  
    .row {
      justify-content: center; /* Center the cards */
    }
  }
  
  /* Button Styling */
  .btn-primary {
    background-color: #fff05a;
    border-color: #fff05a;
    color:black
  }
  
  .btn-primary:hover {
    background-color: #AF9B46;
    border-color: #6c9c88;
  }
  
  /* Modal Popup */
  .modal-body {
    background-color: #fff;
  }
  
  .professional-card {
    transition: transform 0.3s ease-in-out;
  }
  
  .professional-card:hover {
    transform: scale(1.05); /* Zoom in on hover */
  }
  </style>
  