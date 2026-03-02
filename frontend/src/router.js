import { createRouter, createWebHistory } from 'vue-router'
import LoginComp from './components/LoginComp.vue'
import RegisterComp from './components/RegisterComp.vue'
import AdminDashboard from './components/admin/AdminDashboard.vue'
import LandingPage from './components/LandingPage.vue'
import AddDoctor from './components/admin/AddDoctor.vue'
import EditDoctor from './components/admin/EditDoctor.vue'
import UsersContent from './components/admin/UsersContent.vue'
import EditPatient from './components/EditPatient.vue'
import SearchResults from './components/SearchResults.vue'

const routes = [
  {
    path: '/',
    component: LandingPage,
    children: [
      {
        path: 'login',
        component: LoginComp,
      },
      {
        path: 'register',
        component: RegisterComp,
      },
    ],
  },
  {
    path: '/adminDashboard',
    component: AdminDashboard,
    children: [
      {
        path: '',
        component: UsersContent,
      },
      {
        path: 'addDoctor',
        component: AddDoctor,
      },
      {
        path: 'EditDoctor/:id',
        component: EditDoctor,
      },
      {
        path: 'EditPatient/:id',
        component: EditPatient,
      },
      {
        path: 'search',
        component: SearchResults,
      },
    ],
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})
export default router
