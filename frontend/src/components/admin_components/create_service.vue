<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar bg-body-tertiary fixed-top" :style="navbarStyle">
      <div class="container-fluid">
        <a class="navbar-brand" href="#" :style="navbarBrandStyle">ComfortCrew</a>
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

          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="p-5" :style="contentStyle">
      <br><br>
      <h1 :style="headerStyle">Create A Service!</h1>

      <!-- Service Creation Form -->
      <form @submit.prevent="create_service">
        <div class="mb-3">
          <label class="form-label" for="service_name">Enter Service Name</label>
          <input class="form-control" type="text" v-model="service_name" required id="service_name" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_time_required">Enter Service Time Required</label>
          <input class="form-control" type="text" v-model="service_time_required" required id="service_time_required" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_description">Enter Service Description</label>
          <input class="form-control" type="text" v-model="service_description" required id="service_description" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_base_price">Enter Service Base Price</label>
          <input class="form-control" type="text" v-model="service_base_price" required id="service_base_price" :style="inputStyle">
        </div>

        <button class="btn btn-primary" type="submit" :style="buttonStyle">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'create_service',
  data() {
    return {
      admin_username: '',
      service_name: '',
      service_time_required: '',
      service_description: '',
      service_base_price: '' // Added base price field
    };
  },
  mounted() {
    const admin_username = localStorage.getItem("admin_username");
    this.admin_username = admin_username;
  },
  methods: {
    async create_service() {
      try {
        const response = await fetch('http://127.0.0.1:8000/create_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            service_name: this.service_name,
            service_time_required: this.service_time_required,
            service_description: this.service_description,
            service_base_price: this.service_base_price // Include base price in request
          }),
        });
        const data = await response.json();
        if (data.message === "Service created successfully") {
          alert("Service created successfully");
        }
      } catch (error) {
        console.log(error);
      }
    }
  },
  computed: {

    navbarStyle() {
      return {
        backgroundColor: '#BFC8AD',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      };
    },
    navbarBrandStyle() {
      return {
        color: '#3f5b3b',
        fontWeight: 'bold',
      };
    },
    offcanvasHeaderStyle() {
      return {
        backgroundColor: '#3f5b3b',
        color: "White"
      };
    },
    contentStyle() {
      return {
        backgroundColor: '#DBCFB0',
        paddingTop: '80px', // To avoid overlap with fixed navbar
        borderRadius: '8px',
      };
    },
    headerStyle() {
      return {
        color: '#2f4f4f',
        textAlign: 'center',
      };
    },
    inputStyle() {
      return {
        backgroundColor: '#DBCFB0',
        borderColor: '#90B494',
      };
    },
    buttonStyle() {
      return {
        backgroundColor: '#3f5b3b',
        borderColor: '#90B494',
        color: 'white',
      };
    },
    logoutButtonStyle() {
      return {
        backgroundColor: '#3f5b3b',
        color: 'white',
      };
    }
  }
};
</script>

<style scoped>
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

/* Add custom styles for the form, buttons, and layout */
.mb-3 .form-control {
  border-radius: 5px;
  padding: 10px;
  border: 1px solid #90B494;
  background-color: #f8f8f8;
}
</style>





<!-- <template>
  <div>
    <nav class="navbar bg-body-tertiary fixed-top" :style="navbarStyle">
      <div class="container-fluid">
        <a class="navbar-brand" href="#" :style="navbarBrandStyle">HandyHub</a>
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

            <router-link to="/admin_logout"><button class="btn btn-primary" :style="logoutButtonStyle">Logout</button></router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="p-5" :style="contentStyle">
      <br><br>
      <h1 :style="headerStyle">Create A Service!</h1>

      <form @submit.prevent="create_service">
        <div class="mb-3">
          <label class="form-label" for="service_name">Enter Service Name</label>
          <input class="form-control" type="text" v-model="service_name" required id="service_name" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_time_required">Enter Service Time Required</label>
          <input class="form-control" type="text" v-model="service_time_required" required id="service_time_required" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_description">Enter Service Description</label>
          <input class="form-control" type="text" v-model="service_description" required id="service_description" :style="inputStyle">
        </div>

        <div class="mb-3">
          <label class="form-label" for="service_base_price">Enter Service Base Price</label>
          <input class="form-control" type="text" v-model="service_base_price" required id="service_base_price" :style="inputStyle">
        </div>

        <button class="btn btn-primary" type="submit" :style="buttonStyle">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'create_service',
  data() {
    return {
      admin_username: '',
      service_name: '',
      service_time_required: '',
      service_description: '',
      service_base_price: '' // Added base price field
    };
  },
  mounted() {
    const admin_username = localStorage.getItem("admin_username");
    this.admin_username = admin_username;
  },
  methods: {
    async create_service() {
      try {
        const response = await fetch('http://127.0.0.1:8000/create_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            service_name: this.service_name,
            service_time_required: this.service_time_required,
            service_description: this.service_description,
            service_base_price: this.service_base_price // Include base price in request
          }),
        });
        const data = await response.json();
        if (data.message === "Service created successfully") {
          alert("Service created successfully");
        }
      } catch (error) {
        console.log(error);
      }
    }
  },
  computed: {
    navbarStyle() {
      return {
        backgroundColor: '#BFC8AD',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      };
    },
    navbarBrandStyle() {
      return {
        color: '#90B494',
        fontWeight: 'bold',
      };
    },
    offcanvasHeaderStyle() {
      return {
        backgroundColor: '#90B494',
      };
    },
    contentStyle() {
      return {
        backgroundColor: '#DBCFB0',
        paddingTop: '80px', // To avoid overlap with fixed navbar
        borderRadius: '8px',
      };
    },
    headerStyle() {
      return {
        color: 'black',
        textAlign: 'center',
      };
    },
    inputStyle() {
      return {
        backgroundColor: '#DBCFB0',
        borderColor: '#90B494',
      };
    },
    buttonStyle() {
      return {
        backgroundColor: '#90B494',
        borderColor: '#90B494',
        color: 'white',
      };
    },
    logoutButtonStyle() {
      return {
        backgroundColor: '#BFC8AD',
        color: 'white',
      };
    }
  }
};
</script>

<style scoped>
/* Add custom styles for the form, buttons, and layout */
.mb-3 .form-control {
  border-radius: 5px;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
</style> -->

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
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">{{admin_username}}</h5>
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
      <h1>Create A Service!</h1>
      <form @submit.prevent="create_service">
        <label class="form-label" for="service_name">Enter Service Name</label>
        <input class="form-control" type="text" v-model="service_name" required id="service_name">
        
        <label class="form-label" for="service_time_required">Enter Service Time Required</label>
        <input class="form-control" type="text" v-model="service_time_required" required id="service_time_required">
        
        <label class="form-label" for="service_description">Enter Service Description</label>
        <input class="form-control" type="text" v-model="service_description" required id="service_description">
        
        <label class="form-label" for="service_base_price">Enter Service Base Price</label>
        <input class="form-control" type="text" v-model="service_base_price" required id="service_base_price">
        <br>
        <button class="btn btn-primary" type="submit">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'create_service',
  data() {
    return {
      admin_username: '',
      service_name: '',
      service_time_required: '',
      service_description: '',
      service_base_price: '' // Added base price field
    };
  },
  mounted() {
    const admin_username = localStorage.getItem("admin_username");
    this.admin_username = admin_username;
  },
  methods: {
    async create_service() {
      try {
        const response = await fetch('http://127.0.0.1:8000/create_service', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("JWTToken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            service_name: this.service_name,
            service_time_required: this.service_time_required,
            service_description: this.service_description,
            service_base_price: this.service_base_price // Include base price in request
          }),
        });
        const data = await response.json();
        if (data.message === "Service created successfully") {
          alert("Service created successfully");
        }
      } catch (error) {
        console.log(error);
      }
    }
  }
};
</script>

<style>
/* Add any custom styling as needed */
</style> -->
