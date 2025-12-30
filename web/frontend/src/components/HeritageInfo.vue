<!-- HeritageInfo.vue -->
<template>
  <div class="heritage-info">
    <h2>Danh sách di sản văn hóa</h2>

    <!-- Danh sách di tích -->
    <ul class="heritage-list">
      <li 
        v-for="heritage in heritages" 
        :key="heritage.id" 
        @click="selectHeritage(heritage)"
        class="heritage-item"
      >
        <div class="heritage-card">
          <img :src="heritage.image" :alt="heritage.name" class="heritage-thumb" />
          <div class="heritage-overlay">
            <h4 class="heritage-title">{{ heritage.name }}</h4>
            <p class="heritage-desc">{{ heritage.shortDesc }}</p>
          </div>
        </div>
      </li>
    </ul>

    <!-- Thông tin chi tiết -->
    <div v-if="selectedHeritage" class="heritage-detail">
      <h3>{{ selectedHeritage.name }}</h3>
      <img :src="selectedHeritage.image" :alt="selectedHeritage.name" class="detail-image" />
      <p>{{ selectedHeritage.description }}</p>
      <button @click="closeDetail">Đóng</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Dữ liệu mẫu
const heritages = ref([
  {
    id: 1,
    name: 'Di tích lịch sử Chiến thắng Chương Thiện',
    shortDesc: 'Di sản Văn hóa Cách mạng cấp Quốc gia đặc biệt',
    image: new URL("../images/2.jpg", import.meta.url)
            .href,
    description: 'Di tích lịch sử Chiến thắng Chương Thiện tọa lạc tại thành phố Vị Thanh và huyện Long Mỹ, tỉnh Hậu Giang. Đây là địa bàn chiến lược trong kháng chiến chống Mỹ, nơi quân – dân Khu 9 đã giành chiến thắng quan trọng vào năm 1973, đánh bại nhiều tiểu đoàn địch, bảo vệ vùng và góp phần mở đường cho Tổng tiến công năm 1975. Di tích hiện nay được xây dựng thành khu trưng bày hiện vật, tượng đài và sân lễ, lưu giữ nhiều tư liệu, hiện vật quân trang và dấu tích lịch sử, là Di tích Quốc gia đặc biệt, thể hiện giá trị lịch sử, văn hóa và truyền thống cách mạng của địa phương.'
  },
  {
    id: 2,
    name: 'Địa điểm thành lập Đảng An Nam Cộng sản (Đảng Cờ Đỏ)',
    shortDesc: 'Di sản Văn hóa Cách mạng cấp Quốc gia',
     image: new URL("../images/1.png", import.meta.url)
            .href,
    description: 'Di sản văn hóa cách mạng – Địa điểm thành lập Đảng An Nam Cộng sản (Đảng Cờ Đỏ) tọa lạc tại Cờ Đỏ, TP. Cần Thơ. Đây là nơi tổ chức thành lập chi bộ Đảng Cộng sản đầu tiên ở Nam Bộ, đánh dấu bước ngoặt trong phong trào cách mạng tại miền Nam Việt Nam. Di tích hiện được bảo tồn với nhà trưng bày, hiện vật lịch sử và không gian giáo dục truyền thống cách mạng, góp phần nhắc nhở về tinh thần đấu tranh vì độc lập, tự do của dân tộc.'
  },
  {
    id: 3,
    name: 'Di tích lịch sử – Chiến thắng Tầm Vu',
    shortDesc: 'Di sản Văn hóa Cách mạng cấp Tỉnh/Thành Phố',
     image: new URL("../images/2.jpeg", import.meta.url)
            .href,
    description: 'Di tích lịch sử – Chiến thắng Tầm Vu là địa điểm ghi dấu chiến thắng quan trọng trong kháng chiến chống Pháp/Mỹ (tùy theo bối cảnh cụ thể, cần xác định rõ), thể hiện tinh thần chiến đấu kiên cường của quân và dân địa phương. Di tích hiện được bảo tồn, trưng bày hiện vật, hình ảnh và tài liệu lịch sử, góp phần giáo dục truyền thống yêu nước và cách mạng cho thế hệ trẻ.'
  }
]);

const selectedHeritage = ref(null);

function selectHeritage(heritage) {
  selectedHeritage.value = heritage;
}

function closeDetail() {
  selectedHeritage.value = null;
}
</script>

<style scoped>
.heritage-info {
  padding: 1.5rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 0.125rem 0.75rem rgba(0, 0, 0, 0.08);
}

h2 {
  color: #8b4513;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.heritage-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 1.5rem;
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}

.heritage-item {
  cursor: pointer;
  transition: transform 0.2s;
}

.heritage-item:hover {
  transform: scale(1.05);
}

.heritage-card {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.heritage-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.heritage-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.4) 70%, rgba(0, 0, 0, 0) 100%);
  color: white;
}

.heritage-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: white;
}

.heritage-desc {
  font-size: 0.875rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.heritage-detail {
  margin-top: 2rem;
  border-top: 2px solid #8b4513;
  padding-top: 1.5rem;
}

.heritage-detail h3 {
  color: #8b4513;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.detail-image {
  width: 100%;
  max-width: 400px;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.heritage-detail p {
  line-height: 1.6;
  color: #555;
  margin-bottom: 1rem;
}

.heritage-detail button {
  padding: 0.5rem 1.5rem;
  background: #8b4513;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}

.heritage-detail button:hover {
  background: #a0522d;
}
</style>