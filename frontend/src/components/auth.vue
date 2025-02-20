<template>
  <title>Log In</title>
  <div class="auth-page">
    <div class="auth-container">
      <h1>Sign In</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="FormData.username" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="FormData.password" required />
        </div>
        <button type="submit" class="auth-button">Sign In</button>
      </form>
      <p class="toggle-text">Don't have an account? <router-link to="/create">Create Account</router-link></p>
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
  name: 'Auth-page',
  data() {
    return {
      FormData : {
        username: '',
        password: '',
      },
      showPopup: false
    };
  },
  methods: {
    handleLogin() {
      // Handle login logic here
      axiosFetch.post('/api/login', this.FormData).then(resp => {
      const { username, role, access_token } = resp.data;
      localStorage.setItem('authToken', access_token)
      if(role==3){
        console.log(username)
        this.$router.push({ name: 'admin', params: { username: username } });
      }
      else if(role==2){
        //tutor
        this.$router.push({ name: 'tutor-course' });
      } else if(role==1){
        // student
        this.$router.push({ name: 'learner-courses' });
      }
      
      else if (role==0){
        // registeration
        this.showPopup = true; // Show the popup after successful registration
        this.handleRoleSelection();
      }
      else {
        this.$router.push({ name: 'status' });
      }
      })          
      .catch(err => {
        console.log(err)
        console.log("Failed to sign in")
      })
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
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
  animation: fadeIn 1.5s ease-in-out;
}

.auth-container {
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

.auth-button {
  background-color: #ff7e5f;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.auth-button:hover {
  background-color: #eb5a45;
  transform: scale(1.05);
}

.auth-button:focus {
  outline: none;
}

.toggle-text {
  margin-top: 15px;
  color: #333;
}

router-link {
  color: #ff7e5f;
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
