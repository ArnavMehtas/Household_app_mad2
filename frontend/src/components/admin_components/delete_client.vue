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
                <br><br>
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
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Client Management</a>
                  <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" to="/delete_client">Delete Clients</router-link></li>
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
  <br><br>
      <div class="p-5">
        <h1>{{ admin_username }}'s Dashboard</h1>
        
        <div v-for="client in clients" :key="client.client_id" class="mb-4">
          <div class="card">
            <div class="card-header">{{ client.client_name }}</div>
            <div class="card-body">
              <p>{{ client.client_address }}</p>
              <p>{{ client.client_phone }}</p>
              <h5>Services Taken</h5>
              <div v-if="client.services.length" class="card" style="width: 18rem;">
                <ul class="list-group list-group-flush">
                  <li v-for="service in client.services" :key="service.service_id" class="list-group-item">
                    Service: {{ service.service_name }} <br />
                    Status: {{ service.service_request_status }}
                  </li>
                </ul>
              </div>
              <div v-else>
                <p>No services taken by this client.</p>
              </div>
            </div>
            <button @click="delete_client(client.client_id)" class="btn btn-danger mt-3">Delete Client</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'delete_client',
    data() {
      return {
        admin_username: '',
        clients: []
      };
    },
    mounted() {
      this.admin_username = localStorage.getItem("admin_username");
      this.fetch_data();
    },
    methods: {
      async fetch_data() {
        try {
          const response = await fetch('http://127.0.0.1:8000/admin_clients', {
            method: 'GET',
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
              'Content-Type': 'application/json',
            }
          });
          const data = await response.json();
          this.clients = data; // Assuming the API returns the clients with their services
        } catch (error) {
          console.error(error);
        }
      },

      async delete_client(client_id) {
        try {
          const response = await fetch('http://127.0.0.1:8000/delete_client', {
            method: 'DELETE',
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ client_id })
          });
          const data = await response.json();
          if (data.message === "Client deleted successfully") {
            alert("Client deleted successfully");
            this.fetch_data();  // Refresh the client data
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
  </style>
   -->
  

   <template>
    <div>
      <nav class="navbar bg-body-tertiary fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="#"><strong>ComfortCrew</strong></a>
          <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
            <div class="offcanvas-header">
              <br><br>
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
              <li class="nav-item">
                <router-link to="/summary" class="nav-link active" aria-current="page">Summary</router-link>
              </li>
            </ul>
          </div>
          </div>
        </div>
      </nav>
  
      <br><br>
  
      <div class="p-5">
        <h1 class="dashboard-title">{{ admin_username }}'s Dashboard</h1>

        <h3> Available Clients: </h3>
  
        <div v-for="client in clients" :key="client.client_id" class="mb-4 client-card">
          <div class="card">
            <div class="card-header client-header">{{ client.client_name }}</div>
            <div class="card-body">
              <p>City : {{ client.client_address }}</p>
              <p>Phone :{{ client.client_phone }}</p>
              <h5>Services Taken</h5>
              <div v-if="client.services.length" class="card service-card" style="width: 18rem;">
                <ul class="list-group list-group-flush">
                  <li v-for="service in client.services" :key="service.service_id" class="list-group-item">
                    Service: {{ service.service_name }} <br />
                    Status: {{ service.service_request_status }}
                  </li>
                </ul>
              </div>
              <div v-else>
                <p>No services taken by this client.</p>
              </div>
            </div>
            <button @click="delete_client(client.client_id)" class="btn btn-danger mt-3 delete-button">Permanently Ban Client</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'delete_client',
    data() {
      return {
        admin_username: '',
        clients: []
      };
    },
    mounted() {
      this.admin_username = localStorage.getItem("admin_username");
      this.fetch_data();
    },
    methods: {
      async fetch_data() {
        try {
          const response = await fetch('http://127.0.0.1:8000/admin_clients', {
            method: 'GET',
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
              'Content-Type': 'application/json',
            }
          });
          const data = await response.json();
          this.clients = data; // Assuming the API returns the clients with their services
        } catch (error) {
          console.error(error);
        }
      },
  
      async delete_client(client_id) {
        try {
          const response = await fetch('http://127.0.0.1:8000/delete_client', {
            method: 'DELETE',
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ client_id })
          });
          const data = await response.json();
          if (data.message === "Client deleted successfully") {
            alert("Client deleted successfully");
            this.fetch_data();  // Refresh the client data
          }
        } catch (error) {
          console.error(error);
        }
      }
    }
  };
  </script>
  
  <style>
  /* Main Color Palette */
  :root {
    --primary-color: #BFC8AD;
    --secondary-color: #90B494;
    --tertiary-color: #DBCFB0;
  }
  
  /* Navbar */
  .navbar {
    background-color: var(--primary-color);
  }
  
  .navbar-brand {
    color: white;
    font-weight: bold;
  }
  
  .navbar-toggler-icon {
    background-color: white;
  }
  
  .navbar-nav .nav-link {
    color: rgb(46, 14, 14);
  }
  
  .navbar-nav .nav-link.active {
    color: var(--secondary-color);
  }
  
  /* Dashboard Title */
  .dashboard-title {
    color: var(--primary-color);
    font-size: 2rem;
    margin-bottom: 20px;
  }
  
  /* Client Card */
  .client-card .card {
    border-radius: 10px;
    border: none;
    background-color: var(--tertiary-color);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .client-header {
    background-color: var(--secondary-color);
    color: white;
    font-weight: bold;
  }
  
  .card-body p {
    font-size: 1rem;
    color: #333;
  }
  
  /* Service Card */
  .service-card {
    background-color: var(--primary-color);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  /* Button */
  .delete-button {
    background-color: var(--secondary-color);
    border: none;
    color: white;
    font-weight: bold;
    border-radius: 5px;
    transition: background-color 0.3s;
  }
  
  
.navbar-brand {
  color: black; /* Set the text color to black */
  font-weight: bold;
}
  .delete-button:hover {
    background-color: var(--primary-color);
  }
  
  .delete-button:focus {
    outline: none;
  }
  
  /* Add some spacing */
  .mb-4 {
    margin-bottom: 20px;
  }
  
  .p-5 {
    padding: 30px;
  }
  </style>
  