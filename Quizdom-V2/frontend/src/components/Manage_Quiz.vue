<template>
  <!--
    Main admin layout for managing quizzes.
    Includes navigation bar, search, quiz cards, and modals for add/edit.
  -->
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!-- Navigation Bar: Links to admin pages -->
    <nav class="navbar navbar-light px-4">
      <router-link class="navbar-brand fw-semibold display-6 text-dark" to="/admin">QUIZDOM Admin</router-link>  
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">
        <ul class="navbar-nav d-flex flex-row gap-3 ms-auto">
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/manage_subject">SUBJECTS</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/manage_user">USERS</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/">🏠︎</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/admin_statistics">STATS 📊︎</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main Content: Quiz management panel -->
    <main class="flex-grow-1 py-5">
      <div class="container">
        <!-- Page Heading -->
        <h2 class="fw-bold text-success mb-4">Manage Quizzes</h2>

        <!-- Search Bar and Add Quiz Button -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <!-- Search input for filtering quizzes -->
          <input
            v-model="searchQuery"
            type="text"
            class="form-control w-50 me-3 shadow-3d border-light"
            placeholder="Search quizzes..."
          />
          <!-- Button to open Add Quiz modal -->
          <button class="btn btn-success shadow-3d" @click="addQuizModal">+ Add Quiz</button>
        </div>

        <!-- Show if no quizzes match the search -->
        <div v-if="filteredQuizzes.length === 0" class="text-center py-4">
          <p class="text-muted">No quizzes found.</p>
        </div>

        <!-- List of quizzes as cards -->
        <div v-else>
          <div class="row">
            <div v-for="quiz in filteredQuizzes" :key="quiz.quiz_id" class="col-md-4 mb-4">
              <div class="card h-100 bg-sky border border-light shadow-3d">
                <div class="card-body d-flex flex-column">
                  <h5 class="card-title text-success fw-bold">{{ quiz.quiz_name }}</h5>
                  <p class="card-text">{{ quiz.quiz_description }}</p>
                  <p class="card-text"><strong>Subject:</strong> {{ quiz.subject }}</p>
                  <p class="card-text"><strong>Chapter:</strong> {{ quiz.chapter }}</p>
                  <p v-if="quiz.quiz_is_attempted">Attempt: Single attempt allowed.</p>
                  <p v-else>Attempt: Multiple attempts allowed.</p>
                  <p class="card-text"><strong>Time Limit:</strong> {{ quiz.quiz_duration }}</p>
                  <div class="mt-auto">
                    <!-- Edit/Delete quiz buttons -->
                    <button class="btn btn-outline-success btn-sm w-100 mb-2 shadow-3d" @click="editQuizModal(quiz)">✎ Edit</button>
                    <button class="btn btn-outline-danger btn-sm w-100 mb-2 shadow-3d" @click="deleteQuiz(quiz.quiz_id)">⛌ Delete</button>
                  </div>
                </div>
                <!-- Footer: Add/View questions for this quiz -->
                <div class="card-footer bg-sky d-flex justify-content-between border-top border-light">
                  <router-link :to="`/add_question/${quiz.quiz_id}`" class="btn btn-sm btn-success w-50 me-1 shadow-3d">Add Question</router-link>
                  <router-link :to="`/view_questions/${quiz.quiz_id}`" class="btn btn-sm btn-secondary w-50 shadow-3d">View Questions</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Quiz Modal: Form for adding a new quiz -->
    <div class="modal fade" id="addQuizModal" tabindex="-1" aria-labelledby="addQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title" id="addQuizModalLabel">Add New Quiz</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addQuiz">
              <!-- Select chapter for the quiz -->
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select v-model="newQuiz.chapter_id_of_quiz" class="form-select" required>
                  <option disabled value="">Select a chapter</option>
                  <option v-for="chapter in chapters" :value="chapter.chapter_id" :key="chapter.chapter_id">
                    {{ chapter.chapter_name }}
                  </option>
                </select>
              </div>
              <!-- Quiz name input -->
              <div class="mb-3">
                <label class="form-label">Quiz Name</label>
                <input type="text" class="form-control" v-model="newQuiz.quiz_name" required>
              </div>
              <!-- Quiz description input -->
              <div class="mb-3">
                <label class="form-label">Quiz Description</label>
                <textarea class="form-control" rows="3" v-model="newQuiz.quiz_description" required></textarea>
              </div>
              <!-- Time limit input (HH:MM:SS) -->
              <div class="mb-3">
                <label class="form-label">Time Limit</label>
                <input type="text" class="form-control" placeholder="HH:MM:SS" pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$" v-model="newQuiz.quiz_duration" required>
              </div>
              <!-- Release date input -->
              <div class="mb-3">
                <label class="form-label">Release Date</label>
                <input type="date" class="form-control" v-model="newQuiz.quiz_release_date" required>
              </div>
              <!-- Checkbox for single/multiple attempt -->
              <div class="form-check mb-3">
                <input type="checkbox" class="form-check-input" v-model="newQuiz.quiz_is_attempted" id="attemptedCheckbox">
                <label class="form-check-label" for="attemptedCheckbox">Single Attempt</label>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-success">Add Quiz</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Quiz Modal: Form for editing an existing quiz -->
    <div class="modal fade" id="editQuizModal" tabindex="-1" aria-labelledby="editQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title" id="editQuizModalLabel">Edit Quiz</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editQuiz">
              <!-- Select chapter for the quiz -->
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select v-model="SelectedQuiz.chapter_id_of_quiz" class="form-select" required>
                  <option disabled value="">Select a chapter</option>
                  <option v-for="chapter in chapters" :value="chapter.chapter_id" :key="chapter.chapter_id">
                    {{ chapter.chapter_name }}
                  </option>
                </select>
              </div>
              <!-- Quiz name input -->
              <div class="mb-3">
                <label class="form-label">Quiz Name</label>
                <input type="text" class="form-control" v-model="SelectedQuiz.quiz_name" required>
              </div>
              <!-- Quiz description input -->
              <div class="mb-3">
                <label class="form-label">Quiz Description</label>
                <textarea class="form-control" rows="3" v-model="SelectedQuiz.quiz_description" required></textarea>
              </div>
              <!-- Time limit input (HH:MM:SS) -->
              <div class="mb-3">
                <label class="form-label">Time Limit</label>
                <input type="text" class="form-control" placeholder="HH:MM:SS" pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$" v-model="SelectedQuiz.quiz_duration" required>
              </div>
              <!-- Release date input -->
              <div class="mb-3">
                <label class="form-label">Release Date</label>
                <input type="date" class="form-control" v-model="SelectedQuiz.quiz_release_date" required>
              </div>
              <!-- Checkbox for single/multiple attempt -->
              <div class="form-check mb-3">
                <input type="checkbox" class="form-check-input" v-model="SelectedQuiz.quiz_is_attempted" id="attemptedCheckboxEdit">
                <label class="form-check-label" for="attemptedCheckboxEdit">Single Attempt</label>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-success">Update Quiz</button>
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
  // Component state: quizzes, chapters, search/filter text, and form data
  data() {
    return {
      quizzes: [], // All quizzes fetched from backend
      chapters: [], // All chapters fetched from backend (for quiz assignment)
      searchQuery: '', // Search text for filtering quizzes
      // Form data for adding a quiz
      newQuiz: {
        chapter_id_of_quiz: '',
        quiz_name: '',
        quiz_description: '',
        quiz_duration: '',
        quiz_release_date: '',
        quiz_is_attempted: false,
      },
      // Form data for editing a quiz
      SelectedQuiz: {
        chapter_id_of_quiz: '',
        quiz_name: '',
        quiz_description: '',
        quiz_duration: '',
        quiz_release_date: '',
        quiz_is_attempted: '',
      }
    };
  },

  // Computed property to filter quizzes by search query
  computed: {
    filteredQuizzes() {
      return this.quizzes.filter(quiz => {
        return quiz.quiz_name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    }
  },

  methods: {
    // Show the modal for adding a new quiz
    addQuizModal() {
      const modal = new bootstrap.Modal(document.getElementById('addQuizModal'));
      modal.show();
    },

    // Fetch all quizzes from backend API
    fetchQuizzes() {
      const response = fetch('http://127.0.0.1:5000/get_quiz', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      });
      response.then(response => response.json())
      .then(data => {
        this.quizzes = data;
      })
    },
    
    // Send POST request to backend to add a new quiz
    addQuiz() {
      fetch('http://127.0.0.1:5000/add_quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
        body: JSON.stringify(this.newQuiz)
      })
      .then(response => response.json())
      .then(data => {
        // Hide modal, clear form, alert user, and refresh quiz list
        bootstrap.Modal.getInstance(document.getElementById('addQuizModal')).hide();
        this.newQuiz = {
          chapter_id_of_quiz: '',
          quiz_name: '',
          quiz_description: '',
          quiz_duration: '',
          quiz_release_date: '',
          quiz_is_attempted: false
        }
        alert(data.message);
        this.fetchQuizzes();
      });
    },

    // Fetch all chapters from backend (for quiz assignment)
    fetchChapters() {
      fetch('http://127.0.0.1:5000/add_chapter/get', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      })          
      .then(response => response.json())
      .then(data => {
        this.chapters = data;
      })
    },

    // Show modal for editing a quiz, pre-fill with selected quiz data
    editQuizModal(quiz) {
      this.SelectedQuiz.quiz_id = quiz.quiz_id;
      this.SelectedQuiz.chapter_id_of_quiz = quiz.chapter_id_of_quiz;
      this.SelectedQuiz.quiz_name = quiz.quiz_name;
      this.SelectedQuiz.quiz_description = quiz.quiz_description;
      this.SelectedQuiz.quiz_duration = quiz.quiz_duration;
      this.SelectedQuiz.quiz_release_date = quiz.quiz_release_date;
      this.SelectedQuiz.quiz_is_attempted = quiz.quiz_is_attempted;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
    },

    // Send PUT request to backend to update quiz details
    editQuiz() {
      const response = fetch(`http://127.0.0.1:5000/edit_quiz/${this.SelectedQuiz.quiz_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
        body: JSON.stringify(this.SelectedQuiz)
      });
      response.then(response => response.json())
      .then(data => {
        bootstrap.Modal.getInstance(document.getElementById('editQuizModal')).hide();
        alert(data.message);
        this.fetchQuizzes();
      });
    },

    // Confirm and send DELETE request to remove a quiz
    deleteQuiz(quiz_id) {
      if (!confirm('Are you sure you want to delete this quiz?')) {
        return;
      }
      fetch(`http://127.0.0.1:5000/delete_quiz/${quiz_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchQuizzes();
      })
    }
  },

  // When the component is mounted, fetch all quizzes and chapters from backend
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
};
</script>

<style scoped>
/* 
  Styles for the admin Manage Quizzes page.
  Includes custom backgrounds, card shadows, and button hover effects.
*/
.bg-sky {
  background-color: #ffffff;
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #a1b1c9, #ffffff);
}
.shadow-3d {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 8px 20px rgba(0, 0, 0, 0.2);
}
.nav-link:hover {
  transform: translateY(-2px);
  transition: all 0.2s ease-in-out;
  background-color: #ffffff;
}
.nav-text-color {
  color: #667589;
}
.card-footer .btn {
  font-size: 0.85rem;
}
/*.card {
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
}*/
</style>
