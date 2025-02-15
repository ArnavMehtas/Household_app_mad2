<template>
  <div>
    <div class="container">
      <h1><strong>ComfortCrew</strong></h1>
      <br><br>
      <h1>Find the Perfect Professional for Your Home Services!</h1>
      <br><br>
      <div class="button-group">
        <router-link to="/admin_login"><button>Are you an Admin?</button></router-link>
        <router-link to="/client_login"><button>Are you a Client?</button></router-link>
        <router-link to="/professional_login"><button>Are you a Professional?</button></router-link>
      </div>
    </div>
    
    <!-- Footer section with black box and text -->
    <footer class="footer">
      <p>
        © 2024. ComfortCrew. All Rights Reserved. 
        <span class="highlight">Privacy Policy</span> | 
        <span class="highlight">Terms & Conditions</span>
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'index',
  mounted() {
    // Apply body styles dynamically when this component is mounted
    document.body.style.backgroundColor = '#f0f0f0';
    document.body.style.backgroundImage = 'url(/17.jpg)'; // Corrected path to image
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundPosition = 'center center';
    document.body.style.height = '100vh';
    document.body.style.display = 'flex';
    document.body.style.justifyContent = 'center';
    document.body.style.alignItems = 'center';
    document.body.style.fontFamily = 'Arial, sans-serif';
    document.body.style.color = '#333';
  },
  beforeDestroy() {
    // Reset body styles when component is destroyed
    document.body.style.backgroundColor = '';
    document.body.style.backgroundImage = '';
    document.body.style.backgroundSize = '';
    document.body.style.backgroundRepeat = '';
    document.body.style.backgroundPosition = '';
    document.body.style.height = '';
    document.body.style.display = '';
    document.body.style.justifyContent = '';
    document.body.style.alignItems = '';
    document.body.style.fontFamily = '';
    document.body.style.color = '';
  }
};
</script>

<style scoped>
.container {
  text-align: center;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8); /* Optional: Light background for the container */
  border-radius: 10px;
  width: 80%; /* Adjust container width if necessary */
  max-width: 600px; /* Optional: Max width to limit container size */
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;
}

button {
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  padding: 15px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  flex: 1; /* Make buttons take equal width */
  text-align: center; /* Center text inside button */
}

button:hover {
  background-color: rgba(0, 0, 0, 0.9);
}

/* Footer styling */
.footer {
  background-color: black;
  color: white;
  text-align: center;
  padding: 20px 0;
  width: 100%;
  position: fixed; /* Keeps the footer at the bottom */
  bottom: 0;
  left: 0;
  font-size: 14px; /* Adjust font size as needed */
}

.highlight {
  color: yellow;
  cursor: pointer;
}

.highlight:hover {
  text-decoration: underline;
}
</style>
