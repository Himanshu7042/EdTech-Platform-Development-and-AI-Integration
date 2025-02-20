<template>
    <div class="container">
      <h1>GPT Chat Interface</h1>
      <div id="chat-box" ref="chatBox">
        <p v-for="(message, index) in messages" :key="index">
          <strong>{{ message.sender }}:</strong> {{ message.text }}
        </p>
      </div>
      <input
        type="text"
        v-model="userInput"
        @keydown.enter="sendMessage"
        placeholder="Type your message here..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </template>
  
  <script>
  import { GoogleGenerativeAI } from "@google/generative-ai";
  
  export default {
    data() {
      return {
        userInput: "",
        messages: [],
        model: null, // Store the AI model instance
      };
    },
    async created() {
      try {
        const API_KEY = "AIzaSyCESDMdIk_sDsBtW7eoaD_JFnOjvuwTgfg";
        const genAI = new GoogleGenerativeAI(API_KEY);
        this.model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
      } catch (error) {
        console.error("Error initializing the model:", error);
        this.addMessage("System", "Failed to load the AI model. Please try again later.");
      }
    },
    methods: {
      async sendMessage() {
        if (this.userInput.trim()) {
          this.addMessage("User", this.userInput);
          await this.generateText(this.userInput);
          this.userInput = "";
        }
      },
      addMessage(sender, text) {
        this.messages.push({ sender, text });
        this.scrollToBottom();
      },
      async generateText(prompt) {
        try {
          const result = await this.model.generateContent(prompt);
          const text = await result.response.text();
  
          if (text) {
            this.addMessage("GPT", text);
          } else {
            throw new Error("Empty response from the AI model");
          }
        } catch (error) {
          console.error("Error generating text:", error);
          this.addMessage("GPT", "Sorry, something went wrong while generating the response.");
        }
      },
      scrollToBottom() {
        this.$nextTick(() => {
          const chatBox = this.$refs.chatBox;
          chatBox.scrollTop = chatBox.scrollHeight;
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    margin: 50px auto;
  }
  
  #chat-box {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    border-radius: 4px;
  }
  
  input[type="text"] {
    width: calc(100% - 22px);
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  