<template>
  <title>Welcome</title>
    <div class="landing-page">
      <div class="content">
        <h1>Welcome to Virtual Learning Platform</h1>
        <button @click="goToAuth" class="start-button">Start Learning</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LandingPage',
    methods: {
      goToAuth() {
        this.$router.push({ name: 'auth' });
      }
    }
  }
  </script>
  
  <style scoped>
  .landing-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
  }
  
  .content {
    text-align: center;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 50px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }
  
  h1 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 20px;
  }
  
  .start-button {
    background-color: #5c67f2;
    color: white;
    border: none;
    padding: 15px 30px;
    font-size: 1.2rem;
    border-radius: 50px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .start-button:hover {
    background-color: #4a54d4;
  }
  
  .start-button:focus {
    outline: none;
  }
  </style>  