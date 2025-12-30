<!-- ChatView.vue -->
<template>
  <div class="chat-view">
    <div class="chat-view__header">
      <div class="chat-view__header-content">
        <div class="chat-view__branding">
          <img src="../images/logo.jpg" alt="Logo" class="chat-view__logo" />
          <div class="chat-view__title">
            <span class="chat-view__title-main">Trợ lý Di sản</span>
            <span class="chat-view__title-sub">Hỏi đáp về di tích Cần Thơ</span>
          </div>
        </div>
        
        <button class="chat-view__close" @click="closeChat" title="Đóng">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      
      <!-- Warning khi backend chưa ready -->
      <div v-if="!backendReady" class="chat-view__status">
        <i class="fa-solid fa-circle-notch fa-spin"></i>
        <span>Đang tải model AI...</span>
      </div>
      
      <!-- Warning khi đang check spelling -->
      <div v-if="isCheckingSpelling" class="chat-view__status chat-view__status--spell">
        <i class="fa-solid fa-circle-notch fa-spin"></i>
        <span>Đang kiểm tra chính tả...</span>
      </div>
    </div>
    
    <ChatMessages 
      :messages="messages" 
      :isLoading="isLoading"
      :compact="true"
      emptyTitle="Xin chào! 👋"
      emptySubtitle="Hãy gửi ảnh di tích kèm câu hỏi, tôi sẽ giúp bạn tìm hiểu thêm về nó!"
      class="chat-view__messages"
    />
    
    <div class="chat-view__input-wrapper">
      <ChatInput 
        @sendMessage="handleSend" 
        :disabled="isLoading || !backendReady || isCheckingSpelling" 
      />
      
      <div class="chat-view__tips">
        <span class="chat-view__tip">
          💡 <strong>Mẹo:</strong> Hệ thống tự động chỉnh chính tả tiếng Việt cho bạn
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
  console.log('🚨🚨🚨 CHATVIEW.VUE ĐANG CHẠY! 🚨🚨🚨');
import { ref, onMounted, onUnmounted } from 'vue';
import ChatMessages from "../components/ChatMessages.vue";
import ChatInput from "../components/ChatInput.vue";
import { predictVQA, checkHealth } from "../services/index";
import { correctVietnameseSpelling } from "../services/spellcheck";
import { useRouter } from 'vue-router';

const router = useRouter();

const messages = ref([]);
const isLoading = ref(false);
const backendReady = ref(false);
const currentImageFile = ref(null);
const isCheckingSpelling = ref(false); // Thêm state

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
    
    if (backendReady.value) {
      console.log('✓ Backend sẵn sàng');
    }
  } catch (error) {
    console.error('Lỗi kiểm tra backend:', error);
    backendReady.value = false;
  }
}

async function handleSend(newMsg) {
  const hasImage = Boolean(newMsg.image);
  let textToProcess = newMsg.text?.trim() || '';
  
  console.log('🟦 [1] Text gốc:', textToProcess);
  console.log('🔴 DEBUG hasImage:', hasImage);
  console.log('🔴 DEBUG textToProcess:', textToProcess);
  console.log('🔴 DEBUG textToProcess type:', typeof textToProcess);
  console.log('🔴 DEBUG textToProcess.length:', textToProcess?.length);
  
  if (hasImage) {
    currentImageFile.value = newMsg.image;
  }
  
  // SPELL CHECK
  let correctedText = textToProcess;
  const skipSpellCheck = textToProcess && 
    ['hi', 'hello', 'chào', 'hey'].includes(textToProcess.toLowerCase().trim());
  
  console.log('🔴 DEBUG skipSpellCheck:', skipSpellCheck);
  console.log('🔴 DEBUG condition (textToProcess && !skipSpellCheck):', textToProcess && !skipSpellCheck);
  
  
  if (textToProcess && !skipSpellCheck) {
    console.log('🟦 [2] Đang spell check...');
    isCheckingSpelling.value = true;
    
    try {
      const result = await correctVietnameseSpelling(textToProcess);
      console.log('🟦 [3] Kết quả:', result);
      
      if (result.hasCorrected) {
        correctedText = result.corrected;
        console.log('🟦 [4] ✅ Đã sửa:', correctedText);
        
        // addSystemMessage(
        //   `✏️ Đã chỉnh: "${textToProcess}" → "${correctedText}"`
        // );
      } else {
        console.log('🟦 [4] ℹ️ Không cần sửa');
      }
    } catch (error) {
      console.error('🟦 [ERROR]:', error);
      correctedText = textToProcess;
    } finally {
      isCheckingSpelling.value = false;
    }
  } else {
    console.log('🟦 [2] Bỏ qua (greeting đơn giản)');
  }
  
  const hasText = Boolean(correctedText);
  console.log('🟦 [5] Final text:', correctedText);
  
  // Thêm vào UI
  messages.value.push({
    text: correctedText,
    image: hasImage ? URL.createObjectURL(newMsg.image) : null,
    sender: 'user'
  });
  
  // Case 1: Chỉ có ảnh
  if (hasImage && !hasText) {
    addBotMessage('Tôi đã nhận được ảnh của bạn. Bạn muốn hỏi gì về ảnh này?');
    return;
  }
  
  // Case 2: Chỉ có text, không có ảnh
  if (!currentImageFile.value && hasText) {
    if (isGreeting(correctedText)) {
      addBotMessage(
        'Chào bạn! Tôi là trợ lý ảo hỗ trợ về di tích Cần Thơ. ' +
        'Hãy gửi cho tôi một bức ảnh di tích kèm câu hỏi, tôi sẽ giúp bạn!'
      );
    } else {
      addBotMessage(
        'Để tôi có thể trả lời câu hỏi của bạn, vui lòng upload ảnh di tích kèm theo nhé!'
      );
    }
    return;
  }
  
  // Case 3: Có text + ảnh → predict
  if (hasText) {
    console.log('🟦 [6] Gọi predict với:', correctedText);
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
  }, delay);
}

// Thêm function mới cho system message
function addSystemMessage(text) {
  console.log('🟢 ========================================');
  console.log('🟢 [addSystemMessage] ĐƯỢC GỌI!');
  console.log('🟢 Text:', text);
  console.log('🟢 messages.value TRƯỚC:', messages.value.length);
  
  messages.value.push({
    text,
    sender: 'system',
    timestamp: new Date()
  });
  
  console.log('🟢 messages.value SAU:', messages.value.length);
  console.log('🟢 Message vừa thêm:', messages.value[messages.value.length - 1]);
  console.log('🟢 ========================================');
}

function closeChat() {
  router.push('/');
}
</script>

<style scoped>
/* Container - Thiết kế chatbot nhúng */
.chat-view {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f0e8 0%, #faf8f3 100%);
  position: relative;
  overflow: hidden;
}

/* Header với gradient màu di sản */
.chat-view__header {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 10;
}

.chat-view__header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
}

.chat-view__branding {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.chat-view__logo {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-view__title {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.chat-view__title-main {
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.chat-view__title-sub {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.8rem;
  font-weight: 400;
}

.chat-view__close {
  width: 2rem;
  height: 2rem;
  border-radius: 0.4rem;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.chat-view__close:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

/* Status banner */
.chat-view__status {
  background: linear-gradient(90deg, #fff3cd 0%, #ffe8a1 100%);
  color: #856404;
  padding: 0.6rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  border-top: 1px solid rgba(255, 193, 7, 0.3);
}

.chat-view__status i {
  font-size: 1rem;
}

/* Messages area */
.chat-view__messages {
  flex: 1;
  overflow-y: auto;
  background: transparent;
}

/* Input wrapper với tips */
.chat-view__input-wrapper {
  background: white;
  border-top: 1px solid rgba(139, 69, 19, 0.15);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
  padding: 1rem 1.5rem 0.75rem;
}

.chat-view__tips {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 0 0.25rem;
}

.chat-view__tip {
  font-size: 0.85rem;
  color: #666;
  text-align: center;
  line-height: 1.4;
}

.chat-view__tip strong {
  color: #8b4513;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .chat-view__header-content {
    padding: 0.6rem 1rem;
  }

  .chat-view__logo {
    width: 2rem;
    height: 2rem;
  }

  .chat-view__title-main {
    font-size: 1rem;
  }

  .chat-view__title-sub {
    font-size: 0.75rem;
  }

  .chat-view__close {
    width: 1.75rem;
    height: 1.75rem;
    font-size: 1.1rem;
  }

  .chat-view__status {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  .chat-view__input-wrapper {
    padding: 0.75rem 1rem 0.6rem;
  }

  .chat-view__tip {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .chat-view__header-content {
    padding: 0.5rem 0.75rem;
  }

  .chat-view__logo {
    width: 1.75rem;
    height: 1.75rem;
  }

  .chat-view__title-main {
    font-size: 0.95rem;
  }

  .chat-view__title-sub {
    font-size: 0.7rem;
  }

  .chat-view__input-wrapper {
    padding: 0.6rem 0.75rem 0.5rem;
  }
}

/* Scrollbar styling */
.chat-view__messages::-webkit-scrollbar {
  width: 6px;
}

.chat-view__messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-view__messages::-webkit-scrollbar-thumb {
  background: rgba(139, 69, 19, 0.3);
  border-radius: 3px;
}

.chat-view__messages::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 69, 19, 0.5);
}

.chat-view__status--spell {
  background: linear-gradient(90deg, #d1ecf1 0%, #bee5eb 100%);
  color: #0c5460;
}
</style>