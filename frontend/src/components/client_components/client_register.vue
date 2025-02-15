<template>
    <div class="p-5">
      <h1>Client Login</h1>
      <form>
        <label class="form-label" for="client_username">Enter client Username</label>
        <input class="form-control"  type="text" name="client_username">
        <label class="form-label" for="client_password">Enter client Password</label>
        <input class="form-control"  type="text" name="client_password">

        <button class="btn btn-primary" type="submit">Login</button>


      </form>
      
    </div>
  </template>
  



  <script>
  export default {
    name: 'client_register',
    data () {
     
    }
  }
  </script>
  
  <style>
 
  </style>
  