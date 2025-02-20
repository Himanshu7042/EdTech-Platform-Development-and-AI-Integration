<template>
  <title>Register</title>
    <div class="tutor-registration">
      <header class="tutor-header">
        <h1>Tutor Registration</h1>
      </header>
      <div class="content">
        <h2>Available Courses</h2>
        <table class="courses-table">
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Course Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in courses" :key="course.courseId">
              <td>{{ course.courseId }}</td>
              <td>{{ course.courseName }}</td>
              <td>
                <button @click="showPopup(course)" class="apply-button">Apply</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="popupVisible" class="popup">
        <div class="popup-content">
          <span class="close-button" @click="popupVisible = false">&times;</span>
          <h2>Apply for {{ selectedCourse.courseName }}</h2>
          <p>Are you sure you want to apply for course ID: {{ selectedCourse.courseId }}?</p>
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
    name: 'TutorRegistration',
    data() {
      return {
        username: '',
        courses: [],
        selectedCourse: {},
        popupVisible: false,
      };
    },
    created() {
      this.fetchCourses();
      this.usernameInfo();
    },
    methods: {
      fetchCourses() {
        axiosFetch
          .get('/api/admin/courses')
          .then((response) => {
            this.courses = response.data;
          })
          .catch((error) => {
            console.error('An error occurred while fetching courses:', error.message);
          });
      },
      showPopup(course) {
        this.selectedCourse = course;
        this.popupVisible = true;
      },
      async handleSubmit() {
        await this.usernameInfo(); // Ensure usernameInfo completes before proceeding
        console.log('Applying for course:', this.selectedCourse);
        // Handle the apply logic here
        this.popupVisible = false;
        this.addRequest();
        this.updateRole();
      },
      addRequest() {
        axiosFetch
          .post('/api/tutor/add-request', { username: this.username, courseId: this.selectedCourse.courseId })
          .then((resp) => {
            console.log(resp.data);
          })
          .catch((error) => {
            console.error('Error in adding Request:', error);
          });
      },
      updateRole() {
        console.log('updating role for username:', this.username);
        axiosFetch
          .put('/api/update/role', { username: this.username, role: -1 })
          .then((resp) => {
            console.log(resp.data);
            this.$router.push({ name: 'status' });
          })
          .catch((error) => {
            console.error('Error updating role:', error);
          });
      },
      async usernameInfo() {
        try {
          const resp = await axiosFetch.get('/api/info/username');
          this.username = resp.data.username;
          console.log(this.username);
        } catch (error) {
          console.error('Error in getting username:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .tutor-registration {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #74ebd5 0%, #acb6e5 100%);
  }
  
  .tutor-header {
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