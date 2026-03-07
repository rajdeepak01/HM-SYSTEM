<template>

<div class="reg-doc">
    <h4>Departments</h4>

    <table class="table table-primary" v-if="departments.length > 0">
      <thead>
        <tr>
          <th>Department Name</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="department in departments" :key="department.id">
          <th>{{ department.departmentName }}</th>

          <td>
            <router-link
              class="btn btn-primary"
              :to="`/ViewDetails/${department.id}`">
              View Details
            </router-link>
          </td>

        </tr>
      </tbody>
    </table>

    <div v-else class="text-danger-emphasis">
      No Department found.
    </div>
</div>



<div class="reg-doc">
    <h4>Upcoming Appointments</h4>

    <table class="table table-success" v-if="appointments.length > 0">
      <thead>
        <tr>
          <th>Sr. No</th>
          <th>Doctor Name</th>
          <th>Department</th>
          <th>Date</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="(appointment,index) in appointments" :key="appointment.appointmentId">

          <td>{{ index + 1 }}</td>

          <td>{{ appointment.doctorName }}</td>

          <td>{{ appointment.department }}</td>

          <td>{{ appointment.date }}</td>

          <td>{{ appointment.status }}</td>
          
          <td><button class="btn btn-danger" @click="cancelAppointment(appointment.appointmentId)">Cancel</button></td>

        </tr>

      </tbody>
    </table>

    <div v-else class="text-danger-emphasis">
      No Appointments found.
    </div>
</div>

</template>



<script>

export default {

    data(){
        return {
            departments:[],
            appointments:[],
            message: ""
        }
    },

    async mounted() {

        try{

            const token = localStorage.getItem("token")
            // const userId = this.$route.params.userId
            const userId = localStorage.getItem("userId")
            
            const response = await fetch(
                `http://127.0.0.1:5000/hms/PatientDashboard:${userId}`,
                {
                    method: "GET",
                    headers: {
                        "Authorization":`Bearer ${token}`,
                        "Content-Type":"application/json"
                    },
                }
            )

            const data = await response.json()

            if (response.ok) {

                this.departments = data.departments || []
                this.appointments = data.appointments || []

                console.log("Departments:",this.departments)
                console.log("Appointments:",data.appointments)

            }

        }
        catch(error){

            console.log("Error:",error)

        }

    },
    methods: {
      async cancelAppointment(id){
        try{
          const token = localStorage.getItem("token")          
          const response = await fetch(`http://127.0.0.1:5000/hms/deleteAppointment:${id}`,{
            method: "DELETE",
            headers:{
              "Authorization": `Bearer ${token}`,
            }
          });
          const data = await response.json();
          if (response.ok){
            this.appointments = this.appointments.filter(appointment => appointment.appointmentId != id)
          } else{
            console.log(data.message);
            
          }
        }catch(error){
          console.log(error);
          
        }
      }
    }

}

</script>