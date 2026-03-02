<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 120vh">
    <h4 class="mb-4">
      Update Treatment for <span class="text-primary">{{ patientName }}</span>
    </h4>

    <p class="text-danger-emphasis">{{ message }}</p>

    <div class="card" style="width: 400px">
      <div class="card-body p-4">
        <form @submit.prevent="saveTreatment">

          <div class="mb-3">
            <label class="form-label">Diagnosis</label>
            <input type="text" class="form-control" v-model="formdata.diagnosis" />
          </div>

          <div class="mb-3">
            <label class="form-label">Prescription</label>
            <input type="text" class="form-control" v-model="formdata.prescription" />
          </div>

          <div class="mb-3">
            <label class="form-label">Medicines</label>
            <input type="text" class="form-control" v-model="formdata.medicines" />
          </div>

          <div class="mb-3">
            <label class="form-label">Tests Done</label>
            <input type="text" class="form-control" v-model="formdata.tests_done" />
          </div>

          <div class="mb-3">
            <label class="form-label">Visit Type</label>
            <input type="text" class="form-control" v-model="formdata.visit_type" />
          </div>

          <div class="mb-3">
            <label class="form-label">Notes</label>
            <textarea class="form-control" v-model="formdata.notes"></textarea>
          </div>

          <button type="submit" class="btn btn-primary w-100">
            Save Treatment
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UpdatePatient",

  data() {
    return {
      patientName: "",
      message: "",
      formdata: {
        diagnosis: "",
        prescription: "",
        medicines: "",
        tests_done: "",
        visit_type: "",
        notes: "",
      }
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token")
      const appointmentId = this.$route.params.appointmentId
      const userId = this.$route.params.userId

      const response = await fetch(
        `http://127.0.0.1:5000/hms/updatePatient:${appointmentId}:${userId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const data = await response.json()

      if (response.ok) {
        this.patientName = data.patient.patient_name
      } else {
        this.message = data.message
      }

    } catch (error) {
      console.log(error)
      this.message = "Failed to load data"
    }
  },

  methods: {
    async saveTreatment() {
      try {
        const token = localStorage.getItem("token")
        const appointmentId = this.$route.params.appointmentId
        const userId = this.$route.params.userId

        const response = await fetch(
          `http://127.0.0.1:5000/hms/updatePatient:${appointmentId}:${userId}`,
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
          this.message = "Treatment saved successfully"
          this.formdata = {
            diagnosis: "",
            prescription: "",
            medicines: "",
            tests_done: "",
            visit_type: "",
            notes: "",
          }
        } else {
          this.message = data.message
        }

      } catch (error) {
        console.log(error)
        this.message = "Server error"
      }
    }
  }
}
</script>