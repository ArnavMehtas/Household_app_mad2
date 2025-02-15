<template>
    <div class="client-signup-container">
      <div class="signup-content">
        <h1>Client Signup</h1>
        <h3 v-if="error_msg" class="text-danger">{{ error_msg }}</h3>
        <form @submit.prevent="client_signup" class="signup-form">
          <label class="form-label" for="client_name">Enter client name</label>
          <input v-model="client_name" class="form-control" type="text" name="client_name" required>
          
          <label class="form-label" for="client_password">Enter client Password</label>
          <input v-model="client_password" class="form-control" type="password" name="client_password" required>
          
          <label class="form-label" for="client_address">Enter client Address</label>
          <input v-model="client_address" class="form-control" type="text" name="client_address">
          
          <label class="form-label" for="client_phone">Enter client Phone Number</label>
          <input v-model="client_phone" class="form-control" type="text" name="client_phone">
          
          <button class="btn" type="submit">Signup</button>

          <a href="/client_login" style="color: black; text-decoration: none; font-weight: normal;">Already have an account?</a>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'client_signup',
    data () {
      return {
        client_name: '',
        client_password: '',
        client_address: '',
        client_phone: '',
        error_msg: ''
      };
    },
    methods: {
      async client_signup() {
        try {
          const response = await fetch('http://127.0.0.1:8000/client_signup', { 
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              client_name: this.client_name,
              client_password: this.client_password,
              client_address: this.client_address,
              client_phone: this.client_phone
            }),
          });
  
          const data = await response.json();
  
          if (data.client_id) {
            // Store the client information in localStorage or session
            localStorage.setItem("client_name", this.client_name);
            localStorage.setItem("client_id", data.client_id);  // Store client_id
  
            // Navigate to client dashboard
            this.$router.push('/client_dashboard');
          } else {
            this.error_msg = data.message;
          }
        } catch (error) {
          console.log(error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  /* Background color for the entire signup page */
  .client-signup-container {
    background-color: #AF9B46; /* Using #AF9B46 for background */
    color: white; /* Set text color to white for contrast */
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Arial', sans-serif;
    padding: 20px;
  }
  
  /* Container for both heading and form */
  .client-signup-container {
  background-image: url('/2.jpg'); /* Add the background image */
  background-size: cover; /* Ensures the image covers the entire container */
  background-position: center; /* Centers the image */
  color: white; /* Set text color to white for contrast */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Arial', sans-serif;
  padding: 20px;
}
/* Container for both heading and form */
.signup-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 400px;
  background-color: rgba(247, 176, 91, 0.7); /* Light orange with opacity (0.7) */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

  
  /* Heading styling */
  h1 {
    text-align: center;
    color: #1F1300; /* Dark brown color for the heading */
    margin-bottom: 20px;
  }
  
  /* Form label styling */
  .form-label {
    font-size: 1.1rem;
    color: #1F1300; /* Dark brown for the label */
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
    background-color: #1F1300; /* Dark brown for the button */
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
    background-color: #AF9B46; /* Light brown for hover effect */
  }
  
  /* Error message styling */
  .text-danger {
    color: red;
    font-size: 1rem;
    text-align: center;
    margin-top: 10px;
  }
  </style>
  