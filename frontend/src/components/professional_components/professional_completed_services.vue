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
                  <router-link to="/client_reviews" class="nav-link active">Your reviews</router-link>
                </li>
                
                <li class="nav-item">
                  <router-link to="/professional_profile" class="nav-link active">Profile</router-link>
                </li>
              </ul>
              <router-link to="/client_logout">
                <button class="btn btn-primary">Logout</button>
              </router-link>
            </div>
          </div>
        </div>
      </nav>
  
      <br><br><br>
  
      <div class="container mt-4">
        <h1>Completed Service Requests</h1>
  
        <div class="my-3">
          <input 
            type="text" 
            v-model="searchQuery" 
            class="form-control" 
            placeholder="Search completed services by client name..."
          />
        </div>
  
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <div v-if="loading" class="text-center">
          <p>Loading completed requests...</p>
        </div>
  
        <div class="row">
          <div
            v-for="(request, index) in filteredRequests"
            :key="index"
            class="col-md-4 mb-4"
          >
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ request.client_name }}</h5>
                <p class="card-text">
                  <strong>Service Start Date:</strong> {{ request.service_request_date_of_request }}<br />
                  <strong>Service End Date:</strong> {{ request.service_request_date_of_completion }}<br />
                  <strong>Remarks:</strong> {{ request.service_request_remarks }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CompletedServices",
    data() {
      return {
        completedRequests: [],
        loading: true,
        errorMsg: "",
        searchQuery: "", // For filtering completed services
      };
    },
    computed: {
      // Filtered requests based on search query
      filteredRequests() {
        return this.completedRequests.filter(request =>
          request.client_name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
    },
    async created() {
      try {
        const response = await fetch("http://127.0.0.1:8000/completed_services", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
          },
        });
  
        if (!response.ok) {
          throw new Error("Unable to fetch completed requests.");
        }
  
        const data = await response.json();
        this.completedRequests = data;
      } catch (error) {
        this.errorMsg = error.message;
      } finally {
        this.loading = false;
      }
    },
  };
  </script>
  
  <style>
  .card {
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  </style>
   -->
   <template>
    <div>
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
                  <router-link to="/client_reviews" class="nav-link active">Your reviews</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/professional_profile" class="nav-link active">Profile</router-link>
                </li>
              </ul>
              <button @click="logout" class="btn btn-primary">Logout</button>
            </div>
          </div>
        </div>
      </nav>
  
      <br><br><br>
  
      <div class="container mt-4">
        <h1>Completed Service Requests</h1>
  
        <!-- Search bar to filter by client name -->
        <div class="my-3">
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            placeholder="Search completed services by client name..."
          />
        </div>
  
        <!-- Error handling -->
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <div v-if="loading" class="text-center">
          <p>Loading completed requests...</p>
        </div>
  
        <!-- Completed service cards -->
        <div class="row">
          <div
            v-for="(request, index) in filteredRequests"
            :key="index"
            class="col-md-4 mb-4"
          >
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ request.client_name }}</h5>
                <p class="card-text">
                  <strong>Service Start Date:</strong> {{ request.service_request_date_of_request }}<br />
                  <strong>Service End Date:</strong> {{ request.service_request_date_of_completion }}<br />
                  <strong>Remarks:</strong> {{ request.service_request_remarks }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CompletedServicesDashboard",
    data() {
      return {
        requests: [],
        loading: true,
        errorMsg: "",
        searchQuery: "",
      };
    },
    computed: {
      filteredRequests() {
        return this.requests.filter((request) =>
          request.client_name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
    },
    async created() {
      try {
        const response = await fetch("http://127.0.0.1:8000/completed_services", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
          },
        });
  
        if (!response.ok) {
          throw new Error("Unable to fetch completed services.");
        }
  
        const data = await response.json();
        this.requests = data;
      } catch (error) {
        this.errorMsg = error.message;
      } finally {
        this.loading = false;
      }
    },
    methods: {
      logout() {
        localStorage.removeItem("JWTToken");
        window.location.href = "http://localhost:8080/";
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styling for the Completed Services Dashboard Page */
  body {
    background-color: #C3C9E9;
  }
  
  .navbar {
    background-color: #AAABBC !important;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .navbar .navbar-brand {
    color: #000;
    font-weight: bold; /* Make the brand name bold */
  }
  
  .navbar .nav-link {
    color: #000 !important; /* Change all navbar links to black */
  }
  
  .navbar .nav-link.active {
    color: #010101 !important;
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
  
  h1 {
    color: #373F47;
  }
  
  .input-group input {
    background-color: #F4F4F4;
  }
  
  .btn-primary {
    background-color: #373F47;
    border-color: #373F47;
  }
  
  .alert-danger {
    background-color: #F8D7DA;
    color: #721C24;
  }
  
  .navbar .nav-link {
    color: #000 !important; /* Change link text color to black */
  }
  
  .navbar .nav-link.active {
    color: #1b1212 !important; /* Keep the active link white if you want */
  }
  
  .navbar .navbar-toggler-icon {
    color: #000 !important; /* Ensure the hamburger icon is also visible */
  }
  </style>
  