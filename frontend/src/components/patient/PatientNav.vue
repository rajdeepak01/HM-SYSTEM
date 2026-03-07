<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">

      <router-link class="navbar-brand text-success" :to="dashboardLink">
        HM-System
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse">

        <ul class="navbar-nav me-auto">

          <li class="nav-item">
            <router-link class="nav-link" :to="dashboardLink">
              Home
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" :to="`/PatientHistoryComp/${userId}`">
              History
            </router-link>
          </li>

          <!-- EXPORT BUTTON -->
          <li class="nav-item">

            <button class="btn btn-link nav-link" @click="exportCSV" :disabled="loading">

              <span v-if="loading" class="spinner-border spinner-border-sm"></span>

              <span v-if="!loading">Export Treatments CSV</span>

              <span v-if="loading"> Generating...</span>

            </button>

          </li>

          <!-- STATUS -->
          <li v-if="exportStatus" class="nav-item">
            <span class="nav-link text-success">
              {{ exportStatus }}
            </span>
          </li>

          <!-- PROFILE -->
          <li class="nav-item dropdown">

            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
              <i class="bi bi-person-circle fs-4"></i>
            </a>

            <ul class="dropdown-menu">

              <li>
                <router-link :to="`/editProfile/${userId}`" class="dropdown-item">
                  Edit Profile
                </router-link>
              </li>

              <li>
                <button class="dropdown-item" @click="logout">
                  Logout
                </button>
              </li>

            </ul>

          </li>

        </ul>

      </div>
    </div>
  </nav>
</template>


<script>
export default {

  data() {
    return {
      taskId: null,
      exportStatus: "",
      interval: null,
      loading: false
    }
  },

  computed: {

    userId() {
      return localStorage.getItem("userId")
    },

    dashboardLink() {
      return this.userId
        ? `/PatientDashboard/${this.userId}`
        : "/login"
    }

  },

  methods: {

    async exportCSV() {

      try {

        this.loading = true
        this.exportStatus = ""

        const token = localStorage.getItem("token")

        if (!token) {
          this.$router.push("/login")
          return
        }

        const res = await fetch(
          "http://127.0.0.1:5000/hms/exportTreatmentCSV",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (!res.ok) {
          throw new Error("Export request failed")
        }

        const data = await res.json()

        this.taskId = data.task_id

        this.exportStatus = "Export started..."

        this.checkStatus()

      } catch (err) {

        console.error(err)
        this.exportStatus = "Export failed"
        this.loading = false

      }

    },


    checkStatus() {

      const token = localStorage.getItem("token")

      this.interval = setInterval(async () => {

        try {

          const res = await fetch(
            `http://127.0.0.1:5000/hms/exportStatus:${this.taskId}`,
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          )

          if (res.status === 401) {

            clearInterval(this.interval)
            this.$router.push("/login")
            return

          }

          const data = await res.json()

          // WAIT until task is finished
          if (!data.ready) {
            return
          }

          // STOP polling
          clearInterval(this.interval)

          this.loading = false

          // SUCCESS
          if (data.successful && data.download_url) {

            this.exportStatus = "Download ready"

            const fileUrl = `http://127.0.0.1:5000${data.download_url}`

            window.open(fileUrl)

          } else {

            this.exportStatus = "Export failed"

          }

        } catch (err) {

          console.error(err)

          clearInterval(this.interval)

          this.loading = false

          this.exportStatus = "Export failed"

        }

      }, 3000)

    },


    logout() {

      localStorage.removeItem("token")
      localStorage.removeItem("userId")

      this.$router.push("/login")

    }

  }

}
</script>