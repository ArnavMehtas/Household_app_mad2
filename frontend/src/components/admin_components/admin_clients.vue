<template>
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
            <router-link to="/admin_logout"><button class="btn btn-primary">Logout</button></router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="p-5">
      <h1>Clients Overview</h1>
      <!-- Loop through each client to display their details and associated services -->
      <div v-for="client in clients" :key="client.client_id" class="mb-4">
        <div class="card">
          <div class="card-header" style="background-color: #DBCFB0;">
            {{ client.client_name || 'Unnamed Client' }}
          </div>
          <div class="card-body" style="background-color: #BFC8AD;">
            <p>Address: {{ client.client_address || 'N/A' }}</p>
            <p>Phone: {{ client.client_phone || 'N/A' }}</p>
            <h5>Services Taken</h5>
            <div v-if="client.services.length > 0" class="card" style="width: 18rem; background-color: #90B494;">
              <ul class="list-group list-group-flush">
                <li v-for="service in client.services" :key="service.service_id" class="list-group-item">
                  Service: {{ service.service_name }} <br />
                  Status: {{ service.service_request_status }}
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No services taken.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'admin_client',
  data() {
    return {
      clients: [], // List of all clients with their services
      admin_username: 'Admin' // You can dynamically set this from localStorage or backend
    };
  },
  mounted() {
    this.fetch_client_data();
  },
  methods: {
    async fetch_client_data() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin_clients', {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });

        // Check if the response is successful (status 200)
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Fetched client data:", data);  // Log the data structure

        // Ensure 'clients' exists and is an array, fallback to empty array if not
        if (data && Array.isArray(data)) {
          this.clients = data.map(client => ({
            ...client,
            services: client.services || []  // Default to an empty array if 'services' is undefined
          }));
        } else {
          console.error("Unexpected data structure. Expected an array of clients.", data);
          this.clients = [];  // Fallback to an empty array if data structure is incorrect
        }
      } catch (error) {
        console.error('Error fetching client data:', error);
        alert('An error occurred while fetching the data. Please check the network and try again later.');
      }
    }
  }
};
</script>

<style>
/* Apply color scheme */
.card-header {
  background-color: #DBCFB0; /* Light beige */
}

.card-body {
  background-color: #BFC8AD; /* Soft olive */
}

.card {
  border: 1px solid #90B494; /* Greenish border for the cards */
}

.list-group-item {
  background-color: #F8F8F8; /* Light background for list items */
}

button {
  background-color: #90B494; /* Greenish color */
  color: white;
}

button:hover {
  background-color: #3f5b3b; /* Darker green on hover */
}
</style>
