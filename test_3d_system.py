#!/usr/bin/env python3
"""
تست سیستم 3D مدل‌های BIM
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.database import SessionLocal, Base, engine
from app import models

print("\n" + "="*60)
print("🧪 تست سیستم 3D مدل‌های BIM")
print("="*60 + "\n")

# Initialize database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # بررسی فایل‌های آپلود
    uploads_dir = Path(__file__).parent / "backend" / "uploads"
    print(f"📁 بررسی پوشهٔ آپلود: {uploads_dir}")
    
    if uploads_dir.exists():
        files = list(uploads_dir.glob("*.glb")) + list(uploads_dir.glob("*.gltf")) + list(uploads_dir.glob("*.obj"))
        print(f"✅ تعداد مدل‌های 3D: {len(files)}")
        for f in files:
            size_kb = f.stat().st_size / 1024
            print(f"   - {f.name} ({size_kb:.1f} KB)")
    else:
        print("❌ پوشهٔ آپلود یافت نشد")
    
    # بررسی gallery items با مدل 3D
    print(f"\n📊 بررسی پروژه‌های دارای مدل 3D:")
    items = db.query(models.GalleryItem).filter(
        models.GalleryItem.model_url != None
    ).all()
    
    print(f"✅ تعداد پروژه‌ها: {len(items)}")
    for item in items:
        print(f"\n📌 {item.title} (ID: {item.id})")
        print(f"   - مدل: {item.model_url}")
        print(f"   - نوع: {item.model_type}")
        print(f"   - URL کامل: /uploads/{item.model_url}")
    
    # آماری کلی
    print(f"\n📈 آمار کلی:")
    total_items = db.query(models.GalleryItem).count()
    items_with_model = db.query(models.GalleryItem).filter(
        models.GalleryItem.model_url != None
    ).count()
    
    print(f"   - کل پروژه‌ها: {total_items}")
    print(f"   - پروژه‌های با مدل 3D: {items_with_model}")
    print(f"   - درصد: {(items_with_model/total_items*100):.1f}%" if total_items > 0 else "   - درصد: 0%")
    
    # بررسی schema
    print(f"\n✅ ستون‌های مدل:")
    for column in models.GalleryItem.__table__.columns:
        if 'model' in column.name.lower():
            print(f"   - {column.name}: {column.type}")
    
    print("\n" + "="*60)
    print("✨ تست انجام شد")
    print("="*60 + "\n")

finally:
    db.close()
