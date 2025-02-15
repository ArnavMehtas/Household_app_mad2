
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

    <br><br><br>

    <div class="container mt-4">
      <h1>Professional Dashboard</h1>
      <div class="my-3">
        <input 
          type="text" 
          v-model="searchQuery" 
          class="form-control" 
          placeholder="Search clients by name..."
        />
      </div>

      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-if="loading" class="text-center">
        <p>Loading pending requests...</p>
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
                <strong>Request Date:</strong> {{ request.service_request_date_of_request }}<br />
                <strong>Remarks:</strong> {{ request.service_request_remarks }}
              </p>
              <button 
                @click="markAsCompleted(request.service_request_id)" 
                class="btn btn-success"
              >
                Completed
              </button>
              <button 
                @click="rejectRequest(request.service_request_id)" 
                class="btn btn-danger ml-2"
              >
                Reject Request
              </button>
            </div>
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
  name: "ProfessionalDashboard",
  data() {
    return {
      requests: [],
      loading: true,
      errorMsg: "",
      searchQuery: "",
      showLogoutModal: false, // Tracks the visibility of the logout confirmation modal
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
      const response = await fetch("http://127.0.0.1:8000/professional_dashboard", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Unable to fetch pending requests.");
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
    async markAsCompleted(serviceRequestId) {
      if (!serviceRequestId) {
        console.error("Invalid service request ID");
        alert("Invalid service request ID");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/service_request/${serviceRequestId}/complete`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
          },
          body: JSON.stringify({
            service_request_date_of_completion: new Date().toISOString(),
            service_request_status: "Completed",
          }),
        });

        if (!response.ok) {
          throw new Error("Unable to update the service request.");
        }

        const updatedRequest = this.requests.find((request) => request.service_request_id === serviceRequestId);
        if (updatedRequest) {
          updatedRequest.service_request_date_of_completion = new Date().toISOString();
          updatedRequest.service_request_status = "Completed";
        }

        alert("Service request marked as completed.");
      } catch (error) {
        this.errorMsg = error.message;
      }
    },
    async rejectRequest(serviceRequestId) {
      if (!serviceRequestId) {
        console.error("Invalid service request ID");
        alert("Invalid service request ID");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/service_request/${serviceRequestId}/reject`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
          },
          body: JSON.stringify({
            service_request_date_of_completion: new Date().toISOString(),
            service_request_status: "Rejected",
          }),
        });

        if (!response.ok) {
          throw new Error("Unable to reject the service request.");
        }

        const updatedRequest = this.requests.find((request) => request.service_request_id === serviceRequestId);
        if (updatedRequest) {
          updatedRequest.service_request_date_of_completion = new Date().toISOString();
          updatedRequest.service_request_status = "Rejected";
        }

        alert("Service request marked as rejected.");
      } catch (error) {
        this.errorMsg = error.message;
      }
    },
    logout() {
      localStorage.removeItem("JWTToken");
      window.location.href = "http://localhost:8080/";
    },
  },
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
  font-weight: bold; /* Make the brand name bold */
}

.navbar .nav-link {
  color: #000 !important; /* Change all navbar links to black */
}

.navbar .nav-link.active {
  color: #1a30f2 !important;
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

.btn-success {
  background-color: #373F47;
  border-color: #373F47;
}

.btn-danger {
  background-color: #C3C9E9;
  border-color: #C3C9E9;
  color: #000;
}

.modal-content {
  background-color: #9989d9;
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


.ml-2 {
  margin-left: 10px;
}
</style>



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
    
    <br><br><br>
    
    <div class="container mt-4">
      <h1>Professional Dashboard</h1>
      <div class="my-3">
        <input 
          type="text" 
          v-model="searchQuery" 
          class="form-control" 
          placeholder="Search clients by name..."
        />
      </div>

      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-if="loading" class="text-center">
        <p>Loading pending requests...</p>
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
                <strong>Request Date:</strong> {{ request.service_request_date_of_request }}<br />
                <strong>Remarks:</strong> {{ request.service_request_remarks }}
              </p>
              <button 
                @click="markAsCompleted(request.service_request_id)" 
                class="btn btn-success"
              >
                Completed
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfessionalDashboard",
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
      return this.requests.filter(request =>
        request.client_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  async created() {
    try {
      const response = await fetch("http://127.0.0.1:8000/professional_dashboard", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Unable to fetch pending requests.");
      }

      const data = await response.json();
      console.log("Fetched data:", data);  // Log the full data here to check the response
      this.requests = data;
    } catch (error) {
      this.errorMsg = error.message;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async markAsCompleted(serviceRequestId) {
      if (!serviceRequestId) {
        console.error("Invalid service request ID");
        alert("Invalid service request ID");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/service_request/${serviceRequestId}/complete`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
          },
          body: JSON.stringify({
            service_request_date_of_completion: new Date().toISOString(),
            service_request_status: "Completed",
          }),
        });

        if (!response.ok) {
          throw new Error("Unable to update the service request.");
        }

        // Find the request in the local state and update it
        const updatedRequest = this.requests.find(request => request.service_request_id === serviceRequestId);
        if (updatedRequest) {
          updatedRequest.service_request_date_of_completion = new Date().toISOString();
          updatedRequest.service_request_status = "Completed";
        }

        alert("Service request marked as completed.");
      } catch (error) {
        this.errorMsg = error.message;
      }
    },
  },
};
</script>

<style>
.card {
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style> -->
