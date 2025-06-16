<template>
  <div class="bg-light min-vh-100">  
    <div>
      <!--
        Navbar: Responsive Bootstrap navbar for user actions.
        - QUIZDOM brand
        - Scorecard, My Stats, Logout links
      -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/">QUIZDOM</router-link>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link class="nav-link fw-bold" to="/user_scorecard">📝 Scorecard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link fw-bold" to="/user_statistics">📊 My Stats</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link fw-bold" to="/login">🔓 Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!--
        Search Bar: Filter quizzes by name.
      -->
      <div class="container my-4">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search quizzes..."
        />
      </div>

      <!--
        Quiz Cards: List of all available quizzes for the user.
        Each card shows quiz details and a Start Quiz button.
      -->
      <div class="container">
        <div class="row">
          <!-- Render a card for each quiz -->
          <div
            v-for="quiz in filteredQuizzes"
            :key="quiz.quiz_id"
            class="col-md-4 mb-4"
          >
            <div class="card h-100 shadow-sm border-0 bg-beige">
              <div class="card-body">
                <h5 class="card-title text-primary fw-bold">{{ quiz.quiz_name }}</h5>
                <p class="card-text text-muted">{{ quiz.quiz_description }}</p><hr/>
                <p class="card-text">
                  <strong>Subject:</strong> {{ quiz.subject }}
                </p>
                <p class="card-text">
                  <strong>Chapter:</strong> {{ quiz.chapter }}
                </p>
                <p v-if="quiz.quiz_is_attempted">Attempt: Single attempt allowed.</p>
                <p v-else>Attempt: Multiple attempts allowed.</p>
                <p class="card-text"><strong>Time Limit:</strong> {{ quiz.quiz_duration }}</p>
                <!-- Start Quiz button links to quiz attempt page -->
                <router-link 
                  :to="`/start_quiz/${quiz.quiz_id}`" 
                  class="btn btn-success mt-3">
                  ▷ Start Quiz 
                </router-link>
              </div>
            </div>
          </div>

          <!-- No Quizzes Message -->
          <div v-if="filteredQuizzes.length === 0" class="col-12 text-center mt-5">
            <div class="alert alert-warning" role="alert">
              😕 No quizzes found. 
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // Component state: holds all quizzes and the search filter
  data() {
    return {
      quizzes: [],       // All quizzes fetched from backend
      searchQuery: "",   // Search text for filtering quizzes
    };
  },
  // Computed property to filter quizzes by search query
  computed: {
    filteredQuizzes() {
      return this.quizzes.filter((quiz) =>
        quiz.quiz_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    // Fetch all quizzes from backend API (requires JWT token)
    fetchQuizzes() {
      fetch('http://127.0.0.1:5000/get_quiz', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      })
        .then(response => response.json())
        .then(data => {
          this.quizzes = data;
        })
    },
  },
  // When the component is mounted, fetch all quizzes from backend
  mounted() {
    this.fetchQuizzes();
  },
};
</script>

<style scoped>
/*
  Custom background and button hover styles for the user dashboard.
*/
.bg-beige {
  background: linear-gradient(135deg, #fff1eb, #ace0f9);
}
.btn-success {
  transition: all 0.2s ease-in-out;
}
.btn-success:hover {
  transform: scale(1.05);
}
</style>