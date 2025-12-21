# 3D Model Viewer - API & Integration Reference

## 🔗 API Endpoints

All existing gallery endpoints now support 3D model fields.

### Create Gallery Item with Model
```http
POST /api/admin/gallery
Content-Type: application/json

{
  "title": "Modern Architecture Design",
  "description": "High-rise building 3D model",
  "full_description": "<p>Detailed description with HTML</p>",
  "category": "Architecture",
  "image": "https://example.com/thumb.jpg",
  "slider_id": null,
  "technologies": ["BIM", "Revit", "3D Modeling"],
  "duration": "3 months",
  "model_url": "https://example.com/models/building.glb",
  "model_type": "glb"
}

Response (201 Created):
{
  "id": 1,
  "title": "Modern Architecture Design",
  "description": "High-rise building 3D model",
  "model_url": "https://example.com/models/building.glb",
  "model_type": "glb",
  ...other fields
}
```

### Update Gallery Item with Model
```http
PUT /api/admin/gallery/{id}
Content-Type: application/json

{
  "model_url": "https://example.com/models/updated-building.glb",
  "model_type": "glb"
}

Response (200 OK):
{
  "id": 1,
  "model_url": "https://example.com/models/updated-building.glb",
  "model_type": "glb"
  ...other fields
}
```

### Get Gallery Item
```http
GET /api/gallery/{id}

Response (200 OK):
{
  "id": 1,
  "title": "Modern Architecture Design",
  "model_url": "https://example.com/models/building.glb",
  "model_type": "glb",
  ...other fields
}
```

### Upload File
```http
POST /api/upload
Content-Type: multipart/form-data

[Binary file data]

Response (200 OK):
{
  "url": "http://localhost:8000/api/uploads/building-12345.glb",
  "filename": "building-12345.glb",
  "size": 15234567
}
```

---

## 📱 Frontend Component Integration

### Using Viewer3D Component

**Basic Usage:**
```vue
<template>
  <Viewer3D
    :modelUrl="'https://example.com/model.glb'"
    modelType="glb"
  />
</template>

<script setup>
import Viewer3D from '@/components/Viewer3D.vue'
</script>
```

**With All Props:**
```vue
<template>
  <Viewer3D
    :modelUrl="project.model_url"
    :modelType="project.model_type || 'auto'"
    :autoRotate="true"
    backgroundColor="#f5f5f5"
  />
</template>

<script setup>
import Viewer3D from '@/components/Viewer3D.vue'
import { ref } from 'vue'

const project = ref({
  title: 'My Project',
  model_url: 'https://example.com/model.glb',
  model_type: 'glb'
})
</script>
```

### ProjectDetailPage Integration

The 3D viewer is automatically displayed when a project has a model_url:

```vue
<!-- In ProjectDetailPage.vue template -->
<section class="project-3d-viewer" v-if="project.model_url">
  <div class="container">
    <h2>مدل سه‌بعدی پروژه</h2>
    <div class="viewer-wrapper">
      <Viewer3D
        :modelUrl="project.model_url"
        :modelType="project.model_type || 'auto'"
        :autoRotate="true"
        backgroundColor="#f5f5f5"
      />
    </div>
  </div>
</section>
```

### AdminGallery Upload Integration

The admin interface automatically handles 3D model uploads:

```vue
<!-- In AdminGallery.vue template -->
<div class="form-group">
  <label>📦 مدل 3D (اختیاری)</label>
  <div class="file-input-group">
    <input 
      type="file" 
      @change="handleModelUpload" 
      accept=".glb,.gltf,.obj"
    />
    <input v-model="formData.model_url" type="text" />
  </div>
</div>
```

---

## 🔌 Vue 3 Composition API Usage

### Using useApi Composable with 3D Models

```javascript
// In your component
import { useApi } from '@/composables/useApi'

const { data: project, loading, error } = useApi('/api/gallery/1')

// Access model data
console.log(project.value.model_url)   // URL to 3D model
console.log(project.value.model_type)  // 'glb', 'gltf', 'obj', or 'auto'
```

### Conditional Rendering Based on Model

```vue
<template>
  <div v-if="project">
    <!-- Show gallery -->
    <Gallery :images="project.images" />
    
    <!-- Show 3D viewer only if model exists -->
    <Viewer3D v-if="project.model_url" :modelUrl="project.model_url" />
  </div>
</template>
```

---

## 🗄️ Database Schema

### gallery_items Table

```sql
CREATE TABLE gallery_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    full_description TEXT,
    icon VARCHAR(10) DEFAULT '🎨',
    gradient VARCHAR(255),
    image VARCHAR(500),
    slider_id INTEGER,
    category VARCHAR(100) NOT NULL,
    category_color VARCHAR(50),
    date VARCHAR(50),
    duration VARCHAR(50),
    views INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    technologies JSON,
    
    -- 3D Model Support (NEW)
    model_url VARCHAR(500),           -- URL to 3D model file
    model_type VARCHAR(20) DEFAULT 'auto',  -- Format: gltf, glb, obj, auto
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Pydantic Schema

```python
class GalleryItemBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    # ... other fields ...
    model_url: Optional[str] = None      # URL to 3D model file
    model_type: str = "auto"             # Format: gltf, glb, obj, auto

class GalleryItemCreate(GalleryItemBase):
    pass

class GalleryItemUpdate(BaseModel):
    # ... other fields ...
    model_url: Optional[str] = None
    model_type: Optional[str] = None
```

---

## 🎯 Real-World Integration Examples

### Example 1: Project with 3D Model

```javascript
// Create project with 3D model
const projectData = {
  title: "Modern Office Building",
  description: "A 40-story office complex",
  category: "Commercial",
  image: "https://example.com/thumb.jpg",
  model_url: "https://example.com/models/office-building.glb",
  model_type: "glb"
}

// API call
await adminService.createGalleryItem(projectData)

// User sees:
// 1. Project title and description
// 2. Gallery images (if slider_id provided)
// 3. 3D model viewer with interactive controls
```

### Example 2: Multiple Models in Admin

```javascript
// Admin can manage multiple models
const projects = [
  {
    id: 1,
    title: "Building A",
    model_url: "https://cdn.example.com/building-a.glb"
  },
  {
    id: 2,
    title: "Building B",
    model_url: "https://cdn.example.com/building-b.glb"
  },
  {
    id: 3,
    title: "Interior Design",
    model_url: "https://cdn.example.com/interior.obj"
  }
]

// Each has independent model support
```

### Example 3: Optional 3D with Fallback

```vue
<template>
  <div class="project-section">
    <!-- Always show gallery -->
    <Gallery :images="project.images" />
    
    <!-- Show 3D viewer if available, otherwise show note -->
    <div v-if="project.model_url">
      <Viewer3D :modelUrl="project.model_url" />
    </div>
    <div v-else class="info-box">
      📝 3D model not available for this project
    </div>
  </div>
</template>
```

---

## 🔄 Data Flow Examples

### Upload Flow

```
Admin User
    ↓
AdminGallery.vue (form)
    ↓
handleModelUpload(event)
    ├─ Validate file type (.glb, .gltf, .obj)
    ├─ Create FormData with file
    └─ POST /api/upload
         ↓
    Backend Handler
         ├─ Receive file
         ├─ Validate size/type
         ├─ Save to /uploads/
         └─ Return URL
              ↓
    formData.model_url = "http://localhost:8000/api/uploads/..."
         ↓
    Admin clicks "Save"
         ↓
    PUT /api/admin/gallery/{id}
         ├─ Send model_url & model_type
         └─ Backend saves to DB
              ↓
    Database Updated
         └─ gallery_items.model_url = URL
```

### View Flow

```
User visits project
    ↓
GET /api/gallery/{id}
    ↓
Backend returns project data with model_url
    ↓
ProjectDetailPage.vue
    ├─ Check: if project.model_url exists?
    ├─ YES: Render Viewer3D component
    └─ NO: Skip viewer section
         ↓
    Viewer3D.vue
         ├─ Props: modelUrl, modelType
         ├─ Select loader (GLTF or OBJ)
         ├─ Fetch model from URL
         ├─ Setup Three.js scene
         ├─ Add lights & camera
         ├─ Render to canvas
         └─ Wait for user interaction
              ↓
    User can:
    - Rotate (mouse drag)
    - Zoom (scroll)
    - Pan (right click)
    - Reset (button)
    - Fullscreen (button)
```

---

## 🛠️ Configuration & Customization

### Customize Viewer3D Appearance

```vue
<Viewer3D
  :modelUrl="model.url"
  :modelType="model.type"
  :autoRotate="false"
  backgroundColor="#ffffff"
/>
```

### Customize Upload Validation

In `AdminGallery.vue`, modify `handleModelUpload()`:

```javascript
const handleModelUpload = async (event) => {
  const file = event.target.files[0]
  
  // Customize validation
  const MAX_SIZE = 100 * 1024 * 1024  // 100MB
  if (file.size > MAX_SIZE) {
    // Show error
    return
  }
  
  // ... rest of upload logic
}
```

### Add Custom Three.js Configuration

In `Viewer3D.vue`, modify `initViewer()`:

```javascript
const initViewer = () => {
  // ... existing code ...
  
  // Customize lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.2)
  scene.add(ambientLight)
  
  // Customize camera
  camera.fov = 60  // Instead of 75
  camera.updateProjectionMatrix()
}
```

---

## 📊 Performance Optimization

### For Large Models

```javascript
// In Viewer3D.vue
const loadModel = async () => {
  // Reduce quality for large files
  if (props.modelUrl.endsWith('.glb')) {
    const response = await fetch(props.modelUrl)
    const size = response.headers.get('content-length')
    
    if (size > 50 * 1024 * 1024) {
      // Show warning or reduce rendering quality
      renderer.setPixelRatio(window.devicePixelRatio * 0.5)
    }
  }
}
```

### Mobile Optimization

```vue
<template>
  <div class="viewer-container">
    <Viewer3D
      :modelUrl="modelUrl"
      :autoRotate="!isMobile"
      :backgroundColor="isMobile ? '#ffffff' : '#f5f5f5'"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const isMobile = computed(() => window.innerWidth < 768)
</script>
```

---

## 🔐 Security Considerations

### File Upload Security

```javascript
// In backend admin.py (example implementation)
const ALLOWED_EXTENSIONS = ['glb', 'gltf', 'obj']
const MAX_FILE_SIZE = 100 * 1024 * 1024  // 100MB

const validateUpload = (file) => {
  // Check extension
  const ext = file.name.split('.').pop().toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    throw new Error('Invalid file type')
  }
  
  // Check size
  if (file.size > MAX_FILE_SIZE) {
    throw new Error('File too large')
  }
  
  // Additional checks
  // - Virus scan
  // - MIME type validation
  // - Content analysis
}
```

### CORS Configuration

```javascript
// If models hosted on CDN, ensure CORS headers
// Add to server configuration:
// Access-Control-Allow-Origin: *
// or specific domain
```

---

## 🐛 Debugging Tips

### Check Model in Browser Console

```javascript
// View loaded models
console.log(window.THREE)  // Three.js available?

// Check if model loaded
fetch('https://example.com/model.glb')
  .then(r => r.blob())
  .then(blob => console.log('Model size:', blob.size))
```

### View Database

```bash
# Check gallery items with models
sqlite3 /workspaces/BIM/bim.db \
  "SELECT id, title, model_url, model_type FROM gallery_items WHERE model_url IS NOT NULL;"
```

### Monitor Network

```javascript
// In browser DevTools
// Network tab → Filter by XHR
// Watch for:
// 1. /api/gallery/{id} request
// 2. Model file download
// 3. Response times
```

---

## 📝 Testing the Integration

### Manual Test Checklist

- [ ] Upload 3D model via admin
- [ ] Model URL appears in database
- [ ] Project page loads with viewer
- [ ] Can rotate model
- [ ] Can zoom in/out
- [ ] Can pan camera
- [ ] Reset button works
- [ ] Fullscreen works
- [ ] Download button works
- [ ] Mobile responsive
- [ ] Error handling works
- [ ] Retry logic triggers

### Automated Testing Example

```javascript
// cypress test example
describe('3D Viewer', () => {
  it('should load and display model', () => {
    cy.visit('/project/1')
    
    cy.get('.viewer-wrapper').should('be.visible')
    cy.get('canvas').should('exist')
    
    // Test rotation
    cy.get('canvas').trigger('mousedown', { button: 0, x: 100, y: 100 })
    cy.get('canvas').trigger('mousemove', { x: 150, y: 150 })
    cy.get('canvas').trigger('mouseup')
  })
})
```

---

## 🔗 External References

### Three.js
- **Docs:** https://threejs.org/docs/
- **Examples:** https://threejs.org/examples/
- **GLTFLoader:** https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- **OBJLoader:** https://threejs.org/docs/#examples/en/loaders/OBJLoader

### 3D Model Resources
- **Sketchfab:** https://sketchfab.com/ (free GLB models)
- **Poly Haven:** https://polyhaven.com/models (high quality)
- **Three.js Models:** https://threejs.org/examples/?q=models

### File Format Specs
- **glTF:** https://www.khronos.org/gltf/
- **OBJ/MTL:** https://en.wikipedia.org/wiki/Wavefront_.obj_file
- **Blender Export:** https://docs.blender.org/manual/en/latest/addons/io_scene_gltf2/export.html

---

**Last Updated:** 2024  
**Status:** Complete and Ready  
**Support:** Check 3D_VIEWER_GUIDE.md for troubleshooting
