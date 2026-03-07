<template>
  <div class="reg-doc">
    <h4>Upcoming Appointments</h4>

    <table class="table table-primary" v-if="upcomingAppointments.length > 0">
      <thead>
        <tr>
          <th>Id</th>
          <th>Patient Name</th>
          <th>History</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appointment in upcomingAppointments" :key="appointment.id">
          <th>{{ appointment.id }}</th>
          <td>{{ appointment.patientName }}</td>

          <td>
            <router-link
              class="btn btn-warning"
              :to="`/updatePatient/${appointment.id}/${$route.params.id}`">
              Update
            </router-link>
          </td>

          <td>
            <button
              class="btn btn-success me-2"
              @click="completeTreatment(appointment.id)">
              Complete
            </button>

            <button
              class="btn btn-danger"
              @click="deleteRequest(appointment.id)">
              Cancel
            </button>
          </td>

        </tr>
      </tbody>
    </table>

    <div v-else class="text-danger-emphasis">
      No upcoming appointments found.
    </div>
  </div>


  <div class="reg-doc mt-5">
    <h4>Completed Treatments</h4>

    <table class="table table-success" v-if="completedAppointments.length > 0">
      <thead>
        <tr>
          <th>Id</th>
          <th>Patient Name</th>
          <th>View</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appointment in completedAppointments" :key="appointment.id">
          <th>{{ appointment.id }}</th>
          <td>{{ appointment.patientName }}</td>
          <td>
            <router-link
              class="btn btn-secondary"
              :to="`/viewTreatments/${appointment.patientId}/${$route.params.id}`">
              View
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="text-danger-emphasis">
      No completed treatments found.
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      upcomingAppointments: [],
      completedAppointments: [],
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token")
      const id = this.$route.params.id

      const response = await fetch(
        `http://127.0.0.1:5000/hms/doctorDashboard:${id}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (response.ok) {
        this.upcomingAppointments = data.upcomming_appointments || []
        this.completedAppointments = data.completed_appointments || []
        
      }

    } catch (error) {
      console.log(error)
    }
  },

  methods: {

    async completeTreatment(appointmentId) {
      try {
        const token = localStorage.getItem("token")

        const response = await fetch(
          `http://127.0.0.1:5000/hms/completeTreatment:${appointmentId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (response.ok) {
          const completed = this.upcomingAppointments.find(
            a => a.id === appointmentId
          )

          this.upcomingAppointments =
            this.upcomingAppointments.filter(a => a.id !== appointmentId)

          if (completed) {
            this.completedAppointments.push(completed)
          }
        }

      } catch (error) {
        console.log(error)
      }
    },

    async deleteRequest(appointmentId) {
      try {
        const token = localStorage.getItem("token")

        const confirmDelete = confirm("Are you sure you want to delete this appointment?")
        if (!confirmDelete) return

        const response = await fetch(
          `http://127.0.0.1:5000/hms/deleteRequest:${appointmentId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (response.ok) {
          this.upcomingAppointments =
            this.upcomingAppointments.filter(a => a.id !== appointmentId)
        }

      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>