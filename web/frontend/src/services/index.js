// src/services/vqaService.js

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Gọi API dự đoán VQA
 * @param {File} imageFile - File ảnh
 * @param {string} question - Câu hỏi
 */
export async function predictVQA(imageFile, question) {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('question', question);
  
  const response = await fetch(`${API_BASE_URL}/predict/`, {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Prediction failed');
  }
  
  return response.json();
}

/**
 * Kiểm tra backend có sẵn sàng không
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health/`);
    return response.json();
  } catch (error) {
    console.error('Lỗi kết nối backend:', error);
    return { status: 'error', model_loaded: false };
  }
}