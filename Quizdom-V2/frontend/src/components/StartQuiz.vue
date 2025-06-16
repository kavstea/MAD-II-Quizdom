<template>
  <!--
    Quiz Attempt Page
    - Shows quiz title, countdown timer, renders questions with options,
      handles submission and result display.
  -->
  <div class="bg-dark min-vh-100">
    <div class="container py-5 d-flex justify-content-center">
      <div class="card w-100 shadow-sm" style="max-width: 720px;">
        <!-- Quiz Title -->
        <div class="card-header text-center bg-secondary">
          <h2 class="fw-semibold mb-0 text-white">{{ QuizTitle }}</h2>
        </div>
        <div class="card-body bg-secondary">
          <!-- Timer badge -->
          <div class="d-flex justify-content-center mb-3">
            <span class="badge bg-warning fw-bold fs-4 text-dark px-3 py-2">
              ⏱ {{ formatTime }}
            </span>
          </div>

          <!-- Quiz Form: Show only if not submitted -->
          <div v-if="!QuizSubmitted">
            <form @submit.prevent="submitQuiz">
              <!-- Render each question and its options -->
              <div
                v-for="(question, index) in questions"
                :key="index"
                class="mb-3 p-3 border rounded bg-light"
              >
                <h6 class="fw-semibold mb-2" style="white-space: pre-line;">
                  {{ index + 1 }}. {{ question.question_text }}
                </h6>
                <!-- Render options as radio buttons -->
                <div
                  v-for="(option, optionIndex) in question.options"
                  :key="optionIndex"
                  class="form-check mb-1"
                >
                  <input
                    class="form-check-input"
                    type="radio"
                    :name="`question-${index}`"
                    :value="option"
                    v-model="userAnswers[question.question_id]"
                    :disabled="timeleft <= 0"
                  />
                  <label class="form-check-label">
                    {{ option }}
                  </label>
                </div>
              </div>
              <!-- Submit button -->
              <div class="text-center mt-4">
                <button type="submit" class="btn btn-success fw-bold px-4">Submit Quiz</button>
              </div>
            </form>
          </div>

          <!-- Results: Show after quiz is submitted -->
          <div v-else>
            <h4 class="d-flex justify-content-center mb-3 fw-bold text-white bg-info px-3 py-2">
              Your Score: {{ userScore }}/{{ maxScore }}
            </h4>
            <!-- Show each question, user's answer, and correct answer -->
            <div
              v-for="(question, index) in questions"
              :key="index"
              class="mb-3 p-3 border rounded bg-light"
            >
              <h6 class="fw-semibold" style="white-space: pre-line;">
                {{ index + 1 }}. {{ question.question_text }}
              </h6>
              <p
                :class="{
                  'text-danger fw-bold': userAnswers[question.question_id] !== question.question_answer,
                  'text-success fw-bold': userAnswers[question.question_id] === question.question_answer
                }"
              >
                Your Answer: {{ userAnswers[question.question_id] || 'Not Answered' }}
              </p>
              <p class="text-success fw-semibold mb-0">
                Correct Answer: {{ question.question_answer }}
              </p>
            </div>
            <!-- Close button to return to user dashboard -->
            <div class="d-flex justify-content-end">
              <router-link to="/user" class="btn text-white bg-primary fw-bold px-4">
                Close
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: "StartQuiz",
    data() {
        return {
            QuizTitle: "",         // Title of the quiz
            userAnswers: {},       // User's selected answers, keyed by question_id
            QuizSubmitted: false,  // Has the quiz been submitted?
            questions: [],         // Array of quiz questions (with options)
            timelimit: 0,          // Time limit for the quiz (seconds)
            timeleft: 0,           // Time left in seconds
            timer: null,           // Timer interval reference
            userScore: null,       // User's score after submission
            maxScore: null         // Maximum possible score (number of questions)
        }
    },
    computed: {
        // Formats timeleft as MM:SS for display
        formatTime() {
            const minutes = Math.floor(this.timeleft / 60);
            const seconds = this.timeleft % 60;
            return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        },
    },
    methods: {
        // Fetch quiz details and questions from backend API
        async loadQuiz() {
            const response = await fetch(`http://127.0.0.1:5000/start_quiz/${this.$route.params.quiz_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
            const data = await response.json();
            if (response.status !== 200) {
                alert(data.message);
                this.$router.push('/user'); 
                return;
            }
            this.QuizTitle = data.quiz_name;
            this.timelimit = data.time_limit;

            // Timer persists even after refresh using localStorage
            const storageKey = `quiz-${this.$route.params.quiz_id}-start`;
            const savedStart = localStorage.getItem(storageKey);
            if (savedStart) {
                const elapsed = Math.floor((Date.now() - savedStart) / 1000);
                this.timeleft = Math.max(this.timelimit - elapsed, 0);
            } else {
                this.timeleft = this.timelimit;
                localStorage.setItem(storageKey, Date.now().toString());
            }

            // Map backend question data to local format with options array and correct answer
            this.questions = data.questions.map(question => ({
                question_id: question.question_id,
                question_text: question.question_text,
                options: [
                  question.question_option_a, 
                  question.question_option_b, 
                  question.question_option_c, 
                  question.question_option_d
                ],
                // The correct answer is mapped to its text value (e.g., "Option 1" text)
                question_answer: question["question_option_" + question.question_answer]
            }));
        },
        // Start countdown timer for the quiz
        startCountdown() {
            this.timer = setInterval(() => {
                this.timeleft--;
                if (this.timeleft <= 0) {
                    clearInterval(this.timer);
                    this.QuizSubmitted = true;
                    this.submitQuiz();
                }
            }, 1000);
        },
        // Prepare answers for backend: map selected option text to a/b/c/d
        prepareAnswers() {
            const lettermap = ["a", "b", "c", "d"];
            const answers = {};
            this.questions.forEach(question => {
                answers[question.question_id] = lettermap[question.options.indexOf(this.userAnswers[question.question_id])];
            });
            return answers;
        },
        // Submit the quiz answers to backend and show results
        async submitQuiz() {
            clearInterval(this.timer);
            this.QuizSubmitted = true;
            // Remove quiz start time from localStorage
            localStorage.removeItem(`quiz-${this.$route.params.quiz_id}-start`);
            const payload = {
                question_answer: this.prepareAnswers()
            };
            const response = await fetch(`http://127.0.0.1:5000/start_quiz/${this.$route.params.quiz_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            this.userScore = data.score;
            this.maxScore = data.maximum_score;
        }
    },
    // Lifecycle hook: load quiz and start timer on mount
    mounted() {
        this.loadQuiz();
        this.startCountdown();
    }
}
</script>
