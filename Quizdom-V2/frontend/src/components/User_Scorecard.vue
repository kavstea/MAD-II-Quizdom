<template>
  <!--
    User Scorecard Page
    - Shows a table of all the user's quiz scores.
    - Allows user to export their scores as a CSV file.
  -->
  <div class="bg-misty min-vh-100"> <!-- Root element with gradient background -->
    <!-- Back button in top-left corner to return to user dashboard -->
    <div class="d-flex justify-content-start">
      <router-link to="/user" class="btn btn-black fw-bold shadow-3d rounded px-3 py-1">⬅︎ Back</router-link>
    </div>

    <div class="container">
      <!-- Page Heading -->
      <h2 class="text-center fw-bold my-4">Scorecard</h2>  

      <!-- Export Button: triggers CSV export -->
      <div class="d-flex justify-content-end">
        <button class="btn btn-success" @click="exportScoresCSV">Export Scores as CSV</button>
      </div>

      <!-- Table of user scores -->
      <table class="table table-striped table-bordered mt-4">
        <thead>
          <tr>
            <th>Subject</th>
            <th>Chapter</th>
            <th>Quiz</th>
            <th>Your Score</th>
            <th>Maximum Score</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody>
          <!-- Render each score as a table row -->
          <tr v-for="score in userScores" :key="score.id">
            <td>{{ score.subject_name }}</td>
            <td>{{ score.chapter_name }}</td>
            <td>{{ score.quiz_name }}</td>
            <td>{{ score.score }}</td>
            <td>{{ score.maximum_score }}</td>
            <td>{{ score.percentage }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userScores: [] // Array to store all user quiz scores
    }
  },
  methods: {
    // Fetch all scores for the current user from backend API
    fetchScores() {
      fetch('http://127.0.0.1:5000/user_scorecard', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      })
        .then(response => response.json())
        .then(data => {
          this.userScores = data;
        })
    },
    // Trigger backend to export the user's scores as a CSV (emails or downloads)
    exportScoresCSV() {
      fetch('http://127.0.0.1:5000/export_details', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        }
      })
        .then(response => response.json())
        .then(data => {
            alert(data.message) // Notify user export started or completed
        })
        .catch(error => {
            console.error('Export error:', error);
        })
    }
  },
  // When the component is mounted, fetch all user scores from backend
  mounted() {
    this.fetchScores();
  }
}
</script>

<style scoped>
/* 
  Styles for the user scorecard page.
  Includes a soft blue gradient background.
*/
.bg-misty {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}
</style>