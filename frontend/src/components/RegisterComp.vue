<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100vh">
    <h1 class="mb-4">Register to <span class="text-primary">HMS</span></h1>
    <p class="text-danger-emphasis">{{ message }}</p>
    <div class="card" style="width: 350px">
      <div class="card-body p-4">
        <form @submit.prevent="register">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" v-model="formdata.userName" />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="formdata.email" />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="formdata.password" />
          </div>

          <button type="submit" class="btn btn-primary w-100">Register</button>
          Existing user?
          <a href="/login">login here</a>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'RegisterComp',
  data() {
    return {
      formdata: {
        userName: '',
        email: '',
        password: '',
      },
      message: '',
    }
  },
  
  methods: {
    async register() {
      try {
        const response = await fetch('http://127.0.0.1:5000/hms/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formdata),
        })

        const data = await response.json()

        if (response.ok) {
          const token = data.token
          localStorage.setItem('token', token)
          localStorage.setItem('email', this.formdata.email)
          localStorage.setItem('role', data.role)
          this.$router.push({
            path: '/login',
            query: { message: 'Registration successful. Please login.' },
          })
        } else {
          this.message = data.message
        }
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>
