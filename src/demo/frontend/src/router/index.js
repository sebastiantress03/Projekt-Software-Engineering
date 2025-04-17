// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoadView from '../views/LoadView.vue'
import TournamentPlan from '../views/TournamentPlan.vue'
import TournamentStep1 from '../views/TournamentStep1.vue'
import TournamentStep2 from '../views/TournamentStep2.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/step1', name: 'TournamentStep1', component: TournamentStep1 },
  { path: '/step2', name: 'TournamentStep2', component: TournamentStep2 },
  { path: '/load', name: 'LoadView', component: LoadView },
  { path: '/plan', name: 'TournamentPlan', component: TournamentPlan }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
