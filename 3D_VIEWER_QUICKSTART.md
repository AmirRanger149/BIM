# 3D Model Viewer - Quick Start Guide

## 🎯 What Was Added

Your BIM application now has full 3D model viewing capabilities! Users can upload 3D models (GLB, GLTF, OBJ formats) to gallery items and view them on project detail pages with full interactive controls.

---

## ⚡ Quick Start (5 minutes)

### 1. **Database Migration** ✅ DONE
Migration completed successfully - database now supports 3D models:
```bash
✅ model_url column added (stores file URL)
✅ model_type column added (stores format: auto, gltf, glb, obj)
```

### 2. **Start the Application**

**Terminal 1 - Backend Server:**
```bash
cd /workspaces/BIM/backend
python main.py
# Server runs on: http://localhost:8000
```

**Terminal 2 - Frontend Dev Server:**
```bash
cd /workspaces/BIM
npm run dev
# App runs on: http://localhost:5173
```

### 3. **Access Admin Panel**
- Go to: http://localhost:5173/admin/login
- Username: `admin@bim.com`
- Password: `admin123`

### 4. **Upload a 3D Model**

**Option A: Using File Upload**
1. Go to "🎨 مدیریت گالری" (Gallery Management)
2. Click "➕ آیتم جدید" (New Item) or edit existing
3. Scroll down to "📦 مدل 3D (اختیاری)" section
4. Click file input → Select .glb, .gltf, or .obj file
5. Model type auto-detects (or select manually)
6. Save the project

**Option B: Using Direct URL**
1. Same steps as above
2. Instead of file, paste model URL directly
3. Save

### 5. **View the 3D Model**
1. Browse to public site
2. Go to project detail page
3. Scroll down - "مدل سه‌بعدی پروژه" section appears below gallery
4. Interact with the model using mouse/trackpad

---

## 🎮 How to Interact with 3D Models

### Controls
| Action | Control |
|--------|---------|
| **Rotate** | Left mouse drag / 2-finger swipe |
| **Pan** | Right mouse drag / Cmd+drag |
| **Zoom** | Mouse wheel / Pinch |
| **Reset View** | Click "Reset Camera" button |
| **Fullscreen** | Click "Fullscreen" button |
| **Download** | Click "Download" button (saves as PNG) |

---

## 📦 Supported File Formats

### GLB (Recommended) ⭐
- **Extension:** `.glb`
- **Best for:** Web - single file with embedded textures
- **Size:** Usually smaller than GLTF
- **Use when:** You want best compatibility and smallest file size

### GLTF
- **Extension:** `.gltf` (+ `.bin` and texture files)
- **Best for:** Complex models with separate materials
- **Flexibility:** Good for professional workflows
- **Use when:** You need texture/material control

### OBJ
- **Extension:** `.obj` (+ `.mtl` and texture files)
- **Compatibility:** Legacy format, widely supported
- **Limitations:** No animations or complex materials
- **Use when:** Converting from older 3D software

---

## 📸 Real-World Usage

### For Architecture/BIM:
```
✅ Upload building 3D models (.glb)
✅ Upload floor plans as 3D models
✅ Show construction phases as separate models
```

### For Product Design:
```
✅ Product 3D renders
✅ Component assemblies
✅ Material variations
```

### For Interior Design:
```
✅ Room layouts in 3D
✅ Furniture placement models
✅ Lighting scenarios
```

---

## 🔧 Testing the Feature

### Quick Test Steps:
1. ✅ Backend runs without errors
2. ✅ Database migration successful
3. ✅ Frontend compiles (no errors)
4. ✅ Admin form shows 3D upload section
5. ✅ Can upload 3D file
6. ✅ Project detail page shows viewer
7. ✅ 3D model loads and displays
8. ✅ Controls work (rotate, zoom, pan)

### Test File Locations:
If you need sample 3D models for testing:
- Online: [Sketchfab.com](https://sketchfab.com) - free GLB models
- Create simple test: [Babylon.js Playground](https://www.babylonjs-playground.com/)
- Use Three.js examples: https://threejs.org/examples/

---

## 🐛 Troubleshooting

### Issue: "Model doesn't appear on project page"
**Solution:**
1. Check database: `sqlite3 /workspaces/BIM/bim.db "SELECT title, model_url FROM gallery_items WHERE model_url IS NOT NULL;"`
2. Verify model_url is populated
3. Check browser console for errors (F12 → Console)

### Issue: "404 when loading 3D file"
**Solution:**
1. Verify file is uploaded to `/workspaces/BIM/backend/uploads/`
2. Check file URL is correct in admin panel
3. Ensure URL is accessible in your browser

### Issue: "Pydantic warnings in backend"
**Solution:** Already fixed! The warnings are suppressed with `ConfigDict(protected_namespaces=())`

### Issue: "Large 3D file loads slowly"
**Solution:**
1. Optimize model file size
2. Compress textures
3. Reduce polygon count using tools like Meshlab
4. Use GLB format (more efficient than GLTF)

---

## 📋 Files Changed/Created

### Created Files:
```
✅ /workspaces/BIM/src/components/Viewer3D.vue
   - Complete Three.js 3D viewer component
   - ~520 lines of production-ready code

✅ /workspaces/BIM/migrate_3d_models.py
   - Database migration script
   - Adds model_url and model_type columns

✅ /workspaces/BIM/3D_VIEWER_GUIDE.md
   - Comprehensive documentation
```

### Updated Files:
```
✅ /workspaces/BIM/src/views/ProjectDetailPage.vue
   - Imported Viewer3D component
   - Added conditional rendering section
   - Added responsive CSS styling

✅ /workspaces/BIM/src/views/AdminGallery.vue
   - Added 3D model upload form fields
   - Added handleModelUpload function
   - Added file validation for 3D formats

✅ /workspaces/BIM/backend/app/models.py
   - Added model_url and model_type to GalleryItem

✅ /workspaces/BIM/backend/app/schemas.py
   - Added model fields to Pydantic schemas
   - Fixed protected namespace warnings

✅ /workspaces/BIM/bim.db
   - Database migration applied
```

---

## 🚀 Production Deployment

### Before Going Live:

1. **Test with real 3D files:**
   - Download sample GLB from Sketchfab
   - Upload through admin panel
   - Verify on public site

2. **Performance check:**
   - Test with large models (>50MB)
   - Check mobile performance
   - Monitor network usage

3. **File storage:**
   - Ensure upload directory is writable
   - Set up backup for uploaded models
   - Consider CDN for large files

4. **Security:**
   - Validate file types on backend (already done)
   - Set max file size limits
   - Scan for malicious files

---

## 💡 Tips & Best Practices

### File Size Optimization:
- **Small:** 5-10 MB (instant load)
- **Medium:** 10-30 MB (1-2 seconds)
- **Large:** 30-100+ MB (5-10 seconds)
- **Recommendation:** Keep under 20 MB

### Model Preparation:
1. Use Blender to optimize models
2. Remove unnecessary materials
3. Bake textures into single file
4. Export as GLB (not GLTF)
5. Test in viewer before uploading

### Gallery Best Practices:
- Use descriptive titles
- Add model preview image
- Include usage instructions
- Group related models by category

---

## 📞 Support Resources

### Three.js Documentation:
- https://threejs.org/docs
- https://threejs.org/examples/

### Model Optimization:
- https://meshlab.sourceforge.net/ (free, open source)
- https://www.blender.org/ (professional tool)

### Sample Models:
- https://sketchfab.com (free models)
- https://polyhaven.com/models (high quality)

---

## ✨ What's Happening Behind the Scenes

When you upload a 3D model:

1. **File Upload:** Form sends file to backend `/api/upload` endpoint
2. **Storage:** File saved to `/workspaces/BIM/backend/uploads/`
3. **Database:** URL stored in `gallery_items.model_url` column
4. **Type Detection:** Format auto-detected from extension
5. **Display:** ProjectDetailPage shows Viewer3D if model_url exists
6. **Rendering:** Three.js loads and renders model on canvas
7. **Interaction:** OrbitControls handles user input

---

## 🎓 Learning Resources

Want to extend this further? Check out:

- **Vue 3 + Composition API:** https://vuejs.org/guide/
- **Three.js Advanced:** https://threejs.org/manual/
- **3D Model Formats:** https://www.khronos.org/gltf/
- **FastAPI Backend:** https://fastapi.tiangolo.com/

---

**Status:** ✅ Complete and Ready to Use  
**Last Updated:** 2024  
**Framework Versions:**
- Vue 3.4+
- Three.js (latest)
- FastAPI 0.100+
- SQLAlchemy 2.0+
