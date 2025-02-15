<template>
  <div class="container mt-5">
    <h2>Write a Review for Professional</h2>
    <form @submit.prevent="submitReview">
      <div class="form-group">
        <label for="rating">Rating (1 to 5):</label>
        <input type="number" v-model="rating" class="form-control" id="rating" min="1" max="5" required />
      </div>
      <div class="form-group">
        <label for="review">Review:</label>
        <textarea v-model="review" class="form-control" id="review" rows="4" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Submit Review</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: null,
      review: '',
      professionalId: this.$route.params.profId, // Get the professional ID from route params
      serviceRequestId: null, // Keep serviceRequestId as null
      clientId: localStorage.getItem("client_id"), // Replace with the actual client ID
    };
  },
  methods: {
    async submitReview() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/write-review/${this.professionalId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rating: this.rating,
            review: this.review,
            client_id: this.clientId, // Include the client ID in the request body
            service_request_id: 3, 
            professional_id: this.professionalId, // Include the professional ID in the request body
          }),
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          this.$router.push('/service_log'); // Redirect back to the service log page after submission
        } else {
          const errorText = await response.text();
          throw new Error(`Error submitting review: ${errorText}`);
        }
      } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
      }
    }
  }
};
</script>

<style scoped>
.form-group {
  margin-bottom: 20px;
}
</style>
