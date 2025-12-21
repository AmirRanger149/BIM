<template>
  <div class="viewer-3d-container">
    <!-- iFrame View -->
    <div v-if="iframeUrl" class="iframe-wrapper">
      <iframe
        :src="iframeUrl"
        class="viewer-iframe"
        frameborder="0"
        allowfullscreen
        allow="fullscreen"
        title="نمایشگر 3D"
      ></iframe>
    </div>
    
    <!-- Model Not Available -->
    <div v-else class="no-model-state">
      <div class="empty-icon">📦</div>
      <p>هیچ مدل 3D برای این پروژه موجود نیست</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  iframeUrl: {
    type: String,
    default: null
  },
  modelUrl: {
    type: String,
    default: null
  },
  modelType: {
    type: String,
    enum: ['gltf', 'glb', 'obj', 'auto'],
    default: 'auto'
  },
  autoRotate: {
    type: Boolean,
    default: true
  },
  backgroundColor: {
    type: String,
    default: '#f0f0f0'
  }
})

// اگر iframeUrl وجود دارد، آن را استفاده کنید
// در غیر این صورت modelUrl را نادیده بگیرید
const iframeUrl = computed(() => {
  return props.iframeUrl || null
})
</script>

<style scoped>
.viewer-3d-container {
  width: 100%;
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  background: #f5f5f5;
}

.iframe-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.viewer-iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 12px;
}

.no-model-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #666;
  font-size: 14px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

@media (max-width: 768px) {
  .viewer-3d-container {
    height: 400px;
  }
}
</style>
