<template>
  <div class="heritage-view">
    <!-- HEADER -->
    <div class="content-container">
      <div class="banner-container">
        <img
          class="banner-image"
          src="../images/background_only.png"
          alt="Banner"
        />

        <!-- Lớp phủ gradient trắng nhạt dần từ trái qua phải -->
        <div class="gradient-overlay"></div>

        <!-- Logo bên trái -->
        <img
          class="banner-logo"
          src="../images/Green Grey Lotus Inn Logo (2).png"
          alt="Logo"
        />

        <div class="banner-text">
          <div class="text-vietnamese">DI SẢN VĂN HÓA CÁCH MẠNG TÂY NAM BỘ</div>
          <div class="text-english">
            REVOLUTIONARY CULTURAL HERITAGE OF SOUTHWEST VIETNAM
          </div>
        </div>
      </div>

      <!-- Main Content Wrapper -->
      <div
        class="main-wrapper"
        :class="{ 'full-width-content': currentView === 'heritage' }"
      >
        <!-- LEFT SIDEBAR - Menu -->
        <aside class="left-sidebar">
          <nav class="menu-section">
            <ul class="main-menu">
              <li
                class="menu-item"
                :class="{ active: currentView === 'home' }"
                @click="goToHome"
              >
                TRANG CHỦ
              </li>
              <li class="menu-item">GIỚI THIỆU</li>
              <li class="menu-item">TIN TỨC - SỰ KIỆN</li>
              <li
                class="menu-item"
                :class="{ active: currentView === 'heritage' }"
                @click="currentView = 'heritage'"
              >
                THÔNG TIN DI SẢN VĂN HÓA
              </li>
              <li class="menu-item">
                TRAO ĐỔI, HỢP TÁC, QUẢNG BÁ DI SẢN VĂN HÓA
              </li>
            </ul>
          </nav>

          <div class="menu-section">
            <h2 class="section-title">VĂN BẢN PHÁP LUẬT</h2>
            <ul class="sub-menu">
              <li>VĂN BẢN PHÁP LUẬT VIỆT NAM</li>
              <li>VĂN BẢN PHÁP LUẬT QUỐC TẾ</li>
              <li>TRA CỨU VĂN BẢN</li>
            </ul>
          </div>

          <div class="menu-section">
            <h2 class="section-title">ẤN PHẨM TÀI LIỆU</h2>
            <ul class="sub-menu">
              <li>TÀI LIỆU THAM KHẢO</li>
              <li>SÁCH XUẤT BẢN</li>
              <li>THƯ MỤC TÀI LIỆU</li>
            </ul>
          </div>

          <div class="menu-section">
            <h2 class="section-title">LIÊN KẾT WEBSITE</h2>
            <select class="select-box">
              <option value="">-- Liên kết website --</option>
              <option value="1">CỔNG THÔNG TIN DU LỊCH CẦN THƠ</option>
            </select>
          </div>
        </aside>

        <!-- CENTER CONTENT -->
        <main class="center-content">
          <!-- Hiển thị trang chủ -->
          <template v-if="currentView === 'home'">
            <!-- Hero Carousel - Tự động chuyển -->
            <div class="hero-carousel">
              <div class="carousel-wrapper">
                <div
                  class="carousel-slides"
                  :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
                >
                  <div
                    v-for="(slide, index) in carouselSlides"
                    :key="index"
                    class="carousel-slide"
                  >
                    <img :src="slide.image" :alt="slide.alt" />
                    <div class="carousel-caption">
                      {{ slide.caption }}
                    </div>
                  </div>
                </div>

                <!-- Nút điều khiển -->
                <button class="carousel-btn carousel-prev" @click="prevSlide">
                  ❮
                </button>
                <button class="carousel-btn carousel-next" @click="nextSlide">
                  ❯
                </button>

                <!-- Dots -->
                <div class="carousel-dots">
                  <span
                    v-for="(slide, index) in carouselSlides"
                    :key="index"
                    class="dot"
                    :class="{ active: currentSlide === index }"
                    @click="goToSlide(index)"
                  ></span>
                </div>
              </div>
            </div>

            <!-- Featured Banner Slider - Trượt ngang -->
            <div class="featured-banner-section">
              <button
                class="slider-control slider-control-left"
                @click="scrollLeft"
              >
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
                </svg>
              </button>

              <div class="featured-slider-container">
                <div class="featured-slider" ref="sliderContainer">
                  <div
                    v-for="(banner, index) in featuredBanners"
                    :key="index"
                    class="featured-banner"
                  >
                    <img :src="banner.image" :alt="banner.alt" />
                    <div class="banner-text">
                      {{ banner.text }}
                    </div>
                  </div>
                </div>
              </div>

              <button
                class="slider-control slider-control-right"
                @click="scrollRight"
              >
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
                </svg>
              </button>
            </div>

            <!-- News Sections -->
            <div class="news-grid">
              <!-- News Section 1 -->
              <div class="news-card">
                <div class="news-thumbnail">
                  <img
                    src="../images/Trien lam 90 nam Dang CSVN.jpg"
                    alt="News"
                  />
                </div>
                <div class="news-content">
                  <h3 class="news-title">
                    TIN TỨC - SỰ KIỆN <span class="badge-new">MỚI</span>
                  </h3>
                  <hr class="divider" />
                  <ul class="news-list">
                    <li>DI SẢN VĂN HÓA CÁCH MẠNG TÂY NAM BỘ ĐƯỢC ..</li>
                    <li>Bộ VHTTDL chỉ đạo khắc phục hậu quả thiên tai</li>
                    <li>Bồi dưỡng, tập huấn ngành Di sản văn hóa năm ..</li>
                    <li>Khai mạc trung bày "Di sản văn hóa Việt Nam – ..</li>
                    <li>Thêm 04 di tích được xếp hạng di tích quốc gi ..</li>
                  </ul>
                  <a href="#" class="view-more">Xem tiếp >>>></a>
                </div>
              </div>

              <!-- News Section 2 -->
              <div class="news-card">
                <div class="news-thumbnail">
                  <img
                    src="../images/Trien lam OC Eo tai Han Quoc 2020(1).jpg"
                    alt="Heritage Info"
                  />
                </div>
                <div class="news-content">
                  <h3 class="news-title">
                    THÔNG TIN DI SẢN VĂN HÓA <span class="badge-new">MỚI</span>
                  </h3>
                  <hr class="divider" />
                  <ul class="news-list">
                    <li>Khu vực Cầu Kinh – Nơi ghi dấu chiến công của ..</li>
                    <li>Chùa Hội Linh</li>
                    <li>DI SẢN VĂN HÓA CÁCH MẠNG TÂY NAM BỘ ĐƯỢC ..</li>
                  </ul>
                  <a href="#" class="view-more">Xem tiếp >>>></a>
                </div>
              </div>
            </div>
          </template>

          <!-- Hiển thị trang Thông tin Di sản Văn hóa -->
          <HeritageInfo v-else-if="currentView === 'heritage'" />
        </main>

        <!-- RIGHT SIDEBAR - Chỉ hiển thị khi ở trang chủ -->
        <aside class="right-sidebar" v-if="currentView === 'home'">
          <div class="date-display">
            <p>Ngày 16 tháng 12 năm 2025</p>
          </div>

          <!-- Media Tabs -->
          <div class="media-section">
            <div class="media-tabs">
              <button
                class="media-tab"
                :class="{ active: activeTab === 'image' }"
                @click="activeTab = 'image'"
              >
                ẢNH
              </button>
              <button
                class="media-tab"
                :class="{ active: activeTab === 'video' }"
                @click="activeTab = 'video'"
              >
                VIDEO
              </button>
            </div>

            <div class="media-content">
              <div v-if="activeTab === 'image'" class="media-grid">
                <img src="../images/24.jpg" alt="Gallery" />
              </div>
              <div v-else class="video-player">
                <video controls>
                  <source
                    src="../images/TRAILER LỄ HỘI ĐỀN HÙNG final sua17-4.mp4.crdownload"
                    type="video/mp4"
                  />
                </video>
                <p class="video-caption">Xem tất cả</p>
              </div>
            </div>
          </div>

          <!-- Notifications -->
          <div class="notification-section">
            <div class="section-header">
              <span class="notification-icon">🔔</span>
              <h3>THÔNG BÁO MỚI</h3>
            </div>
            <div class="notification-list">
              <div class="notification-item">
                <p>
                  Bồi dưỡng, tập huấn hàng cao nhân thức và kiến thức chuyên môn
                  nghiệp ... <span class="new-badge">NEW!</span>
                </p>
              </div>
              <hr class="notification-divider" />
              <div class="notification-item">
                <p>
                  Bộ Văn hóa, Thể thao và Du lịch thông báo tuyển dụng công chức
                  năm 202... <span class="new-badge">NEW!</span>
                </p>
              </div>
              <hr class="notification-divider" />
              <div class="notification-item">
                <p>
                  Trang Thông tin điện tử đang trong quá trình nâng cấp. Tổ
                  chức, cá nhà... <span class="new-badge">NEW!</span>
                </p>
              </div>
            </div>
          </div>

          <!-- Quick Links with Images -->
          <div class="quick-links">
            <div class="link-card">
              <img src="../images/thu tuc hanh chinh.png" alt="Info System" />
            </div>
            <div class="link-card">
              <img
                src="../images/ht thong tin ql dsvh phi vat the.png"
                alt="Info System"
              />
            </div>
            <div class="link-card">
              <img
                src="../images/he thong thong tin ql bảo tàng.png"
                alt="Info System"
              />
            </div>
            <div class="link-card">
              <img
                src="../images/LogoDanhmucchungchihanhnghe(1).png"
                alt="Info System"
              />
            </div>
            <div class="link-card">
              <img
                src="../images/Logotailieuphongchongruiro(1).jpg"
                alt="Info System"
              />
            </div>
          </div>
        </aside>
      </div>

      <footer class="footer">
        <div class="footer-content">
          <div class="footer-info">
            <p>
              <strong>Địa chỉ:</strong> 25 Nguyễn Văn Linh, Hưng Lợi, Ninh Kiều, Cần Thơ, Việt Nam
            </p>
            <p>
              <strong>Tel:</strong> (84-24) 12345678 *
              <strong>Fax:</strong> (84-24) 12345678 *
              <strong>Email:</strong> abc@gmail.com
            </p>
            <p>© 2025 Bản quyền thuộc luận văn về Di sản văn hóa cách mạng Tây Nam Bộ</p>
            <p>
              <strong>Chịu trách nhiệm chính:</strong> SV. Lê Thị Ngọc Ngân
            </p>
          </div>

          <div class="footer-stats">
            <p>
              <strong>Đang truy cập:</strong>
              <span class="stat-number">957</span>
            </p>
            <p>
              <strong>Tổng:</strong> <span class="stat-number">1,101,474</span>
            </p>
          </div>
        </div>
      </footer>
    </div>

    <!-- Chatbot Button Component -->
    <ChatbotButton />
  </div>
</template>

<script>
import ChatbotButton from "../components/ChatbotButton.vue";
import HeritageInfo from "../components/HeritageInfo.vue";

export default {
  components: {
    ChatbotButton,
    HeritageInfo,
  },

  data() {
    return {
      currentView: "home",
      activeTab: "image",

      // Carousel
      currentSlide: 0,
      carouselInterval: null,
      carouselSlides: [
        {
          image: new URL(
            "../images/27-8-cac-dai-bieu-tham-quan-trien-lam-1363-7472.jpg.webp",
            import.meta.url
          ).href,
          alt: "Heritage slide 1",
          caption:
            "KHAI MẠC TRIỂN LÃM DI SẢN VĂN HÓA CẦN THƠ: HÀNH TRÌNH BẢO TỒN VÀ TRUYỀN THỐNG",
        },
        {
          image: new URL("../images/49.png", import.meta.url).href,
          alt: "Heritage slide 2",
          caption:
            "CHÙA HỘI LINH - DI TÍCH LỊCH SỬ VĂN HÓA QUAN TRỌNG CỦA CẦN THƠ",
        },
        {
          image: new URL("../images/2.jpg", import.meta.url).href,
          alt: "Heritage slide 3",
          caption:
            "DI TÍCH LỊCH SỬ CHƯƠNG THIỆN - BIỂU TƯỢNG CỦA TINH THẦN CÁCH MẠNG",
        },
      ],

      // Featured Banners
      featuredBanners: [
        {
          image: new URL("../images/5.webp", import.meta.url).href,
          alt: "Featured 1",
          text: "THỦ TƯỚNG CHÍNH PHỦ KÝ QUYẾT ĐỊNH CÔNG NHẬN BẢO VẬT QUỐC GIA ĐỢT 11",
        },
        {
          image: new URL("../images/1.png", import.meta.url).href,
          alt: "Featured 2",
          text: "BỘ VĂN HÓA CÔNG BỐ DANH SÁCH DI SẢN VĂN HÓA PHI VẬT THỂ MỚI",
        },
        {
          image: new URL("../images/27.jpg", import.meta.url).href,
          alt: "Featured 3",
          text: "HỘI NGHỊ BẢO TỒN VÀ PHÁT HUY GIÁ TRỊ DI SẢN VĂN HÓA",
        },
        {
          image: new URL("../images/32.jpg", import.meta.url).href,
          alt: "Featured 4",
          text: "KHAI MẠC TRIỂN LÃM DI SẢN VĂN HÓA CẦN THƠ",
        },
      ],
    };
  },

  mounted() {
    this.startCarousel();
  },

  beforeUnmount() {
    if (this.carouselInterval) {
      clearInterval(this.carouselInterval);
    }
  },

  methods: {
    // Method để quay về trang chủ và reset
    goToHome() {
      this.currentView = "home";
      // Reset carousel
      this.currentSlide = 0;
      if (this.carouselInterval) {
        clearInterval(this.carouselInterval);
      }
      this.startCarousel();
    },

    // Carousel methods
    startCarousel() {
      this.carouselInterval = setInterval(() => {
        this.nextSlide();
      }, 3000);
    },

    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.carouselSlides.length;
    },

    prevSlide() {
      this.currentSlide =
        this.currentSlide === 0
          ? this.carouselSlides.length - 1
          : this.currentSlide - 1;
    },

    goToSlide(index) {
      this.currentSlide = index;
      clearInterval(this.carouselInterval);
      this.startCarousel();
    },

    // Slider methods
    scrollLeft() {
      this.$refs.sliderContainer.scrollBy({
        left: -350,
        behavior: "smooth",
      });
    },

    scrollRight() {
      this.$refs.sliderContainer.scrollBy({
        left: 350,
        behavior: "smooth",
      });
    },
  },
};
</script>

<style scoped>
/* Reset cơ bản */
* {
  box-sizing: border-box;
}

/* Container chính */
.heritage-view {
  min-height: 100vh;
  width: 100%;
  background-image: url("@/images/bg.jpg");
  background-repeat: repeat;
  background-size: auto;
  background-position: top left;
  background-color: #f5f0e8;
  overflow-x: hidden;
  overflow-y: auto;
  position: relative;
}

/* Container cho toàn bộ nội dung với margin 5rem */
.content-container {
  margin: 0 5rem;
  width: calc(100% - 10rem);
}

/* Banner */
.banner-container {
  width: 100%;
  margin-bottom: 1rem;
}

.banner-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  display: block;
}

/* Main wrapper */
.main-wrapper {
  background-image: url(../images/bg-content.jpg);
  background-repeat: repeat;
  background-size: auto;
  background-position: top left;
  background-color: #f5f0e8;
  display: grid;
  grid-template-columns: 280px 1fr 380px;
  gap: 1.5rem;
  padding: 1.5rem;
  min-height: auto;
  transition: grid-template-columns 0.3s ease;
}

/* Khi ở trang Heritage Info - Ẩn sidebar phải */
.main-wrapper.full-width-content {
  grid-template-columns: 280px 1fr;
}

/* LEFT SIDEBAR */
.left-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.menu-section {
  background: transparent;
}

.main-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  padding: 0.75rem 0;
  font-weight: 600;
  font-size: 0.875rem;
  color: #8b4513;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 1px solid rgba(139, 69, 19, 0.2);
}

.menu-item:hover {
  color: #d2691e;
  background: rgba(210, 105, 30, 0.05);
  padding-left: 0.5rem;
}

.menu-item.active {
  color: #d2691e;
  background: rgba(210, 105, 30, 0.1);
  padding-left: 0.5rem;
  border-left: 3px solid #d2691e;
}

.section-title {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  padding: 0.75rem 1rem;
  margin: 1.25rem 0 0.625rem 0;
  font-size: 0.875rem;
  font-weight: 700;
  border-radius: 0.5rem 0.5rem 0 0;
  text-transform: uppercase;
}

.sub-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  background: white;
  border-radius: 0 0 0.5rem 0.5rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
}

.sub-menu li {
  padding: 0.625rem 1rem;
  font-size: 0.8125rem;
  color: #333;
  cursor: pointer;
  transition: background 0.3s;
  border-bottom: 1px solid #eee;
}

.sub-menu li:last-child {
  border-bottom: none;
}

.sub-menu li:hover {
  background: #f9f6f0;
}

.select-box {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #8b4513;
  border-radius: 0.375rem;
  background: white;
  color: #666;
  font-size: 0.8125rem;
  cursor: pointer;
  margin-top: 0.625rem;
}

/* CENTER CONTENT */
.center-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  min-width: 0;
}

/* ========== HERO CAROUSEL ========== */
.hero-carousel {
  position: relative;
  width: 100%;
  height: 25rem;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.15);
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.carousel-slides {
  display: flex;
  height: 100%;
  width: 100%;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  position: relative;
  min-width: 100%;
  max-width: 100%;
  width: 100%;
  height: 100%;
  flex-shrink: 0;
  flex-grow: 0;
}

.carousel-slide img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  padding: 1.875rem 1.25rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.6;
  z-index: 2;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  font-size: 1.5rem;
  color: #8b4513;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s;
}

.carousel-btn:hover {
  background: white;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.2);
}

.carousel-prev {
  left: 1rem;
}

.carousel-next {
  right: 1rem;
}

.carousel-dots {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  background: white;
  width: 2rem;
  border-radius: 0.375rem;
}

/* ========== FEATURED SLIDER ========== */
.featured-banner-section {
  position: relative;
  width: 100%;
  margin: 1rem 0;
}

.slider-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(139, 69, 19, 0.9);
  border: none;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slider-control:hover {
  background: #8b4513;
  transform: translateY(-50%) scale(1.1);
}

.slider-control-left {
  left: -1rem;
}

.slider-control-right {
  right: -1rem;
}

.featured-slider-container {
  width: 100%;
  overflow: hidden;
  padding: 0 1rem;
}

.featured-slider {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding: 0.5rem 0;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.featured-slider::-webkit-scrollbar {
  display: none;
}

.featured-banner {
  position: relative;
  min-width: 22rem;
  max-width: 22rem;
  height: 12rem;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
  transition: transform 0.3s;
}

.featured-banner:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
}

.featured-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-text {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.9375rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-align: center;
  line-height: 1.4;
}

/* NEWS GRID */
.news-grid {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.news-card {
  display: grid;
  grid-template-columns: 12.5rem 1fr;
  gap: 1.25rem;
  background: white;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 0.125rem 0.75rem rgba(0, 0, 0, 0.08);
}

.news-thumbnail {
  width: 100%;
  height: 9.375rem;
  border-radius: 0.5rem;
  overflow: hidden;
}

.news-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-content {
  display: flex;
  flex-direction: column;
}

.news-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.625rem 0;
  text-transform: uppercase;
}

.badge-new {
  background: #ff0000;
  color: white;
  padding: 0.125rem 0.5rem;
  font-size: 0.6875rem;
  border-radius: 0.25rem;
  margin-left: 0.5rem;
}

.divider {
  border: none;
  border-top: 0.125rem solid #8b4513;
  margin: 0 0 0.9375rem 0;
}

.news-list {
  list-style: disc;
  padding-left: 1.25rem;
  margin: 0 0 0.9375rem 0;
  flex-grow: 1;
}

.news-list li {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #555;
  line-height: 1.6;
}

.view-more {
  color: #d2691e;
  font-weight: 600;
  text-decoration: none;
  align-self: flex-end;
  font-size: 0.875rem;
}

.view-more:hover {
  text-decoration: underline;
}

/* RIGHT SIDEBAR */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.date-display {
  text-align: right;
  font-style: italic;
  color: #666;
  font-size: 0.875rem;
  padding: 0.625rem 0;
}

.media-section {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.75rem rgba(0, 0, 0, 0.08);
}

.media-tabs {
  display: flex;
  border-bottom: 0.125rem solid #e0e0e0;
}

.media-tab {
  flex: 1;
  padding: 0.9375rem;
  background: #f5f5f5;
  border: none;
  font-weight: 700;
  font-size: 0.875rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.media-tab.active {
  background: #8b4513;
  color: white;
}

.media-content {
  padding: 1.25rem;
}

.media-grid img {
  width: 100%;
  border-radius: 0.5rem;
}

.video-player video {
  width: 100%;
  border-radius: 0.5rem;
}

.video-caption {
  text-align: center;
  margin-top: 0.625rem;
  color: #666;
  font-size: 0.875rem;
}

.notification-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 0.125rem 0.75rem rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
  padding: 0.75rem 1rem;
  margin: -1.25rem -1.25rem 0.9375rem -1.25rem;
  border-radius: 0.75rem 0.75rem 0 0;
}

.section-header h3 {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
}

.notification-list {
  display: flex;
  flex-direction: column;
}

.notification-item {
  padding: 0.75rem 0;
}

.notification-item p {
  margin: 0;
  font-size: 0.8125rem;
  color: #333;
  line-height: 1.6;
}

.new-badge {
  background: #ff0000;
  color: white;
  padding: 0.125rem 0.375rem;
  font-size: 0.625rem;
  font-weight: 700;
  border-radius: 0.1875rem;
  margin-left: 0.3125rem;
}

.notification-divider {
  border: none;
  border-top: 1px solid #eee;
  margin: 0;
}

.quick-links {
  display: flex;
  flex-direction: column;
  gap: 0.9375rem;
}

.link-card {
  position: relative;
  height: 7.5rem;
  border-radius: 0.5rem;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.link-card:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.15);
}

.link-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== FOOTER ========== */
.footer {
  background-image: url(../images/bg-content.jpg);
  background-repeat: repeat;
  background-size: auto;
  background-position: top left;
  background-color: #f5f0e8;
  padding: 2rem 1.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.1);
  position: relative;
}

.footer-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2rem;
  align-items: start;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-info p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.6;
}

.footer-info strong {
  font-weight: 700;
}

.footer-note {
  font-style: italic;
  margin-top: 0.5rem !important;
  opacity: 0.9;
}

.footer-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  min-width: 12rem;
  backdrop-filter: blur(5px);
}

.footer-stats p {
  margin: 0;
  font-size: 0.875rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-number {
  font-size: 1.125rem;
  font-weight: 700;
  color: #3300ff;
  margin-left: 1rem;
}

/* Responsive Design */
@media (max-width: 1400px) {
  .content-container {
    margin: 0 3rem;
    width: calc(100% - 6rem);
  }
}

@media (max-width: 1200px) {
  .content-container {
    margin: 0 2rem;
    width: calc(100% - 4rem);
  }

  .main-wrapper {
    grid-template-columns: 15rem 1fr 20rem;
  }

  .main-wrapper.full-width-content {
    grid-template-columns: 15rem 1fr;
  }

  .featured-banner {
    min-width: 18rem;
    max-width: 18rem;
  }
}

@media (max-width: 992px) {
  .content-container {
    margin: 0 1rem;
    width: calc(100% - 2rem);
  }

  .main-wrapper,
  .main-wrapper.full-width-content {
    grid-template-columns: 1fr;
  }

  .left-sidebar,
  .right-sidebar {
    display: none;
  }

  .featured-banner {
    min-width: 16rem;
    max-width: 16rem;
  }
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
  }

  .footer-stats {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .content-container {
    margin: 0 0.5rem;
    width: calc(100% - 1rem);
  }

  .hero-carousel {
    height: 18rem;
  }

  .carousel-btn {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1.2rem;
  }

  .featured-banner {
    min-width: 14rem;
    max-width: 14rem;
    height: 10rem;
  }

  .slider-control {
    width: 2.5rem;
    height: 2.5rem;
  }
}

.banner-container {
  position: relative;
  width: 100%;
  height: 140px;
  overflow: hidden;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
}

/* Lớp phủ gradient trắng nhạt dần từ trái qua phải */
.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 70%; /* Chiếm 70% chiều rộng */
  height: 100%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 1) 0%,
    /* Trắng đục bên trái */ rgba(255, 255, 255, 0.9) 25%,
    rgba(255, 255, 255, 0.7) 50%,
    rgba(255, 255, 255, 0.3) 75%,
    rgba(255, 255, 255, 0) 100% /* Trong suốt hoàn toàn bên phải */
  );
  z-index: 1;
}

/* Logo bên trái */
.banner-logo {
  position: absolute;
  left: 30px;
  top: 50%;
  transform: translateY(-50%);
  height: 75%;
  width: auto;
  z-index: 2;
  object-fit: contain;
}

/* Text bên phải */
.banner-text {

  position: absolute;
  right: 50px;
  top: 40%;
  transform: translateY(-50%);
  text-align: right;
  z-index: 10;
  background: none;
}

.text-vietnamese {
  font-size: 48px;
  color: #b41e28;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 8px;
  text-shadow: 
    -1px -1px 0 #fff,
     1px -1px 0 #fff,
    -1px  1px 0 #fff,
     1px  1px 0 #fff,
    -1px  0   0 #fff,
     1px  0   0 #fff,
     0   -1px 0 #fff,
     0    1px 0 #fff;
}

.text-english {
  font-size: 22px;
  color: #503c28;
  font-weight: 500;
  /* KHÔNG có text-shadow - không có viền */
}

.text-vietnamese {
  font-size: 38px;
  color: #b41e28;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 8px;
}

.text-english {
  font-size: 22px;
  color: #503c28;
  font-weight: 500;
}

/* Responsive cho mobile */
@media (max-width: 768px) {
  .banner-container {
    height: 120px;
  }

  .banner-logo {
    height: 60%;
    left: 15px;
  }

  .gradient-overlay {
    width: 80%;
  }
}
</style>
