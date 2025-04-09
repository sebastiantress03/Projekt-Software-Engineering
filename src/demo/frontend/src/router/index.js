import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CreateTournament from '../views/CreateTournament.vue'
import LoadView from '../views/LoadView.vue' // <- Neue Datei einbinden

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/create', name: 'Create', component: CreateTournament },
  { path: '/load', name: 'Load', component: LoadView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
