<template>
  <div>
    <nav class="navbar bg-body-tertiary fixed-top" :style="navbarStyle">
      <div class="container-fluid">
        <a class="navbar-brand" href="#" :style="navbarBrandStyle"><strong>ComfortCrew</strong></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header" :style="offcanvasHeaderStyle">
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
                  <li><router-link class="dropdown-item" to="/create_service">Create Service</router-link></li>
                  <li><router-link class="dropdown-item" to="/delete_service">Delete Service</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Professional Management
                </a>
                <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin_professionals">View Professionals</router-link></li>
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
    <br><br>
    <div class="p-5" :style="contentStyle">
      <h1>Professionals</h1>
      <br><br>

      <!-- Search Bar -->
      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search by name"
          :style="searchStyle"
        />
      </div>

      <div class="mb-4">
        <label for="experience-sort" class="form-label" :style="labelStyle"><strong>Sort by Experience</strong></label>
        <select v-model="sortByExperience" id="experience-sort" class="form-select" :style="selectStyle">
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>

      <!-- Professionals List -->
      <div class="professionals-container" style="display: flex; flex-wrap: wrap; gap: 20px;">
        <div v-for="professional in filteredProfessionals" :key="professional.professional_id" class="card" :style="cardStyle">
          <div class="card-header" :style="cardHeaderStyle">
            {{ professional.professional_name }}
          </div>
          <div class="card-body">
            <p><strong>Rating:</strong> {{ professional.professional_rating }}</p>
            <p><strong>Experience:</strong> {{ professional.professional_experience }} years</p>
            <p><strong>Description:</strong> {{ professional.professional_description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'admin_professionals',
  data() {
    return {
      admin_username: '',
      professionals: [],
      searchQuery: '', // For searching by name
      sortByExperience: 'asc', // Sort experience (ascending or descending)
    };
  },
  mounted() {
    const admin_username = localStorage.getItem("admin_username");
    this.admin_username = admin_username;
    this.fetchProfessionals();
  },
  methods: {
    async fetchProfessionals() {
      try {
        const response = await fetch('http://127.0.0.1:8000/professionals', {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        console.log(data);

        // Assign fetched data to professionals
        this.professionals = data.professionals;

      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    }
  },
  computed: {


    labelStyle() {
    return {
      display: 'block',    // Ensure the label is a block element
      textAlign: 'center', // Center the text within the label
      marginBottom: '10px', // Add some space below the label
    };
  },
    // Filter professionals based on search query
    filteredProfessionals() {
      let filtered = this.professionals.filter(professional =>
        professional.professional_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );

      // Sort professionals by experience
      if (this.sortByExperience === 'asc') {
        filtered.sort((a, b) => a.professional_experience - b.professional_experience);
      } else {
        filtered.sort((a, b) => b.professional_experience - a.professional_experience);
      }

      return filtered;
    },

    // Styling for search bar
    searchStyle() {
      return {
        width: '300px',
        padding: '10px',
        margin: '0 auto',
        borderRadius: '8px',
      };
    },

    // Styling for sorting select
    selectStyle() {
      return {
        width: '200px',
        padding: '10px',
        margin: '0 auto',
        borderRadius: '8px',
      };
    },

    // Styling for the professional cards
    cardStyle() {
      return {
        width: '18rem',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        backgroundColor: '#DBCFB0', // Light beige background color for card
      };
    },
    cardHeaderStyle() {
      return {
        backgroundColor: '#BFC8AD', // Soft olive color for header
        fontWeight: 'bold',
        fontSize: '1.1rem',
        padding: '10px',
        borderRadius: '8px 8px 0 0',
        color: '#333'
      };
    },
    navbarStyle() {
      return {
        backgroundColor: '#90B494', // Muted green background for the navbar
      };
    },
    navbarBrandStyle() {
      return {
        color: 'black', // White text color for navbar brand
      };
    },
    offcanvasHeaderStyle() {
      return {
        backgroundColor: '#90B494', // Muted green for offcanvas header
        color: '#fff',
      };
    },
    logoutButtonStyle() {
      return {
        backgroundColor: '#BFC8AD', // Olive color for the logout button
        borderColor: '#BFC8AD', // Border matches button color
      };
    },
    contentStyle() {
      return {
        backgroundColor: '#DBCFB0', // Light beige background for content area
        padding: '20px',
        borderRadius: '8px',
      };
    }
  }
};
</script>
