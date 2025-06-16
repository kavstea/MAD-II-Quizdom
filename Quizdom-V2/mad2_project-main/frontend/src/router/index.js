import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import Admin from '@/components/Admin.vue'
import Signup from '@/components/Signup.vue'
import Manage_Subject from '@/components/Manage_Subject.vue'
import Manage_Quiz from '@/components/Manage_Quiz.vue'
import Add_Question from '@/components/Add_Question.vue'
import View_Questions from '@/components/View_Questions.vue'
import User from '@/components/User.vue'
import StartQuiz from '@/components/StartQuiz.vue'
import User_Scorecard from '@/components/User_Scorecard.vue'
import Manage_User from '@/components/Manage_User.vue'
import Admin_Statistics from '@/components/Admin_Statistics.vue'
import User_Statistics from '@/components/User_Statistics.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/manage_subject',
      name: 'manage_subject',
      component: Manage_Subject,
    },
    {
      path: '/manage_quiz',
      name: 'manage_quiz',
      component: Manage_Quiz,
    },
    {
      path: '/add_question/:quiz_id',
      name: 'add_question',
      component: Add_Question,
    },
    {
      path: '/view_questions/:quiz_id',
      name: 'view_questions',
      component: View_Questions,
    },
    {
      path: '/user',
      name: 'user',
      component: User,
    },
    {
      path: '/start_quiz/:quiz_id',
      name: 'start_quiz',
      component: StartQuiz,
    },
    {
      path: '/user_scorecard',
      name: 'user_scorecard',
      component: User_Scorecard,
    },
    {
      path: '/manage_user',
      name: 'manage_user',
      component: Manage_User,
    },
    {
      path: '/admin_statistics',
      name: 'admin_statistics',
      component: Admin_Statistics,
    },
    {
      path: '/user_statistics',
      name: 'user_statistics',
      component: User_Statistics,
    },
  ],
})

export default router
