<template>
  <section id="contact" class="contact-section">
    <div class="container">
      <div class="contact-wrapper">
        <div class="contact-info">
          <h2 class="section-title">تماس با ما</h2>
          <p class="section-subtitle">آماده همکاری با شما هستیم</p>
          
          <div class="info-items">
            <div class="info-item">
              <div class="info-icon">📧</div>
              <div class="info-content">
                <h4>ایمیل</h4>
                <p>info@b1m.ir</p>
              </div>
            </div>
            
            <div class="info-item">
              <div class="info-icon">📱</div>
              <div class="info-content">
                <h4>تلفن</h4>
                <p>021-91094014</p>
              </div>
            </div>
            
            <div class="info-item">
              <div class="info-icon">📍</div>
              <div class="info-content">
                <h4>دفتر مر کزی</h4>
                <p>تهران، ایران, زعفرانیه، تقاطع بلوار بهزادی و ماکویی پور، ساختمان سروین، طبقه 3، واحد 33</p>
              </div>
            </div>
            
            <div class="info-item">
              <div class="info-icon">🕒</div>
              <div class="info-content">
                <h4>ساعات کاری</h4>
                <p>شنبه تا پنج‌شنبه: ۹ صبح تا ۶ عصر</p>
              </div>
            </div>
          </div>
          
          <div class="social-links">
            <a href="#" class="social-link">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path>
              </svg>
            </a>
            <a href="#" class="social-link">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"></path>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
            </a>
            <a href="#" class="social-link">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"></path>
              </svg>
            </a>
          </div>
        </div>
        
        <div class="contact-form-wrapper">
          <form @submit.prevent="submitForm" class="contact-form">
            <div class="form-group">
              <label for="name">نام و نام خانوادگی</label>
              <input 
                type="text" 
                id="name" 
                v-model="formData.name" 
                required
                placeholder="نام خود را وارد کنید"
              >
            </div>
            
            <div class="form-group">
              <label for="email">ایمیل</label>
              <input 
                type="email" 
                id="email" 
                v-model="formData.email" 
                required
                placeholder="example@email.com"
              >
            </div>
            
            <div class="form-group">
              <label for="phone">شماره تماس</label>
              <input 
                type="tel" 
                id="phone" 
                v-model="formData.phone"
                placeholder="۰۹۱۲ ۳۴۵ ۶۷۸۹"
              >
            </div>
            
            <div class="form-group">
              <label for="subject">موضوع</label>
              <select id="subject" v-model="formData.subject" required>
                <option value="">انتخاب کنید</option>
                <option value="consultation">مشاوره</option>
                <option value="project">سفارش پروژه</option>
                <option value="support">پشتیبانی</option>
                <option value="other">سایر</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="message">پیام</label>
              <textarea 
                id="message" 
                v-model="formData.message" 
                rows="5" 
                required
                placeholder="پیام خود را بنویسید..."
              ></textarea>
            </div>
            
            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              <span v-if="!isSubmitting">ارسال پیام</span>
              <span v-else>در حال ارسال...</span>
            </button>
            
            <Transition name="fade">
              <div v-if="submitMessage" class="submit-message" :class="submitStatus">
                {{ submitMessage }}
              </div>
            </Transition>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { sendContactForm } from '../api/services'

const formData = reactive({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const isSubmitting = ref(false)
const submitMessage = ref('')
const submitStatus = ref('')

const subjectLabel = (value) => {
  switch (value) {
    case 'consultation': return 'مشاوره'
    case 'project': return 'سفارش پروژه'
    case 'support': return 'پشتیبانی'
    case 'other': return 'سایر'
    default: return 'عمومی'
  }
}

const resetForm = () => {
  formData.name = ''
  formData.email = ''
  formData.phone = ''
  formData.subject = ''
  formData.message = ''
}

const submitForm = async () => {
  isSubmitting.value = true
  submitMessage.value = ''
  submitStatus.value = ''

  try {
    const payload = {
      name: formData.name,
      email: formData.email,
      subject: subjectLabel(formData.subject),
      message: `${formData.message}\n\nشماره تماس: ${formData.phone || 'ثبت نشده'}`
    }

    await sendContactForm(payload)
    submitMessage.value = 'پیام شما با موفقیت ارسال شد! به زودی با شما تماس خواهیم گرفت.'
    submitStatus.value = 'success'
    resetForm()
  } catch (err) {
    console.error('Contact submit error', err)
    submitMessage.value = err.response?.data?.detail || 'ارسال پیام ناموفق بود. لطفا دوباره تلاش کنید.'
    submitStatus.value = 'error'
  } finally {
    isSubmitting.value = false
    setTimeout(() => { submitMessage.value = '' }, 5000)
  }
}
</script>

<style scoped>
.contact-section {
  padding: 6rem 0;
  background: rgba(248, 249, 250, 0.5);
}

.dark-mode .contact-section {
  background: rgba(45, 45, 45, 0.3);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.contact-wrapper {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 4rem;
  align-items: start;
}

.contact-info {
  position: sticky;
  top: 100px;
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
  margin-bottom: 3rem;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 3rem;
}

.info-item {
  display: flex;
  gap: 1.5rem;
  align-items: start;
}

.info-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-content h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.dark-mode .info-content h4 {
  color: #ffffff;
}

.info-content p {
  color: #6c757d;
  line-height: 1.6;
}

.dark-mode .info-content p {
  color: #a0a0a0;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0ea5e9;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  color: white;
  transform: translateY(-3px);
}

.contact-form-wrapper {
  background: white;
  padding: 3rem;
  border-radius: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.dark-mode .contact-form-wrapper {
  background: rgba(45, 45, 45, 0.8);
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 0.95rem;
}

.dark-mode .form-group label {
  color: #ffffff;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 1rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: white;
}

.dark-mode .form-group input,
.dark-mode .form-group select,
.dark-mode .form-group textarea {
  background: rgba(26, 26, 26, 0.5);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.submit-btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-message {
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
}

.submit-message.success {
  background: rgba(67, 233, 123, 0.1);
  color: #43e97b;
  border: 1px solid rgba(67, 233, 123, 0.3);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1024px) {
  .contact-wrapper {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .contact-info {
    position: static;
  }
}

@media (max-width: 768px) {
  .contact-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .contact-form-wrapper {
    padding: 2rem;
  }
  
  .info-items {
    gap: 1.5rem;
  }
}
</style>
