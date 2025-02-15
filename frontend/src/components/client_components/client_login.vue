
<template>
  <div class="client-login-container">
    <div class="login-content">
      <h1>Client Login</h1>
      <h3 v-if="error_msg" class="text-danger">{{ error_msg }}</h3>
      <form @submit.prevent="client_login" class="login-form">
        <label class="form-label" for="client_name">Enter client name</label>
        <input v-model="client_name" class="form-control" type="text" name="client_name">
        
        <label class="form-label" for="client_password">Enter client Password</label>
        <input v-model="client_password" class="form-control" type="password" name="client_password">
        
        <button class="btn" type="submit">Login</button>
        <a href="/client_signup" style="color: black; text-decoration: none; font-weight: normal;">Create a new account?</a>

      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'client_login',
  data () {
    return {
      client_name: '',
      client_password: '',
      error_msg: ''
    };
  },
  methods: {
    async client_login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/client_login', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            client_name: this.client_name,
            client_password: this.client_password
          }),
        });

        const data = await response.json();

        if (data.access_token) {
          // Store the access token, client_name, and client_id in localStorage
          localStorage.setItem("JWTToken", data.access_token);
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
/* Background color for the entire login page */
.client-login-container {
  background-color: #AF9B46; /* Using #AF9B46 for background */
  color: white; /* Set text color to white for contrast */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Arial', sans-serif;
  padding: 20px;
}
.client-login-container {
  background-image: url('/7.jpg'); /* Add the background image */
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
.login-content {
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




<!-- <template>
  <div class="p-5">
    <h1>client Login</h1>
    <h3 v-if="error_msg" class="text-danger">{{error_msg}}</h3>
    <form @submit.prevent="client_login">
      <label class="form-label" for="client_name">Enter client name</label>
      <input v-model="client_name" class="form-control"  type="text" name="client_name">
      <label for="client_password">Enter client Password</label>
      <input v-model="client_password" class="form-control"  type="text" name="client_password">
      <button class="btn btn-primary" type="submit">Login</button>
    </form>
 </div>
</template>




<script>
export default {
  name: 'client_login',
  data () {
    return {
      client_name: '',
      client_password: '',
      error_msg: ''
    };
  },
  methods:{

    async client_login(){
      try{
        const response = await fetch('http://127.0.0.1:8000/client_login', { 
          method: 'POST',
          headers:{
            'Content-Type': 'application/json',
          },
          body:JSON.stringify({
            client_name: this.client_name,
            client_password: this.client_password
          }),
        });
        const data = await response.json();
        if (data.access_token){
          console.log(data.access_token);
          localStorage.setItem("JWTToken", data.access_token);
          localStorage.setItem("client_name", this.client_name);
          this.$router.push('/client_dashboard');
        }
        else{
          this.error_msg =data.message;
        }
      }
      catch(error){
        console.log(error);
      }

    }
    
  }
}
</script>

<style>

</style> -->
<!-- 

<template>
  <div class="p-5">
    <h1>client Login</h1>
    <h3 v-if="error_msg" class="text-danger">{{error_msg}}</h3>
    <form @submit.prevent="client_login">
      <label class="form-label" for="client_name">Enter client name</label>
      <input v-model="client_name" class="form-control" type="text" name="client_name">
      
      <label for="client_password">Enter client Password</label>
      <input v-model="client_password" class="form-control" type="text" name="client_password">
      
      <button class="btn btn-primary" type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'client_login',
  data () {
    return {
      client_name: '',
      client_password: '',
      error_msg: ''
    };
  },
  methods: {
    async client_login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/client_login', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            client_name: this.client_name,
            client_password: this.client_password
          }),
        });

        const data = await response.json();

        if (data.access_token) {
          // Store the access token, client_name, and client_id in localStorage
          localStorage.setItem("JWTToken", data.access_token);
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

<style>
</style> -->
