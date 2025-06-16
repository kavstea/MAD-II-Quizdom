<template>
  <!--
    Quiz Questions Management Page
    Shows all questions for a quiz, allows admin to edit or delete each question.
  -->
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!-- Back button to return to Manage Quizzes page -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <router-link to="/manage_quiz" class="btn btn-black fw-bold shadow-3d rounded px-3 py-1">⬅︎ Back</router-link>
    </div>

    <!-- Main Content: List of questions for the quiz -->
    <main class="flex-grow-1 py-1">
      <div class="container">
        <!-- Page Heading -->
        <h2 class="text-center mb-4 fw-bold text-black">Questions for Quiz</h2>
        
        <!-- Show if there are no questions -->
        <div v-if="questions.length === 0" class="text-center py-4">
          <p class="text-muted">No questions found for this quiz.</p>
        </div>
        
        <!-- List of questions as cards -->
        <div v-else class="row g-4 justify-content">
          <div class="col-sm-10 col-md-6 col-lg-4" v-for="question in questions" :key="question.question_id">
            <div class="card h-100 bg-sky border border-light shadow-3d">
              <div class="card-body">
                <!-- Question tag and text -->
                <h5 class="card-title text-black fw-bold"># {{ question.question_tag }}</h5><hr/>
                <p class="card-text" style="white-space: pre-line">{{ question.question_text }}</p>
                <hr class="border-light">
                <!-- Options -->
                <p class="card-text"><strong>Option 1:</strong> {{ question.question_option1 }}</p>
                <p class="card-text"><strong>Option 2:</strong> {{ question.question_option2 }}</p>
                <p class="card-text"><strong>Option 3:</strong> {{ question.question_option3 }}</p>
                <p class="card-text"><strong>Option 4:</strong> {{ question.question_option4 }}</p><hr/>
                <!-- Correct answer -->
                <p class="card-text text-success fw-bold">Correct Answer: {{ question.question_answer }}</p>
              </div>
              <!-- Edit/Delete buttons for each question -->
              <div class="card-footer bg-sky border-top border-light d-flex justify-content-end">
                <button class="btn btn-outline-secondary btn-sm shadow-3d" @click="editQuestionModal(question)">✎</button>
                <button class="btn btn-outline-danger btn-sm shadow-3d" style="margin-left: 10px;" @click="deleteQuestion(question.question_id)">⛌</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Question Modal: Form for editing an existing question -->
    <div class="modal fade" id="editQuestionModal" tabindex="-1" aria-labelledby="editQuestionModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-secondary text-white">
            <h5 class="modal-title" id="editQuestionModalLabel">Edit Question</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editQuestion">
              <!-- All fields for editing the question -->
              <div class="mb-3">
                <label class="form-label">Question Tag</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_tag" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Question Text</label>
                <textarea class="form-control" v-model="SelectedQuestion.question_text" rows="4" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 1</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_option1" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 2</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_option2" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 3</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_option3" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Option 4</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_option4" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Answer</label>
                <input type="text" class="form-control" v-model="SelectedQuestion.question_answer" placeholder="a/b/c/d" required>
              </div>
              <div class="d-flex justify-content-between">
                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-secondary">Update Question</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // Component state: holds all questions and the currently selected question for editing
  data() {
    return {
      questions: [], // All questions for this quiz
      SelectedQuestion: {
        question_tag: '',
        question_text: '',
        question_option1: '',
        question_option2: '',
        question_option3: '',
        question_option4: '',
        question_answer: ''
      }
    }
  },
 
  methods: {
    // Fetch all questions for the current quiz from backend API
    fetchQuestions() {
      const response = fetch(`http://127.0.0.1:5000/get_questions/${this.$route.params.quiz_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
      })
      response.then(response => response.json())
        .then(data => {
          this.questions = data
        })
    },
    // Show modal for editing a question, pre-fill with selected question data
    editQuestionModal(question) {
      this.SelectedQuestion.question_id = question.question_id
      this.SelectedQuestion.question_tag = question.question_tag
      this.SelectedQuestion.question_text = question.question_text
      this.SelectedQuestion.question_option1 = question.question_option1
      this.SelectedQuestion.question_option2 = question.question_option2
      this.SelectedQuestion.question_option3 = question.question_option3
      this.SelectedQuestion.question_option4 = question.question_option4
      this.SelectedQuestion.question_answer = question.question_answer
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuestionModal')).show()
    },
    // Send PUT request to backend to update question details
    editQuestion() {
      fetch(`http://127.0.0.1:5000/edit_question/${this.SelectedQuestion.question_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
        body: JSON.stringify(this.SelectedQuestion)
      })
      .then(response => response.json())
      .then(data => {
          alert(data.message)
          bootstrap.Modal.getInstance(document.getElementById('editQuestionModal')).hide()
          this.fetchQuestions()
      })  
    },
    // Confirm and send DELETE request to remove a question
    deleteQuestion(question_id) {
      if(!confirm('Are you sure you want to delete this question?')) {
        return
      }  
      fetch(`http://127.0.0.1:5000/delete_question/${question_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message)
        this.fetchQuestions()
      })
    }
  },
  // When the component is mounted, fetch all questions from backend
  mounted() {
    this.fetchQuestions()
  },
}
</script>

<style scoped>
/* 
  Styles for the quiz questions page.
  Includes custom backgrounds and card footer button sizing.
*/
.bg-sky {
  background-color: #fafafa;
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #c1c5cb, #ffffff);
}
/* .shadow-3d, .nav-link:hover, .nav-text-color, .card, .card:hover
   are commented out, but can be enabled for extra effects. */
.card-footer .btn {
  font-size: 0.85rem;
}
</style>