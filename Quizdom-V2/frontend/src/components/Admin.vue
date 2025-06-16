<template>
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!--
      Navbar: Shows the Quizdom Admin brand and navigation links.
      - LOGOUT: Navigates to login page (simulate logout)
      - Home: Navigates to main site
      - STATS: Admin statistics page
    -->
    <nav class="navbar navbar-light px-4">
      <router-link class="navbar-brand fw-semibold display-6 text-dark" to="/admin">QUIZDOM Admin</router-link>  
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">
        <ul class="navbar-nav d-flex flex-row gap-3 ms-auto">
          <li class="nav-item">
            <router-link
              class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold"
              to="/login">LOGOUT 🔓︎ 
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold"
              to="/">🏠︎
            </router-link>
          </li>
          <li class="nav-item">  
            <router-link
              class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold"
              to="/admin_statistics">STATS 📊︎
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!--
      Dashboard Main Section: Three cards for Subjects, Quizzes, and Users.
      Each card links to the respective management page.
    -->
    <main class="flex-grow-1 py-5">
      <div class="container">
        <div class="row g-4 justify-content-center">
          <!-- Subjects Card -->
          <div class="col-sm-10 col-md-4">
            <div class="card bg-sky text-dark border border-light shadow-3d">
              <div class="card-body text-center">
                <h5 class="fw-bold text-primary mb-2">Manage Subject</h5>
                <p>Create, update, or delete quiz subjects.</p>
                <router-link to="/manage_subject" class="btn btn-outline-primary">Go to Subjects</router-link>
              </div>
            </div>
          </div>

          <!-- Quizzes Card -->
          <div class="col-sm-10 col-md-4">
            <div class="card bg-sky text-dark border border-light shadow-3d">
              <div class="card-body text-center">
                <h5 class="fw-bold text-success mb-2">Manage Quiz</h5>
                <p>Create and organize quizzes for users.</p>
                <router-link to="/manage_quiz" class="btn btn-outline-success">Go to Quizzes</router-link>
              </div>
            </div>
          </div>

          <!-- Users Card -->
          <div class="col-sm-10 col-md-4">
            <div class="card bg-sky text-dark border border-light shadow-3d">
              <div class="card-body text-center">
                <h5 class="fw-bold text-info mb-2">Manage User</h5>
                <p>Find and view user information.</p>
                <router-link to="/manage_user" class="btn btn-outline-info">Go to Users</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 
  Styles for the admin dashboard page.
  Includes custom backgrounds, card hover effects, and navigation link colors.
*/
.bg-sky {
  background-color: #fafafa;
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #a1b1c9, #ffffff);
}
.shadow-3d {
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 8px 20px rgba(0, 0, 0, 0.2);
}
.nav-link:hover {
  transform: translateY(-2px);
  transition: all 0.2s ease-in-out;
}
.nav-text-color {
  color: #667589; /* slightly deeper sky blue */
}
.card {
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
}
</style>
