<template>
  <div class="test-container">
    <h1>🧪 Test Chỉnh Chính Tả Tiếng Việt</h1>
    
    <div class="test-section">
      <h2>Nhập văn bản test:</h2>
      <textarea 
        v-model="inputText" 
        placeholder="Ví dụ: ddaay laf ddaau"
        rows="4"
      ></textarea>
      
      <button 
        @click="testSpellCheck" 
        :disabled="isChecking || !inputText.trim()"
        class="btn-test"
      >
        {{ isChecking ? 'Đang kiểm tra...' : 'Kiểm tra chính tả' }}
      </button>
    </div>
    
    <div v-if="result" class="result-section">
      <h2>📊 Kết quả:</h2>
      
      <div class="result-card">
        <div class="result-item">
          <strong>Text gốc:</strong>
          <div class="text-box original">{{ result.original }}</div>
        </div>
        
        <div class="result-item">
          <strong>Text đã sửa:</strong>
          <div class="text-box corrected">{{ result.corrected }}</div>
        </div>
        
        <div class="result-item">
          <strong>Có thay đổi:</strong>
          <span :class="result.hasCorrected ? 'badge-yes' : 'badge-no'">
            {{ result.hasCorrected ? '✅ Có' : '❌ Không' }}
          </span>
        </div>
        
        <div v-if="result.hasCorrected" class="result-item highlight">
          <strong>⚡ So sánh:</strong>
          <div class="comparison">
            <span class="old">{{ result.original }}</span>
            <span class="arrow">→</span>
            <span class="new">{{ result.corrected }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Test cases mẫu -->
    <div class="examples-section">
      <h2>📝 Các test case mẫu:</h2>
      <div class="examples-grid">
        <button 
          v-for="(example, index) in examples" 
          :key="index"
          @click="inputText = example"
          class="example-btn"
        >
          {{ example }}
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-message">
      ❌ Lỗi: {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { correctVietnameseSpelling } from '../services/spellcheck';

const inputText = ref('');
const result = ref(null);
const isChecking = ref(false);
const error = ref('');

const examples = [
  'ddaay laf ddaau',
  'tooi muuon di choi',
  'caau hỏii vềe ddi tícch',
  'Khaam Lớn Cần Thơ ở đâuu',
  'nha thờ đức bà có đepẹ khong',
  'chùaa ông đươc xây nămm naof'
];

async function testSpellCheck() {
  if (!inputText.value.trim()) return;
  
  isChecking.value = true;
  error.value = '';
  result.value = null;
  
  try {
    const spellCheckResult = await correctVietnameseSpelling(inputText.value);
    
    result.value = {
      original: inputText.value,
      corrected: spellCheckResult.corrected,
      hasCorrected: spellCheckResult.hasCorrected
    };
    
    console.log('🎯 Test Result:', result.value);
    
  } catch (err) {
    error.value = err.message;
    console.error('Test error:', err);
  } finally {
    isChecking.value = false;
  }
}
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  color: #8b4513;
  text-align: center;
  margin-bottom: 2rem;
}

h2 {
  color: #333;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.test-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 1rem;
}

textarea:focus {
  outline: none;
  border-color: #8b4513;
}

.btn-test {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-test:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
}

.btn-test:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.result-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.text-box {
  padding: 1rem;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 500;
}

.text-box.original {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  color: #856404;
}

.text-box.corrected {
  background: #d1ecf1;
  border-left: 4px solid #17a2b8;
  color: #0c5460;
}

.badge-yes {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #d4edda;
  color: #155724;
  border-radius: 20px;
  font-weight: 600;
}

.badge-no {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f8d7da;
  color: #721c24;
  border-radius: 20px;
  font-weight: 600;
}

.highlight {
  background: #f0f8ff;
  padding: 1rem;
  border-radius: 6px;
  border: 2px solid #17a2b8;
}

.comparison {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.2rem;
  margin-top: 0.5rem;
}

.comparison .old {
  color: #dc3545;
  text-decoration: line-through;
  font-weight: 500;
}

.comparison .arrow {
  color: #666;
  font-size: 1.5rem;
}

.comparison .new {
  color: #28a745;
  font-weight: 600;
}

.examples-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.example-btn {
  padding: 0.75rem;
  background: #f8f9fa;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.example-btn:hover {
  background: #e9ecef;
  border-color: #8b4513;
  transform: scale(1.02);
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 6px;
  border-left: 4px solid #dc3545;
}

@media (max-width: 768px) {
  .test-container {
    padding: 1rem;
  }
  
  .examples-grid {
    grid-template-columns: 1fr;
  }
}
</style>