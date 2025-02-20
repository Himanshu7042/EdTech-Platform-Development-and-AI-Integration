<template>
  <div class="main-tutor">
    <header class="header">
      <div class="username">{{ username }}</div>
      <h1>{{courseName}}: Tutor Portal</h1>
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
        <button class="add-content" @click="showAddContentPopup = true">Add Content</button>
      </aside>
      <main class="main-content">
        <div v-if="selectedTopic === 'about'">
          <p>This is all about Course information and About Instructor.</p>
        </div>
        <div v-else-if="selectedContent === 'video'">
          <h1>video</h1>
          <div v-if="!video.link">
            <input type="text" v-model="newVideoLink" placeholder="Enter video link">
            <button @click="addVideo">Submit</button>
          </div>
          <div v-else>
            <iframe :src="video.link" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
        <div v-else-if="selectedContent === 'quiz'">
            <ol>
              <ul>
                <li v-for="question in quizQuestions" :key="question.id">
                  <!-- Display the question -->
                  <div>{{ question.question }}</div>
                  
                  <!-- Display the options -->
                  <ul>
                    <li v-for="(option, index) in question.options" :key="index">
                      {{ option }}
                    </li>
                  </ul>
                  
                  <!-- Display the correct answer -->
                  <div><strong>Correct Answer:</strong> {{ question.correct_option }}</div>
                </li>
              </ul>
            </ol>
        
            <button @click="showAddQuizQuestionPopup = true">Add Questions</button>
          
        </div>
        <div v-else-if="selectedContent === 'codingQuiz'">
          <div v-if="!codingQuiz.question">
            <div>
              <textarea style="width: 100%;" v-model="newCodingLanguage" placeholder="Enter Programming language Name in lower case"></textarea>
            </div>
            <div>
  
              <textarea style="width: 100%;" v-model="newCodingQuizQuestion" placeholder="Enter Programmng question"></textarea>
            </div>
            
            <div>
              <textarea style="width: 100%;" v-model="newCodingQuizInput" placeholder="Enter Input"></textarea>
            </div>
            
            <div>
              <textarea style="width: 100%;" v-model="newCodingQuizOutput" placeholder="Enter Output"></textarea>
            </div>
            
            <div>
              <button @click="addCodingQuiz">Submit</button>
            </div>

          </div>
          <div v-else>
            <div><strong>Programming language : </strong>{{ codingQuiz.language }} </div>
            <p>{{ codingQuiz.question }}</p>
            <p>Input: {{ codingQuiz.test_cases[0] }}</p>
            <p>Expected Output: {{ codingQuiz.test_cases[1] }}</p>
          </div>
        </div>
      </main>
    </div>

    <!-- Add Topic Popup -->
    <div v-if="showAddContentPopup" class="popup">
      <div class="popup-content">
        <button @click="showAddContentPopup = false">X</button>
        <h2>Add Topic</h2>
        <input type="text" v-model="newTopicData.newTopicName" placeholder="Enter topic name">
        <label>
          <input type="checkbox" v-model="newTopicData.includeVideo"> Video
        </label>
        <label>
          <input type="checkbox" v-model="newTopicData.includeQuiz"> Quiz
        </label>
        <label>
          <input type="checkbox" v-model="newTopicData.includeCodingQuiz"> Coding Quiz
        </label>
        <button id="addTopicBtnSbt" @click="addTopic">Submit</button>
      </div>
    </div>

    <!-- Add Quiz Question Popup -->
    <div v-if="showAddQuizQuestionPopup" class="popup">
      <div class="popup-content">
        <h2>Add Quiz Question</h2>
        <textarea v-model="newQuizQuestion" placeholder="Enter question"></textarea>
        <input type="text" v-model="newQuizOption1" placeholder="Option 1">
        <input type="text" v-model="newQuizOption2" placeholder="Option 2">
        <input type="text" v-model="newQuizOption3" placeholder="Option 3">
        <input type="text" v-model="newQuizOption4" placeholder="Option 4">
        <input type="text" v-model="newQuizCorrectOption" placeholder="Correct option">
        <button style="top: 365px;" @click="addQuizQuestion">Submit</button>
        <button @click="showAddQuizQuestionPopup = false">X</button>
      </div>
    </div>
  </div>
</template>

<script>
import axiosFetch from '@/axios';

export default {
  name: 'MainTutor',
  props: ['courseId', 'courseName'],
  data() {
    return {
      username: null,
      //selectedSection: 'about',
      currentQuizId: null,
      selectedTopic: 'about',
      selectedContent: null,
      topics: [],
      video: {},
      quizQuestions: [],
      codingQuiz: {},
      showAddContentPopup: false,
      showAddQuizQuestionPopup: false,
      newTopicData: {
        courseId: this.courseId,
        newTopicName: '',
        includeVideo: false,
        includeQuiz: false,
        includeCodingQuiz: false
      },
      newVideoLink: '',
      newQuizQuestion: '',
      newQuizOption1: '',
      newQuizOption2: '',
      newQuizOption3: '',
      newQuizOption4: '',
      newQuizCorrectOption: '',
      newCodingQuizQuestion: '',
      newCodingQuizInput: null,
      newCodingQuizOutput: null,
      newCodingLanguage:''
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
        const resp = await axiosFetch.get(`/api/tutor/course/get-topics`, { params: { courseId: this.courseId } });
        this.topics = resp.data;
      } catch (error) {
        console.error("Error fetching topics:", error);
      }
    },
    async selectSection(section) {
    // this.selectedSection = section;
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
      console.log(topicId);
      console.log(this.selectedContent);
      await this.fetchContent(topicId); // Fetch the content for a video/Quiz//CodingQuiz
    },
    async fetchContent(topicId) {
      try {

        const resp = await axiosFetch.get(`/api/tutor/topic/content`, { params : { 'topicId' : topicId, 'type': this.selectedContent } } );
        const content = resp.data;

        // Process and store the content as needed
        console.log(content.details)
        
        if (content.type === 'video') {
          this.video = content.details;
          this.quizQuestions = '';
          this.codingQuiz = '';
        } else if (content.type === 'quiz') {
          this.currentQuizId = content.quizId;
          this.quizQuestions = content.details;
          this.video = '';
          this.codingQuiz = '';
        } else if (content.type === 'codingQuiz') {
          this.codingQuiz = content.details;
          this.video = '';
          this.quizQuestions = '';
        }
        
      } catch (error) {
        console.error("Error fetching topic content:", error);
      }
    },
    signOut() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'landingPage' });
    },
    async addTopic() {
      try {
        const response = await axiosFetch.post('/api/tutor/add_topic', this.newTopicData);
        this.topics.push(response.data);
        this.newTopicData.newTopicName = '';
        this.newTopicData.includeVideo = false;
        this.newTopicData.includeQuiz = false;
        this.newTopicData.includeCodingQuiz = false;
        this.showAddContentPopup = false;
      } catch (error) {
        console.error("Error adding topic:", error);
      }
    },
    async addVideo() {
      try {
        const response = await axiosFetch.put('/api/tutor/add_video', {
          videoId: this.video.id,
          videoLink: this.newVideoLink
        });
        console.log(response.data.message);
        this.video.link = this.newVideoLink;
        this.newVideoLink = '';
      } catch (error) {
        console.error("Error adding video:", error);
      }
    },
    async addQuizQuestion() {
      try {
        console.log("quizId: ",this.currentQuizId)
        const response = await axiosFetch.post('/api/tutor/add_quiz_question', {
          quizId: this.currentQuizId,
          question: this.newQuizQuestion,
          options: [
            this.newQuizOption1,
            this.newQuizOption2,
            this.newQuizOption3,
            this.newQuizOption4
          ],
          correctOption: this.newQuizCorrectOption
        });
        // this.quizQuestions.push(response.data);
        console.log(response)
        this.selectContent('quiz', this.selectedTopic)
        this.newQuizQuestion = '';
        this.newQuizOption1 = '';
        this.newQuizOption2 = '';
        this.newQuizOption3 = '';
        this.newQuizOption4 = '';
        this.newQuizCorrectOption = '';
        this.showAddQuizQuestionPopup = false;
      } catch (error) {
        console.error("Error adding quiz question:", error);
      }
    },
    async addCodingQuiz() {
      try {
        const response = await axiosFetch.put('/api/tutor/add_coding_quiz', {
          id: this.codingQuiz.id,
          language: this.newCodingLanguage,
          question: this.newCodingQuizQuestion,
          testCases: [this.newCodingQuizInput, this.newCodingQuizOutput]
        });
        console.log(response.data.message);
        this.selectContent('codingQuiz', this.selectedTopic);
        this.newCodingQuizQuestion = '';
        this.newCodingQuizInput = '';
        this.newCodingQuizOutput = '';
        this.newCodingLanguage = '';
      } catch (error) {
        console.error("Error adding coding quiz:", error);
      }
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
  background-color: #c5d17a;
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
.add-content {
  margin-top: 20px;
  background-color: green;
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  cursor: pointer;
  bottom: 1%;
}
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  position: relative;
}
.popup-content button {
  background-color: rgb(0, 157, 255);
  color: white;
  border: none;
  padding: 5px;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}
.popup-content h2 {
  margin-top: 0;
}
.popup-content input[type="text"],
.popup-content textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
#addTopicBtnSbt{
  top: 120px;
}
</style>

