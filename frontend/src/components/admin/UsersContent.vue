<template>
  <div class="reg-doc">
    <h4>Registerd Doctors</h4>

    <table class="table table-primary">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Doctor Name</th>
          <th scope="col">specialization</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doctor in doctors" :key="doctor.userId">
          <th scope="row">{{ doctor.userId }}</th>
          <td>{{ doctor.doctorName }}</td>
          <td>{{ doctor.specialization }}</td>
          <td>
            <router-link type="button" class="btn btn-primary me-2"
              :to="`/adminDashboard/EditDoctor/${doctor.doctorId}`">Edit</router-link>

            <button type="button" class="btn me-2"
              :class="doctor.isBlock == '1' ? 'btn-success' : 'btn-warning'"
              @click="toggleBlock(doctor)">
              {{ doctor.isBlock == '1' ? 'Unblock' : 'Block' }}
            </button>

            <button type="button" class="btn btn-danger me-2"
              @click="deleteDoctor(doctor)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="reg-doc">
    <h4>Registerd Patients</h4>

    <table class="table table-success">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Patient Name</th>
          <th scope="col">Email</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="patient in patients" :key="patient.userId">
          <th scope="row">{{ patient.userId }}</th>
          <td>{{ patient.userName }}</td>
          <td>{{ patient.email }}</td>
          <td>
            <router-link type="button" class="btn btn-primary me-2"
              :to="`/adminDashboard/EditPatient/${patient.userId}`">Edit</router-link>

            <button type="button" class="btn me-2"
              :class="patient.isBlock == '1' ? 'btn-success' : 'btn-warning'"
              @click="toggleBlockPatient(patient)">
              {{ patient.isBlock == '1' ? 'Unblock' : 'Block' }}
            </button>

            <button type="button" class="btn btn-danger me-2"
              @click="deletePatient(patient)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="reg-doc">
    <h4>Upcommint Appointments</h4>

    <table class="table table-warning">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Patient Name</th>
          <th scope="col">Doctor Name</th>
          <th scope="col">View History</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">1</th>
          <td>Mark</td>
          <td>Otto</td>
          <td>
            <button type="button" class="btn btn-primary me-2">View</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      doctors: [],
      patients: [],
      appointments: [],
      message: '',
      err: '',
    }
  },

  watch: {
    '$route.query.search': {
      immediate: true,
      handler(newSearch) {
        if (newSearch) {
          this.searchUsers(newSearch)
        } else {
          this.loadData()
        }
      }
    }
  },

  mounted() {
    if (!this.$route.query.search) {
      this.loadData()
    }
  },

  methods: {

    async loadData() {
      try {
        const token = localStorage.getItem('token')

        const response = await fetch(
          'http://127.0.0.1:5000/hms/adminDashboard',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const data = await response.json()

        if (response.ok) {
          this.doctors = data.doctors
          this.patients = data.patients
        } else {
          this.err = data.message
        }
      } catch (error) {
        console.log(error)
      }
    },

    async searchUsers(keyword) {
      try {
        const token = localStorage.getItem('token')

        const response = await fetch(
          `http://127.0.0.1:5000/hms/adminSearch?search=${keyword}`,
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const data = await response.json()

        if (response.ok) {
          this.doctors = []
          this.patients = data.activeUsers
        } else {
          console.log(data.message)
        }
      } catch (error) {
        console.log(error)
      }
    },

    async toggleBlock(doctor) {
      const token = localStorage.getItem('token')

      try {
        let url = doctor.isBlock == '1'
          ? `http://127.0.0.1:5000/hms/unblockDoctor:${doctor.userId}`
          : `http://127.0.0.1:5000/hms/blockDoctor:${doctor.userId}`

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (response.ok) {
          doctor.isBlock = doctor.isBlock == '1' ? '0' : '1'
        }
      } catch (error) {
        console.log(error)
      }
    },

    async deleteDoctor(doctor) {
      const token = localStorage.getItem('token')

      if (!confirm('Are you sure you want to delete this doctor?')) return

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/hms/deleteDoctor:${doctor.userId}`,
          {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${token}` },
          }
        )

        if (response.ok) {
          this.doctors = this.doctors.filter(
            (d) => d.userId !== doctor.userId
          )
        }
      } catch (error) {
        console.log(error)
      }
    },

    async toggleBlockPatient(patient) {
      const token = localStorage.getItem('token')

      try {
        let url = patient.isBlock == '1'
          ? `http://127.0.0.1:5000/hms/unblockPatient:${patient.userId}`
          : `http://127.0.0.1:5000/hms/blockPatient:${patient.userId}`

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (response.ok) {
          patient.isBlock = patient.isBlock == '1' ? '0' : '1'
        }
      } catch (error) {
        console.log(error)
      }
    },

    async deletePatient(patient) {
      const token = localStorage.getItem('token')

      if (!confirm('Are you sure you want to delete this patient?')) return

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/hms/deletePatient:${patient.userId}`,
          {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${token}` },
          }
        )

        if (response.ok) {
          this.patients = this.patients.filter(
            (p) => p.userId !== patient.userId
          )
        }
      } catch (error) {
        console.log(error)
      }
    }
  },
}
</script>