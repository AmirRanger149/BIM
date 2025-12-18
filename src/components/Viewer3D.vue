<template>
  <div class="viewer-3d-container">
    <div ref="canvasContainer" class="canvas-wrapper">
      <canvas ref="canvasElement" class="viewer-canvas"></canvas>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-overlay">
        <div class="spinner"></div>
        <p>در حال بارگذاری مدل 3D...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-overlay">
        <p class="error-message">{{ error }}</p>
        <button @click="retryLoad" class="btn-retry">تلاش مجدد</button>
      </div>

      <!-- Controls -->
      <div class="viewer-controls">
        <div class="control-group">
          <button @click="resetCamera" title="بازنشانی دوربین" class="control-btn">
            🔄 بازنشانی
          </button>
          <button @click="toggleFullscreen" title="تمام صفحه" class="control-btn">
            ⛶ تمام صفحه
          </button>
          <button @click="downloadModel" v-if="modelUrl" title="دانلود" class="control-btn">
            ⬇️ دانلود
          </button>
        </div>
        <div class="info-text">
          <p>چپ‌کلیک و بکشید برای چرخش | اسکرول برای زوم</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const props = defineProps({
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

// Refs
const canvasContainer = ref(null)
const canvasElement = ref(null)
const loading = ref(false)
const error = ref(null)
const retryCount = ref(0)
const maxRetries = 3

// مطمئن شویم URL مطلق است
const getAbsoluteModelUrl = (url) => {
  if (!url) return null
  
  // اگر URL مطلق است
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  
  // اگر URL نسبی است
  if (url.startsWith('/')) {
    const baseUrl = import.meta.env.VITE_API_URL || window.location.origin
    return `${baseUrl.replace(/\/$/, '')}${url}`
  }
  
  // اگر فقط نام فایل است
  const baseUrl = import.meta.env.VITE_API_URL || window.location.origin
  return `${baseUrl.replace(/\/$/, '')}/uploads/${url}`
}

// Three.js objects
let scene, camera, renderer, controls, model
let animationId = null

const initViewer = () => {
  if (!canvasElement.value) return

  // Scene Setup
  scene = new THREE.Scene()
  scene.background = new THREE.Color(props.backgroundColor)

  // Camera Setup
  const width = canvasContainer.value.clientWidth
  const height = canvasContainer.value.clientHeight
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 10000)
  camera.position.set(0, 0, 5)

  // Renderer Setup
  renderer = new THREE.WebGLRenderer({
    canvas: canvasElement.value,
    antialias: true,
    alpha: true,
    preserveDrawingBuffer: true
  })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.shadowMap.enabled = true

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(5, 10, 7)
  directionalLight.castShadow = true
  directionalLight.shadow.mapSize.width = 2048
  directionalLight.shadow.mapSize.height = 2048
  scene.add(directionalLight)

  // Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.autoRotate = props.autoRotate
  controls.autoRotateSpeed = 4
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.enableZoom = true
  controls.enablePan = true

  // Handle Resize
  window.addEventListener('resize', onWindowResize)

  // Animation Loop
  animate()
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  if (controls) {
    controls.update()
  }

  renderer.render(scene, camera)
}

const loadModel = async () => {
  if (!props.modelUrl) {
    error.value = 'مدل 3D موجود نیست'
    return
  }

  loading.value = true
  error.value = null

  try {
    // دریافت URL مطلق
    const absoluteUrl = getAbsoluteModelUrl(props.modelUrl)
    console.log('📦 بارگذاری مدل:', absoluteUrl)
    
    const fileExtension = props.modelUrl.split('.').pop().toLowerCase()
    
    // Determine loader type
    let loader, modelData
    
    if (fileExtension === 'glb' || fileExtension === 'gltf' || props.modelType === 'gltf') {
      loader = new GLTFLoader()
      modelData = await loader.loadAsync(absoluteUrl)
      model = modelData.scene
      console.log('✅ مدل GLTF بارگذاری شد')
    } else if (fileExtension === 'obj' || props.modelType === 'obj') {
      loader = new OBJLoader()
      model = await loader.loadAsync(absoluteUrl)
      console.log('✅ مدل OBJ بارگذاری شد')
    } else {
      throw new Error(`فرمت فایل پشتیبانی نشده: ${fileExtension}`)
    }

    // Remove old model if exists
    if (scene && model) {
      const oldModel = scene.children.find(child => child.userData.isLoadedModel)
      if (oldModel) {
        scene.remove(oldModel)
      }
    }

    // Add model to scene
    if (scene && model) {
      model.userData.isLoadedModel = true
      scene.add(model)

      // Auto-fit camera to model
      fitCameraToModel(model)
    }

    loading.value = false
    retryCount.value = 0
  } catch (err) {
    console.error('❌ خطا در بارگذاری مدل:', err)
    
    if (retryCount.value < maxRetries) {
      retryCount.value++
      console.log(`🔄 تلاش مجدد (${retryCount.value}/${maxRetries})...`)
      setTimeout(loadModel, 1000)
    } else {
      error.value = `خطا در بارگذاری مدل: ${err.message || 'خطای نامشخص'}`
      loading.value = false
    }
  }
}

const fitCameraToModel = (object) => {
  const box = new THREE.Box3().setFromObject(object)
  const size = box.getSize(new THREE.Vector3())
  const center = box.getCenter(new THREE.Vector3())

  const maxDim = Math.max(size.x, size.y, size.z)
  const fov = camera.fov * (Math.PI / 180)
  let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2))

  cameraZ *= 1.5

  camera.position.copy(center)
  camera.position.z += cameraZ
  camera.lookAt(center)

  if (controls) {
    controls.target.copy(center)
    controls.update()
  }
}

const resetCamera = () => {
  if (model) {
    fitCameraToModel(model)
  }
}

const onWindowResize = () => {
  if (!canvasContainer.value) return

  const width = canvasContainer.value.clientWidth
  const height = canvasContainer.value.clientHeight

  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    canvasContainer.value.requestFullscreen().catch(err => {
      console.error('خطا در ورود به تمام صفحه:', err)
    })
  } else {
    document.exitFullscreen()
  }
}

const downloadModel = () => {
  if (props.modelUrl) {
    const link = document.createElement('a')
    link.href = props.modelUrl
    link.download = props.modelUrl.split('/').pop()
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const retryLoad = () => {
  loadModel()
}

// Lifecycle
onMounted(() => {
  initViewer()
  if (props.modelUrl) {
    loadModel()
  }
})

onBeforeUnmount(() => {
  // Cleanup
  window.removeEventListener('resize', onWindowResize)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
  }
  if (scene) {
    scene.clear()
  }
})

// Watch for model URL changes
watch(() => props.modelUrl, (newUrl) => {
  if (newUrl && scene) {
    // Remove old model
    if (model) {
      scene.remove(model)
    }
    // Load new model
    loadModel()
  }
})
</script>

<style scoped>
.viewer-3d-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.canvas-wrapper {
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background: #f5f5f5;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.viewer-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

/* Loading State */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  z-index: 100;
  backdrop-filter: blur(4px);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-overlay p {
  color: #667eea;
  font-weight: 600;
  font-size: 1rem;
}

/* Error State */
.error-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  z-index: 100;
  padding: 2rem;
  text-align: center;
}

.error-message {
  color: #ef4444;
  font-weight: 600;
  font-size: 0.95rem;
  line-height: 1.6;
  max-width: 400px;
}

.btn-retry {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

/* Controls */
.viewer-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.4), transparent);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  z-index: 50;
}

.control-group {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  padding: 0.6rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  color: #1f2937;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.control-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.info-text {
  color: white;
  font-size: 0.85rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  margin: 0;
  text-align: right;
}

/* Responsive */
@media (max-width: 768px) {
  .canvas-wrapper {
    min-height: 300px;
  }

  .viewer-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .control-group {
    width: 100%;
    justify-content: space-between;
  }

  .control-btn {
    flex: 1;
  }

  .info-text {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .canvas-wrapper {
    min-height: 250px;
  }

  .control-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>
