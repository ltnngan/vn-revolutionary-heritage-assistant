<!-- ChatMessages.vue -->
<template>
  <div ref="messagesContainer" class="chat-messages">
    <!-- Messages list -->
    <div class="chat-messages__list">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="chat-message"
        :class="`chat-message--${msg.sender}`"
      >
        <!-- Avatar bot -->
        <div v-if="msg.sender === 'bot'" class="chat-message__avatar avatar">
          <i class="fa-solid fa-robot"></i>
        </div>

        <!-- Message bubble CHỈ cho user và bot -->
        <div v-if="msg.sender === 'user' || msg.sender === 'bot'" class="chat-message__bubble">
          <img
            v-if="msg.image"
            :src="msg.image"
            alt="uploaded"
            class="chat-message__image"
          />

          <div v-if="msg.text" class="chat-message__text">
            {{ msg.text }}
          </div>

          <div v-if="msg.processingTime" class="chat-message__meta">
            ⏱️ {{ msg.processingTime }}s
          </div>
        </div>

        <!-- System notification -->
        <div v-if="msg.sender === 'system'" class="chat-message__system">
          <i class="fa-solid fa-spell-check"></i>
          <span>{{ msg.text }}</span>
        </div>
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading" class="chat-message chat-message--bot">
        <div class="chat-message__avatar avatar">
          <i class="fa-solid fa-robot"></i>
        </div>
        <div class="chat-message__bubble">
          <div class="chat-message__loading">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from "vue";

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  emptyTitle: {
    type: String,
    default: "Xin chào! 👋",
  },
  emptySubtitle: {
    type: String,
    default: "Hãy gửi ảnh di tích kèm câu hỏi để bắt đầu!",
  },
});

const messagesContainer = ref(null);

const isEmpty = computed(() => props.messages.length === 0);

// Debug watch
watch(
  () => props.messages,
  (newMessages) => {
    console.log('🟣 [ChatMessages] Total messages:', newMessages.length);
    newMessages.forEach((msg, idx) => {
      console.log(`   [${idx}] sender="${msg.sender}" | text="${msg.text?.substring(0, 40)}..."`);
    });
  },
  { deep: true }
);

// Auto scroll khi có message mới hoặc loading
watch(
  () => [props.messages.length, props.isLoading],
  async () => {
    await nextTick();
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  },
  { flush: "post" }
);
</script>

<style scoped>
/* Container */
.chat-messages {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
}

/* Empty state */
.chat-messages__empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem 1rem;
  gap: 0.75rem;
}

.chat-messages__empty-icon {
  font-size: 3.5rem;
  opacity: 0.8;
}

.chat-messages__empty-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.chat-messages__empty-text {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.5;
  max-width: 400px;
  margin: 0;
}

/* Messages list */
.chat-messages__list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-message {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-message--user {
  justify-content: flex-end;
}

.chat-message--bot {
  justify-content: flex-start;
}

.chat-message--system {
  justify-content: center;
  margin: 0.75rem 0;
}

/* Avatar */
.chat-message__avatar {
  width: 2rem;
  height: 2rem;
  flex-shrink: 0;
  border-radius: 50%;
  border: 2px solid rgba(139, 69, 19, 0.2);
  object-fit: cover;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Message bubble */
.chat-message__bubble {
  max-width: 75%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chat-message--user .chat-message__bubble {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  border-bottom-right-radius: 0.3rem;
}

.chat-message--bot .chat-message__bubble {
  background: white;
  color: #333;
  border: 1px solid rgba(139, 69, 19, 0.15);
  border-bottom-left-radius: 0.3rem;
}

/* System message */
.chat-message__system {
  background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
  color: #0c5460;
  padding: 0.6rem 1.2rem;
  border-radius: 1.5rem;
  font-size: 0.85rem;
  text-align: center;
  border: 1px solid rgba(23, 162, 184, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  max-width: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  animation: slideIn 0.3s ease;
}

.chat-message__system i {
  font-size: 1rem;
  color: #17a2b8;
}

/* Message content */
.chat-message__image {
  max-width: 100%;
  max-height: 12rem;
  border-radius: 0.5rem;
  object-fit: cover;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.chat-message__image:hover {
  transform: scale(1.02);
}

.chat-message__text {
  font-size: 0.95rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-message__meta {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  opacity: 0.7;
}

/* Loading animation */
.chat-message__loading {
  display: flex;
  gap: 0.4rem;
  padding: 0.3rem 0;
}

.chat-message__loading span {
  width: 0.5rem;
  height: 0.5rem;
  background: #8b4513;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.chat-message__loading span:nth-child(1) {
  animation-delay: -0.32s;
}

.chat-message__loading span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Scrollbar */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(139, 69, 19, 0.3);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 69, 19, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .chat-messages {
    padding: 0.75rem;
  }

  .chat-message__bubble {
    max-width: 85%;
    padding: 0.65rem 0.85rem;
    font-size: 0.9rem;
  }

  .chat-message__avatar {
    width: 1.75rem;
    height: 1.75rem;
  }

  .chat-message__system {
    font-size: 0.8rem;
    padding: 0.5rem 1rem;
    max-width: 95%;
  }

  .chat-messages__empty-icon {
    font-size: 3rem;
  }

  .chat-messages__empty-title {
    font-size: 1.1rem;
  }

  .chat-messages__empty-text {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .chat-messages {
    padding: 0.6rem;
  }

  .chat-message__bubble {
    max-width: 90%;
    padding: 0.6rem 0.8rem;
  }

  .chat-message__image {
    max-height: 10rem;
  }

  .chat-messages__empty {
    padding: 1.5rem 0.75rem;
  }
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
  color: rgba(0, 0, 0, 0.2);
}
</style>