import { ref, readonly } from 'vue'
import { adminService } from '../api/services'

const logoUrl = ref('')
const faviconUrl = ref('')
const siteName = ref('BIM')
const siteDescription = ref('')

// Event emitter برای بروز رسانی تنظیمات
const listeners = new Set()

export const useSiteSettings = () => {
  const loadSettings = async () => {
    try {
      const settings = await adminService.getSettings()
      
      const logoSetting = settings.find(s => s.key === 'logo')
      if (logoSetting && logoSetting.value) {
        logoUrl.value = logoSetting.value
      }

      const faviconSetting = settings.find(s => s.key === 'favicon')
      if (faviconSetting && faviconSetting.value) {
        faviconUrl.value = faviconSetting.value
      }

      const namesSetting = settings.find(s => s.key === 'site_name')
      if (namesSetting && namesSetting.value) {
        siteName.value = namesSetting.value
      }

      const descriptionSetting = settings.find(s => s.key === 'site_description')
      if (descriptionSetting && descriptionSetting.value) {
        siteDescription.value = descriptionSetting.value
      }
    } catch (err) {
      console.warn('Unable to load settings:', err)
    }
  }

  const refreshLogo = async () => {
    try {
      const settings = await adminService.getSettings()
      const logoSetting = settings.find(s => s.key === 'logo')
      if (logoSetting && logoSetting.value) {
        logoUrl.value = logoSetting.value
        // Emit refresh event
        notifyListeners()
      }
    } catch (err) {
      console.warn('Unable to refresh logo:', err)
    }
  }

  const addListener = (callback) => {
    listeners.add(callback)
  }

  const removeListener = (callback) => {
    listeners.delete(callback)
  }

  const notifyListeners = () => {
    listeners.forEach(callback => callback())
  }

  return {
    logoUrl: readonly(logoUrl),
    faviconUrl: readonly(faviconUrl),
    siteName: readonly(siteName),
    siteDescription: readonly(siteDescription),
    loadSettings,
    refreshLogo,
    addListener,
    removeListener,
    notifyListeners
  }
}
