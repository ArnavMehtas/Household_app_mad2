<template>
  <div class="admin-login-container">
    <div class="login-content">
      <h1>Admin Login</h1>
      <h3 v-if="error_msg" class="text-danger">{{ error_msg }}</h3>
      <form @submit.prevent="admin_login" class="login-form">
        <label class="form-label" for="admin_username">Enter admin Username</label>
        <input v-model="admin_username" class="form-control" type="text" name="admin_username">
        <label for="admin_password">Enter admin Password</label>
        <input v-model="admin_password" class="form-control" type="password" name="admin_password">
        <button class="btn" type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'admin_login',
  data () {
    return {
      admin_username: '',
      admin_password: '',
      error_msg: ''
    };
  },
  methods: {
    async admin_login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin_login', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            admin_username: this.admin_username,
            admin_password: this.admin_password
          }),
        });
        const data = await response.json();
        if (data.access_token) {
          console.log(data.access_token);
          localStorage.setItem("JWTToken", data.access_token);
          localStorage.setItem("admin_username", this.admin_username);
          this.$router.push('/admin_dashboard');
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
/* Background color and image for the entire login page */
.admin-login-container {
  background-color: #89937C; /* Using #89937C for background color */
  background-image: url('/4.jpg'); /* Adding the background image */
  background-size: cover; /* Ensures the image covers the entire container */
  background-position: center center; /* Centers the background image */
  background-repeat: no-repeat; /* Ensures the background image doesn't repeat */
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
  background-color: rgba(193, 174, 159, 0.9); /* Semi-transparent beige background */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Heading styling */
h1 {
  text-align: center;
  color: white; /* White color for the heading */
  margin-bottom: 20px;
}

/* Form label styling */
.form-label {
  font-size: 1.1rem;
  color: #fff;
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
  background-color: #89937C; /* Dark olive green for the button */
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
  background-color: #C1AE9F; /* Light beige for hover effect */
}

/* Error message styling */
.text-danger {
  color: red;
  font-size: 1rem;
  text-align: center;
  margin-top: 10px;
}
</style>
