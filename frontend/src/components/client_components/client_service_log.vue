<!-- <template>
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
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
              Explore
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
                <router-link to="/client_dashboard" class="nav-link active">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/service_log" class="nav-link active">My Services</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <br><br><br>
    <h1 class="text-center my-4">My Service Log</h1>

    <div class="d-flex justify-content-center mb-3">
      <input
        v-model="searchQuery"
        type="text"
        class="form-control w-50"
        placeholder="Search by name or service type"
      />
      <select v-model="statusFilter" class="form-select w-auto ms-2">
        <option value="">All Statuses</option>
        <option value="Completed">Completed</option>
        <option value="Rejected">Rejected</option>
        <option value="pending">Pending</option>
      </select>
    </div>

    <div class="row">
      <div
        v-for="(log, index) in filteredServiceLog"
        :key="index"
        class="col-md-4 mb-4"
      >
        <div class="card" :class="log.status_color">
          <div class="card-body">
            <h5 class="card-title">{{ log.professional_name }}</h5>
            <p><strong>Service Type:</strong> {{ log.service_type }}</p>
            <p><strong>Request Date:</strong> {{ log.service_request_date }}</p>
            <p><strong>Completion Date:</strong> {{ log.service_completion_date || 'Not Completed Yet' }}</p>

            <button class="btn btn-primary" @click="viewProfile(log.professional_id)">
              View Profile
            </button>
            <button
              v-if="log.status === 'Completed'"
              class="btn btn-success ms-2"
              @click="giveReview(log.professional_id)"
            >
              Give Review
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isPopupVisible" class="modal fade show d-block" style="background: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; right: 0; bottom: 0;" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="profileModalLabel">{{ professionalProfile.professional_name }}</h5>
            <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Rating:</strong> {{ professionalProfile.professional_rating }}</p>
            <p><strong>Description:</strong> {{ professionalProfile.professional_description }}</p>
            <p><strong>Experience:</strong> {{ professionalProfile.professional_experience }} years</p>
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
      serviceLog: [],
      searchQuery: '',
      statusFilter: '',
      isPopupVisible: false,
      professionalProfile: {
        professional_name: '',
        professional_rating: '',
        professional_description: '',
        professional_experience: ''
      }
    };
  },
  computed: {
    filteredServiceLog() {
      return this.serviceLog.filter(log => {
        const matchesSearch =
          log.professional_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          log.service_type.toLowerCase().includes(this.searchQuery.toLowerCase());

        const matchesStatus =
          !this.statusFilter || log.status === this.statusFilter;

        return matchesSearch && matchesStatus;
      });
    }
  },
  methods: {
    async fetchServiceLog() {
      const clientId = localStorage.getItem("client_id");

      if (!clientId) {
        console.error("Client ID not found in local storage.");
        alert("Client ID is not available in local storage");
        return;
      }

      const url = `http://127.0.0.1:8000/service-log?client_id=${clientId}`;

      try {
        const response = await fetch(url);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching service log: ${response.status} ${errorText}`);
        }
        const data = await response.json();
        this.serviceLog = data;
      } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
      }
    },
    async viewProfile(professionalId) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/professionals/${professionalId}`);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching professional profile: ${response.status} ${errorText}`);
        }
        const data = await response.json();
        this.professionalProfile = data;
        this.isPopupVisible = true;
      } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
      }
    },
    giveReview(professionalId) {
      this.$router.push({ path: `/write-review/${professionalId}` });
    },
    closePopup() {
      this.isPopupVisible = false;
    }
  },
  mounted() {
    this.fetchServiceLog();
  }
};
</script>

<style scoped>
.card.bg-danger {
  background-color: #f8d7da;
}
.card.bg-success {
  background-color: #d4edda;
}
.modal-dialog {
  max-width: 500px;
  margin: auto;
}
.modal-content {
  padding: 20px;
}
</style>  -->


<template>
  <div>
    <nav class="navbar fixed-top custom-navbar">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"><strong>ComfortCrew</strong></a>
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
              Explore
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
                <router-link to="/client_dashboard" class="nav-link">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/service_log" class="nav-link">My Services</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <br><br><br>
    <h1 class="text-center my-4">My Service Log</h1>

    <div class="d-flex justify-content-center mb-3">
      <input
        v-model="searchQuery"
        type="text"
        class="form-control w-50"
        placeholder="Search by name or service type"
      />
      <select v-model="statusFilter" class="form-select w-auto ms-2">
        <option value="">All Statuses</option>
        <option value="Completed">Completed</option>
        <option value="Rejected">Rejected</option>
        <option value="pending">Pending</option>
      </select>
    </div>

    <div class="row">
      <div
        v-for="(log, index) in filteredServiceLog"
        :key="index"
        class="col-md-4 mb-4"
      >
        <div class="card" :class="[
            log.status === 'Rejected' ? 'bg-warning' : '',
            log.status === 'Completed' ? 'bg-success' : '',
            log.status === 'Pending' ? 'bg-danger' : ''
          ]">
          <div class="card-body">
            <h5 class="card-title">{{ log.professional_name }}</h5>
            <p><strong>Service Type:</strong> {{ log.service_type }}</p>
            <p><strong>Request Date:</strong> {{ log.service_request_date }}</p>
            <p><strong>Completion Date:</strong> {{ log.service_completion_date || 'Not Completed Yet' }}</p>

            <button class="btn custom-btn" @click="viewProfile(log.professional_id)">
              View Profile
            </button>
            <button
              v-if="log.status === 'Completed'"
              class="btn custom-btn ms-2"
              @click="giveReview(log.professional_id)"
            >
              Give Review
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isPopupVisible" class="modal fade show d-block" style="background: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; right: 0; bottom: 0;" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="profileModalLabel">{{ professionalProfile.professional_name }}</h5>
            <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Rating:</strong> {{ professionalProfile.professional_rating }}</p>
            <p><strong>Description:</strong> {{ professionalProfile.professional_description }}</p>
            <p><strong>Experience:</strong> {{ professionalProfile.professional_experience }} years</p>
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
      serviceLog: [],
      searchQuery: '',
      statusFilter: '',
      isPopupVisible: false,
      professionalProfile: {
        professional_name: '',
        professional_rating: '',
        professional_description: '',
        professional_experience: ''
      }
    };
  },
  computed: {
    filteredServiceLog() {
      return this.serviceLog.filter(log => {
        const matchesSearch =
          log.professional_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          log.service_type.toLowerCase().includes(this.searchQuery.toLowerCase());

        const matchesStatus =
          !this.statusFilter || log.status === this.statusFilter;

        return matchesSearch && matchesStatus;
      });
    }
  },
  methods: {
    async fetchServiceLog() {
      const clientId = localStorage.getItem("client_id");

      if (!clientId) {
        console.error("Client ID not found in local storage.");
        alert("Client ID is not available in local storage");
        return;
      }

      const url = `http://127.0.0.1:8000/service-log?client_id=${clientId}`;

      try {
        const response = await fetch(url);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching service log: ${response.status} ${errorText}`);
        }
        const data = await response.json();
        this.serviceLog = data;
      } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
      }
    },
    async viewProfile(professionalId) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/professionals/${professionalId}`);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching professional profile: ${response.status} ${errorText}`);
        }
        const data = await response.json();
        this.professionalProfile = data;
        this.isPopupVisible = true;
      } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
      }
    },
    giveReview(professionalId) {
      this.$router.push({ path: `/write-review/${professionalId}` });
    },
    closePopup() {
      this.isPopupVisible = false;
    }
  },
  mounted() {
    this.fetchServiceLog();
  }
};
</script>

<style scoped>
.custom-navbar {
  background-color: #AF9B46;
}
.nav-link {
  color: black !important;
}
.custom-btn {
  background-color: #FFF05A;
  color: black !important;
  border: none;
}
.custom-btn:hover {
  opacity: 0.8;
}
.card.bg-danger {
  background-color: #f8d7da;
}
.card.bg-success {
  background-color: #d4edda;
}
.card.bg-warning {
  background-color: #f4c21f; /* Yellowish color for Rejected status */
}
.modal-dialog {
  max-width: 500px;
  margin: auto;
}

.modal-content {
  padding: 20px;
}
</style>
