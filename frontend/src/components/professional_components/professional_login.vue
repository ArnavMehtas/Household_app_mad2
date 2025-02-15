<template>
  <div class="professional-login-container">
    <div class="login-content">
      <h1>Professional Login</h1>
      <h3 v-if="error_msg" class="text-danger">{{ error_msg }}</h3>
      <form @submit.prevent="professionalLogin" class="login-form">
        <!-- Name -->
        <label class="form-label" for="professional_name">Name</label>
        <input
          v-model="professional_name"
          class="form-control"
          type="text"
          name="professional_name"
          placeholder="Enter your name"
          required
        />

        <!-- Password -->
        <label class="form-label" for="professional_password">Password</label>
        <input
          v-model="professional_password"
          class="form-control"
          type="password"
          name="professional_password"
          placeholder="Enter your password"
          required
        />

        <button class="btn" type="submit">Login</button>
        <a href="/professional_signup" >Sign Up?</a>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfessionalLogin",
  data() {
    return {
      professional_name: "",
      professional_password: "",
      error_msg: "",
    };
  },
  methods: {
    // Professional login method
    async professionalLogin() {
      try {
        const response = await fetch("http://127.0.0.1:8000/professional_login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            professional_name: this.professional_name,
            professional_password: this.professional_password,
          }),
        });
        const data = await response.json();

        if (data.access_token) {
          // Save the token and redirect to dynamic dashboard route
          localStorage.setItem("JWTToken", data.access_token);
          localStorage.setItem("professional_name", this.professional_name);
          localStorage.setItem("professional_id", data.professional_id);
          this.$router.push(`/professional_dashboard`);
        } else {
          this.error_msg = data.message;
        }
      } catch (error) {
        console.error("Error during login:", error);
        this.error_msg = "Something went wrong. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Background color for the entire login page */
.professional-login-container {
  background-image: url('/9.jpg'); /* Set the background image */
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

/* Container for both heading and form */
.login-content {
  display: flex;
  flex-direction: column; /* Align the heading and form vertically */
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 400px;
  background-color: rgba(219, 203, 216, 0.8); /* Add a semi-transparent background for the form */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Heading styling */
h1 {
  text-align: center;
  color: #564787; /* Dark purple color for the heading */
  margin-bottom: 20px;
}

/* Form label styling */
.form-label {
  font-size: 1.1rem;
  color: #564787; /* Dark purple for the label */
  margin-bottom: 5px;
}

/* Input field styling */
.form-control {
  background-color: #fff; /* White background for inputs */
  color: #333; /* Dark text color for input fields */
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  width: 100%;
  margin-bottom: 15px;
}

/* Button styling */
.btn {
  background-color: #564787; /* Dark purple for the button */
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease;
}

/* Button hover effect */
.btn:hover {
  background-color: #9AD4D6; /* Light blue for hover effect */
}

/* Error message styling */
.text-danger {
  color: red;
  font-size: 1rem;
  text-align: center;
  margin-top: 10px;
}
</style>
