<template>
  <Teleport to="body">
    <div class="toast-wrapper" aria-live="assertive" aria-atomic="true">
      <transition-group name="toast-fade" tag="div">
        <div v-for="t in store.items" :key="t.id" class="toast" :class="t.type">
          <div class="toast-bar" />
          <div class="toast-content">
            <div class="toast-title">
              <span v-if="t.type === 'success'">✅</span>
              <span v-else-if="t.type === 'error'">❌</span>
              <span v-else-if="t.type === 'warn'">⚠️</span>
              <span v-else>ℹ️</span>
              <strong>{{ t.title }}</strong>
            </div>
            <div class="toast-message">{{ t.message }}</div>
          </div>
          <button class="toast-close" @click="dismiss(t.id)" aria-label="بستن">×</button>
        </div>
      </transition-group>
    </div>
  </Teleport>
</template>

<script setup>
import { toastStore as store, dismiss } from '../composables/useToast'
</script>

<style scoped>
.toast-wrapper {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 99999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: min(96vw, 520px);
  pointer-events: none;
}

.toast-fade-enter-active, .toast-fade-leave-active {
  transition: all 0.25s ease;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}

.toast {
  display: grid;
  grid-template-columns: 6px 1fr auto;
  align-items: center;
  gap: 12px;
  background: #ffffff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px 12px 12px 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  pointer-events: auto;
}

.dark-mode .toast {
  background: #2b2b2b;
  border-color: #3a3a3a;
  color: #eaeaea;
}

.toast.success .toast-bar { background: #10b981; }
.toast.error .toast-bar { background: #ef4444; }
.toast.info .toast-bar { background: #3b82f6; }
.toast.warn .toast-bar { background: #f59e0b; }

.toast-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
}

.toast-message {
  font-size: 0.95rem;
  color: #444;
}
.dark-mode .toast-message { color: #cfcfcf; }

.toast-close {
  background: transparent;
  border: none;
  color: #888;
  font-size: 1.25rem;
  cursor: pointer;
}
.toast-close:hover { color: #333; }
.dark-mode .toast-close:hover { color: #fff; }
</style>
