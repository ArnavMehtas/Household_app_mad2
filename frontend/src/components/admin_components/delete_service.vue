<!-- <template>
    <div>
      <nav class="navbar bg-body-tertiary fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">The Helper!</a>
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
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Service Management</a>
                  <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" to="/create_service">Create Service</router-link></li>
                    <li><router-link class="dropdown-item" to="/delete_service">Delete Service</router-link></li>
                  </ul>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Professional Management</a>
                  <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin_professionals">View Professionals </router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link></li>
                </ul>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Client Management</a>
                  <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <router-link to="/summary" class="nav-link active" aria-current="page">Summary</router-link>
                </li>
              </ul>
              <router-link to="/admin_logout"><button class="btn btn-primary">Logout</button></router-link>
            </div>
          </div>
        </div>
      </nav>
      <div class="p-5">
        <h1>{{ admin_username }}'s Dashboard</h1>
        <div v-for="service in services" :key="service.service_id" class="mb-4">
          <div class="card">
            <div class="card-header">{{ service.service_name }}</div>
            <div class="card-body">
              <p>{{ service.service_description }}</p>
              <p>Time Required: {{ service.service_time_required }} hrs</p>
              <p>Base Price: ${{ service.service_base_price }}</p>
              <h5>Professionals</h5>
              <div v-if="serviceRequests[service.service_id]" class="card" style="width: 18rem;">
                <ul class="list-group list-group-flush">
                  <li v-for="request in serviceRequests[service.service_id]" :key="request.professional_id" class="list-group-item">
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
            <button @click="delete_service(service.service_id)" class="btn btn-danger mt-3">Abort Service</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'delete_service',
  data() {
    return {
      admin_username: '',
      services: [],
      serviceRequests: {}
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
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        this.services = data.services;
        this.serviceRequests = {};
        data.serviceRequests.forEach((request) => {
          const serviceId = request.service_id;
          if (!this.serviceRequests[serviceId]) this.serviceRequests[serviceId] = [];
          this.serviceRequests[serviceId].push({
            professional_id: request.professional_id,
            professional_name: request.professional_name,
            professional_rating: request.professional_rating,
            professional_experience: request.professional_experience
          });
        });
      } catch (error) {
        console.error(error);
      }
    },
    
    async delete_service(service_id) {
      try {
        const response = await fetch('http://127.0.0.1:8000/delete_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ service_id })
        });
        const data = await response.json();
        if (data.message === "Service deleted successfully") {
          alert("Service Aborted successfully");
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
/* Add any custom styling as needed */
</style> -->



































<!-- 
<template>
  <div>
    <nav class="navbar bg-body-tertiary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand"  href="#">HandyHub</a>
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
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Service Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/create_service">Create Service</router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_service">Delete Service</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Professional Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin_professionals">View Professionals </router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Client Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link></li>
                </ul>
              </li>
              <li class="nav-item">
                <router-link to="/summary" class="nav-link active" aria-current="page">Summary</router-link>
              </li>
            </ul>
            <router-link to="/admin_logout"><button class="btn btn-primary">Logout</button></router-link>
          </div>
        </div>
      </div>
    </nav>
    <div class="p-5">
      <br><br>
      <h1 class="text-center">Delete Services</h1>
      <div v-for="service in services" :key="service.service_id" class="mb-4">
        <div class="card custom-card">
          <div class="card-header custom-card-header">{{ service.service_name }}</div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Time Required: {{ service.service_time_required }} hrs</p>
            <p>Base Price: ${{ service.service_base_price }}</p>
          </div>
          <button @click="delete_service(service.service_id)" class="btn btn-danger mt-3">Abort Service</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'delete_service',
  data() {
    return {
      admin_username: '',
      services: [],
      serviceRequests: {}
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
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        this.services = data.services;
      } catch (error) {
        console.error(error);
      }
    },
    
    async delete_service(service_id) {
      try {
        const response = await fetch('http://127.0.0.1:8000/delete_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ service_id })
        });
        const data = await response.json();
        if (data.message === "Service deleted successfully") {
          alert("Service Aborted successfully");
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
/* Custom Styles using the provided color palette */
body {
  background-color: #BFC8AD; /* Pale Greenish */
  font-family: Arial, sans-serif;
}

.navbar {
  background-color: #90B494; /* Muted Green */
}

.navbar-brand {
  color: rgb(74, 10, 10);
  font-weight: bold;
}

.navbar-nav .nav-link {
  color: rgb(44, 36, 36);
}

.navbar-nav .nav-link:hover {
  background-color: #DBCFB0; /* Light Cream */
}

.card {
  background-color: #DBCFB0;
  border: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #90B494;
  color: white;
  font-weight: bold;
}

.card-body {
  background-color: #F8F8F8;
}

.card-body p {
  color: #333;
}

.custom-card-header {
  background-color: #90B494;
  color: rgb(50, 42, 42);
}

.custom-card {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.navbar-brand {
  color: black; /* Set the text color to black */
  font-weight: bold;
}


h1 {
  color: #196722;
  margin-bottom: 30px;
}

.btn-primary {
  background-color: #90B494;
  border: none;
}

.btn-danger {
  background-color: #FF4C4C;
  border: none;
}

.btn-primary:hover {
  background-color: #BFC8AD;
}

.btn-danger:hover {
  background-color: #D65A5A;
}
</style> -->










<template>
  <div>
    <nav class="navbar">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">ComfortCrew</a>
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
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Service Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/create_service">Create Service</router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_service">Delete Service</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Professional Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin_professionals">View Professionals</router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_professional">BAN Professionals</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Client Management</a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/ban_client">Ban Clients</router-link></li>
                </ul>
              </li>
              <li class="nav-item">
                <router-link to="/summary" class="nav-link active" aria-current="page">Summary</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
    <div class="p-5">
      <br><br>
      <h1 class="text-center">Delete Services</h1>
      <div v-for="service in services" :key="service.service_id" class="mb-4">
        <div class="card">
          <div class="card-header">{{ service.service_name }}</div>
          <div class="card-body">
            <p>{{ service.service_description }}</p>
            <p>Time Required: {{ service.service_time_required }} hrs</p>
            <p>Base Price: ${{ service.service_base_price }}</p>
          </div>
          <button @click="delete_service(service.service_id)" class="btn btn-danger mt-3">Abort Service</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'delete_service',
  data() {
    return {
      admin_username: '',
      services: [],
      serviceRequests: {}
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
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        this.services = data.services;
      } catch (error) {
        console.error(error);
      }
    },
    
    async delete_service(service_id) {
      try {
        const response = await fetch('http://127.0.0.1:8000/delete_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ service_id })
        });
        const data = await response.json();
        if (data.message === "Service deleted successfully") {
          alert("Service Aborted successfully");
        }
      } catch (error) {
        console.error(error);
      }
    }
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
</style>
