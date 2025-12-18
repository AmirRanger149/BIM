#!/bin/bash

# 🎉 راهنمای شروع سریع سیستم 3D BIM
# آخرین به‌روزرسانی: December 18, 2025

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🚀 راهنمای شروع سریع BIM 3D Viewer             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# بررسی اجزا
echo -e "${BLUE}📋 بررسی اجزای سیستم...${NC}"
echo ""

# بررسی پوشه‌ها
echo -e "${YELLOW}1️⃣  بررسی پوشه‌ها:${NC}"
if [ -d "backend/uploads" ]; then
    echo -e "${GREEN}   ✅ backend/uploads exists${NC}"
    file_count=$(find backend/uploads -type f | wc -l)
    echo -e "   📦 تعداد فایل‌ها: $file_count"
    ls -lh backend/uploads/ | tail -n +2 | awk '{print "      " $9 " (" $5 ")"}'
else
    echo -e "${RED}   ❌ backend/uploads not found${NC}"
    mkdir -p backend/uploads
fi
echo ""

# بررسی Node modules
echo -e "${YELLOW}2️⃣  بررسی Node modules:${NC}"
if [ -d "node_modules/three" ]; then
    echo -e "${GREEN}   ✅ Three.js installed${NC}"
else
    echo -e "${YELLOW}   ⚠️  Three.js not installed, installing...${NC}"
    npm install three
fi
echo ""

# بررسی Python
echo -e "${YELLOW}3️⃣  بررسی Python dependencies:${NC}"
if python -c "import fastapi" 2>/dev/null; then
    echo -e "${GREEN}   ✅ FastAPI installed${NC}"
else
    echo -e "${YELLOW}   ⚠️  FastAPI not installed${NC}"
fi
echo ""

# Build frontend
echo -e "${YELLOW}4️⃣  Build کردن Frontend:${NC}"
npm run build 2>&1 | grep -E "^✓|^(!)|(ERR!)" | tail -5
echo ""

# تست سیستم
echo -e "${YELLOW}5️⃣  تست سیستم:${NC}"
python test_3d_system.py 2>/dev/null | grep -E "^(✅|❌|📊)" | head -10
echo ""

# راهنمای شروع
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ آماده برای شروع!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}📚 مراحل شروع:${NC}"
echo ""
echo -e "${YELLOW}1. ترمینال 1 - Backend:${NC}"
echo -e "   ${GREEN}cd backend${NC}"
echo -e "   ${GREEN}python main.py${NC}"
echo ""

echo -e "${YELLOW}2. ترمینال 2 - Frontend:${NC}"
echo -e "   ${GREEN}npm run dev${NC}"
echo ""

echo -e "${YELLOW}3. مرورگر:${NC}"
echo -e "   ${GREEN}http://localhost:5173/project/3${NC}"
echo ""

echo -e "${BLUE}🎮 کنترل‌ها:${NC}"
echo "   • چپ‌کلیک + بکش = چرخش"
echo "   • اسکرول = زوم"
echo "   • راست‌کلیک + بکش = حرکت"
echo "   • دکمه‌های کنترل = بازنشانی/تمام‌صفحه/دانلود"
echo ""

echo -e "${BLUE}📚 منابع:${NC}"
echo "   • 3D_VIEWER_USAGE_GUIDE.md - راهنمای کامل"
echo "   • 3D_VIEWER_IMPLEMENTATION.md - توضیحات تکنیکی"
echo "   • backend/uploads/README.md - فایل‌های نمونه"
echo ""

echo -e "${GREEN}✅ تمام! خوش آمدید 🎉${NC}"
echo ""
