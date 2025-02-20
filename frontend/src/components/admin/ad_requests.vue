<template>
  <div class="admin-requests">
    <header class="admin-header">
      <h1>Admin Panel - Requests</h1>
      <div class="header-buttons">
        <button @click="goHome" class="header-button">Home</button>
        <button @click="handleLogout" class="header-button">Log Out</button>
      </div>
    </header>
    <div class="content">
      <div class="table-section">
        <h2>Pending Requests</h2>
        <table class="requests-table">
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Course Name</th>
              <th>Username</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in pendingRequests" :key="request.courseId">
              <td>{{ request.courseId }}</td>
              <td>{{ request.course_name }}</td>
              <td>{{ request.username }}</td>
              <td>
                <button @click="handleAccept(request)" class="action-button">Accept</button>
                <button @click="handleReject(request)" class="action-button">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-section">
        <h2>Accepted Requests</h2>
        <table class="requests-table">
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Course Name</th>
              <th>Username</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in acceptedRequests" :key="request.courseId">
              <td>{{ request.courseId }}</td>
              <td>{{ request.course_name }}</td>
              <td>{{ request.username }}</td>
              <td>
                <button @click="handleRevoke(request)" class="action-button">Revoke</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-section">
        <h2>Denied Requests</h2>
        <table class="requests-table">
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Course Name</th>
              <th>Username</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in deniedRequests" :key="request.courseId">
              <td>{{ request.courseId }}</td>
              <td>{{ request.course_name }}</td>
              <td>{{ request.username }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axiosFetch from '@/axios';

export default {
  name: 'AdminRequests',
  data() {
    return {
      pendingRequests: [],
      acceptedRequests: [],
      deniedRequests: [],
      role: null,
      username: null,
      courseId: null,
    };
  },
  created() {
    this.fetchRequests();
  },
  methods: {
    fetchRequests() {
      // Fetch pending requests
      axiosFetch.get('/api/admin/requests', { params: { role: -1 } })
        .then(response => {
          this.pendingRequests = response.data;
        })
        .catch(error => {
          console.error("Error fetching pending requests:", error);
        });

      // Fetch accepted requests
      axiosFetch.get('/api/admin/requests', { params: { role: 2 } })
        .then(response => {
          this.acceptedRequests = response.data;
        })
        .catch(error => {
          console.error("Error fetching accepted requests:", error);
        });

      // Fetch denied requests
      axiosFetch.get('/api/admin/requests', { params: { role: -2 } })
        .then(response => {
          this.deniedRequests = response.data;
        })
        .catch(error => {
          console.error("Error fetching denied requests:", error);
        });
    },
    updateRole() {
      axiosFetch.put('/api/update/role', { username: this.username, role: this.role })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(error => {
          console.error("Error updating role:", error);
        });
    },
    updateCourseTutor() {
      axiosFetch.put('/api/update/course-tutor', { username: this.username, courseId: this.courseId })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(error => {
          console.error("Error updating course tutor:", error);
        });
    },
    handleAccept(request) {
      this.username = request.username;
      this.role = 2;
      this.courseId = request.courseId;
      this.updateRole();
      this.updateCourseTutor();

      this.pendingRequests = this.pendingRequests.filter(req => req !== request);
      this.acceptedRequests.push(request);

      const user = request.username;
      this.pendingRequests = this.pendingRequests.filter(req => {
        if (req.courseId === request.courseId && req.username !== user) {
          this.username = req.username;
          this.role = -2;
          this.updateRole();
          this.deniedRequests.push(req);
          return false;
        }
        return true;
      });

      this.username = null;
      this.role = null;
      this.courseId = null;
    },
    handleReject(request) {
      this.username = request.username;
      this.role = -2;
      this.updateRole();

      this.pendingRequests = this.pendingRequests.filter(req => req !== request);
      this.deniedRequests.push(request);

      this.username = null;
      this.role = null;
    },
    handleRevoke(request) {
      this.username = request.username;
      this.role = -2;
      this.updateRole();

      this.acceptedRequests = this.acceptedRequests.filter(req => req !== request);
      this.pendingRequests.push(request);

      this.username = null;
      this.role = null;
    },
    handleLogout() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'landingPage' });
    },
    goHome() {
      this.$router.push({ name: 'admin' });
    }
  }
}
</script>

<style scoped>
.admin-requests {
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

.table-section {
  margin-bottom: 30px;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table th, .requests-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.requests-table th {
  background-color: #f4f4f4;
}

.action-button {
  background-color: #5c67f2;
  color: white;
  border: none;
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #4a54d4;
}
</style>
