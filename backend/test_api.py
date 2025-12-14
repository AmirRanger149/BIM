#!/usr/bin/env python3
"""
اسکریپت تست سریع API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """تست health check"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_articles():
    """تست دریافت مقالات"""
    print("📰 Testing articles endpoint...")
    response = requests.get(f"{BASE_URL}/api/articles")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total articles: {data.get('total', 0)}")
    if data.get('data'):
        print(f"First article: {data['data'][0]['title']}\n")

def test_gallery():
    """تست دریافت گالری"""
    print("🎨 Testing gallery endpoint...")
    response = requests.get(f"{BASE_URL}/api/gallery")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total items: {data.get('total', 0)}")
    if data.get('data'):
        print(f"First item: {data['data'][0]['title']}\n")

def test_login():
    """تست ورود"""
    print("🔐 Testing login...")
    login_data = {
        "username": "admin@bim.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"Token: {data['access_token'][:50]}...\n")
        return data['access_token']
    else:
        print(f"❌ Login failed: {response.status_code}\n")
        return None

def test_contact():
    """تست ارسال فرم تماس"""
    print("📧 Testing contact form...")
    contact_data = {
        "name": "کاربر تست",
        "email": "test@example.com",
        "subject": "تست API",
        "message": "این یک پیام تستی است"
    }
    response = requests.post(f"{BASE_URL}/api/contact", json=contact_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_newsletter():
    """تست ثبت‌نام خبرنامه"""
    print("📬 Testing newsletter subscription...")
    email_data = {
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/api/newsletter/subscribe", json=email_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_statistics():
    """تست دریافت آمار"""
    print("📊 Testing statistics...")
    response = requests.get(f"{BASE_URL}/api/statistics")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Statistics count: {len(data.get('data', []))}\n")

def main():
    print("=" * 60)
    print("🚀 BIM Backend API Test")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_articles()
        test_gallery()
        test_statistics()
        test_contact()
        test_newsletter()
        token = test_login()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
