import { ref, onMounted } from 'vue'

/**
 * Composable برای مدیریت API calls با loading و error handling
 * @param {Function} apiFunction - تابع API که باید صدا زده شود
 * @param {Boolean} immediate - آیا بلافاصله اجرا شود؟ (پیش‌فرض: true)
 * @returns {Object} { data, loading, error, execute, refresh }
 */
export function useApi(apiFunction, immediate = true) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  /**
   * اجرای API call
   * @param  {...any} args - آرگومان‌های تابع API
   */
  const execute = async (...args) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiFunction(...args)
      data.value = response.data
      return response
    } catch (err) {
      error.value = err.response?.data?.message || err.message || 'خطایی رخ داده است'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * بارگذاری مجدد داده
   */
  const refresh = () => {
    return execute()
  }

  // اگر immediate true باشد، بلافاصله اجرا می‌شود
  if (immediate) {
    onMounted(() => {
      execute()
    })
  }

  return {
    data,
    loading,
    error,
    execute,
    refresh
  }
}

/**
 * Composable برای pagination
 * @param {Function} apiFunction - تابع API
 * @param {Number} itemsPerPage - تعداد آیتم در هر صفحه
 * @returns {Object} { data, loading, error, currentPage, totalPages, nextPage, prevPage, goToPage }
 */
export function usePagination(apiFunction, itemsPerPage = 10) {
  const data = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentPage = ref(1)
  const totalItems = ref(0)
  const totalPages = ref(0)

  const fetchPage = async (page = 1) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiFunction({ 
        page, 
        limit: itemsPerPage 
      })
      
      data.value = response.data
      totalItems.value = response.total || response.data.length
      totalPages.value = Math.ceil(totalItems.value / itemsPerPage)
      currentPage.value = page
      
      return response
    } catch (err) {
      error.value = err.response?.data?.message || err.message || 'خطایی رخ داده است'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      return fetchPage(currentPage.value + 1)
    }
  }

  const prevPage = () => {
    if (currentPage.value > 1) {
      return fetchPage(currentPage.value - 1)
    }
  }

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      return fetchPage(page)
    }
  }

  onMounted(() => {
    fetchPage(1)
  })

  return {
    data,
    loading,
    error,
    currentPage,
    totalPages,
    totalItems,
    nextPage,
    prevPage,
    goToPage,
    refresh: () => fetchPage(currentPage.value)
  }
}

/**
 * Composable برای form submission
 * @param {Function} submitFunction - تابع submit
 * @returns {Object} { loading, error, success, submit }
 */
export function useForm(submitFunction) {
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  const submit = async (formData) => {
    loading.value = true
    error.value = null
    success.value = false
    
    try {
      const response = await submitFunction(formData)
      success.value = true
      return response
    } catch (err) {
      error.value = err.response?.data?.message || err.message || 'خطا در ارسال فرم'
      console.error('Form Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    loading.value = false
    error.value = null
    success.value = false
  }

  return {
    loading,
    error,
    success,
    submit,
    reset
  }
}

export default {
  useApi,
  usePagination,
  useForm
}
