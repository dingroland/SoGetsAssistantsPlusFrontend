<template>
  <div class="chat-container">
    <!-- Add company selection -->
    <div class="company-selector">
      <select v-model="selectedCompany" @change="loadCompanyData">
        <option value="">Select a Company</option>
        <option v-for="(company, id) in companies" 
                :key="id" 
                :value="id">
          {{ id }}
        </option>
      </select>
    </div>

    <!-- Add thread selection -->
    <div class="thread-selector" v-if="selectedCompany">
      <select v-model="selectedThread" @change="loadThreadMessages">
        <option value="">Select a Thread</option>
        <option v-for="(thread, id) in threads" 
                :key="id" 
                :value="id">
          {{ thread.name }}
        </option>
      </select>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.role]">
        <div class="message-content">
          <div class="avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="text">{{ message.content }}</div>
        </div>
      </div>
    </div>
    
    <div class="input-container">
      <textarea 
        v-model="userInput"
        @keydown.enter.prevent="sendMessage"
        placeholder="Send a message..."
        rows="1"
        ref="inputArea"
        :disabled="!selectedThread"
      ></textarea>
      <button @click="sendMessage" class="send-button" :disabled="!selectedThread">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatApp',
  data() {
    return {
      messages: [],
      userInput: '',
      companies: {},
      threads: {},
      selectedCompany: '',
      selectedThread: '',
      companyId: '',
      threadId: ''
    }
  },
  async created() {
    await this.loadStateData();
  },
  methods: {
    async loadStateData() {
      try {
        const response = await axios.get('http://localhost:8000/api/company');
        if (response.data) {
          this.companies = response.data;
          console.log('Loaded companies:', this.companies); // Debug log
        }
      } catch (error) {
        console.error('Error loading state data:', error);
      }
    },

    async loadCompanyData(event) {
      if (!this.selectedCompany) return;
      
      try {
        const response = await axios.get(`http://localhost:8000/api/company/${this.selectedCompany}`);
        if (response.data && response.data.threads) {
          this.threads = response.data.threads;
          this.companyId = this.selectedCompany;
          this.messages = []; // Clear messages when changing company
          this.selectedThread = ''; // Reset thread selection
          console.log('Loaded threads:', this.threads); // Debug log
        }
      } catch (error) {
        console.error('Error loading company data:', error);
      }
    },

    async loadThreadMessages() {
      if (!this.selectedThread || !this.threads[this.selectedThread]) return;
      
      try {
        this.threadId = this.selectedThread;
        const threadData = this.threads[this.threadId];
        if (threadData && threadData.messages) {
          this.messages = threadData.messages;
          console.log('Loaded messages:', this.messages); // Debug log
        } else {
          this.messages = [];
        }
      } catch (error) {
        console.error('Error loading thread messages:', error);
      }
    },

    async sendMessage() {
      if (!this.userInput.trim() || !this.selectedThread) return;
      
      const userMessage = this.userInput.trim();
      this.messages.push({
        role: 'user',
        content: userMessage
      });

      this.userInput = '';

      try {
        const response = await axios.post(
          `http://localhost:8000/api/company/${this.companyId}/threads/${this.threadId}/message`,
          { content: userMessage }
        );

        this.messages.push({
          role: 'assistant',
          content: response.data.assistantResponse
        });
      } catch (error) {
        console.error('Error sending message:', error);
        this.messages.push({
          role: 'assistant',
          content: 'Sorry, there was an error processing your message.'
        });
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.company-selector,
.thread-selector {
  padding: 1rem;
  background-color: #444654;
  border-bottom: 1px solid #565869;
}

select {
  width: 100%;
  padding: 0.5rem;
  background-color: #40414f;
  border: 1px solid #565869;
  border-radius: 0.5rem;
  color: white;
  font-size: 1rem;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 2rem;
}

.message {
  margin-bottom: 1.5rem;
}

.message-content {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}

.message.user {
  background-color: #343541;
}

.message.assistant {
  background-color: #444654;
}

.avatar {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text {
  flex-grow: 1;
  white-space: pre-wrap;
}

.input-container {
  border-top: 1px solid #4c4c4c;
  padding: 1.5rem;
  position: relative;
}

textarea {
  width: 100%;
  padding: 0.75rem 3rem 0.75rem 1rem;
  background-color: #40414f;
  border: 1px solid #565869;
  border-radius: 0.5rem;
  color: white;
  resize: none;
  outline: none;
  font-size: 1rem;
}

textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-button {
  position: absolute;
  right: 2rem;
  bottom: 2rem;
  background: none;
  border: none;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-button svg {
  width: 16px;
  height: 16px;
  stroke: #ffffff;
}

textarea::placeholder {
  color: #8e8ea0;
}
</style>