<template>
  <!--
    Add New Question Form
    Allows admin to enter question details and options, then submit to backend.
  -->
  <div class="container mt-5">
    <!-- Page Heading -->
    <h2 class="text-center mb-4">Add New Question</h2>
    <!-- Question Form -->
    <form @submit.prevent="addQuestion">
      <!-- Question Tag (topic or category) -->
      <div class="mb-3">
        <label class="form-label">Question Tag</label>
        <input type="text" class="form-control" v-model="newQuestion.question_tag" required>
      </div>
      <!-- Question Text (main question body) -->
      <div class="mb-3">
        <label class="form-label">Question Text</label>
        <textarea class="form-control" v-model="newQuestion.question_text" rows="4" required></textarea>
      </div>
      <!-- Option 1 -->
      <div class="mb-3">
        <label class="form-label">Option 1</label>
        <input type="text" class="form-control" v-model="newQuestion.question_option1" required>
      </div>
      <!-- Option 2 -->
      <div class="mb-3">
        <label class="form-label">Option 2</label>
        <input type="text" class="form-control" v-model="newQuestion.question_option2" required>
      </div>
      <!-- Option 3 -->
      <div class="mb-3">
        <label class="form-label">Option 3</label>
        <input type="text" class="form-control" v-model="newQuestion.question_option3" required>
      </div>
      <!-- Option 4 -->
      <div class="mb-3">
        <label class="form-label">Option 4</label>
        <input type="text" class="form-control" v-model="newQuestion.question_option4" required>
      </div>
      <!-- Correct Answer (expects a/b/c/d or similar) -->
      <div class="mb-3">
        <label class="form-label">Correct Answer</label>
        <input type="text" class="form-control" v-model="newQuestion.question_answer" placeholder="a/b/c/d" required>
      </div>
      <!-- Submit Button -->
      <button type="submit" class="btn btn-success w-100">Add Question</button>
    </form>
  </div>
</template>

<script>
export default {
  // Component state: holds the new question's details
  data() {
    return {
      newQuestion: {
        question_tag: '',      // Tag or topic for the question
        question_text: '',     // The main question text
        question_option1: '',  // Option 1 text
        question_option2: '',  // Option 2 text
        question_option3: '',  // Option 3 text
        question_option4: '',  // Option 4 text
        question_answer: ''    // Correct answer (e.g., "a", "b", "c", or "d")
      },
    };
  },
  methods: {
    // Submit the new question to the backend API
    addQuestion() {
      // Send POST request to backend with new question data
      const response = fetch('http://127.0.0.1:5000/add_question/' + this.$route.params.quiz_id, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
        body: JSON.stringify(this.newQuestion)
      });
      response.then(response => response.json())
      .then(data => {
        // If backend returns a message, alert user and redirect to Manage Quiz page
        if (data.message) {
          alert(data.message);
          this.$router.push(`/manage_quiz`);
        }
      })
    }
  }
};
</script>

<style scoped>
/* 
  Add any custom styles for the Add Question page here.
  For example: 
*/  
  .container { max-width: 600px; }

</style>
