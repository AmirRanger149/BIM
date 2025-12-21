#!/usr/bin/env python3
"""
اضافه کردن یک پروژه نمونه با مدل 3D به دیتابیس
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SessionLocal, engine
from app import models
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # بررسی اینکه پروژه قبلاً وجود دارد
    existing = db.query(models.GalleryItem).filter(
        models.GalleryItem.title == "نمونه: ساختمان 3D"
    ).first()
    
    if existing:
        print("✅ پروژه نمونه قبلاً وجود دارد")
        print(f"   ID: {existing.id}")
        print(f"   Model URL: {existing.model_url}")
    else:
        # ایجاد پروژه جدید با مدل 3D
        sample_project = models.GalleryItem(
            title="نمونه: ساختمان 3D",
            description="یک نمونه ساختمان برای تست مدل‌های 3D",
            full_description="<p>این یک نمونه از یک ساختمان سادهٔ سه‌بعدی است که برای تست قابلیت نمایش مدل‌های 3D در سیستم BIM ایجاد شده است.</p>",
            category="نمونه",
            image="https://via.placeholder.com/400x300?text=Building+3D",
            model_url="/uploads/building_complex.glb",
            model_type="glb",
            technologies=["Three.js", "WebGL", "glTF"],
            duration="تا 2 دقیقه",
            views=0,
            comments=0
        )
        
        db.add(sample_project)
        db.commit()
        db.refresh(sample_project)
        
        print("✅ پروژه نمونه ایجاد شد!")
        print(f"   ID: {sample_project.id}")
        print(f"   عنوان: {sample_project.title}")
        print(f"   مدل: {sample_project.model_url}")
        print(f"   نوع: {sample_project.model_type}")

except Exception as e:
    print(f"❌ خطا: {e}")
    db.rollback()
finally:
    db.close()

print("\n✅ تمام! شما می‌توانید به صفحهٔ پروژه برای دیدن مدل 3D برروید")
print("   URL: http://localhost:5173/project/1")
