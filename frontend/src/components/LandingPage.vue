<template>
  <div class="mb-2">
   <h2> <router-link class="text-decoration-none" to="/">
    {{ message }}
  </router-link></h2>
  </div>

  <router-link class="link-success " to="/login"> Login </router-link>
  <router-link class="link-warning ms-4" to="/register"> Register </router-link>
  <router-view />
</template>
<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      message: '',
    }
  },
  mounted() {
    fetch('http://127.0.0.1:5000')
      .then((response) => response.json())
      .then((data) => {
        this.message = data.message
      })
      .catch((error) => {
        console.error(error)
      })
  },
}
</script>
