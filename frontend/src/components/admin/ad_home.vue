<template>
  <div class="admin-home">
    <header class="admin-header">
      <h1>Admin Panel</h1>
      <span class="username">{{ username }}</span>
      <div class="header-buttons">
        <button @click="handleRequests" class="header-button">Requests</button>
        <button @click="handleLogout" class="header-button">Log Out</button>
      </div>
    </header>
    <div class="content">
      <h2>Courses</h2>
      <table class="courses-table">
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Tutor ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in courses" :key="course.courseId">
            <td>{{ course.courseId }}</td>
            <td>{{ course.courseName }}</td>
            <td>{{ course.courseTutorId }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="plus-button" @click="showPopup = true">+</button>
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <span class="close-button" @click="showPopup = false">&times;</span>
        <h2>Add Course</h2>
        <form @submit.prevent="handleAddCourse">
          <div class="form-group">
            <label for="courseId">Course ID</label>
            <input type="text" id="courseId" v-model="Course.courseId" required />
          </div>
          <div class="form-group">
            <label for="courseName">Course Name</label>
            <input type="text" id="courseName" v-model="Course.courseName" required />
          </div>
          <button type="submit" class="submit-button">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axiosFetch from '@/axios';

export default {
  name: 'AdminHome',
  data() {
    return {
      showPopup: false,
      Course: {
        courseId: '',
        courseName: '',
      },
      courses: []
    };
  },
  created() {
    this.fetchCourses();
  },
  methods: {
    fetchCourses() {
      axiosFetch.get('/api/admin/courses')
        .then(response => {
          this.courses = response.data;
        })
        .catch(error => {
          console.error("An error occurred while fetching courses:", error.message);
        });
    },
    handleRequests() {
      this.$router.push({ name: 'adminRequest' });
      console.log("Requests button clicked");
    },
    handleLogout() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'landingPage' });
    },
    handleAddCourse() {
      console.log('Course Details:', this.Course);
      axiosFetch.post('/api/admin/courses', this.Course)
        .then(resp => {
          console.log(resp);
          this.showPopup = false; // Close popup after successful submission
          this.fetchCourses(); // Refresh the courses list
          this.Course = { courseId: '', courseName: '' }; // Reset form
        })
        .catch(error => {
          if (error.response && error.response.status === 409) {
            console.log("courseId should be unique.");
          } else {
            console.error("An error occurred:", error.message);
          }
        });
    }
  }
}
</script>

<style scoped>
.admin-home {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #74ebd5 0%, #acb6e5 100%);
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 20px;
  background-color: #3e4a61;
  color: white;
}

.username {
  font-size: 1.2rem;
}

.header-buttons {
  display: flex;
}

.header-button {
  background-color: #5c67f2;
  color: white;
  border: none;
  padding: 10px 15px;
  margin-left: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.header-button:hover {
  background-color: #4a54d4;
}

.content {
  flex: 1;
  width: 80%;
  padding: 20px;
  background-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  border-radius: 10px;
}

.courses-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.courses-table th, .courses-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.courses-table th {
  background-color: #f4f4f4;
}

.plus-button {
  position: fixed;
  right: 20px;
  bottom: 20px;
  background-color: #5c67f2;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 2rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.plus-button:hover {
  background-color: #4a54d4;
  transform: scale(1.1);
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.popup-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  cursor: pointer;
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

.submit-button {
  background-color: #5c67f2;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #4a54d4;
}
</style>
