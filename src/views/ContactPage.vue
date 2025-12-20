<template>
  <div class="contact-page" :class="{ 'dark-mode': isDark }">
    <Navbar />
    
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <h1 class="page-title">تماس با ما</h1>
        <p class="page-subtitle">ما آماده‌ایم از شما بشنویم و به سوالات شما پاسخ دهیم</p>
      </div>
    </section>

    <!-- Main Contact Content -->
    <section class="contact-content">
      <div class="container">
        <div class="contact-grid">
          <!-- Left: Contact Form -->
          <div class="contact-form-section">
            <ContactForm />
          </div>

          <!-- Right: Contact Info & Phone Numbers -->
          <div class="contact-info-section">
            <!-- Basic Info -->
            <div class="info-card">
              <h3 class="info-title">اطلاعات تماس</h3>
              
              <div class="info-item">
                <span class="info-icon">📧</span>
                <div class="info-content">
                  <h5>ایمیل</h5>
                  <a href="mailto:info@b1m.ir">info@b1m.ir</a>
                </div>
              </div>

              <div class="info-item">
                <span class="info-icon">📍</span>
                <div class="info-content">
                  <h5>دفتر مرکزی</h5>
                  <p>تهران، ایران<br>زعفرانیه، تقاطع بلوار بهزادی و ماکویی پور<br>ساختمان سروین، طبقه 3، واحد 33</p>
                </div>
              </div>

              <div class="info-item">
                <span class="info-icon">🕒</span>
                <div class="info-content">
                  <h5>ساعات کاری</h5>
                  <p>شنبه تا پنج‌شنبه: ۹ صبح تا ۶ عصر</p>
                </div>
              </div>
            </div>

            <!-- Phone Numbers Section -->
            <div class="phone-section">
              <h3 class="phone-title">
                <span class="title-icon">📞</span>
                شماره تماس شعبه‌ها
              </h3>

              <div class="phone-grid">
                <!-- Cities -->
                <div class="phone-card city">
                  <div class="card-icon">🏛️</div>
                  <div class="card-content">
                    <div class="city-name">تهران</div>
                    <a href="tel:02191094014" class="phone-number">021-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">🕌</div>
                  <div class="card-content">
                    <div class="city-name">اصفهان</div>
                    <a href="tel:03191094014" class="phone-number">031-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">🏜️</div>
                  <div class="card-content">
                    <div class="city-name">کرمان</div>
                    <a href="tel:03491094014" class="phone-number">034-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">🏛️</div>
                  <div class="card-content">
                    <div class="city-name">یزد</div>
                    <a href="tel:03591094014" class="phone-number">035-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">⭐</div>
                  <div class="card-content">
                    <div class="city-name">مشهد</div>
                    <a href="tel:05191094014" class="phone-number">051-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">🌹</div>
                  <div class="card-content">
                    <div class="city-name">شیراز</div>
                    <a href="tel:07191094014" class="phone-number">071-91094014</a>
                  </div>
                </div>

                <div class="phone-card city">
                  <div class="card-icon">🏝️</div>
                  <div class="card-content">
                    <div class="city-name">کیش</div>
                    <a href="tel:07691094014" class="phone-number">076-91094014</a>
                  </div>
                </div>

                <!-- Support -->
                <div class="phone-card support">
                  <div class="card-icon">🎧</div>
                  <div class="card-content">
                    <div class="city-name">پشتیبانی ۱</div>
                    <a href="tel:09120064014" class="phone-number">0912-0064014</a>
                  </div>
                </div>

                <div class="phone-card support">
                  <div class="card-icon">💬</div>
                  <div class="card-content">
                    <div class="city-name">پشتیبانی ۲</div>
                    <a href="tel:09130064014" class="phone-number">0913-0064014</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { inject } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import ContactForm from '../components/ContactForm.vue'

const { isDark } = inject('theme')
</script>

<style scoped>
.contact-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding-top: 80px;
  transition: background 0.3s ease;
}

.contact-page.dark-mode {
  background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
}

.hero-section {
  padding: 3rem 0 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.contact-page.dark-mode .hero-section {
  background: rgba(0, 0, 0, 0.3);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #555;
}

.contact-page.dark-mode .page-subtitle {
  color: #aaa;
}

.contact-content {
  padding: 4rem 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: start;
}

.contact-form-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.contact-page.dark-mode .contact-form-section {
  background: #1a1a1a;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.contact-info-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.contact-page.dark-mode .info-card {
  background: #1a1a1a;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.info-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

.contact-page.dark-mode .info-title {
  color: #fff;
}

.info-item {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.contact-page.dark-mode .info-item {
  border-bottom-color: #333;
}

.info-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.info-content h5 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.contact-page.dark-mode .info-content h5 {
  color: #fff;
}

.info-content p,
.info-content a {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.6;
}

.contact-page.dark-mode .info-content p,
.contact-page.dark-mode .info-content a {
  color: #aaa;
}

.info-content a {
  text-decoration: none;
  transition: color 0.3s ease;
}

.info-content a:hover {
  color: #0ea5e9;
}

/* Phone Numbers Section */
.phone-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.contact-page.dark-mode .phone-section {
  background: #1a1a1a;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.phone-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

.contact-page.dark-mode .phone-title {
  color: #fff;
}

.title-icon {
  font-size: 2rem;
}

.phone-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.phone-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.contact-page.dark-mode .phone-card {
  background: #2a2a2a;
}

.phone-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.phone-card.support::before {
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
}

.phone-card:hover {
  border-color: #0ea5e9;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.phone-card.support:hover {
  border-color: #34d399;
  box-shadow: 0 8px 20px rgba(52, 211, 153, 0.15);
}

.phone-card:hover::before {
  opacity: 1;
}

.card-icon {
  font-size: 1.75rem;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.phone-card:hover .card-icon {
  transform: scale(1.15) rotate(5deg);
}

.card-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.city-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #666;
  margin-bottom: 0.25rem;
  transition: color 0.3s ease;
}

.contact-page.dark-mode .city-name {
  color: #aaa;
}

.phone-card:hover .city-name {
  color: #0ea5e9;
}

.phone-card.support:hover .city-name {
  color: #34d399;
}

.phone-number {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  text-decoration: none;
  direction: ltr;
  font-family: 'Courier New', monospace;
  transition: all 0.3s ease;
}

.contact-page.dark-mode .phone-number {
  color: #fff;
}

.phone-number:hover {
  color: #0ea5e9;
  transform: translateX(-2px);
}

.phone-card.support:hover .phone-number {
  color: #34d399;
}

/* Responsive */
@media (max-width: 1024px) {
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .phone-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .contact-content {
    padding: 2rem 0;
  }

  .contact-form-section,
  .info-card,
  .phone-section {
    padding: 1.5rem;
  }

  .info-title,
  .phone-title {
    font-size: 1.25rem;
  }

  .phone-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .phone-card {
    padding: 1rem;
    gap: 0.5rem;
  }

  .card-icon {
    font-size: 1.5rem;
  }

  .city-name {
    font-size: 0.75rem;
  }

  .phone-number {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }

  .contact-form-section,
  .info-card,
  .phone-section {
    padding: 1rem;
  }

  .phone-grid {
    grid-template-columns: 1fr;
  }

  .phone-card {
    flex-direction: column;
    text-align: center;
  }

  .card-content {
    text-align: center;
  }

  .phone-number {
    direction: ltr;
    text-align: center;
  }
}
</style>
