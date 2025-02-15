<!-- <template>
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
              {{ client_name }}
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
                <router-link to="/client_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/client_services" class="nav-link">My Services</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/client_requests" class="nav-link">Service Requests</router-link>
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
      <h1 align="center">{{ client_name }}'s Dashboard</h1>
      <h2>Available Services:</h2>
      <div v-for="service in services" :key="service.id" class="mb-4">
        <div class="card">
          <div class="card-header">{{ service.service_name }}</div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Price: ${{ service.service_base_price }}</p>
            <p>Time Required: {{ service.service_time_required }} hours</p>
            <router-link :to="`/services/${service.service_id}/professionals`" class="btn btn-primary">
              Book Service
            </router-link>
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
  name: "ClientDashboard",
  data() {
    return {
      client_name: "",
      services: [],
      showLogoutModal: false,
    };
  },
  mounted() {
    this.client_name = localStorage.getItem("client_name");
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('http://127.0.0.1:8000/services', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data)
          this.services = data || [];
          console.log("Fetched services:", this.services);
        } else {
          console.error("Failed to fetch services:", response.status);
        }
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      this.$router.push("/");
    },
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
  background-color: #BFC8AD;
}

.card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #90B494;
  color: white;
  font-weight: bold;
}

.modal-content {
  background-color: #FFFAF0;
}
</style> -->


<!-- 
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
              {{ client_name }}
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
                <router-link to="/client_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/service_log" class="nav-link">My Services</router-link>
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
      <h1 align="center">Welcome {{ client_name }}</h1>
      <br><br>
      <h2 style="text-align: center;">Available Services:</h2>

      <div class="d-flex justify-content-center mb-4">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control w-50"
          placeholder="Search for services"
        />
      </div>

      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div
          v-for="service in filteredServices"
          :key="service.id"
          class="col"
        >
          <div class="card">
            <div class="card-header">{{ service.service_name }}</div>
            <div class="card-body">
              <p>{{ service.service_description }}</p>
              <p>Price: ${{ service.service_base_price }}</p>
              <p>Time Required: {{ service.service_time_required }} hours</p>
              <router-link :to="`/services/${service.service_id}/professionals`" class="btn btn-primary">
                Book Service
              </router-link>
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
  name: "ClientDashboard",
  data() {
    return {
      client_name: "",
      services: [],
      showLogoutModal: false,
      searchQuery: "",
    };
  },
  computed: {
    filteredServices() {
      return this.services.filter(service => {
        return service.service_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
               service.service_description.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    }
  },
  mounted() {
    this.client_name = localStorage.getItem("client_name");
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('http://127.0.0.1:8000/services', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.services = data || [];
        } else {
          console.error("Failed to fetch services:", response.status);
        }
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      this.$router.push("/");
    },
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
  background-color: #BFC8AD;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 12rem; /* Smaller width for a more rectangular look */
  height: 18rem; /* Larger vertical length */
  margin: 15px; /* Add space between cards */
  text-align: center; 
  
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
  background-color: #90B494;
  color: white;
  font-weight: bold;
}

.modal-content {
  background-color: #FFFAF0;
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
    width: 100%; /* Full width for small screens */
    height: auto; /* Auto height for small screens */
  }
}
</style> -->


<template>
  <div>
    <nav class="navbar fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/"><strong>ComfortCrew</strong></router-link>
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
              {{ client_name }}
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
                <router-link to="/client_dashboard" class="nav-link active" aria-current="page">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/service_log" class="nav-link">My Services</router-link>
              </li>
            </ul>
            <div>
              <button class="btn btn-logout" @click="showLogoutModal = true">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="p-5 mt-5">
      <h1 align="center">Welcome {{ client_name }}</h1>
      <br><br>
      <h2 style="text-align: center;">Available Services:</h2>

      <!-- Search Bar -->
      <div class="d-flex justify-content-center mb-4">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control w-50"
          placeholder="Search for services"
        />
      </div>

      <!-- Service Cards -->
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div
          v-for="service in filteredServices"
          :key="service.id"
          class="col"
        >
          <div class="card">
            <div class="card-header">{{ service.service_name }}</div>
            <div class="card-body">
              <p>{{ service.service_description }}</p>
              <p>Price: ${{ service.service_base_price }}</p>
              <p>Time Required: {{ service.service_time_required }} hours</p>
              <router-link :to="`/services/${service.service_id}/professionals`" class="btn btn-book">
                Book Service
              </router-link>
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
  name: "ClientDashboard",
  data() {
    return {
      client_name: "",
      services: [],
      showLogoutModal: false,
      searchQuery: "",
    };
  },
  computed: {
    filteredServices() {
      return this.services.filter(service => {
        return service.service_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
               service.service_description.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    }
  },
  mounted() {
    this.client_name = localStorage.getItem("client_name");
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('http://127.0.0.1:8000/services', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.services = data || [];
        } else {
          console.error("Failed to fetch services:", response.status);
        }
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* Styling specific to this page */
body {
  background-color: #a5f7a0; /* Secondary color */
  font-family: Arial, sans-serif;
  color: #0f130e;
  background-image: url('/7.jpg'); /* Set the background image */
  background-size: cover; /* Ensure the image covers the whole background */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Prevent the image from repeating */
}
.navbar-brand {
  font-weight: bold;
  color: white !important; /* Ensure the brand text is white */
}
.navbar {
  background-color: #AF9B46;
  color: white; /* Primary color */
}

.nav-link, .navbar-brand {
  color: rgb(7, 0, 0) !important;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 12rem;
  height: 18rem;
  margin: 15px;
  text-align: center;
  background-color: #F7B05B; /* Tertiary color */
  color: rgb(7, 7, 7);
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  height: calc(100% - 40px);
  overflow: hidden;
}

.card-header {
  background-color: #AF9B46; /* Primary color */
  color: black;
  font-weight: bold;
}

.modal-content {
  background-color: #AF9B46; /* Tertiary color */
}

.card {
  flex: 0 0 30%;
}

/* Service Cards - Layout */
.row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin: 0 auto;
  max-width: 100%;
}

.card {
  flex: 0 0 12rem;
}

/* Responsive Layout - Adjust the layout for different screen sizes */
@media (max-width: 10991px) {
  .card {
    width: 25rem;
    height: 20rem;
  }
}

@media (max-width: 768px) {
  .card {
    width: 100%;
    height: auto;
  }
}

/* Button Styles */
.btn-book {
  background-color: #fff05a; /* Primary color */
  color: rgb(11, 4, 4);
  border: none;
  width: 100%;
}

.btn-book:hover {
  background-color: #AF9B46; /* Tertiary color */
}

.btn-logout {
  background-color: #AF9B46; /* Tertiary color */
  color: white;
  border: none;
}

.btn-logout:hover {
  background-color: #AF9B46; /* Primary color */
}
</style>
