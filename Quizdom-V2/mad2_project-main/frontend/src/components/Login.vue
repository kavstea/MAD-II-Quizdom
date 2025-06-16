<template>
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!--
      Navbar: Shows the Quizdom brand and links to home.
    -->
    <nav class="navbar navbar-light px-4 ">
      <router-link class="navbar-brand fw-semibold display-6 text-dark" to="/">QUIZDOM</router-link>
    </nav>

    <!--
      Login Section: Contains two cards, one for user login and one for admin login.
    -->
    <main class="flex-grow-1 py-5">
      <div class="container">
        <div class="row justify-content-center g-4">
          <!-- User Login Card -->
          <div class="col-sm-10 col-md-5 col-lg-4">
            <div class="card bg-sky text-body border border-muted shadow-3d">
              <div class="card-body p-3">
                <h5 class="text-center text-body mb-3 fw-semibold">User Login</h5>
                <form @submit.prevent="login('user')">
                  <div class="mb-2">
                    <input
                      v-model="user.user_name"
                      type="text"
                      class="form-control form-control-sm custom-input"
                      placeholder="Username"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <input
                      v-model="user.user_password"
                      type="password"
                      class="form-control form-control-sm custom-input"
                      placeholder="Password"
                      required
                    />
                  </div>
                  <button
                    type="submit"
                    class="btn btn-success w-100 fw-semibold"
                    :disabled="loading.user"
                  >
                    {{ loading.user ? 'Logging in...' : 'Login as User' }}
                  </button>
                </form>
                <p class="mt-2 text-center text-muted small fw-semibold">
                  New here? <router-link to="/signup" class="text-success ">Sign up</router-link>
                </p>
              </div>
            </div>
          </div>

          <!-- Admin Login Card -->
          <div class="col-sm-10 col-md-5 col-lg-4">
            <div class="card bg-mint text-body border border-muted shadow-3d ">
              <div class="card-body p-3">
                <h5 class="text-center text-body mb-3 fw-semibold">Admin Login</h5>
                <form @submit.prevent="login('admin')">
                  <div class="mb-2">
                    <input
                      v-model="admin.user_name"
                      type="text"
                      class="form-control form-control-sm custom-input"
                      placeholder="Admin Name"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <input
                      v-model="admin.user_password"
                      type="password"
                      class="form-control form-control-sm custom-input"
                      placeholder="Admin Password"
                      required
                    />
                  </div>
                  <button
                    type="submit"
                    class="btn btn-outline-primary w-100 fw-semibold"
                    :disabled="loading.admin"
                  >
                    {{ loading.admin ? 'Logging in...' : 'Login as Admin' }}
                  </button>
                </form>
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
  // Component state: holds user/admin login form data and loading state
  data() {
    return {
      user: { user_name: '', user_password: '' },   // User login fields
      admin: { user_name: '', user_password: '' },  // Admin login fields
      loading: { user: false, admin: false }        // Loading states for buttons
    }
  },
  methods: {
    // Handles login for both user and admin roles
    async login(role) { // 'role' is either 'user' or 'admin'
      this.loading[role] = true;
      try {
        // Use the appropriate credentials object
        const credentials = role === 'admin' ? this.admin : this.user;
        
        // Send POST request to backend login endpoint
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        });

        // Parse backend response
        const data = await response.json();

        if (response.ok) {
          // Save JWT token to localStorage for future requests
          localStorage.setItem('auth_token', data.access_token);

          // Redirect based on user type
          if (data.message.includes('Admin')) {
            alert(data.message);
            this.$router.push('/admin');
          } else {
            alert(data.message);
            this.$router.push('/user');
          }
        } else {
          alert(data.message || 'Login failed');
        }
      } catch (error) {
        console.error('Login error:', error);
        alert('Network error - please try again');
      } finally {
        this.loading[role] = false;
      }
    }
  }
}
</script>

<style scoped>
/*
  Custom background and shadow styles for the login page.
*/
.bg-mint {
  background-color: #c9d5d2; /* Light mint green */
}
.bg-paper {
  background-color: #fefcf5; /* Natural tree paper white */
}
.bg-sky {
  background-color: #b2c3c7; /* Light sky blue */
}
.bg-blue {
  background-color: #e2f5ff; /* Light sky blue */
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #a1b1c9, #ffffff); /* Lilac to Fuchsia */
}
.shadow-3d {
  box-shadow:
    0 5px 7px rgba(0, 0, 0, 0.1),
    0 9px 21px rgba(0, 0, 0, 0.2); /* Deeper, layered 3D effect */
}
</style>