<template>
    <div class="container mt-4">

        <div v-if="results.length === 0" class="alert alert-warning mt-3">
            No users found.
        </div>

        <table v-else class="table table-info mt-3">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in results" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.userName }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.role }}</td>
                    <td>
                        <span>
                            {{ user.isBlock == '1' ? 'Blocked' : 'Active' }}
                        </span>
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
            results: []
        }
    },

    async mounted() {
        this.searchUsers()
    },

    watch: {
        '$route.query.search'() {
            this.searchUsers()
        }
    },

    methods: {
        async searchUsers() {
            const keyword = this.$route.query.search
            if (!keyword) return

            try {
                const token = localStorage.getItem('token')

                const response = await fetch(
                    `http://127.0.0.1:5000/hms/adminSearch?search=${keyword}`,
                    {
                        method: 'GET',
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )

                const data = await response.json()

                if (response.ok) {
                    this.results = data.activeUsers
                }
            } catch (error) {
                console.log(error)
            }
        }
    }
}
</script>