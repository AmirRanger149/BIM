import { reactive } from 'vue'

// Global reactive store for toasts
export const toastStore = reactive({
  items: []
})

let idSeq = 1

/**
 * Push a toast
 * @param {Object} opts
 * @param {'success'|'error'|'info'|'warn'} [opts.type]
 * @param {String} [opts.title]
 * @param {String} [opts.message]
 * @param {Number} [opts.duration] ms (default 3500)
 */
export function toast(opts = {}) {
  const { type = 'info', title = '', message = '', duration = 3500 } = opts
  const id = idSeq++
  const item = { id, type, title, message, createdAt: Date.now(), duration }
  toastStore.items.unshift(item)
  if (duration && duration > 0) {
    setTimeout(() => dismiss(id), duration)
  }
  return id
}

export function dismiss(id) {
  const idx = toastStore.items.findIndex(t => t.id === id)
  if (idx !== -1) toastStore.items.splice(idx, 1)
}

export const success = (message, title = 'موفق') => toast({ type: 'success', title, message })
export const error = (message, title = 'خطا') => toast({ type: 'error', title, message, duration: 5000 })
export const info = (message, title = 'اطلاع') => toast({ type: 'info', title, message })
export const warn = (message, title = 'هشدار') => toast({ type: 'warn', title, message })
