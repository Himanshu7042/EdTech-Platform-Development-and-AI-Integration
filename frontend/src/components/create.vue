<template>
  <title>Create</title>
  <div class="create-page">
    <div class="create-container">
      <h1>Create Account</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="FormData.username" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="FormData.password" required />
        </div>
        <button type="submit" class="create-button">Create Account</button>
      </form>
      <p class="toggle-text">Already have an account? <router-link to="/auth">Sign In</router-link></p>
    </div>
    <div v-if="showPopup" class="popup-overlay">
      <div class="popup-content">
        <h2>Choose Your Role</h2>
        <button class="role-button" @click="handleRoleSelection('learner')">Learner</button>
        <button class="role-button" @click="handleRoleSelection('tutor')">Tutor</button>
      </div>
    </div>
  </div>
</template>

<script>
import axiosFetch from '@/axios';
export default {
  name: 'Create-page',
  data() {
    return {
      FormData: {
        username: '',
        password: '',
      },
      showPopup: false
    };
  },
  methods: {
    handleRegister() {
      // Handle registration logic here
      axiosFetch.post('/api/create', this.FormData).then(resp => {
        localStorage.setItem('authToken', resp.data.access_token)
        console.log(resp);
        this.showPopup = true; // Show the popup after successful registration
      })
      .catch(err => {
        console.log(err);
        console.log(this.FormData);
        console.log("Failed to sign up");
      });
    },
    handleRoleSelection(role) {
      if (role === 'learner') {
        this.$router.push({ name: 'learnerRegistration' });
      } else if (role === 'tutor') {
        this.$router.push({ name: 'tutorRegistration' });
      }
    }
  }
}
</script>

<style scoped>
.create-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
  animation: fadeIn 1.5s ease-in-out;
  position: relative;
}

.create-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  animation: slideIn 1s ease-in-out;
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

h1 {
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.create-button {
  background-color: #48c6ef;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.create-button:hover {
  background-color: #36a2db;
  transform: scale(1.05);
}

.create-button:focus {
  outline: none;
}

.toggle-text {
  margin-top: 15px;
  color: #333;
}

router-link {
  color: #48c6ef;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.role-button {
  background-color: #48c6ef;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin: 10px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.role-button:hover {
  background-color: #36a2db;
  transform: scale(1.05);
}
</style>
