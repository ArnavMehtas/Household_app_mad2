
<template>
    <div>
      <!-- Navbar -->
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
              </li>
            </ul>
          </div>
          </div>
        </div>
      </nav>
  
      <!-- Service Requests Content -->
      <div class="container mt-5 pt-5">
        <h2 class="text-center mb-4">Service Requests</h2>
        <table class="table table-striped">
          <thead class="thead-light">
            <tr>
              <th>Request ID</th>
              <th>Client Name</th>
              <th>Service Name</th>
              <th>Professional Name</th>
              <th>Status</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.service_request_id">
              <td>{{ request.service_request_id }}</td>
              <td>{{ request.client_name }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.professional_name }}</td>
              <td>{{ request.service_request_status }}</td>
              <td>{{ request.service_request_remarks }}</td>
            </tr>
          </tbody>
        </table>
  
        <!-- Review Table -->
        <h2 class="text-center mb-4">Reviews</h2>
        <table class="table table-striped">
          <thead class="thead-light">
            <tr>
              <th>Review ID</th>
              <th>Client Name</th>
              <th>Professional Name</th>
              <th>Rating</th>
              <th>Comment</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="review in reviews" :key="review.review_id">
              <td>{{ review.review_id }}</td>
              <td>{{ review.client_name }}</td>
              <td>{{ review.professional_name }}</td>
              <td>{{ review.review_rating }}</td>
              <td>{{ review.review_comment }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Logout Modal -->
      <!-- ... -->
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        serviceRequests: [],
        reviews: [], // Added for reviews
        showLogoutModal: false,
        admin_username: "Admin", // or fetch from local storage if needed
      };
    },
    mounted() {
      this.fetchServiceRequests();
      this.fetchReviews(); // Fetch reviews data on mount
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await fetch('http://localhost:8000/service_requests');
          const data = await response.json();
          this.serviceRequests = data;
        } catch (error) {
          console.error('Error fetching service requests:', error);
        }
      },
      async fetchReviews() {
        try {
          const response = await fetch('http://localhost:8000/reviews');
          const data = await response.json();
          this.reviews = data;
        } catch (error) {
          console.error('Error fetching reviews:', error);
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
  /* Global styling */
  body {
    background-color: #DBCDB0; /* Light beige background */
    font-family: Arial, sans-serif;
  }
  
  h2 {
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
  
  .table {
    background-color: #FFF;
  }
  
  .table-striped tbody tr:nth-child(odd) {
    background-color: #f2f2f2;
  }
  
  /* Additional specific styling for tables */
  .table th,
  .table td {
    vertical-align: middle;
    text-align: center;
  }
  </style>
  











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
          </div>
          </div>
        </div>
      </nav>
  
      <div class="container mt-5 pt-5">
        <h2 class="text-center mb-4">Service Requests</h2>
        <table class="table table-striped">
          <thead class="thead-light">
            <tr>
              <th>Request ID</th>
              <th>Client Name</th>
              <th>Service Name</th>
              <th>Professional Name</th>
              <th>Status</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.service_request_id">
              <td>{{ request.service_request_id }}</td>
              <td>{{ request.client_name }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.professional_name }}</td>
              <td>{{ request.service_request_status }}</td>
              <td>{{ request.service_request_remarks }}</td>
            </tr>
          </tbody>
        </table>
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
    data() {
      return {
        serviceRequests: [],
        showLogoutModal: false,
        admin_username: "Admin", // or fetch from local storage if needed
      };
    },
    mounted() {
      this.fetchServiceRequests();
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await fetch('http://localhost:8000/service_requests');
          const data = await response.json();
          this.serviceRequests = data;
        } catch (error) {
          console.error('Error fetching service requests:', error);
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
  /* Global styling */
  body {
    background-color: #DBCDB0; /* Light beige background */
    font-family: Arial, sans-serif;
  }
  
  /* Navbar styling */
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
  
  /* Table styling */
  .table {
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .table-striped tbody tr:nth-of-type(odd) {
    background-color: #f0f8f0; /* Light greenish rows */
  }
  
  thead {
    background-color: #90B494; /* Soft green */
    color: white;
    font-weight: bold;
  }
  
  th, td {
    padding: 12px;
    text-align: center;
  }
  
  td {
    font-size: 1rem;
    color: #2f4f4f;
  }
  
  /* Logout Modal */
  .modal-content {
    background-color: #FFFAF0; /* Floral white */
  }
  
  button {
    background-color: #3f5b3b;
    color: white;
  }
  
  button:hover {
    background-color: #2f4f4f;
  }
  </style> -->
  
<!-- <template>
    <div>
      <h2>Service Requests</h2>
      <table>
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Client Name</th>
            <th>Service Name</th>
            <th>Professional Name</th>
            <th>Status</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.service_request_id">
            <td>{{ request.service_request_id }}</td>
            <td>{{ request.client_name }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.professional_name }}</td>
            <td>{{ request.service_request_status }}</td>
            <td>{{ request.service_request_remarks }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        serviceRequests: [],
      };
    },
    mounted() {
      this.fetchServiceRequests();
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await fetch('http://localhost:8000/service_requests');
          const data = await response.json();
          this.serviceRequests = data;
        } catch (error) {
          console.error('Error fetching service requests:', error);
        }
      },
    },
  };
  </script>
   -->