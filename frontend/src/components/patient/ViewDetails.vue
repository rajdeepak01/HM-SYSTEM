<template>
  <div class="reg-doc">

    <h3>{{ departmentName }}</h3>

    <div class="mb-3">
      <strong>Description :</strong> {{ description }}
    </div>

    <table class="table table-primary" v-if="doctors.length > 0">

      <thead>
        <tr>
          <th>Doctor Name</th>
          <th>Specialization</th>
          <th>Availability</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="doctor in doctors" :key="doctor.id">

          <td>{{ doctor.doctorName }}</td>
          <td>{{ doctor.specialization }}</td>
          <td>{{ doctor.availability }}</td>

          <td>
          <td>
            <router-link :to="'/book/' + doctor.id" class="btn btn-primary">
              check Avability
            </router-link>
            <router-link :to="`/doctorProfile/${doctor.id}`" class="btn btn-success">
              Doctor Profile
            </router-link>
          </td>
          </td>

        </tr>

      </tbody>
    </table>

    <div v-else class="text-danger-emphasis">
      No doctors available.
    </div>

  </div>
</template>



<script>
export default {

  data() {
    return {
      departmentName: "",
      description: "",
      doctors: []
    }
  },

  async mounted() {

    try {

      const token = localStorage.getItem("token")
      const userId = localStorage.getItem("userId")
      const departmentId = this.$route.params.id

      const response = await fetch(`http://127.0.0.1:5000/hms/PatientDashboard:${userId}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      })

      const data = await response.json()

      if (response.ok) {

        const department = data.departments.find(
          dept => dept.id == departmentId
        )

        if (department) {
          this.departmentName = department.departmentName
          this.description = department.deptDescription
          this.doctors = department.doctors
        }

      }

    } catch (error) {
      console.log(error)
    }

  }

}
</script>