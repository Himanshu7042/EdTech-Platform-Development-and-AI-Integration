<template>
  <title>Register</title>
    <div class="learner-registration">
      <header class="learner-header">
        <h1>Learner Registration</h1>
      </header>
      <div class="content">
        <h2>Available Courses</h2>
        <table class="courses-table">
          <thead>
            <tr>
              <th>Select</th>
              <th>Course ID</th>
              <th>Course Name</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in courses" :key="course.courseId">
              <td>
                <input type="checkbox" :value="course" v-model="selectedCourses" />
              </td>
              <td>{{ course.courseId }}</td>
              <td>{{ course.courseName }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="showPopup" class="apply-button">Apply</button>
      </div>
      <div v-if="popupVisible" class="popup">
        <div class="popup-content">
          <span class="close-button" @click="popupVisible = false">&times;</span>
          <h2>Selected Courses</h2>
          <ul>
            <li v-for="course in selectedCourses" :key="course.courseId">
              {{ course.courseName }} (ID: {{ course.courseId }})
            </li>
          </ul>
          <div class="popup-buttons">
            <button @click="handleSubmit" class="submit-button">Submit</button>
            <button @click="popupVisible = false" class="cancel-button">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axiosFetch from '@/axios';
  
  export default {
    name: 'LearnerRegistration',
    data() {
      return {
        courses: [],
        selectedCourses: [],
        popupVisible: false,
        username: null
      };
    },
    mounted() {
      this.usernameInfo();
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
      showPopup() {
        if (this.selectedCourses.length < 1 || this.selectedCourses.length > 4) {
          alert('Please select between 1 and 4 courses.');
          return;
        }
        this.popupVisible = true;
      },
      handleSubmit() {
        for (let subject of this.selectedCourses) {
          console.log({'username': this.username,'courseId': subject.courseId})
          axiosFetch.post('/api/learner/add-course', {'username': this.username,'courseId': subject.courseId})
          .then(resp => console.log(resp.data.message))
          .catch(error => {
            console.error("Error adding courseId in Student Courses:", error);
          });
        }

        this.updateRole();
        this.popupVisible = false;
        this.$router.push({ name: 'learner-courses' });
      },
      usernameInfo() {
        axiosFetch.get('/api/info/username').then(resp => {
          this.username = resp.data.username
          console.log(this.username)
        })
        .catch(error => {
          console.error("Error in getting username:", error);
        });
      },
      updateRole() {
        this.usernameInfo();
        axiosFetch.put(`/api/update/role`, {'username':this.username,"role":1})
          .then(resp=> {
          console.log(resp.data)
        })
        .catch(error => {
          console.error("Error updating role:", error);
        });
      }
    }
  }
  </script>
  
  <style scoped>
  .learner-registration {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #74ebd5 0%, #acb6e5 100%);
  }
  
  .learner-header {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 20px;
    background-color: #3e4a61;
    color: white;
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
  
  .apply-button {
    background-color: #5c67f2;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 20px;
  }
  
  .apply-button:hover {
    background-color: #4a54d4;
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
  
  .popup-buttons {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .submit-button, .cancel-button {
    background-color: #5c67f2;
    color: white;
    border: none;
    padding: 10px 20px;
    margin: 0 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .submit-button:hover, .cancel-button:hover {
    background-color: #4a54d4;
  }
  </style>  