<template>
  <div class="d-flex flex-column min-vh-100 bg-gradient-auth text-dark">
    <!--
      Navbar: Shows the Quizdom brand and links to home.
    -->
    <nav class="navbar navbar-light px-4 ">
      <router-link class="navbar-brand display-6 fw-semibold text-dark" to="/">QUIZDOM</router-link>
    </nav>

    <!--
      Main Section: Sign Up form centered in the page.
    -->
    <main class="flex-grow-1 py-4">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-sm-10 col-md-5 col-lg-4">
            <div class="card bg-blue text-body border border-light shadow-3d">
              <div class="card-body p-3">
                <h5 class="text-center text-body mb-3 fw-semibold">Sign Up</h5>
                <!-- Sign Up Form -->
                <form @submit.prevent="signup">
                  <!-- Username -->
                  <div class="mb-2">
                    <input
                      type="text"
                      v-model="user_name"
                      class="form-control form-control-sm custom-input"
                      placeholder="Username"
                      required
                    />
                  </div>
                  <!-- Email -->
                  <div class="mb-2">
                    <input
                      type="email"
                      v-model="user_email"
                      class="form-control form-control-sm custom-input"
                      placeholder="Email"
                      required
                    />
                  </div>
                  <!-- Password -->
                  <div class="mb-2">
                    <input
                      type="password"
                      v-model="user_password"
                      class="form-control form-control-sm custom-input"
                      placeholder="Password"
                      required
                    />
                  </div>
                  <!-- Full Name -->
                  <div class="mb-2">
                    <input
                      type="text"
                      v-model="user_complete_name"
                      class="form-control form-control-sm custom-input"
                      placeholder="Full Name"
                      required
                    />
                  </div>
                  <!-- Date of Birth -->
                  <div class="mb-2">
                    <input
                      type="date"
                      v-model="user_dob"
                      class="form-control form-control-sm custom-input"
                      required
                    />
                  </div>
                  <!-- Education Level Dropdown -->
                  <div class="mb-3">
                    <select
                      v-model="user_education_level"
                      class="form-select form-select-sm custom-input"
                      required
                    >
                      <option value="">Education Level</option>
                      <option value="High School">High School</option>
                      <option value="Bachelor's Degree">Bachelor's Degree</option>
                      <option value="Master's Degree">Master's Degree</option>
                      <option value="PhD">PhD</option>
                    </select>
                  </div>
                  <!-- Submit Button -->
                  <button type="submit" class="btn btn-success w-100 fw-semibold">
                    Sign Up as User
                  </button>
                </form>
                <!-- Link to Login page -->
                <p class="mt-2 text-center text-muted small fw-semibold">
                  Already have an account?
                  <router-link to="/login" class="text-success">Login here</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="text-center py-2 fw-bold">
      <div class="small">&copy; 2025 Quizdom. All rights reserved.</div>
    </footer>
  </div>
</template>

<script>
export default {
  // Component state: holds all user sign up form data
  data() {
    return {
      user_name: '',             // Username
      user_email: '',            // Email
      user_password: '',         // Password
      user_complete_name: '',    // Full Name
      user_dob: '',              // Date of Birth
      user_education_level: ''   // Education Level
    }
  },
  methods: {
    // Handles sign up form submission
    async signup() {
      try {
        // Send POST request to backend signup endpoint
        const response = await fetch('http://localhost:5000/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_name: this.user_name,
            user_email: this.user_email,
            user_password: this.user_password,
            user_complete_name: this.user_complete_name,
            user_dob: this.user_dob,
            user_education_level: this.user_education_level
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert(data.message || 'Signup successful');
          this.$router.push('/login'); // Redirect to login page
        } else {
          alert(data.message || 'Signup failed');
        }
      } catch (error) {
        console.error('Signup error:', error);
        alert('Network error - please try again');
      }
    }
  }
}
</script>

<style scoped>
/*
  Custom background and input styles for the signup page.
*/
.bg-sky {
  background-color: #d0f0ff; /* Light sky blue */
}
.bg-blue {
  background-color: #e0ecf1; /* Slightly deeper sky blue */
}
.custom-input {
  height: 32px !important; /* Slightly smaller than default */
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #a1b1c9, #ffffff); /* Lilac to Fuchsia */
}
.shadow-3d {
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 8px 20px rgba(0, 0, 0, 0.2); /* Deeper, layered 3D effect */
}
</style>