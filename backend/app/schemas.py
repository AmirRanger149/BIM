from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============= Article Schemas =============

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    excerpt: str
    full_content: Optional[str] = None
    category: str
    icon: str = "📝"
    gradient: Optional[str] = None
    image: Optional[str] = None  # تصویر شاخص
    slider_id: Optional[int] = None  # اسلایدر (بجای images)
    author: str
    author_avatar: Optional[str] = None
    author_role: Optional[str] = None
    read_time: Optional[str] = None
    featured: bool = False
    tags: List[str] = []
    iframe_url: Optional[str] = None  # URL iframe برای نمایش مدل 3D
    model_url: Optional[str] = None  # URL فایل مدل 3D
    model_type: str = "auto"  # نوع مدل: gltf, glb, obj, auto


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    full_content: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    author: Optional[str] = None
    author_avatar: Optional[str] = None
    author_role: Optional[str] = None
    read_time: Optional[str] = None
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    iframe_url: Optional[str] = None  # URL iframe برای نمایش مدل 3D
    model_url: Optional[str] = None  # URL فایل مدل 3D
    model_type: Optional[str] = None  # نوع مدل


class Article(ArticleBase):
    id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============= Settings Schemas =============

class SettingsBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: Optional[str] = None
    description: Optional[str] = None


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class Settings(SettingsBase):
    id: int
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============= Gallery Schemas =============

class GalleryItemBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    full_description: Optional[str] = None  # توضیح کامل با HTML
    icon: str = "🎨"
    gradient: Optional[str] = None
    image: Optional[str] = None  # تصویر شاخص
    slider_id: Optional[int] = None  # اسلایدر (بجای images)
    category: str
    category_color: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[str] = None
    technologies: List[str] = []
    model_url: Optional[str] = None  # URL فایل مدل 3D
    model_type: str = "auto"  # نوع مدل: gltf, glb, obj, auto
    iframe_url: Optional[str] = None  # URL iframe برای نمایش مدل 3D


class GalleryItemCreate(GalleryItemBase):
    pass


class GalleryItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None  # توضیح کامل با HTML
    icon: Optional[str] = None
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    category: Optional[str] = None
    category_color: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[str] = None
    technologies: Optional[List[str]] = None
    model_url: Optional[str] = None  # URL فایل مدل 3D
    model_type: Optional[str] = None  # نوع مدل
    iframe_url: Optional[str] = None  # URL iframe برای نمایش مدل 3D


class GalleryItem(GalleryItemBase):
    id: int
    views: int
    comments: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Testimonial Schemas =============

class TestimonialBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str
    avatar: Optional[str] = None
    text: str
    rating: int = Field(default=5, ge=1, le=5)
    date: Optional[str] = None
    project: Optional[str] = None


class TestimonialCreate(TestimonialBase):
    pass


class Testimonial(TestimonialBase):
    id: int
    approved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Certificate Schemas =============

class CertificateBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    issuer: str = Field(..., min_length=1, max_length=255)
    date: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = "📜"
    color: Optional[str] = None
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    type: Optional[str] = None
    type_label: Optional[str] = None


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    type: Optional[str] = None
    type_label: Optional[str] = None


class Certificate(CertificateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============= Statistics Schemas =============

class StatisticBase(BaseModel):
    number: str
    label: str
    icon: Optional[str] = None
    order: int = 0


class StatisticCreate(StatisticBase):
    pass


class Statistic(StatisticBase):
    id: int
    
    class Config:
        from_attributes = True


# ============= Visit Schemas =============

class VisitCreate(BaseModel):
    path: str
    referer: Optional[str] = None


class VisitSummary(BaseModel):
    total_visits: int
    unique_ips: int
    today_visits: int
    last7_visits: int
    last30_visits: int
    per_day: list


# ============= Contact Schemas =============

class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Newsletter Schemas =============

class NewsletterBase(BaseModel):
    email: EmailStr


class NewsletterCreate(NewsletterBase):
    pass


class Newsletter(NewsletterBase):
    id: int
    active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= User Schemas =============

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_admin: bool = False
    is_active: bool = True


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ============= Service Schemas =============

class ServiceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    icon: str = "🎯"
    color: str = "#667eea"
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    features: List[str] = []
    price: Optional[str] = None
    order: int = 0
    active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    gradient: Optional[str] = None
    image: Optional[str] = None
    slider_id: Optional[int] = None
    features: Optional[List[str]] = None
    price: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None


class Service(ServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============= Slider Schemas =============

class SliderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    images: List[str] = []  # لیست URL های تصاویر


class SliderCreate(SliderBase):
    pass


class SliderUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None


class Slider(SliderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============= Response Schemas =============

class ResponseModel(BaseModel):
    """مدل پاسخ استاندارد"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    """مدل پاسخ pagination"""
    data: List
    total: int
    page: int
    limit: int
    pages: int

# ============= Video Schemas =============

class VideoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    video_url: str = Field(..., min_length=1)
    thumbnail: Optional[str] = None
    duration: Optional[str] = None
    active: bool = True
    order: int = 0


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[str] = None
    active: Optional[bool] = None
    order: Optional[int] = None


class Video(VideoBase):
    id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True