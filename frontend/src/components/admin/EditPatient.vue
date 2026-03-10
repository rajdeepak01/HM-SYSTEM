<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100vh">
    <h1 class="mb-4">Edit <span class="text-primary">HMS</span></h1>
    <p class="text-danger">{{ message }}</p>

    <div class="card" style="width: 350px">
      <div class="card-body p-4">
        <form @submit.prevent="editPatient">

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
  name: "editPatient",

  data() {
    return {
      id: null,
      form: {
        userName: "",
        email: "",
        password: "",
      },
      message: ""
    }
  },

  async mounted() {
    this.id = this.$route.params.id
    await this.loadpatients()
  },

  methods: {

    async loadpatients() {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/hms/editPatient:${this.id}`,
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
      } catch (err) {
        this.message = "Server error"
      }
    },

    async editPatient() {

      const payload = {
        userName: this.form.userName,
        email: this.form.email,
      }

      if (this.form.password) {
        payload.password = this.form.password
      }

      try {
        const res = await fetch(
          `http://127.0.0.1:5000/hms/editPatient:${this.id}`,
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

        this.message = data.message || "Patient updated successfully"

      } catch (err) {
        this.message = "Update failed"
      }
    }

  }
}
</script>