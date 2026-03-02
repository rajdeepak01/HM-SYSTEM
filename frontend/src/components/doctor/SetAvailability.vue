<template>
  <div class="d-flex flex-column align-items-center" style="min-height: 100vh">

    <h4 class="mb-4 mt-4">
      Set Availability for <span class="text-primary">{{ doctorName }}</span>
    </h4>

    <p class="text-success">{{ message }}</p>

    <div class="card mb-4" style="width: 350px">
      <div class="card-body p-4">

        <form @submit.prevent="setAvailability">

          <div class="mb-3">
            <label class="form-label">Select Date</label>
            <input
              type="date"
              class="form-control"
              v-model="formdata.date"
              :min="min_date"
              :max="max_date"
            />
          </div>

          <div class="form-check mb-2">
            <input type="checkbox"
                   class="form-check-input"
                   v-model="formdata.morningSlot" />
            <label class="form-check-label">Morning Slot</label>
          </div>

          <div class="form-check mb-3">
            <input type="checkbox"
                   class="form-check-input"
                   v-model="formdata.eveningSlot" />
            <label class="form-check-label">Evening Slot</label>
          </div>

          <button type="submit" class="btn btn-primary w-100">
            Save Availability
          </button>

        </form>
      </div>
    </div>

    <!-- Availability Table -->
    <div style="width: 600px" v-if="availabilities.length > 0">
      <h5 class="mb-3">Your Set Availability</h5>

      <table class="table table-success">
        <thead>
          <tr>
            <th>Date</th>
            <th>Morning</th>
            <th>Evening</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(a, index) in availabilities" :key="index">
            <td>{{ a.date }}</td>
            <td>
              <span v-if="a.morningSlot" class="badge bg-success">Available</span>
              <span v-else class="badge bg-secondary">Not Set</span>
            </td>
            <td>
              <span v-if="a.eveningSlot" class="badge bg-success">Available</span>
              <span v-else class="badge bg-secondary">Not Set</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>
<script>
export default {
  name: "SetAvailability",

  data() {
    return {
      doctorName: "",
      min_date: "",
      max_date: "",
      message: "",
      availabilities: [],
      formdata: {
        date: "",
        morningSlot: false,
        eveningSlot: false
      }
    }
  },

  async mounted() {
    await this.loadAvailability()
  },

  methods: {

    async loadAvailability() {
      try {
        const token = localStorage.getItem("token")
        const userId = this.$route.params.userId

        const response = await fetch(
          `http://127.0.0.1:5000/hms/setAvailability:${userId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        const data = await response.json()

        if (response.ok) {
          this.min_date = data.min_date
          this.max_date = data.max_date
          this.doctorName = data.this_doctor.username
          this.availabilities = data.availabilities
        }

      } catch (error) {
        console.log(error)
      }
    },

    async setAvailability() {
      try {
        const token = localStorage.getItem("token")
        const userId = this.$route.params.userId

        const response = await fetch(
          `http://127.0.0.1:5000/hms/setAvailability:${userId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(this.formdata)
          }
        )

        const data = await response.json()

        if (response.ok) {
          this.message = data.message
          this.formdata.date = ""
          this.formdata.morningSlot = false
          this.formdata.eveningSlot = false
          await this.loadAvailability()
        }

      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>