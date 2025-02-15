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
      <h1>Ban Professionals</h1>
      <br>
      <!-- Iterate over serviceRequests to display professionals independently -->
      <div class="professionals-container d-flex flex-wrap">
        <div v-for="request in allProfessionals" :key="request.professional_id" class="mb-4 card-container">
          <div class="card" :style="cardStyle">
            <div class="card-header" :style="cardHeaderStyle">
              {{ request.professional_name }}
            </div>
            <div class="card-body">
              <p><strong>Rating:</strong> {{ request.professional_rating }}</p>
              <p><strong>Experience:</strong> {{ request.professional_experience }} years</p>
              <p><strong>Description:</strong> {{ request.professional_description }}</p>
            </div>
            <button @click="delete_professional(request.professional_id)" class="btn btn-danger mt-3">Permanently Ban Personnel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'delete_professionals',
  data() {
    return {
      admin_username: '',
      allProfessionals: []
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

        // Check if the response contains 'services'
        if (data.services && Array.isArray(data.services)) {
          const allProfessionals = [];

          // Iterate through each service in 'services' to collect associated professionals
          data.services.forEach(service => {
            service.professionals.forEach(professional => {
              allProfessionals.push({
                professional_id: professional.professional_id,
                professional_name: professional.professional_name,
                professional_rating: professional.professional_rating,
                professional_experience: professional.professional_experience,
                professional_description: professional.professional_description,
              });
            });
          });

          // Assign the professional list to the component data
          this.allProfessionals = allProfessionals;
        } else {
          console.error('Services data is not available or is in an unexpected format.');
        }

      } catch (error) {
        console.log(error);
      }
    },

    async delete_professional(professional_id) {
      try {
        const response = await fetch('http://127.0.0.1:8000/delete_professional', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ professional_id })
        });
        const data = await response.json();
        
        if (data.message === "Personnel Banned successfully") {
          alert("Personnel Banned successfully");
        }
      } catch (error) {
        console.error(error);
      }
    }
  },

  computed: {
    cardStyle() {
      return {
        width: '18rem',
        marginBottom: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        backgroundColor: '#DBCDB0' // Applying the light olive color for card background
      };
    },
    cardHeaderStyle() {
      return {
        backgroundColor: '#BFC8AD', // Soft Green for card header
        fontWeight: 'bold',
        fontSize: '1.1rem',
        padding: '10px',
        borderRadius: '8px 8px 0 0',
        color: '#3f5b3b' // Dark Green for text
      };
    }
  }
};
</script>

<style scoped>
.professionals-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* space between cards */
}

.card-container {
  display: flex;
  justify-content: center;
  flex: 1 1 18rem; /* each card will take at least 18rem, and space will be evenly distributed */
}

.card-body p {
  font-size: 1rem;
  color: #3f5b3b; /* Dark Green for text inside cards */
}

button.btn-danger {
  background-color: #3f5b3b; /* Dark Green for the Ban button */
  border: none;
}
button.btn-danger:hover {
  background-color: #90B494; /* Muted Green for hover effect */
}
</style>


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
              </a><ul class="dropdown-menu">
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

      <div v-for="request in allProfessionals" :key="request.professional_id" class="mb-4">
        <div class="card" :style="cardStyle">
          <div class="card-header" :style="cardHeaderStyle">
            {{ request.professional_name }}
          </div>
          <div class="card-body">
            <p><strong>Rating:</strong> {{ request.professional_rating }}</p>
            <p><strong>Experience:</strong> {{ request.professional_experience }} years</p>
            <p><strong>Description:</strong> {{ request.professional_description }}</p>
          </div>
          <button @click="delete_professional(request.professional_id)" class="btn btn-danger mt-3">Ban Personnel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'delete_professionals',
  data() {
    return {
      admin_username: '',
      allProfessionals: []
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
      method: 'GET',  // Changed to GET, since your backend expects GET for the /admin_dashboard route
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
        'Content-Type': 'application/json',
      }
    });
    const data = await response.json();
    console.log(data);

    // Check if the response contains 'services'
    if (data.services && Array.isArray(data.services)) {
      const allProfessionals = [];

      // Iterate through each service in 'services' to collect associated professionals
      data.services.forEach(service => {
        service.professionals.forEach(professional => {
          allProfessionals.push({
            professional_id: professional.professional_id,
            professional_name: professional.professional_name,
            professional_rating: professional.professional_rating,
            professional_experience: professional.professional_experience,
            professional_description: professional.professional_description,
          });
        });
      });

      // Assign the professional list to the component data
      this.allProfessionals = allProfessionals;
    } else {
      console.error('Services data is not available or is in an unexpected format.');
    }

  } catch (error) {
    console.log(error);
  }
}
,

    async delete_professional(professional_id) {
      try {
        const response = await fetch('http://127.0.0.1:8000/delete_professional', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ professional_id })
        });
        const data = await response.json();
        
        // Corrected response message condition
        if (data.message === "Personnel Banned successfully") {
          alert("Personnel Banned successfully");
        }
      } catch (error) {
        console.error(error);
      }
    }
  },

  computed: {
    // Styling for the professional cards
    cardStyle() {
      return {
        width: '18rem',
        marginBottom: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      };
    },
    cardHeaderStyle() {
      return {
        backgroundColor: '#f8f9fa',
        fontWeight: 'bold',
        fontSize: '1.1rem',
        padding: '10px',
        borderRadius: '8px 8px 0 0',
        color: '#333'
      };
    }
  }
};
</script>

<style scoped>
.card-body p {
  font-size: 1rem;
  color: #555;
}
</style>
 -->


<!-- <template>
  <div>
    <h1>Manage Professionals</h1>
    <div v-for="professional in professionals" :key="professional.professional_id" class="card mb-3">
      <div class="card-header">
        {{ professional.professional_name }}
      </div>
      <div class="card-body">
        <p>{{ professional.professional_description }}</p>
        <p>Experience: {{ professional.professional_experience }} years</p>
        <p>Rating: {{ professional.professional_rating }}</p>
        <button class="btn btn-danger" @click="deleteProfessional(professional.professional_id)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminProfessionalManagement",
  data() {
    return {
      professionals: [],
    };
  },
  mounted() {
    this.fetchProfessionals();
  },
  methods: {
    async fetchProfessionals() {
      try {
        const response = await fetch('http://127.0.0.1:8000/get_professionals_list', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        this.professionals = data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    async deleteProfessional(id) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/delete_professional/${id}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.professionals = this.professionals.filter(prof => prof.professional_id !== id);
          alert(data.message);
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error("Error deleting professional:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Add your custom styling here */
</style> -->
