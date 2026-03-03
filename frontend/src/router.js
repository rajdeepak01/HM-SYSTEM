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
import DoctorDashboard from './components/doctor/DoctorDashboard.vue'
import DoctorTable from './components/doctor/DoctorTable.vue'
import UpdatePatient from './components/doctor/UpdatePatient.vue'
import ViewTreatment from './components/doctor/ViewTreatment.vue'
import SetAvailability from './components/doctor/SetAvailability.vue'
import PatientHistory from './components/admin/PatientHistory.vue'

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
      {
        path: "AdminViewTreatments/:patientId/:userId",
        component: PatientHistory
      },
    ],
  },
  {
    path: "/DoctorDashboard/:id",
    component: DoctorDashboard,
    children: [
      {
        path: "",
        component: DoctorTable,
      },
      {
        path: "/updatePatient/:appointmentId/:userId",
        component: UpdatePatient
      },
      {
        path: "/viewTreatments/:patientId/:userId",
        component: ViewTreatment
      },
      {
        path: "/setAvailability/:userId",
        component: SetAvailability
      }
    ]
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})
export default router
