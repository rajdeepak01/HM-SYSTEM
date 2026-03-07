<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100vh">
    <h1 class="mb-4">Edit Your <span class="text-primary">Profile</span></h1>

    <p class="text-danger-emphasis">{{ message }}</p>

    <div class="card shadow" style="width: 350px">
      <div class="card-body p-4">

        <form @submit.prevent="editProfile">

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

          <button type="submit" class="btn btn-primary w-100">
            Update Profile
          </button>

        </form>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formdata: {
        userName: "",
        email: "",
        password: ""
      },
      message: ""
    }
  },

  async mounted() {

    const id = localStorage.getItem("userId")
    const token = localStorage.getItem("token")

    const response = await fetch(`http://127.0.0.1:5000/hms/editProfile:${id}`,{
      headers:{
        Authorization:`Bearer ${token}`
      }
    })

    const data = await response.json()

    if(response.ok){
      this.formdata.userName = data.userName
      this.formdata.email = data.email
    }

  },

  methods: {

    async editProfile(){

      try{

        const id = localStorage.getItem("userId")
        const token = localStorage.getItem("token")

        const response = await fetch(`http://127.0.0.1:5000/hms/editProfile:${id}`,{
          method:"POST",
          headers:{
            "Content-Type":"application/json",
            Authorization:`Bearer ${token}`
          },
          body: JSON.stringify(this.formdata)
        })

        const data = await response.json()

        if(response.ok){
          this.message = data.message
        }
        else{
          this.message = data.message
        }

      }catch(error){
        console.log(error)
      }

    }

  }
}
</script>