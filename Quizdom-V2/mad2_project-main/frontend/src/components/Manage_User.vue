<template>
  <!--
    Main admin layout for managing users.
    Includes navigation bar, search bar, and a table listing all users.
  -->
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!-- Navigation Bar: Links to admin pages -->
    <nav class="navbar navbar-light px-4">
      <router-link class="navbar-brand fw-semibold display-6 text-dark" to="/admin">QUIZDOM Admin</router-link>  
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">
        <ul class="navbar-nav d-flex flex-row gap-3 ms-auto">
          <li class="nav-item">
            <router-link
              class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold"
              to="/manage_subject">SUBJECTS
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold"
              to="/manage_quiz">QUIZZES
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

    <!-- Main Content: User management panel -->
    <main class="flex-grow-1 py-4">
      <div class="container">
        <!-- Page Heading -->
        <div class="container my-4">
          <h2 class="text-info fw-bold">Manage Users</h2>
        </div>

        <!-- Search Bar -->
        <div class="container mt-4">
          <div class="row mb-4">
            <div class="col-md-8">
              <!-- Search input for filtering users -->
              <input
                type="text"
                class="form-control shadow-3d"
                placeholder="Search users..."
                v-model="searchQuery"
              >
            </div>
          </div>

          <!-- Show if no users match the search -->
          <div v-if="filteredUsers.length === 0" class="text-center py-4">
            <p class="text-muted">No users found.</p>
          </div>

          <!-- Table of users -->
          <div v-else>
            <div class="card shadow-3d bg-sky mb-4">
              <div class="card-body">
                <table class="table table-hover">
                  <thead>
                    <tr class="table-info fw-bold">
                      <th>User ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Full Name</th>
                      <th>Education Level</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in filteredUsers" :key="user.user_id">
                      <td class="fw-bold">{{ user.user_id }}</td>
                      <td>{{ user.user_name }}</td>
                      <td>{{ user.user_email }}</td>
                      <td>{{ user.user_complete_name }}</td>
                      <td>{{ user.user_education_level }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  // Component state: holds all users and search/filter text
  data () {
    return {
      users: [],      // All users fetched from backend
      searchQuery: '' // Search text for filtering users
    }
  },
  // Computed property to filter users by search query
  computed: {
    filteredUsers() {
      // Returns users whose username, full name, or email matches the search query (case-insensitive)
      return this.users.filter(user => 
        user.user_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.user_complete_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.user_email.toLowerCase().includes(this.searchQuery.toLowerCase()) 
      );
    }
  },

  methods: {
    // Fetch all users from backend API (requires JWT token)
    fetchUser() {
      const response = fetch(`http://127.0.0.1:5000/manage_user`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      });
      response.then(response => response.json())
      .then(data => {
        this.users = data
      })
    }
  },
  // When the component is mounted, fetch all users from backend
  mounted() {
    this.fetchUser();
  }
};
</script>

<style scoped>
/* 
  Styles for the admin Manage Users page.
  Includes custom backgrounds, card shadows, and button hover effects.
*/
.bg-sky {
  background-color: #ffffff;
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
  background-color: #ffffff;
}
.nav-text-color {
  color: #667589;
}
</style>
