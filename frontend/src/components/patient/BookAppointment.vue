<template>
    <div class="container">

        <h3>Book Appointment</h3>

        <h4>{{ doctorName }}</h4>

        <table class="table table-bordered">

            <thead>
                <tr>
                    <th>Date</th>
                    <th>Morning</th>
                    <th>Evening</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="slot in slots" :key="slot.date">

                    <td>{{ slot.date }}</td>

                    <td>
                        <button v-if="slot.morningSlot" class="btn btn-success" @click="book(slot, '09:00')">
                            Book
                        </button>

                        <span v-else>Not Available</span>
                    </td>

                    <td>
                        <button v-if="slot.eveningSlot" class="btn btn-success" @click="book(slot, '17:00')">
                            Book
                        </button>

                        <span v-else>Not Available</span>
                    </td>

                </tr>

            </tbody>

        </table>

    </div>
</template>

<script>

export default {

    data() {
        return {
            doctorName: "",
            slots: []
        }
    },

    async mounted() {

        const doctorId = this.$route.params.doctorId

        const token = localStorage.getItem("token")

        const response = await fetch(
            `http://127.0.0.1:5000/hms/doctorAvailability:${doctorId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

        const data = await response.json()

        this.doctorName = data.doctorName
        this.slots = data.availability

    },

    methods: {

        async book(slot, time) {

            const token = localStorage.getItem("token")
            const userId = localStorage.getItem("userId")

            const response = await fetch(
                "http://127.0.0.1:5000/hms/bookAppointment",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        doctorId: slot.doctorId,
                        userId: userId,
                        date: slot.date,
                        time: time
                    })
                })

            const data = await response.json()

            alert(data.message)

        }

    }

}

</script>