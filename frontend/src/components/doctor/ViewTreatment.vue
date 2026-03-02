<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="min-height: 100vh">

    <h4 class="mb-4">
      Treatment History for <span class="text-primary">{{ patientName }}</span>
    </h4>

    <div class="card mb-4" style="width: 600px"
         v-for="(treatment, index) in treatments"
         :key="index">

      <div class="card-body">

        <p><strong>Diagnosis:</strong> {{ treatment.diagnosis }}</p>
        <p><strong>Prescription:</strong> {{ treatment.prescription }}</p>
        <p><strong>Medicines:</strong> {{ treatment.medicines }}</p>
        <p><strong>Tests Done:</strong> {{ treatment.testsDone }}</p>
        <p><strong>Visit Type:</strong> {{ treatment.visitType }}</p>
        <p><strong>Notes:</strong> {{ treatment.notes }}</p>

      </div>
    </div>

    <div v-if="treatments.length === 0" class="text-danger">
      No treatments found.
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      treatments: [],
      patientName: ""
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token")
      const patientId = this.$route.params.patientId
      const userId = this.$route.params.userId

      const response = await fetch(
        `http://127.0.0.1:5000/hms/viewPatientTreatments:${patientId}:${userId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const data = await response.json()

      if (response.ok) {
        this.treatments = data.treatments
        this.patientName = data.patient.name
      }

    } catch (error) {
      console.log(error)
    }
  }
}
</script>