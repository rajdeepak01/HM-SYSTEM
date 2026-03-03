<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/adminDashboard" href="#">HMS</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link active" aria-current="page" to="/adminDashboard"
              >Home</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/adminDashboard/addDoctor">Add Doctor</router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-person-circle fs-4"></i>
            </a>
            <ul class="dropdown-menu">
              <li><button class="dropdown-item" @click="logout">Logout</button></li>
            </ul>
          </li>
        </ul>
        <form class="d-flex" role="search" @submit.prevent="handleSearch">
          <input
            v-model="searchKeyword"
            class="form-control me-2"
            type="search"
            placeholder="Search users..."
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBarComp',

  data() {
    return {
      searchKeyword: '',
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    },

    handleSearch() {
  if (!this.searchKeyword.trim()) return

  this.$router.push({
    path: "/adminDashboard/search",
    query: { search: this.searchKeyword }
  })
},
  },
}
</script>
