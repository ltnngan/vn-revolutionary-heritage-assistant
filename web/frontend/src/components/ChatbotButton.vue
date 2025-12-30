<!-- ChatbotButton.vue -->
<template>
  <div class="chatbot-container">
    <!-- Nút floating chatbot -->
    <Transition name="bounce">
      <button
        v-if="!isOpen"
        class="chatbot-button"
        @click="toggleChat"
        :class="{ 'has-notification': hasNotification }"
      >
        <i class="fa-solid fa-comments"></i>
        <span v-if="hasNotification" class="notification-badge">1</span>
      </button>
    </Transition>

    <!-- Chat window -->
    <Transition name="slide-up">
      <div v-if="isOpen" class="chat-window">
        <!-- Chat header -->
        <div class="chat-window__header">
          <div class="header-info">
            <div class="avatar">
              <i class="fa-solid fa-robot"></i>
            </div>
            <div class="header-text">
              <h3>Trợ lý Di sản</h3>
              <span class="status">
                <span class="status-dot"></span>
                Đang hoạt động
              </span>
            </div>
          </div>
          <div class="header-actions">
            <button class="action-btn" @click="minimizeChat" title="Thu nhỏ">
              <i class="fa-solid fa-minus"></i>
            </button>
            <button class="action-btn" @click="toggleChat" title="Đóng">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
        </div>

        <!-- Chat content -->
        <div class="chat-window__content">
          <ChatMessages :messages="messages" :isLoading="isLoading" />
        </div>

        <!-- Chat input -->
        <div class="chat-window__footer">
          <ChatInput @sendMessage="handleSend" :disabled="isLoading" />
        </div>
      </div>
    </Transition>

    <!-- Minimized window -->
    <Transition name="fade">
      <div v-if="isMinimized" class="chat-minimized" @click="restoreChat">
        <i class="fa-solid fa-comments"></i>
        <span>Trợ lý Di sản</span>
        <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import ChatMessages from './ChatMessages.vue';
import ChatInput from './ChatInput.vue';
import { predictVQA, checkHealth } from '../services/index';
import { correctVietnameseSpelling } from '../services/spellcheck';

const isOpen = ref(false);
const isMinimized = ref(false);
const hasNotification = ref(true);
const unreadCount = ref(0);
const messages = ref([]);
const isLoading = ref(false);
const backendReady = ref(false);
const currentImageFile = ref(null);

const GREETINGS = ['chào', 'hello', 'hi', 'xin chào', 'hey', 'chao'];
let healthCheckInterval = null;

onMounted(async () => {
  await checkBackendHealth();
  
  if (!backendReady.value) {
    healthCheckInterval = setInterval(async () => {
      await checkBackendHealth();
      if (backendReady.value) {
        clearInterval(healthCheckInterval);
        healthCheckInterval = null;
      }
    }, 3000);
  }

  // Welcome message khi mở lần đầu
  setTimeout(() => {
    if (!isOpen.value) {
      hasNotification.value = true;
    }
  }, 2000);
});

onUnmounted(() => {
  if (healthCheckInterval) {
    clearInterval(healthCheckInterval);
  }
});

async function checkBackendHealth() {
  try {
    const health = await checkHealth();
    backendReady.value = health.model_loaded;
  } catch (error) {
    console.error('Lỗi kiểm tra backend:', error);
    backendReady.value = false;
  }
}

function toggleChat() {
  isOpen.value = !isOpen.value;
  isMinimized.value = false;
  
  if (isOpen.value) {
    hasNotification.value = false;
    unreadCount.value = 0;
    messages.value = [];
    
    // Add welcome message nếu chưa có tin nhắn
    if (messages.value.length === 0) {
      addBotMessage(
        'Xin chào! Tôi là trợ lý ảo hỗ trợ về di tích văn hóa. ' +
        'Hãy gửi cho tôi ảnh di tích kèm câu hỏi, tôi sẽ giúp bạn tìm hiểu về di sản văn hóa Việt Nam!'
      );
    }
  }
}

function minimizeChat() {
  isOpen.value = false;
  isMinimized.value = true;
}

function restoreChat() {
  isOpen.value = true;
  isMinimized.value = false;
  unreadCount.value = 0;
}

async function handleSend(newMsg) {
  const hasImage = Boolean(newMsg.image);
  let textToProcess = newMsg.text?.trim() || '';
  
  console.log('🟦 [ChatbotButton] Text gốc:', textToProcess);
  
  if (hasImage) {
    currentImageFile.value = newMsg.image;
  }
  
  // ✅ SPELL CHECK
  let correctedText = textToProcess;
  const skipSpellCheck = textToProcess && 
    ['hi', 'hello', 'chào', 'hey'].includes(textToProcess.toLowerCase().trim());
  
  if (textToProcess && !skipSpellCheck) {
    console.log('🟦 [ChatbotButton] Đang spell check...');
    
    try {
      const result = await correctVietnameseSpelling(textToProcess);
      console.log('🟦 [ChatbotButton] Kết quả:', result);
      
      if (result.hasCorrected) {
        correctedText = result.corrected;
        console.log('🟦 [ChatbotButton] ✅ Đã sửa:', correctedText);
        
        // addSystemMessage(
        //   `✏️ Đã chỉnh: "${textToProcess}" → "${correctedText}"`
        // );
      } else {
        console.log('🟦 [ChatbotButton] ℹ️ Không cần sửa');
      }
    } catch (error) {
      console.error('🟦 [ChatbotButton ERROR]:', error);
      correctedText = textToProcess;
    }
  } else if (skipSpellCheck) {
    console.log('🟦 [ChatbotButton] Bỏ qua greeting');
  }
  
  const hasText = Boolean(correctedText);
  
  messages.value.push({
    text: correctedText,
    image: hasImage ? URL.createObjectURL(newMsg.image) : null,
    sender: 'user'
  });
  
  if (hasImage && !hasText) {
    addBotMessage('Tôi đã nhận được ảnh của bạn. Bạn muốn hỏi gì về ảnh này?');
    return;
  }
  
  if (!currentImageFile.value && hasText) {
    if (isGreeting(correctedText)) {
      addBotMessage(
        'Chào bạn! Tôi là trợ lý ảo hỗ trợ về di tích. ' +
        'Hãy gửi cho tôi một bức ảnh di tích kèm câu hỏi, tôi sẽ giúp bạn!'
      );
    } else {
      addBotMessage(
        'Để tôi có thể trả lời câu hỏi của bạn, vui lòng upload ảnh di tích kèm theo nhé!'
      );
    }
    return;
  }
  
  if (hasText) {
    await predict(correctedText);
  }
}

function isGreeting(text) {
  const normalized = text.toLowerCase().trim();
  return GREETINGS.some(greeting => normalized.includes(greeting));
}

async function predict(question) {
  isLoading.value = true;

  try {
    const result = await predictVQA(currentImageFile.value, question);
    addBotMessage(result.answer, result.processing_time);
  } catch (error) {
    console.error('Lỗi predict:', error);
    addBotMessage('Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu. Vui lòng thử lại sau!');
  } finally {
    isLoading.value = false;
  }
}

function addBotMessage(text, processingTime = null) {
  const delay = processingTime ? 0 : 500;
  
  setTimeout(() => {
    messages.value.push({
      text,
      sender: 'bot',
      ...(processingTime && { processingTime })
    });
    
    // Nếu chat đang minimize, tăng unread count
    if (isMinimized.value) {
      unreadCount.value++;
    }
  }, delay);
}

function addSystemMessage(text) {
  console.log('🟢 [ChatbotButton] addSystemMessage được gọi!');
  messages.value.push({
    text,
    sender: 'system',
    timestamp: new Date()
  });
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 9999;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ===== FLOATING BUTTON ===== */
.chatbot-button {
  position: relative;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  border: none;
  color: white;
  font-size: 1.75rem;
  cursor: pointer;
  box-shadow: 0 0.5rem 1.5rem rgba(139, 69, 19, 0.4);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-button:hover {
  transform: scale(1.1);
  box-shadow: 0 0.75rem 2rem rgba(139, 69, 19, 0.5);
}

.chatbot-button.has-notification {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0.5rem 1.5rem rgba(139, 69, 19, 0.4);
  }
  50% {
    box-shadow: 0 0.5rem 2rem rgba(139, 69, 19, 0.6), 0 0 0 0.5rem rgba(139, 69, 19, 0.2);
  }
}

.notification-badge {
  position: absolute;
  top: -0.25rem;
  right: -0.25rem;
  background: #ff0000;
  color: white;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  border: 2px solid white;
}

/* ===== CHAT WINDOW ===== */
.chat-window {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 400px;
  height: 500px;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-window__header {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.header-text h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.status {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  opacity: 0.9;
}

.status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: #4ade80;
  animation: blink 2s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 2rem;
  height: 2rem;
  border-radius: 0.375rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.chat-window__content {
  flex: 1;
  padding-bottom: 1.5rem;
  overflow-y: auto;
  overflow: hidden;
  background: #f9f6f0;
}

.chat-window__footer {
  border-top: 1px solid #e5e5e5;
  background: white;
}

/* ===== MINIMIZED WINDOW ===== */
.chat-minimized {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: white;
  padding: 0.875rem 1.25rem;
  border-radius: 2rem;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid #8b4513;
}

.chat-minimized:hover {
  transform: translateY(-0.25rem);
  box-shadow: 0 0.75rem 2rem rgba(0, 0, 0, 0.2);
}

.chat-minimized i {
  color: #8b4513;
  font-size: 1.25rem;
}

.chat-minimized span {
  color: #333;
  font-weight: 600;
  font-size: 0.875rem;
}

.unread-badge {
  background: #ff0000;
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 700;
}

/* ===== TRANSITIONS ===== */
.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-out 0.3s;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce-out {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(0);
    opacity: 0;
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  transform: translateY(1rem);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(1rem);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100vw - 2rem);
    height: calc(100vh - 4rem);
    bottom: 1rem;
    right: 1rem;
  }

  .chatbot-container {
    bottom: 1rem;
    right: 1rem;
  }

  .chat-minimized {
    bottom: 1rem;
    right: 1rem;
  }
}
</style>