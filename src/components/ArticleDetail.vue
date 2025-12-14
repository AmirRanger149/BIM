<template>
  <div class="article-detail-overlay" @click.self="$emit('close')">
    <div class="article-detail">
      <button @click="$emit('close')" class="back-button">
        <span>→</span>
        بازگشت
      </button>
    
    <div class="article-header" :style="{ background: article.gradient }">
      <div class="article-category-badge">{{ article.category }}</div>
      <div class="article-icon-large">{{ article.icon }}</div>
    </div>
    
    <div class="article-body">
      <div class="article-meta">
        <span class="meta-item">📅 {{ article.date }}</span>
        <span class="meta-item">⏱️ {{ article.readTime }}</span>
        <span class="meta-item">👁️ {{ article.views }} بازدید</span>
      </div>
      
      <h1 class="article-title">{{ article.title }}</h1>
      
      <div class="article-author-section">
        <div class="author-avatar-large">{{ article.authorAvatar }}</div>
        <div class="author-info">
          <div class="author-name">{{ article.author }}</div>
          <div class="author-role">{{ article.authorRole }}</div>
        </div>
      </div>
      
      <div class="article-content">
        <p class="lead">{{ article.excerpt }}</p>
        
        <div v-html="article.fullContent"></div>
      </div>
      
      <div class="article-tags">
        <span v-for="tag in article.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
      
      <div class="article-footer">
        <div class="share-section">
          <h3>اشتراک‌گذاری</h3>
          <div class="share-buttons">
            <button class="share-btn twitter">🐦 توییتر</button>
            <button class="share-btn linkedin">💼 لینکدین</button>
            <button class="share-btn telegram">✈️ تلگرام</button>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

defineProps({
  article: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const handleEscape = (e) => {
  if (e.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.article-detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  z-index: 10000;
  overflow-y: auto;
  animation: fadeIn 0.3s ease;
}

.article-detail {
  background: white;
  min-height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  animation: slideUp 0.3s ease;
}

.dark-mode .article-detail-overlay {
  background: rgba(0, 0, 0, 0.9);
}

.dark-mode .article-detail {
  background: #1a1a1a;
}

.back-button {
  position: sticky;
  top: 1rem;
  right: 2rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  color: #1a1a1a;
  transition: all 0.3s ease;
  z-index: 100;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin: 1rem 2rem 0 auto;
  float: left;
}

.dark-mode .back-button {
  background: #2d2d2d;
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.1);
}

.back-button:hover {
  transform: translateX(5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.article-header {
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.article-category-badge {
  position: absolute;
  top: 2rem;
  right: 2rem;
  background: rgba(255, 255, 255, 0.95);
  color: #1a1a1a;
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
}

.article-icon-large {
  font-size: 6rem;
}

.article-body {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.article-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.meta-item {
  color: #6c757d;
  font-size: 0.95rem;
}

.dark-mode .meta-item {
  color: #a0a0a0;
}

.article-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 2rem;
  color: #1a1a1a;
}

.dark-mode .article-title {
  color: #ffffff;
}

.article-author-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 15px;
  margin-bottom: 3rem;
}

.dark-mode .article-author-section {
  background: rgba(102, 126, 234, 0.1);
}

.author-avatar-large {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.5rem;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.author-name {
  font-weight: 700;
  font-size: 1.1rem;
  color: #1a1a1a;
}

.dark-mode .author-name {
  color: #ffffff;
}

.author-role {
  color: #6c757d;
  font-size: 0.9rem;
}

.dark-mode .author-role {
  color: #a0a0a0;
}

.article-content {
  color: #1a1a1a;
  line-height: 1.8;
}

.dark-mode .article-content {
  color: #ffffff;
}

.lead {
  font-size: 1.25rem;
  font-weight: 500;
  color: #6c757d;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-right: 4px solid #667eea;
  border-radius: 10px;
}

.dark-mode .lead {
  color: #a0a0a0;
  background: rgba(102, 126, 234, 0.1);
}

.article-content :deep(h2) {
  font-size: 2rem;
  font-weight: 700;
  margin: 2.5rem 0 1rem;
  color: #1a1a1a;
}

.dark-mode .article-content :deep(h2) {
  color: #ffffff;
}

.article-content :deep(h3) {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 2rem 0 1rem;
  color: #1a1a1a;
}

.dark-mode .article-content :deep(h3) {
  color: #ffffff;
}

.article-content :deep(p) {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.9;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 1.5rem 0;
  padding-right: 2rem;
}

.article-content :deep(li) {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}

.article-content :deep(code) {
  background: rgba(102, 126, 234, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin: 3rem 0;
}

.tag {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 50px;
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 500;
}

.article-footer {
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .article-footer {
  border-top-color: rgba(255, 255, 255, 0.1);
}

.share-section h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .share-section h3 {
  color: #ffffff;
}

.share-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.share-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.share-btn.twitter {
  background: #1DA1F2;
}

.share-btn.linkedin {
  background: #0077B5;
}

.share-btn.telegram {
  background: #0088cc;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .article-detail {
    margin: 0;
    border-radius: 0;
  }
  
  .back-button {
    position: sticky;
    top: 0.5rem;
    right: 1rem;
    margin: 0.5rem 1rem 0 auto;
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
  
  .article-header {
    height: 300px;
  }
  
  .article-icon-large {
    font-size: 4rem;
  }
  
  .article-body {
    padding: 2rem 1.5rem;
  }
  
  .article-title {
    font-size: 2rem;
  }
  
  .article-content :deep(h2) {
    font-size: 1.5rem;
  }
  
  .article-content :deep(h3) {
    font-size: 1.25rem;
  }
  
  .article-content :deep(p),
  .article-content :deep(li) {
    font-size: 1rem;
  }
  
  .lead {
    font-size: 1.1rem;
  }
}
</style>
