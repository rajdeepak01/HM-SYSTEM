<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">

      <router-link
        class="navbar-brand text-success"
        :to="dashboardLink">
        HM-System
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">

          <li class="nav-item">
            <router-link
              class="nav-link"
              :to="dashboardLink">
              Home
            </router-link>
          </li>

          <router-link
  class="nav-link"
  :to="`/setAvailability/${doctorId}`">
  Set Schedule
</router-link>

          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown">
              <i class="bi bi-person-circle fs-4"></i>
            </a>

            <ul class="dropdown-menu">
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
  name: "NavBarComp",

  computed: {
    doctorId() {
      return localStorage.getItem("userId")
    },

    dashboardLink() {
      return this.doctorId
        ? `/DoctorDashboard/${this.doctorId}`
        : "/login"
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("userId")
      this.$router.push("/login")
    }
  }
}
</script>