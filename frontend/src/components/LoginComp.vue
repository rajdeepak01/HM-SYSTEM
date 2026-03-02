<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 75vh">
    <h1 class="mb-4">Login to <span class="text-primary">HMS</span></h1>
    <p class="text-danger-emphasis">{{ message }}</p>

    <div class="card" style="width: 350px">
      <div class="card-body p-4">
        <form @submit.prevent="login">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="formdata.email" />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="formdata.password" />
          </div>

          <button type="submit" class="btn btn-primary w-100">Login</button> new user?
          <a href="/register">Register here</a>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'LoginComp',
  data() {
    return {
      formdata: {
        email: '',
        password: '',
      },
      message: '',
    }
  },
  mounted() {
  if (this.$route.query.message) {
    this.message = this.$route.query.message
  }
},
  methods: {
    async login() {
   try {
        const response = await fetch('http://127.0.0.1:5000/hms/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formdata),
        })

        const data = await response.json()

        if (response.ok) {
          localStorage.setItem('token', data.authToken)
          localStorage.setItem('email', this.formdata.email)
          localStorage.setItem('role', data.role)
          localStorage.setItem("userId", data.userId)
            console.log(data);

          if (data.role == 'admin') {
            this.$router.push('/adminDashboard')
          }
          if (data.role == "doctor"){
            this.$router.push(`/DoctorDashboard/${data.userId}`)
              
          }
          
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
