<template>
  <div class="bg-breeze min-vh-100">
    <!--
      Back button in top-left corner to return to admin dashboard
    -->
    <div class="d-flex justify-content-start">
      <router-link to="/admin" class="btn text-white fw-bold shadow-3d rounded px-3 py-1">⬅︎ BACK</router-link>
    </div>

    <div class="container py-4">
      <!-- Page Heading -->
      <h2 class="text-center text-white fw-bold mb-5">A D M I N - S T A T S</h2>
      <div class="row justify-content-center g-4">
        <!-- Bar Chart Card: Top Scores by Subject -->
        <div class="col-12 col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h3 class="card-title text-center fs-5 mb-4">Top Scores by Subject (All-Time, All Users)</h3>
              <div class="d-flex justify-content-center">
                <div style="width: 300px; height: 300px; position: relative;">
                  <!-- Bar chart (rendered when data is loaded) -->
                  <Bar v-if="loaded" :data="bardata" :options="baroptions" :key="chartKey"/>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Pie Chart Card: Quiz Attempts by Subject -->
        <div class="col-12 col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h3 class="card-title text-center fs-5 mb-4">Total Quiz Attempts by Subject</h3>
              <div class="d-flex justify-content-center">
                <div style="width: 300px; height: 300px; position: relative;">
                  <!-- Pie chart (rendered when data is loaded) -->
                  <Pie v-if="loaded" :data="pieData" :options="pieOptions" :key="chartKey"/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import Vue composition API helpers and chart components
import {ref, onMounted} from 'vue';
import {Bar, Pie} from 'vue-chartjs';
// Import chart.js modules for chart rendering
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    ArcElement,
    PieController
} from 'chart.js';

// Register all necessary chart.js components
ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    ArcElement,
    PieController
);

export default {
    components: {Bar, Pie},
    setup() {
        // Chart data and options as reactive references
        const bardata = ref({ labels: [], datasets: [] }); // Bar chart data
        const pieData = ref({ labels: [], datasets: [] }); // Pie chart data
        const chartKey = ref(0); // Used to force chart re-render
        const loaded = ref(false); // Only show charts when data is loaded

        // Bar chart options
        const baroptions = ref({
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'All-Time Highest Scores Achieved per Subject (Across All Users & Quizzes)',
                },
            },
        });
        // Pie chart options
        const pieOptions = ref({
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Total Number of Quiz Attempts Recorded per Subject',
                },
            },
        });

        // Fetch stats data from backend when component is mounted
        onMounted(async() => {
            const response = await fetch('http://127.0.0.1:5000/admin_stats', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }},
            );
            const data = await response.json();
            // Set bar chart data
            bardata.value.labels = data.bar_labels;
            bardata.value.datasets = [{
                label: 'Top Scores (in %)',
                data: data.bar_values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }]
            // Set pie chart data
            pieData.value.labels = data.pie_labels;
            pieData.value.datasets = [{
                label: 'User Attempts',
                data: data.pie_values,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1,
            }]
            loaded.value = true; // Show charts only after data is loaded
            chartKey.value++;    // Force chart re-render
        })
        // Expose chart data, options, and state to template
        return {bardata, baroptions, pieData, pieOptions, chartKey, loaded};
    }
};
</script>

<style scoped>
/*
  Background gradients for the admin stats page.
*/
.bg-pastel {
  background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}
.bg-breeze {
  background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
}
</style>