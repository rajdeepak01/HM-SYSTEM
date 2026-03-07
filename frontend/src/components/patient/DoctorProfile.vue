<template>
  <div>
    <i class="bi bi-person-circle fs-1"></i>

    <div class="details" v-for="doctor in doctorList" :key="doctor.doctorName">
      <p><strong>Name:</strong> {{ doctor.doctorName }}</p>
      <p><strong>Specialization:</strong> {{ doctor.specialization }}</p>
      <p v-if="doctor.availability == 'Available'">Status:<strong>Booking is Open</strong></p>
    </div>
    <button class="btn btn-primary" @click="$router.back()">Back</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      doctorList: [],
      message: "",
    };
  },

  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const id = this.$route.params.id;

      const response = await fetch(`http://127.0.0.1:5000/hms/doctorProfile:${id}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        this.doctorList = data.doctorList;
        console.log(data.doctorList);
      } else {
        this.message = data.message;
      }
    } catch (error) {
      console.log(error);
      this.message = "Something went wrong";
    }
  },
};
</script>

<style scoped>
.details {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 10px;
  border-radius: 5px;
}
</style>