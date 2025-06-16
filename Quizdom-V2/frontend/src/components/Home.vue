<template>
  <div>
    <!--
      Navbar: Shows the Quizdom brand and links to home.
    -->
    <nav class="navbar navbar-light bg-sky px-4">
      <router-link class="navbar-brand fw-semibold display-6" to="/">QUIZDOM</router-link>
    </nav>

    <!--
      Hero Section: Main landing area with background image, title, and call-to-action buttons.
    -->
    <header class="bg-dark text-white position-relative">
      <!-- Background image for hero section, faded with opacity -->
      <img
        src="@/assets/images/quizdom.jpg"
        class="w-100 h-100 position-absolute top-0 start-0 object-fit-cover"
        style="z-index: 0; opacity: 0.4;"
        alt="Background"
      />
      <!--
        Main hero content: centered heading, subheading, and action buttons.
        Uses flexbox to center vertically and horizontally.
      -->
      <div class="container text-center d-flex flex-column justify-content-center align-items-center"
           style="height: 100vh; position: relative; z-index: 1;">
        <h1 class="display-4 fw-bold text-sky">Start With a Question.</h1>
        <p class="lead mb-4 text-ivory">
          Explore at your pace. Discover more than answers.
        </p>
        <div>
          <!-- Login and Signup buttons -->
          <router-link to="/login" class="btn btn-outline-primary me-2 fw-bold">Login</router-link>
          <router-link to="/signup" class="btn btn-secondary">Sign Up</router-link>
        </div>
      </div>
    </header>

    <!--
      Footer: Simple copyright notice.
    -->
    <footer class="bg-dark text-center py-3 fw-bold">
      <div class="small text-sky">&copy; 2025 Quizdom. All rights reserved.</div>
    </footer>
  </div>
</template>

<style scoped>
/* 
  Custom background and text color classes for the landing page.
*/
.bg-ivory {
  background-color: #f9f6ef; /* Warm off-white ivory tone */
}
.bg-sky {
  background-color: #bfd9e5; /* Light sky blue */
}
.text-sky {
  color: #d0f0ff; /* Light sky blue for headings and footer */
}
/* 
.hero-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* Optional: dark overlay for image 
  z-index: 0;
}
*/
</style>

