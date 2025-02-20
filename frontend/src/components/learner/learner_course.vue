<template>
  <div class="main-tutor">
    <header class="header">
      <div class="username">{{ username }}</div>
      <h1>{{ courseName }}: Learner Portal</h1>
      <button class="sign-out" @click="signOut">Sign Out</button>
    </header>
    <div class="content">
      <aside class="sidebar">
        <ul>
          <li @click="selectSection('about')" :class="{ active: selectedTopic === 'about' }">About</li>
          <li v-for="topic in topics" :key="topic.id" class="topic">
            <div @click="toggleTopic(topic.id)" :class="{ active: selectedTopic === topic.id }">
              {{ topic.name }}
              <span class="arrow" :class="{ down: selectedTopic === topic.id }">&#9660;</span>
            </div>
            <ul v-if="selectedTopic === topic.id" class="topic-content">
              <li v-if="topic.content.video" @click="selectContent('video', topic.id)" :class="{ active: selectedContent === 'video' && selectedTopic === topic.id }">
                Video
              </li>
              <li v-if="topic.content.quiz" @click="selectContent('quiz', topic.id)" :class="{ active: selectedContent === 'quiz' && selectedTopic === topic.id }">
                Quiz
              </li>
              <li v-if="topic.content.codingQuiz" @click="selectContent('codingQuiz', topic.id)" :class="{ active: selectedContent === 'codingQuiz' && selectedTopic === topic.id }">
                Coding Quiz
              </li>
            </ul>
          </li>
        </ul>
      </aside>
      <main class="main-content">
        <div v-if="selectedTopic === 'about'">
          <p>This is all about Course information and About Instructor.</p>
        </div>
        <div v-else-if="selectedContent === 'video'">
          <h1>Video</h1>
          <div v-if="!video.link">
            <p>The content will be added soon</p>
          </div>
          <div v-else>
            <iframe :src="video.link" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
        <div v-else-if="selectedContent === 'quiz'">
          <h1>Quiz</h1>
          <div v-if="quizQuestions.length === 0">
            <p>The content will be added soon</p>
          </div>
          <form v-else @submit.prevent="submitQuiz">
            <ol>
              <li v-for="question in quizQuestions" :key="question.id">
                <div>{{ question.question }}</div>
                <ul>
                  <li v-for="(option, index) in question.options" :key="index">
                    <label>
                      <input type="radio" :name="'question-' + question.id" :value="option" v-model="userAnswers[question.id]" />
                      {{ option }}
                    </label>
                  </li>
                </ul>
                <!-- Show correct or incorrect sign after submission -->
                <div v-if="submitted">
                  <span v-if="userAnswers[question.id] === question.correct_option" style="color: green;">&#10004; Correct</span>
                  <span v-else style="color: red;">&#10008; Incorrect</span>
                  <div><strong>Correct Answer:</strong> {{ question.correct_option }}</div>
                </div>
              </li>
            </ol>
            <button type="submit">Submit</button>
          </form>
          <!-- Display cumulative score after submission -->
          <div v-if="submitted">
            <h2>Your Score: {{ score }} / {{ quizQuestions.length }}</h2>
          </div>
        </div>
        <div v-else-if="selectedContent === 'codingQuiz'">
          <div v-if="!codingQuiz.question">
            <p>The content will be added soon</p>
          </div>
          <div v-else>
            <div><strong>Programming language: </strong>{{ codingQuiz.language }} </div>
            <p>{{ codingQuiz.question }}</p>
            <p>Input: {{ codingQuiz.test_cases[0] }}</p>
            <p>Expected Output: {{ codingQuiz.test_cases[1] }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axiosFetch from '@/axios';

export default {
  name: 'MainLearner',
  props: ['courseId', 'courseName'],
  data() {
    return {
      username: null,
      currentQuizId: null,
      selectedTopic: 'about',
      selectedContent: null,
      topics: [],
      video: {},
      quizQuestions: [], // Ensure this is initialized as an empty array
      codingQuiz: {},
      userAnswers: {}, // Store user's answers
      score: 0, // Store user's score
      submitted: false // Track if the quiz has been submitted
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
        await this.fetchTopics();
      } catch (error) {
        console.error("Error in getting username:", error);
      }
    },
    async fetchTopics() {
      try {
        const resp = await axiosFetch.get(`/api/learner/course/get-topics`, { params: { courseId: this.courseId } });
        this.topics = resp.data;
      } catch (error) {
        console.error("Error fetching topics:", error);
      }
    },
    selectSection(section) {
      this.selectedTopic = section;
      this.selectedContent = null;
    },
    toggleTopic(topicId) {
      this.selectedTopic = this.selectedTopic === topicId ? null : topicId;
      this.selectedContent = null;
    },
    async selectContent(content, topicId) {
      this.selectedContent = content;
      this.selectedTopic = topicId;
      await this.fetchContent(topicId);
    },
    async fetchContent(topicId) {
      try {
        const resp = await axiosFetch.get(`/api/learner/topic/content`, { params: { 'topicId': topicId, 'type': this.selectedContent } });
        const content = resp.data;

        if (content.type === 'video') {
          this.video = content.details;
          this.quizQuestions = [];
          this.codingQuiz = {};
        } else if (content.type === 'quiz') {
          this.currentQuizId = content.quizId;
          this.quizQuestions = content.details || []; // Ensure it's an array
          this.video = {};
          this.codingQuiz = {};
          this.userAnswers = {}; // Reset user answers
          this.submitted = false; // Reset submission status
          this.score = 0; // Reset score
        } else if (content.type === 'codingQuiz') {
          this.codingQuiz = content.details;
          this.video = {};
          this.quizQuestions = [];
        }

      } catch (error) {
        console.error("Error fetching topic content:", error);
      }
    },
    submitQuiz() {
      this.submitted = true;
      this.calculateScore();
    },
    calculateScore() {
      this.score = 0;
      this.quizQuestions.forEach(question => {
        if (this.userAnswers[question.id] === question.correct_option) {
          this.score++;
        }
      });
    },
    signOut() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'landingPage' });
    }
  }
};
</script>

<style scoped>
.main-tutor {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #53df7d;
  color: white;
  padding: 10px;
}
.username {
  font-size: 1.2em;
}
.sign-out {
  background-color: rgb(0, 157, 255);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}
.content {
  display: flex;
  flex: 1;
}
.sidebar {
  width: 250px;
  background-color: #f5f5f5;
  padding: 10px;
  border-right: 1px solid #ddd;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}
.sidebar li.active {
  background-color: #ddd;
}
.arrow {
  float: right;
  transition: transform 0.3s ease;
}
.arrow.down {
  transform: rotate(180deg);
}
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
