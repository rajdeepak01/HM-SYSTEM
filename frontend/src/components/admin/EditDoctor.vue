<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100vh">
    <h1 class="mb-4">Edit <span class="text-primary">HMS</span></h1>
    <p class="text-danger">{{ message }}</p>

    <div class="card" style="width: 350px">
      <div class="card-body p-4">
        <form @submit.prevent="editDoctor">

          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" v-model="form.userName">
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="form.email">
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="form.password">
          </div>

          <div class="mb-3">
            <label class="form-label">Specialization</label>
            <input type="text" class="form-control" v-model="form.specialization">
          </div>

          <div class="mb-3">
            <label class="form-label">Department</label>
            <input type="text" class="form-control" v-model="form.departmentName">
          </div>

          <div class="mb-3">
            <label class="form-label">Availability</label>
            <input type="text" class="form-control" v-model="form.availability">
          </div>

          <div class="mb-3">
            <label class="form-label">Dept Description</label>
            <input type="text" class="form-control" v-model="form.description">
          </div>

          <button type="submit" class="btn btn-primary w-100">
            Update
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "editDoctor",

  data() {
    return {
      id: null,
      form: {
        userName: "",
        email: "",
        password: "",
        specialization: "",
        departmentName: "",
        availability: "",
        description: ""
      },
      message: ""
    }
  },

  async mounted() {
    this.id = this.$route.params.id
    await this.loadDoctor()
  },

  methods: {

    async loadDoctor() {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/hms/editDoctor:${this.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        )

        if (!res.ok) {
          this.message = "Failed to load doctor data"
          return
        }

        const data = await res.json()

        this.form.userName = data.activeUser?.userName || ""
        this.form.email = data.activeUser?.email || ""
        this.form.specialization = data.doctor?.specialization || ""
        this.form.departmentName = data.department?.departmentName || ""
        this.form.availability = data.doctor?.availability || ""
        this.form.description = data.department?.description || ""

      } catch (err) {
        this.message = "Server error"
      }
    },

    async editDoctor() {

      const payload = {
        userName: this.form.userName,
        email: this.form.email,
        specialization: this.form.specialization,
        departmentName: this.form.departmentName,
        availability: this.form.availability,
        description: this.form.description
      }

      if (this.form.password) {
        payload.password = this.form.password
      }

      try {
        const res = await fetch(
          `http://127.0.0.1:5000/hms/editDoctor:${this.id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(payload)
          }
        )

        const data = await res.json()

        if (!res.ok) {
          this.message = data.message || "Update failed"
          return
        }

        this.message = data.message || "Doctor updated successfully"
        this.$router.push("/AdminDashboard")


      } catch (err) {
        this.message = "Update failed"
      }
    }

  }
}
</script>