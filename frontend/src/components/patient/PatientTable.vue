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
</template>

<script>
export default{
    data(){
        return {
            departments:[],
            message: ""
        }
    },
    async mounted() {
        try{
            const token = localStorage.getItem("token")            
            const userId = this.$route.params.userId
            console.log(userId);
            
            const response = await fetch(`http://127.0.0.1:5000/hms/PatientDashboard:${userId}`,{
                method: "GET",
                headers: {
                    "Authorization":`Bearer ${token}`
                },
            });

            const data = await response.json();
            if (response.ok) {
                this.departments = data.departments || []
                
            }
        }catch(error){
            console.log(error);
            
        }
    }
}
</script>