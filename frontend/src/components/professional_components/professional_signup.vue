<template>
  <div class="signup-container">
    <div class="signup-content">
      <h1>Professional Signup</h1>
      <form @submit.prevent="submitForm" class="signup-form">
        <!-- Name -->
        <label class="form-label" for="professional_name">Name</label>
        <input
          type="text"
          id="professional_name"
          v-model="form.professional_name"
          class="form-control"
          required
        />

        <!-- Password -->
        <label class="form-label" for="professional_password">Password</label>
        <input
          type="password"
          id="professional_password"
          v-model="form.professional_password"
          class="form-control"
          required
        />

        <!-- Description -->
        <label class="form-label" for="professional_description">Description</label>
        <textarea
          id="professional_description"
          v-model="form.professional_description"
          class="form-control"
          required
        ></textarea>

        <!-- Experience -->
        <label class="form-label" for="professional_experience">Experience (in years)</label>
        <input
          type="number"
          id="professional_experience"
          v-model="form.professional_experience"
          class="form-control"
          required
        />

        <!-- Service Type -->
        <label class="form-label" for="professional_service_type">Service Type</label>
        <select
          id="professional_service_type"
          v-model="form.professional_service_type"
          class="form-control"
          required
        >
          <option v-for="service in services" :key="service.service_id" :value="service.service_id">
            {{ service.service_name }}
          </option>
        </select>

        <button class="btn" type="submit">Signup</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        professional_name: '',
        professional_password: '',
        professional_description: '',
        professional_experience: 0,
        professional_service_type: null,
      },
      services: [],
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    fetchServices() {
      fetch('http://127.0.0.1:8000/services')
        .then((response) => response.json())
        .then((data) => {
          if (data) {
            this.services = data;
          }
        })
        .catch((error) => {
          console.error('Error fetching services:', error.message);
        });
    },

    submitForm() {
      const payload = {
        professional_name: this.form.professional_name,
        professional_password: this.form.professional_password,
        professional_description: this.form.professional_description,
        professional_experience: this.form.professional_experience,
        professional_service_type: this.form.professional_service_type,
        professional_date_created: new Date().toISOString(),
      };

      fetch('http://127.0.0.1:8000/signup-professional', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert('Signup successful!');
            this.$router.push('/professional_dashboard');
          } else {
            alert('Signup failed. Please try again.');
          }
        })
        .catch((error) => {
          console.error('Error during signup:', error.message);
        });
    },
  },
};
</script>

<style scoped>
.signup-container {
  background-image: url('/11.jpg'); /* Set the background image */
  background-size: cover; /* Make the image cover the entire container */
  background-position: center; /* Center the background image */
  color: white; /* Set text color to white for contrast */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Arial', sans-serif;
  padding: 20px;
}

.signup-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 500px;
  background-color: rgba(219, 203, 216, 0.8); /* Add a semi-transparent background for the form */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #564787;
  margin-bottom: 20px;
}

.form-label {
  font-size: 1.1rem;
  color: #564787;
  margin-bottom: 5px;
}

.form-control {
  background-color: #fff;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  width: 100%;
  margin-bottom: 15px;
}

textarea.form-control {
  height: 100px;
}

.btn {
  background-color: #564787;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #9ad4d6;
}
</style>
