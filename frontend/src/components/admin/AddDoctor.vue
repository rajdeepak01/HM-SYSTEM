<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="height: 120vh">
    <h4 class="mb-4">Add Doctor to  <span class="text-primary">HMS</span></h4>
    <p class="text-danger-emphasis">{{ message }}</p>
    <div class="card" style="width: 350px">
      <div class="card-body p-4">
        <form @submit.prevent="addDoctor">
          <div class="mb-3">
            <label class="form-label">Doctor Name</label>
            <input type="text" class="form-control" v-model="formdata.doctorName" />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="formdata.email" />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="formdata.password" />
          </div>

          <div class="mb-3">
            <label class="form-label">Specialization</label>
            <input type="text" class="form-control" v-model="formdata.specialization" />
          </div>

          <div class="mb-3">
            <label class="form-label">Availability</label>
            <input type="text" class="form-control" v-model="formdata.availability" />
          </div>

          <div class="mb-3">
            <label class="form-label">Department Name</label>
            <input type="text" class="form-control" v-model="formdata.departmentName" />
          </div>

          <div class="mb-3">
            <label class="form-label">Deptment Description</label>
            <input type="text" class="form-control" v-model="formdata.deptDescription" />
          </div>
          
          <button type="submit" class="btn btn-primary w-100">Add</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AddDoctorComp',
  data() {
    return {
      formdata: {
        doctorName: '',
        email: '',
        password: '',
        specialization: "",
        availability: "", 
        departmentName: "",
        deptDescription: "",
      },
      message: '',
    }
  },
  
  methods: {
    async addDoctor() {
        console.log("Form Data:", this.formdata)
  try {
    const token = localStorage.getItem("token")

    if (!token) {
      this.message = "Unauthorized. Please login."
      return
    }
console.log("Token:", token)
    const response = await fetch('http://127.0.0.1:5000/hms/addDoctor', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(this.formdata),
    })

    const data = await response.json()

    if (response.ok) {
      this.message = "Doctor added successfully "

      this.formdata = {
        doctorName: '',
        email: '',
        password: '',
        specialization: "",
        availability: "", 
        departmentName: "",
        deptDescription: "",
      }

    } else {
      this.message = data.message || "Something went wrong"
    }

  } catch (error) {
    console.log(error)
    this.message = "Server error"
  }
},
  },
}
</script>
