<template>
  <div class="status-page">
    <h1>Status</h1>
    <div v-if="loading" class="status-message">
      <p>Loading your application status...</p>
    </div>
    <div v-else-if="role === -1" class="status-message">
      <p>Your application is under process for Tutor.</p>
    </div>
    <div v-else-if="role === -2" class="status-message">
      <p>Your application has been declined.</p>
    </div>
    <div v-else class="status-message">
      <p>Unknown status. Please contact support.</p>
    </div>
    <button @click="handleLogout" class="logout-button">Log Out</button>
  </div>
</template>

<script>
import axiosFetch from '@/axios';  // Adjust the import path according to your project structure

export default {
  name: 'StatusPage',
  data() {
    return {
      username: '',
      role: null,
      loading: true
    };
  },
  mounted() {
    this.fetchRole();
  },
  methods: {
    fetchRole() {
      this.usernameInfo().then(() => {
        axiosFetch.post('/api/get-role', { username: this.username }, { headers: { 'Content-Type': 'application/json' } })
          .then(response => {
            this.role = response.data.role;
            this.loading = false;
            console.log(this.role);
          })
          .catch(error => {
            console.error("Error fetching the role:", error);
            this.loading = false;
          });
      });
    },
    usernameInfo() {
      return axiosFetch.get('/api/info/username')
        .then(resp => {
          this.username = resp.data.username;
          console.log(this.username);
        })
        .catch(error => {
          console.error("Error in getting username:", error);
        });
    },
    handleLogout() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'landingPage' });
    }
  }
}
</script>

<style scoped>
.status-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
  animation: fadeIn 1.5s ease-in-out;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
  animation: slideIn 1s ease-in-out;
}

.status-message {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  animation: slideIn 1s ease-in-out;
}

.status-message p {
  font-size: 1.2rem;
  color: #333;
}

.logout-button {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: 20px;
}

.logout-button:hover {
  background-color: #e55a5a;
  transform: scale(1.05);
}

.logout-button:focus {
  outline: none;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes slideIn {
  0% {
    transform: translateY(50px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>