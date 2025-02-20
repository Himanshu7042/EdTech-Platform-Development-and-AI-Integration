<template>
    <div class="my-courses">
      <header class="header">
        <div class="username">{{ username }}</div>
        <button class="sign-out" @click="signOut">Sign Out</button>
      </header>
      <div class="content">
        <h1>Tutor Courses</h1>
        <div class="courses-grid">
          <div v-for="course in courses" :key="course.courseId" class="course-card">
            <div class="course-name">{{ course.courseName }}</div>
            <button @click="goToCoursePage(course.courseId,course.courseName)">Go to Course Page</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axiosFetch from '@/axios';
  
  export default {
    name: 'MyCourses',
    data() {
      return {
        username: null,
        courses: [],
      };
    },
    created() {
      this.fetchUsername();
    },
    methods: {
      async fetchUsername() {
        try {
          const resp = await axiosFetch.get('/api/info/username');
          this.username = resp.data.username;
          console.log(this.username);
          // Once username is fetched, fetch the courses
          await this.fetchCourses();
        } catch (error) {
          console.error("Error in getting username:", error);
        }
      },
      async fetchCourses() {
        try {
          console.log("My courses for Username:", this.username);
          const response = await axiosFetch.get('/api/tutor/course', { params: { username: this.username } });
          this.courses = response.data;
        } catch (error) {
          console.error("Error fetching courses:", error);
        }
      },
      signOut() {
        // Implement sign out logic
        localStorage.removeItem('authToken');
        this.$router.push({ name: 'landingPage' });
      },
      goToCoursePage(courseId,courseName) {
        // Navigate to the course page
        this.$router.push({ name: 'tutor', params: { courseId: courseId, courseName:courseName } })
      }
    }
  }
  </script>
  
  <style scoped>
  .my-courses {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #f0f9ff 0%, #cbebff 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .header {
    width: 100%;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #4a90e2;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .username {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .sign-out {
    background-color: #ff6b6b;
    color: #fff;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }
  
  .sign-out:hover {
    background-color: #e55a5a;
    transform: scale(1.05);
  }
  
  .content {
    width: 100%;
    max-width: 1200px;
    padding: 20px;
    text-align: center;
  }
  
  
  
  h1 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 30px;
  }
  
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .course-card {
    background-color: rgba(157, 153, 153, 0.9);
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-top: 20px;
    margin-left: 5px;
    margin-right: 5px;
    height: 200px; /* Increased height */
    width: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s ease;
  }
  
  .course-card:hover {
    transform: translateY(-5px);
  }
  
  .course-name {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 15px;
  }
  
  button {
    background-color: #48c6ef;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
    align-self: center;
  }
  
  button:hover {
    background-color: #36a2db;
    transform: scale(1.05);
  }
  </style>
  