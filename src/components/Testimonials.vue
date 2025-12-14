<template>
  <section class="testimonials-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">نظرات مشتریان</h2>
        <p class="section-subtitle">آنچه مشتریان ما درباره ما می‌گویند</p>
      </div>
      
      <div class="testimonials-wrapper">
        <button @click="prevTestimonial" class="nav-button prev" aria-label="قبلی">
          <span>→</span>
        </button>
        
        <div class="testimonials-slider">
          <div 
            class="testimonial-card"
            v-for="(testimonial, index) in testimonials"
            :key="testimonial.id"
            :class="{ active: index === currentIndex }"
          >
            <div class="quote-icon">❝</div>
            <p class="testimonial-text">{{ testimonial.text }}</p>
            <div class="testimonial-author">
              <div class="author-avatar" :style="{ background: testimonial.gradient }">
                {{ testimonial.initial }}
              </div>
              <div class="author-info">
                <h4 class="author-name">{{ testimonial.name }}</h4>
                <p class="author-position">{{ testimonial.position }}</p>
                <p class="author-company">{{ testimonial.company }}</p>
              </div>
            </div>
            <div class="rating">
              <span v-for="i in 5" :key="i" class="star">⭐</span>
            </div>
          </div>
        </div>
        
        <button @click="nextTestimonial" class="nav-button next" aria-label="بعدی">
          <span>←</span>
        </button>
      </div>
      
      <div class="testimonial-dots">
        <button 
          v-for="(testimonial, index) in testimonials"
          :key="index"
          @click="goToTestimonial(index)"
          class="dot"
          :class="{ active: index === currentIndex }"
          :aria-label="`نظر ${index + 1}`"
        ></button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const testimonials = ref([
  {
    id: 1,
    name: 'محمد رضایی',
    position: 'مدیر عامل',
    company: 'شرکت تکنولوژی پارس',
    text: 'همکاری با این تیم تجربه‌ای فوق‌العاده بود. حرفه‌ای‌گری و تخصص آن‌ها در طراحی و توسعه وب واقعاً قابل تحسین است. پروژه ما در زمان مقرر و با کیفیتی فراتر از انتظار تحویل شد.',
    initial: 'م',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 2,
    name: 'سارا احمدی',
    position: 'مدیر بازاریابی',
    company: 'استارتاپ نوآوران',
    text: 'تیمی بسیار خلاق و متعهد! طراحی وبسایت ما نه تنها زیبا شد، بلکه کاربرپسند و بهینه هم هست. تعداد بازدیدکنندگان ما بعد از راه‌اندازی وبسایت جدید ۳ برابر شده است.',
    initial: 'س',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: 3,
    name: 'علی کریمی',
    position: 'بنیانگذار',
    company: 'فروشگاه آنلاین دیجی‌استور',
    text: 'از ابتدا تا انتهای پروژه، ارتباط عالی و شفاف بود. تیم به تمام نیازها و درخواست‌های ما توجه کرد و راه‌حل‌های خلاقانه‌ای ارائه داد. به شدت توصیه می‌کنم!',
    initial: 'ع',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    id: 4,
    name: 'فاطمه موسوی',
    position: 'مدیر فنی',
    company: 'شرکت نرم‌افزاری سپهر',
    text: 'تخصص فنی بالا، پشتیبانی عالی و قیمت منصفانه. بهترین انتخاب برای پروژه‌های وب! سیستم مدیریت محتوایی که برای ما طراحی کردند بسیار کاربردی و قدرتمند است.',
    initial: 'ف',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  {
    id: 5,
    name: 'رضا حسینی',
    position: 'مدیر محصول',
    company: 'اپلیکیشن سفر',
    text: 'کیفیت کد و معماری پروژه فوق‌العاده بود. همه چیز مستندسازی شده و قابل توسعه است. تیمی که واقعاً به کارشان اهمیت می‌دهد و برای موفقیت مشتری تلاش می‌کند.',
    initial: 'ر',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
])

const currentIndex = ref(0)
let autoPlayInterval = null

const nextTestimonial = () => {
  currentIndex.value = (currentIndex.value + 1) % testimonials.value.length
}

const prevTestimonial = () => {
  currentIndex.value = (currentIndex.value - 1 + testimonials.value.length) % testimonials.value.length
}

const goToTestimonial = (index) => {
  currentIndex.value = index
}

const startAutoPlay = () => {
  autoPlayInterval = setInterval(() => {
    nextTestimonial()
  }, 5000)
}

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
  }
}

onMounted(() => {
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.testimonials-section {
  padding: 6rem 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.dark-mode .testimonials-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .section-title {
  color: #ffffff;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.testimonials-wrapper {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.testimonials-slider {
  flex: 1;
  position: relative;
  min-height: 400px;
  display: flex;
  align-items: center;
}

.testimonial-card {
  position: absolute;
  width: 100%;
  background: white;
  padding: 3rem;
  border-radius: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transform: scale(0.9);
  transition: all 0.5s ease;
  pointer-events: none;
}

.dark-mode .testimonial-card {
  background: rgba(45, 45, 45, 0.8);
}

.testimonial-card.active {
  opacity: 1;
  transform: scale(1);
  pointer-events: all;
  position: relative;
}

.quote-icon {
  font-size: 4rem;
  color: rgba(102, 126, 234, 0.2);
  line-height: 1;
  margin-bottom: 1rem;
}

.testimonial-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #1a1a1a;
  margin-bottom: 2rem;
  font-style: italic;
}

.dark-mode .testimonial-text {
  color: #ffffff;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.author-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  flex-shrink: 0;
}

.author-info {
  flex: 1;
}

.author-name {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #1a1a1a;
}

.dark-mode .author-name {
  color: #ffffff;
}

.author-position {
  font-size: 1rem;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.author-company {
  font-size: 0.9rem;
  color: #6c757d;
}

.dark-mode .author-company {
  color: #a0a0a0;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.star {
  font-size: 1.2rem;
}

.nav-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.testimonial-dots {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 3rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.3);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.dot.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 30px;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .testimonials-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .testimonials-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-button {
    width: 45px;
    height: 45px;
    font-size: 1.2rem;
  }
  
  .nav-button.prev,
  .nav-button.next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
  }
  
  .nav-button.prev {
    right: 0;
  }
  
  .nav-button.next {
    left: 0;
  }
  
  .testimonials-slider {
    min-height: 450px;
  }
  
  .testimonial-card {
    padding: 2rem;
  }
  
  .testimonial-text {
    font-size: 1rem;
  }
  
  .author-avatar {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
}
</style>
