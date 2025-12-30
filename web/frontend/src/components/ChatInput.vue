<!-- ChatInput.vue -->
<template>
  <div class="chat-input-wrapper">
    <!-- Preview ảnh đã chọn -->
    <div v-if="imagePreview" class="image-preview">
      <div class="image-preview__container">
        <img :src="imagePreview" alt="preview" class="image-preview__img" />
        <button 
          class="image-preview__remove" 
          @click="removeImage"
          title="Xóa ảnh"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>

    <!-- Input chính -->
    <div class="chat-input" :class="{ 'chat-input--disabled': disabled }">
      <!-- Upload ảnh -->
      <label class="chat-input__upload" :class="{ 'disabled': disabled }">
        <input
          type="file"
          accept="image/*"
          @change="handleImageUpload"
          :disabled="disabled"
          hidden
        />
        <i class="fa-solid fa-image"></i>
      </label>

      <!-- Text input -->
      <input
        v-model="message"
        @keyup.enter="sendMessage"
        type="text"
        class="chat-input__field"
        placeholder="Nhập câu hỏi về di tích..."
        :disabled="disabled"
      />

      <!-- Nút gửi -->
      <button 
        class="chat-input__send"
        :class="{ 'chat-input__send--disabled': !canSend || disabled }"
        @click="sendMessage"
        :disabled="!canSend || disabled"
        title="Gửi tin nhắn"
      >
        <i class="fa-solid fa-paper-plane"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["sendMessage"]);

const message = ref("");
const imageFile = ref(null);
const imagePreview = ref(null);

// Cho phép gửi nếu có text hoặc ảnh
const canSend = computed(() => 
  message.value.trim() !== "" || imageFile.value !== null
);

function sendMessage() {
  if (!canSend.value || props.disabled) return;

  emit("sendMessage", { 
    text: message.value.trim(), 
    image: imageFile.value
  });

  // Reset form
  message.value = "";
  imageFile.value = null;
  imagePreview.value = null;
}

function handleImageUpload(event) {
  if (props.disabled) return;
  
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
}

function removeImage() {
  if (props.disabled) return;
  
  imageFile.value = null;
  imagePreview.value = null;
}
</script>

<style scoped>
/* Container */
.chat-input-wrapper {
  margin: .5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Preview ảnh */
.image-preview {
  display: flex;
  justify-content: flex-start;
  padding: 0 0.5rem;
}

.image-preview__container {
  position: relative;
  display: inline-block;
}

.image-preview__img {
  max-width: 8rem;
  max-height: 8rem;
  border-radius: 0.75rem;
  object-fit: cover;
  border: 2px solid rgba(139, 69, 19, 0.2);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.image-preview__remove {
  position: absolute;
  top: -0.4rem;
  right: -0.4rem;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: none;
  background: #dc3545;
  color: white;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.image-preview__remove:hover {
  background: #c82333;
  transform: scale(1.1);
}

/* Input chính */
.chat-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 2px solid rgba(139, 69, 19, 0.2);
  border-radius: 1.5rem;
  padding: 0.5rem 0.75rem;
  transition: all 0.2s ease;
}

.chat-input:focus-within {
  border-color: #8b4513;
  box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.1);
}

.chat-input--disabled {
  opacity: 0.6;
  pointer-events: none;
  background: #f5f5f5;
}

/* Upload button */
.chat-input__upload {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #8b4513;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.chat-input__upload:hover:not(.disabled) {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  transform: scale(1.05);
}

.chat-input__upload.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Text input */
.chat-input__field {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: none;
  font-size: 0.95rem;
  outline: none;
  background: transparent;
  color: #333;
  min-width: 0;
}

.chat-input__field::placeholder {
  color: #999;
}

.chat-input__field:disabled {
  background: transparent;
  cursor: not-allowed;
}

/* Send button */
.chat-input__send {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(139, 69, 19, 0.3);
}

.chat-input__send:hover:not(.chat-input__send--disabled) {
  background: linear-gradient(135deg, #a0522d 0%, #8b4513 100%);
  transform: scale(1.05);
  box-shadow: 0 3px 6px rgba(139, 69, 19, 0.4);
}

.chat-input__send--disabled {
  background: #e9ecef;
  color: #adb5bd;
  cursor: not-allowed;
  box-shadow: none;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-input {
    padding: 0.4rem 0.6rem;
  }

  .chat-input__upload,
  .chat-input__send {
    width: 2rem;
    height: 2rem;
    font-size: 1rem;
  }

  .chat-input__field {
    font-size: 0.9rem;
    padding: 0.4rem 0.6rem;
  }

  .image-preview__img {
    max-width: 7rem;
    max-height: 7rem;
  }
}

@media (max-width: 480px) {
  .chat-input {
    padding: 0.35rem 0.5rem;
  }

  .chat-input__upload,
  .chat-input__send {
    width: 1.85rem;
    height: 1.85rem;
    font-size: 0.95rem;
  }

  .chat-input__field {
    font-size: 0.85rem;
  }

  .image-preview__img {
    max-width: 6rem;
    max-height: 6rem;
  }

  .image-preview__remove {
    width: 1.35rem;
    height: 1.35rem;
    font-size: 0.8rem;
  }
}
</style>