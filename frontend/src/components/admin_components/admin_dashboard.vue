<template>
  <div>
    <nav class="navbar fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">ComfortCrew</router-link>
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
              {{ admin_username }}
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
                <router-link to="/admin_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Service Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/create_service">Create Service</router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/delete_service">Delete Service</router-link>
                  </li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Professional Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/admin_professionals">View Professionals</router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link>
                  </li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Client Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link>
                  </li>
                </ul>
                <li class="nav-item">
                <router-link to="/summary" class="nav-link active" aria-current="page">Summary</router-link>
              </li>
              </li>
            </ul>
            <div>
            <button class="btn btn-primary" @click="showLogoutModal = true">Logout</button>
          </div>
        </div>
        </div>
      </div>
    </nav>

    <div class="p-5 mt-5">
      <h1 align="center">{{ admin_username }}'s Dashboard</h1>
      <h2>Available Services:</h2>
      <br>

      <div v-for="service in services" :key="service.service_id" class="mb-4">
        <div class="card service-card">
          <div class="card-header card-header-custom">
            {{ service.service_name }}
          </div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Time Required: {{ service.service_time_required }} hrs</p>
            <p>Base Price: ${{ service.service_base_price }}</p>
            <h5>Professionals</h5>

            <div v-if="service.professionals.length" class="card">
              <ul class="list-group list-group-flush">
                <li v-for="professional in service.professionals" :key="professional.professional_id" class="list-group-item professional-item">
                  Professional: {{ professional.professional_name }} <br />
                  Rating: {{ professional.professional_rating }} <br />
                  Experience: {{ professional.professional_experience }} years
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No professionals available for this service.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

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
            <button type="button" class="btn btn-primary" @click="logout" >Logout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Global styling */
body {
  background-color: #DBCDB0; /* Light beige background */
  font-family: Arial, sans-serif;
}

h1 {
  color: #2f4f4f; /* Dark slate gray for contrast */
  font-size: 2.5rem;
  margin-bottom: 30px;
}

.navbar {
  background-color: #BFC8AD; /* Light olive green */
  padding: 10px 30px;
}

.navbar-brand {
  font-size: 1.8rem;
  color: #3f5b3b; /* Dark green */
  font-weight: bold;
}

.navbar-nav .nav-link {
  font-size: 1.1rem;
  color: #3f5b3b;
}

.navbar-nav .nav-link.active {
  background-color: #90B494; /* Soft green */
  color: white;
}

.offcanvas-body {
  padding: 20px;
}

.card {
  margin-bottom: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #90B494; /* Soft green */
  color: white;
  font-weight: bold;
  padding: 15px;
}

.card-body {
  background-color: #F5F5F5; /* Light grey */
  padding: 20px;
  border-radius: 8px;
}

.professional-item {
  font-size: 1rem;
  padding: 12px;
  background-color: #f0f8f0;
}

.professional-item:not(:last-child) {
  margin-bottom: 15px;
}

.card-header-custom {
  background-color: #A9B59D; /* Light olive */
}

button {
  background-color: #3f5b3b;
  color: white;
  margin-top: 15px; /* Adds a little space between the button and other elements */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
}


button:hover {
  background-color: #2f4f4f;
}

/* Logout Modal */
.modal-content {
  background-color: #FFFAF0; /* Floral white */
}
</style>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      admin_username: "",
      services: [],
      showLogoutModal: false,
    };
  },
  mounted() {
    this.admin_username = localStorage.getItem("admin_username");
    this.fetch_data();
  },
  methods: {
    async fetch_data() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin_dashboard', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();
        console.log("Full Response Data:", data);

        this.services = data.services || [];
        console.log("Services:", this.services);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      this.$router.push("/");
    },
  },
};
</script>




<!-- <template>
  <div>
    <nav class="navbar bg-body-tertiary fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">HandyHub</router-link>
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
              {{ admin_username }}
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
                <router-link to="/admin_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Service Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/create_service">Create Service</router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/delete_service">Delete Service</router-link>
                  </li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Professional Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/admin_professionals">View Professionals</router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link>
                  </li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Client Management
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link>
                  </li>
                </ul>
              </li>
            </ul>
            <button class="btn btn-primary" @click="showLogoutModal = true">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <div class="p-5 mt-5">
      <h1>{{ admin_username }}'s Dashboard</h1>

      <div v-for="service in services" :key="service.service_id" class="mb-4">
        <div class="card service-card">
          <div class="card-header card-header-custom">
            {{ service.service_name }}
          </div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Time Required: {{ service.service_time_required }} hrs</p>
            <p>Base Price: ${{ service.service_base_price }}</p>
            <h5>Professionals</h5>

            <div v-if="service.professionals.length" class="card">
              <ul class="list-group list-group-flush">
                <li v-for="professional in service.professionals" :key="professional.professional_id" class="list-group-item professional-item">
                  Professional: {{ professional.professional_name }} <br />
                  Rating: {{ professional.professional_rating }} <br />
                  Experience: {{ professional.professional_experience }} years
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No professionals available for this service.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

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
  name: "AdminDashboard",
  data() {
    return {
      admin_username: "",
      services: [],
      showLogoutModal: false,
    };
  },
  mounted() {
    this.admin_username = localStorage.getItem("admin_username");
    this.fetch_data();
  },
  methods: {
    async fetch_data() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin_dashboard', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();
        console.log("Full Response Data:", data);

        this.services = data.services || [];
        console.log("Services:", this.services);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      this.$router.push("/");
    },
  },
};
</script>
 -->





<!-- 

<template>
  <div>
    <nav class="navbar bg-body-tertiary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">HandyHub</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">{{ admin_username }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                <router-link to="/admin_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Service Management
                </a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/create_service">Create Service </router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_service">Delete Service</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Professional Management
                </a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin_professionals">View Professionals </router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Client Management
                </a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link></li>
                </ul>
              </li>
            </ul>
            <button class="btn btn-primary" @click="showLogoutModal = true">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <div class="p-5 mt-5">
      <h1>{{ admin_username }}'s Dashboard</h1>

      <div v-for="service in services" :key="service.service_id" class="mb-4">
        <div class="card service-card">
          <div class="card-header card-header-custom">
            {{ service.service_name }}
          </div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Time Required: {{ service.service_time_required }} hrs</p>
            <p>Base Price: ${{ service.service_base_price }}</p>
            <h5>Professionals</h5>

            <div v-if="serviceRequests[service.service_id]" class="card" style="width: 18rem;">
              <ul class="list-group list-group-flush">
                <li
                  v-for="request in serviceRequests[service.service_id]"
                  :key="request.professional_id"
                  class="list-group-item professional-item"
                >
                  Professional: {{ request.professional_name }} <br />
                  Rating: {{ request.professional_rating }} <br />
                  Experience: {{ request.professional_experience }} years
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No professionals assigned to this service.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

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
  name: 'admin_dashboard',
  data() {
    return {
      admin_username: '',
      services: [], // List of all services
      serviceRequests: {}, // Object to hold professionals by service
      showLogoutModal: false,
    };
  },
  mounted() {
    const admin_username = localStorage.getItem("admin_username");
    this.admin_username = admin_username;
    this.fetch_data();
  },
  methods: {
    async fetch_data() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin_dashboard', {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        console.log(data);

        // Assign services data
        this.services = data.services;

        // Organize professionals under each service and deduplicate
        this.serviceRequests = {};
        data.serviceRequests.forEach((request) => {
          const serviceId = request.service_id;

          // Find the professional details by matching professional_id
          const professional = data.profession.find(
            (prof) => prof.professional_id === request.professional_id
          );

          if (professional) {
            // Create a professional object with detailed information
            const professionalDetails = {
              professional_id: professional.professional_id,
              professional_name: professional.professional_name,
              professional_rating: professional.professional_rating,
              professional_experience: professional.professional_experience,
              professional_description: professional.professional_description,
            };

            // Ensure serviceRequests object for the serviceId exists
            if (!this.serviceRequests[serviceId]) {
              this.serviceRequests[serviceId] = [];
            }

            // Check if the professional is already in the array
            const isDuplicate = this.serviceRequests[serviceId].some(
              (prof) => prof.professional_id === professionalDetails.professional_id
            );

            // Add only unique professionals
            if (!isDuplicate) {
              this.serviceRequests[serviceId].push(professionalDetails);
            }
          }
        });

        console.log("Service Requests with Professionals (Deduplicated):", this.serviceRequests);

      } catch (error) {
        console.log(error);
      }
    },
    logout() {
      // Clear the JWT token
      localStorage.removeItem("JWTToken");
      // Redirect to home panel
      window.location.href = "http://localhost:8080/";
    },
  }
};
</script>

<style>
/* Global styling */
body {
  background-color: #DBCDB0; /* Light beige background */
  font-family: Arial, sans-serif;
}

h1 {
  color: #2f4f4f; /* Dark slate gray for contrast */
  font-size: 2.5rem;
  margin-bottom: 30px;
}

.navbar {
  background-color: #BFC8AD; /* Light olive green */
  padding: 10px 30px;
}

.navbar-brand {
  font-size: 1.8rem;
  color: #3f5b3b; /* Dark green */
  font-weight: bold;
}

.navbar-nav .nav-link {
  font-size: 1.1rem;
  color: #3f5b3b;
}

.navbar-nav .nav-link.active {
  background-color: #90B494; /* Soft green */
  color: white;
}

.offcanvas-body {
  padding: 20px;
}

.card {
  margin-bottom: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #90B494; /* Soft green */
  color: white;
  font-weight: bold;
  padding: 15px;
}

.card-body {
  background-color: #F5F5F5; /* Light grey */
  padding: 20px;
  border-radius: 8px;
}

.professional-item {
  font-size: 1rem;
  padding: 12px;
  background-color: #f0f8f0;
}

.professional-item:not(:last-child) {
  margin-bottom: 15px;
}

.card-header-custom {
  background-color: #A9B59D; /* Light olive */
}

button {
  background-color: #3f5b3b;
  color: white;
}

button:hover {
  background-color: #2f4f4f;
}

/* Logout Modal */
.modal-content {
  background-color: #FFFAF0; /* Floral white */
}
</style> -->
