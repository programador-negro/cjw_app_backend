import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'


import PeopleView from '../views/PeopleView.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import PrivilegesView from '../views/PrivilegesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'people',
          name: 'people',
          component: PeopleView
        },
        {
          path: 'assignments',
          name: 'assignments',
          component: AssignmentsView
        },
        {
          path: 'privileges',
          name: 'privileges',
          component: PrivilegesView
        }
      ]
    }
  ]
})

export default router