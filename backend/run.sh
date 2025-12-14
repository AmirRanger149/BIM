#!/bin/bash

# رنگ‌ها برای output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  BIM Backend API Setup & Run  ${NC}"
echo -e "${BLUE}================================${NC}\n"

# بررسی وجود virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}\n"
fi

# فعال‌سازی virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# نصب dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencies installed${NC}\n"

# بررسی و ایجاد .env
if [ ! -f ".env" ]; then
    echo -e "${BLUE}⚙️  Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created (please update it)${NC}\n"
fi

# اجرای سرور
echo -e "${GREEN}🚀 Starting server...${NC}\n"
echo -e "${BLUE}Server will run on: http://localhost:8000${NC}"
echo -e "${BLUE}API Docs: http://localhost:8000/docs${NC}"
echo -e "${BLUE}ReDoc: http://localhost:8000/redoc${NC}\n"
echo -e "${BLUE}Press Ctrl+C to stop${NC}\n"

python main.py
