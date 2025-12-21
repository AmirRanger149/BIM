<template>
  <div class="media-archive-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <!-- SEO Hero Section -->
    <section class="archive-hero">
      <div class="container">
        <div class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/" itemprop="item">
              <span itemprop="name">خانه</span>
            </router-link>
            <meta itemprop="position" content="1" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span class="current" itemprop="name">
              {{ activeTab === 'articles' ? 'مقالات' : activeTab === 'gallery' ? 'گالری' : activeTab === 'services' ? 'خدمات' : 'گواهینامه‌ها' }}
            </span>
            <meta itemprop="position" content="2" />
          </span>
        </div>
        
        <h1 class="page-title">
          {{ activeTab === 'articles' ? 'مقالات و آموزش‌های BIM' : 
             activeTab === 'gallery' ? 'گالری پروژه‌های BIM' :
             activeTab === 'services' ? 'خدمات مهندسی BIM' :
             'گواهینامه‌ها و افتخارات' }}
        </h1>
        <p class="page-description">
          {{ activeTab === 'articles' 
            ? 'مقالات تخصصی مدل‌سازی اطلاعات ساختمان، آموزش‌های BIM، و آخرین اخبار صنعت ساخت و ساز' 
            : activeTab === 'gallery'
            ? 'نمونه کارها و پروژه‌های انجام شده با استفاده از فناوری BIM'
            : activeTab === 'services'
            ? 'خدمات مهندسی، مشاوره و نظارت در پروژه‌های ساختمانی با استفاده از BIM'
            : 'گواهینامه‌ها، افتخارات و دستاوردهای شرکت در صنعت ساخت و ساز'
          }}
        </p>
        
        <!-- Tab Switcher -->
        <div class="tab-switcher">
          <button 
            @click="switchTab('articles')" 
            :class="['tab-btn', { active: activeTab === 'articles' }]"
            :aria-label="'نمایش مقالات'"
          >
            📝 مقالات و آموزش‌ها
          </button>
          <button 
            @click="switchTab('gallery')" 
            :class="['tab-btn', { active: activeTab === 'gallery' }]"
            :aria-label="'نمایش گالری'"
          >
            🖼️ گالری پروژه‌ها
          </button>
          <button 
            @click="switchTab('services')" 
            :class="['tab-btn', { active: activeTab === 'services' }]"
            :aria-label="'نمایش خدمات'"
          >
            🔧 خدمات مهندسی
          </button>
          <button 
            @click="switchTab('certificates')" 
            :class="['tab-btn', { active: activeTab === 'certificates' }]"
            :aria-label="'نمایش گواهینامه‌ها'"
          >
            🏆 گواهینامه‌ها
          </button>
        </div>
      </div>
    </section>

    <!-- Articles Section -->
    <section v-if="activeTab === 'articles'" class="archive-content">
      <div class="container">
        <!-- Loading state -->
        <div v-if="articlesLoading" class="loading-state">
          <div class="spinner"></div>
          <p>در حال بارگیری مقالات...</p>
        </div>
        
        <!-- Error state -->
        <div v-if="articlesError && !articlesLoading" class="error-state">
          <p>{{ articlesError }}</p>
        </div>

        <!-- Search and Filter -->
        <div v-if="!articlesLoading" class="archive-controls">
          <div class="search-box">
            <label for="article-search" class="sr-only">جستجو در مقالات</label>
            <span class="search-icon" aria-hidden="true">🔍</span>
            <input 
              id="article-search"
              v-model="articleSearchQuery" 
              type="search" 
              placeholder="جستجو در مقالات..."
              class="search-input"
              aria-label="جستجو در مقالات"
            />
          </div>
          
          <div class="filter-tabs" role="tablist" aria-label="دسته‌بندی مقالات">
            <button 
              v-for="category in articleCategories" 
              :key="category"
              @click="selectedArticleCategory = category"
              :class="['filter-btn', { active: selectedArticleCategory === category }]"
              role="tab"
              :aria-selected="selectedArticleCategory === category"
            >
              <span class="filter-text">{{ category }}</span>
              <span v-if="selectedArticleCategory === category" class="active-indicator"></span>
            </button>
          </div>

          <select 
            v-model="articleSortBy" 
            class="sort-select"
            aria-label="مرتب‌سازی مقالات"
          >
            <option value="latest">جدیدترین</option>
            <option value="popular">محبوب‌ترین</option>
            <option value="trending">پربازدیدترین</option>
          </select>
        </div>

        <div class="results-info" role="status" aria-live="polite">
          <span class="results-count">{{ filteredArticles.length }} مقاله یافت شد</span>
        </div>

        <!-- Articles Grid with Schema.org markup -->
        <TransitionGroup 
          name="article-list" 
          tag="div" 
          class="articles-archive-grid"
          role="list"
        >
          <router-link
            v-for="article in paginatedArticles" 
            :key="article.id"
            :to="`/article/${article.id}`"
            class="article-card"
            tag="article"
            itemscope 
            itemtype="https://schema.org/Article"
            role="listitem"
          >
            <ImageSlider 
              class="article-image"
              :image="article.image"
              :images="article.images"
              :icon="article.icon"
              :gradient="article.gradient"
              itemprop="image"
            />
            <div class="article-badges">
              <div class="article-category" itemprop="articleSection">{{ article.category }}</div>
              <div v-if="article.featured" class="featured-badge">ویژه</div>
            </div>
            
            <div class="article-content">
              <div class="article-meta">
                <time 
                  :datetime="article.created_at" 
                  class="article-date"
                  itemprop="datePublished"
                >
                  {{ article.created_at ? new Date(article.created_at).toLocaleDateString('fa-IR') : 'نامشخص' }}
                </time>
                <span class="article-read-time">{{ article.read_time || '۵ دقیقه' }}</span>
              </div>
              
              <h2 class="article-title" itemprop="headline">{{ article.title }}</h2>
              <p class="article-excerpt" itemprop="description">{{ article.excerpt }}</p>
              
              <div class="article-tags-preview" itemprop="keywords">
                <span v-for="tag in (article.tags || []).slice(0, 3)" :key="tag" class="tag-mini">
                  {{ tag }}
                </span>
              </div>
              
              <div class="article-footer">
                <div class="article-author" itemprop="author" itemscope itemtype="https://schema.org/Person">
                  <div class="author-avatar">{{ article.author_avatar || 'ن' }}</div>
                  <span class="author-name" itemprop="name">{{ article.author || 'نامشخص' }}</span>
                </div>
                <span class="read-more">
                  بیشتر
                  <span class="arrow">←</span>
                </span>
              </div>
            </div>
          </router-link>
        </TransitionGroup>

        <!-- Pagination -->
        <nav 
          v-if="filteredArticles.length > itemsPerPage" 
          class="pagination"
          aria-label="صفحه‌بندی مقالات"
        >
          <button 
            @click="currentArticlePage--" 
            :disabled="currentArticlePage === 1"
            class="pagination-btn"
            aria-label="صفحه قبل"
          >
            قبلی
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in totalArticlePages"
              :key="page"
              @click="currentArticlePage = page"
              :class="['page-btn', { active: currentArticlePage === page }]"
              :aria-label="`صفحه ${page}`"
              :aria-current="currentArticlePage === page ? 'page' : null"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentArticlePage++" 
            :disabled="currentArticlePage === totalArticlePages"
            class="pagination-btn"
            aria-label="صفحه بعد"
          >
            بعدی
          </button>
        </nav>
      </div>
    </section>

    <!-- Gallery Section -->
    <section v-if="activeTab === 'gallery'" class="archive-content">
      <div class="container">
        <!-- Loading state -->
        <div v-if="galleryLoading" class="loading-state">
          <div class="spinner"></div>
          <p>در حال بارگیری پروژه‌ها...</p>
        </div>
        
        <!-- Error state -->
        <div v-if="galleryError && !galleryLoading" class="error-state">
          <p>{{ galleryError }}</p>
        </div>

        <!-- Search and Filter -->
        <div v-if="!galleryLoading" class="archive-controls">
          <div class="search-box">
            <label for="gallery-search" class="sr-only">جستجو در پروژه‌ها</label>
            <span class="search-icon" aria-hidden="true">🔍</span>
            <input 
              id="gallery-search"
              v-model="gallerySearchQuery" 
              type="search" 
              placeholder="جستجو در پروژه‌ها..."
              class="search-input"
              aria-label="جستجو در پروژه‌ها"
            />
          </div>
          
          <div class="filter-buttons" role="group" aria-label="دسته‌بندی پروژه‌ها">
            <button 
              v-for="category in galleryCategories" 
              :key="category"
              @click="selectedGalleryCategory = category"
              :class="['filter-btn', { active: selectedGalleryCategory === category }]"
              :aria-pressed="selectedGalleryCategory === category"
            >
              {{ category }}
            </button>
          </div>

          <div class="view-toggle" role="group" aria-label="حالت نمایش">
            <button 
              @click="viewMode = 'grid'" 
              :class="{ active: viewMode === 'grid' }"
              aria-label="نمایش شبکه‌ای"
              :aria-pressed="viewMode === 'grid'"
            >
              <span aria-hidden="true">⊞</span>
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="{ active: viewMode === 'list' }"
              aria-label="نمایش لیستی"
              :aria-pressed="viewMode === 'list'"
            >
              <span aria-hidden="true">☰</span>
            </button>
          </div>
        </div>

        <div class="results-info" role="status" aria-live="polite">
          <span class="results-count">{{ filteredGalleryItems.length }} پروژه یافت شد</span>
        </div>

        <!-- Gallery Grid/List with Schema.org markup -->
        <TransitionGroup 
          name="gallery-list" 
          tag="div" 
          :class="['gallery-archive-grid', viewMode]"
          role="list"
        >
          <router-link
            v-for="item in paginatedGalleryItems" 
            :key="item.id"
            :to="`/project/${item.id}`"
            class="gallery-card"
            itemscope 
            itemtype="https://schema.org/CreativeWork"
            role="listitem"
          >
            <ImageSlider 
              class="card-image"
              :image="item.image"
              :images="item.images"
              :icon="item.icon"
              :gradient="item.gradient"
              itemprop="image"
            />
            <div class="card-overlay">
              <div class="overlay-content">
                <span class="view-btn">مشاهده پروژه</span>
              </div>
            </div>
            <div class="card-badge" :style="{ background: item.categoryColor }">
              {{ item.category }}
            </div>
            
            <div class="card-content">
              <h2 class="card-title" itemprop="name">{{ item.title }}</h2>
              <p class="card-description" itemprop="description">{{ item.description }}</p>
              <div class="card-meta">
                <time 
                  :datetime="item.created_at || item.date" 
                  class="card-date"
                  itemprop="dateCreated"
                >
                  {{ item.date || item.created_at || 'نامشخص' }}
                </time>
                <div class="card-tech" v-if="item.tech">
                  <span v-for="t in item.tech.slice(0, 3)" :key="t" class="tech-tag">
                    {{ t }}
                  </span>
                </div>
              </div>
            </div>
          </router-link>
        </TransitionGroup>

        <!-- Pagination -->
        <nav 
          v-if="filteredGalleryItems.length > itemsPerPage" 
          class="pagination"
          aria-label="صفحه‌بندی پروژه‌ها"
        >
          <button 
            @click="currentGalleryPage--" 
            :disabled="currentGalleryPage === 1"
            class="pagination-btn"
            aria-label="صفحه قبل"
          >
            قبلی
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in totalGalleryPages"
              :key="page"
              @click="currentGalleryPage = page"
              :class="['page-btn', { active: currentGalleryPage === page }]"
              :aria-label="`صفحه ${page}`"
              :aria-current="currentGalleryPage === page ? 'page' : null"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentGalleryPage++" 
            :disabled="currentGalleryPage === totalGalleryPages"
            class="pagination-btn"
            aria-label="صفحه بعد"
          >
            بعدی
          </button>
        </nav>
      </div>
    </section>

    <!-- Services Section -->
    <section v-if="activeTab === 'services'" class="archive-content">
      <div class="container">
        <!-- Loading state -->
        <div v-if="servicesLoading" class="loading-state">
          <div class="spinner"></div>
          <p>در حال بارگیری خدمات...</p>
        </div>
        
        <!-- Error state -->
        <div v-if="servicesError && !servicesLoading" class="error-state">
          <p>{{ servicesError }}</p>
        </div>

        <!-- Search and Filter -->
        <div v-if="!servicesLoading" class="archive-controls">
          <div class="search-box">
            <label for="services-search" class="sr-only">جستجو در خدمات</label>
            <span class="search-icon" aria-hidden="true">🔍</span>
            <input 
              id="services-search"
              v-model="servicesSearchQuery" 
              type="search" 
              placeholder="جستجو در خدمات..."
              class="search-input"
              aria-label="جستجو در خدمات"
            />
          </div>
          
          <div class="filter-buttons" role="group" aria-label="دسته‌بندی خدمات">
            <button 
              v-for="category in serviceCategories" 
              :key="category"
              @click="selectedServiceCategory = category"
              :class="['filter-btn', { active: selectedServiceCategory === category }]"
              :aria-pressed="selectedServiceCategory === category"
            >
              {{ category }}
            </button>
          </div>
        </div>

        <div class="results-info" role="status" aria-live="polite">
          <span class="results-count">{{ filteredServices.length }} خدمت یافت شد</span>
        </div>

        <!-- Services Grid -->
        <TransitionGroup 
          name="services-list" 
          tag="div" 
          class="services-grid"
          role="list"
        >
          <div
            v-for="service in paginatedServices" 
            :key="service.id"
            class="service-card"
            itemscope 
            itemtype="https://schema.org/Service"
            role="listitem"
          >
            <ImageSlider 
              v-if="service.images && service.images.length > 0"
              class="service-image"
              :image="service.image"
              :images="service.images"
              :icon="service.icon"
              :gradient="service.gradient"
            />
            <div v-else class="service-icon">
              <span v-if="service.icon">{{ service.icon }}</span>
              <span v-else>🔧</span>
            </div>
            
            <div class="service-content">
              <h2 class="service-title" itemprop="name">{{ service.title }}</h2>
              <p class="service-description" itemprop="description">{{ service.description }}</p>
              <div class="service-meta">
                <span class="service-category">{{ service.category }}</span>
              </div>
            </div>
          </div>
        </TransitionGroup>

        <!-- Pagination -->
        <nav 
          v-if="filteredServices.length > itemsPerPage" 
          class="pagination"
          aria-label="صفحه‌بندی خدمات"
        >
          <button 
            @click="currentServicePage--" 
            :disabled="currentServicePage === 1"
            class="pagination-btn"
            aria-label="صفحه قبل"
          >
            قبلی
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in totalServicePages"
              :key="page"
              @click="currentServicePage = page"
              :class="['page-btn', { active: currentServicePage === page }]"
              :aria-label="`صفحه ${page}`"
              :aria-current="currentServicePage === page ? 'page' : null"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentServicePage++" 
            :disabled="currentServicePage === totalServicePages"
            class="pagination-btn"
            aria-label="صفحه بعد"
          >
            بعدی
          </button>
        </nav>
      </div>
    </section>

    <!-- Certificates Section -->
    <section v-if="activeTab === 'certificates'" class="archive-content">
      <div class="container">
        <!-- Loading state -->
        <div v-if="certificatesLoading" class="loading-state">
          <div class="spinner"></div>
          <p>در حال بارگیری گواهینامه‌ها...</p>
        </div>
        
        <!-- Error state -->
        <div v-if="certificatesError && !certificatesLoading" class="error-state">
          <p>{{ certificatesError }}</p>
        </div>

        <!-- Search and Filter -->
        <div v-if="!certificatesLoading" class="archive-controls">
          <div class="search-box">
            <label for="certificates-search" class="sr-only">جستجو در گواهینامه‌ها</label>
            <span class="search-icon" aria-hidden="true">🔍</span>
            <input 
              id="certificates-search"
              v-model="certificatesSearchQuery" 
              type="search" 
              placeholder="جستجو در گواهینامه‌ها..."
              class="search-input"
              aria-label="جستجو در گواهینامه‌ها"
            />
          </div>
          
          <div class="filter-buttons" role="group" aria-label="دسته‌بندی گواهینامه‌ها">
            <button 
              v-for="category in certificateCategories" 
              :key="category"
              @click="selectedCertificateCategory = category"
              :class="['filter-btn', { active: selectedCertificateCategory === category }]"
              :aria-pressed="selectedCertificateCategory === category"
            >
              {{ category }}
            </button>
          </div>
        </div>

        <div class="results-info" role="status" aria-live="polite">
          <span class="results-count">{{ filteredCertificates.length }} گواهینامه یافت شد</span>
        </div>

        <!-- Certificates Grid -->
        <TransitionGroup 
          name="certificates-list" 
          tag="div" 
          class="certificates-grid"
          role="list"
        >
          <div
            v-for="cert in paginatedCertificates" 
            :key="cert.id"
            class="certificate-card"
            itemscope 
            itemtype="https://schema.org/EducationalOccupationalCredential"
            role="listitem"
          >
            <ImageSlider 
              class="certificate-image"
              :image="cert.image"
              :images="cert.images"
              :icon="cert.icon"
              :gradient="cert.gradient"
              itemprop="image"
            />
            
            <div class="certificate-content">
              <h2 class="certificate-title" itemprop="name">{{ cert.title }}</h2>
              <p class="certificate-description" itemprop="description">{{ cert.description }}</p>
              <div class="certificate-meta">
                <span class="certificate-category">{{ cert.category }}</span>
                <time 
                  v-if="cert.date"
                  :datetime="cert.date" 
                  class="certificate-date"
                  itemprop="validFrom"
                >
                  {{ cert.date }}
                </time>
              </div>
            </div>
          </div>
        </TransitionGroup>

        <!-- Pagination -->
        <nav 
          v-if="filteredCertificates.length > itemsPerPage" 
          class="pagination"
          aria-label="صفحه‌بندی گواهینامه‌ها"
        >
          <button 
            @click="currentCertificatePage--" 
            :disabled="currentCertificatePage === 1"
            class="pagination-btn"
            aria-label="صفحه قبل"
          >
            قبلی
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in totalCertificatePages"
              :key="page"
              @click="currentCertificatePage = page"
              :class="['page-btn', { active: currentCertificatePage === page }]"
              :aria-label="`صفحه ${page}`"
              :aria-current="currentCertificatePage === page ? 'page' : null"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentCertificatePage++" 
            :disabled="currentCertificatePage === totalCertificatePages"
            class="pagination-btn"
            aria-label="صفحه بعد"
          >
            بعدی
          </button>
        </nav>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticles, getGalleryItems, getSlider, getServices, getCertificates } from '../api/services'
import ImageSlider from '../components/ImageSlider.vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

// Inject theme from App.vue
const { isDark, toggleTheme } = inject('theme')

const route = useRoute()
const router = useRouter()

// Active tab management
const activeTab = ref('articles')

// Articles state
const articleSearchQuery = ref('')
const selectedArticleCategory = ref('همه')
const articleSortBy = ref('latest')
const currentArticlePage = ref(1)
const articlesLoading = ref(true)
const articlesError = ref(null)
const articleCategories = ref(['همه'])
const articles = ref([])

// Gallery state
const gallerySearchQuery = ref('')
const selectedGalleryCategory = ref('همه')
const viewMode = ref('grid')
const currentGalleryPage = ref(1)
const galleryLoading = ref(true)
const galleryError = ref(null)
const galleryCategories = ref(['همه'])
const galleryItems = ref([])

// Services state
const servicesSearchQuery = ref('')
const selectedServiceCategory = ref('همه')
const currentServicePage = ref(1)
const servicesLoading = ref(true)
const servicesError = ref(null)
const serviceCategories = ref(['همه'])
const services = ref([])

// Certificates state
const certificatesSearchQuery = ref('')
const selectedCertificateCategory = ref('همه')
const currentCertificatePage = ref(1)
const certificatesLoading = ref(true)
const certificatesError = ref(null)
const certificateCategories = ref(['همه'])
const certificates = ref([])

const itemsPerPage = 12

// Switch between tabs
const switchTab = (tab) => {
  activeTab.value = tab
  currentArticlePage.value = 1
  currentGalleryPage.value = 1
  currentServicePage.value = 1
  currentCertificatePage.value = 1
  
  // Update URL without full navigation
  router.push({ query: { tab } })
  
  // Update page title and meta for SEO
  updateMetaTags()
}

// Update meta tags for SEO
const updateMetaTags = () => {
  const title = activeTab.value === 'articles' 
    ? 'مقالات و آموزش‌های BIM | مهندسین مشاور دانش‌بنیان'
    : activeTab.value === 'gallery'
    ? 'گالری پروژه‌های BIM | نمونه کارهای شرکت'
    : activeTab.value === 'services'
    ? 'خدمات مهندسی BIM | مهندسین مشاور دانش‌بنیان'
    : 'گواهینامه‌ها و افتخارات | مهندسین مشاور دانش‌بنیان'
  
  const description = activeTab.value === 'articles'
    ? 'مقالات تخصصی و آموزشی در زمینه مدل‌سازی اطلاعات ساختمان (BIM)، طراحی معماری، سازه و تاسیسات. آخرین اخبار و روش‌های نوین در صنعت ساخت و ساز'
    : activeTab.value === 'gallery'
    ? 'نمونه کارها و پروژه‌های انجام شده با استفاده از فناوری BIM شامل طراحی معماری، مدل‌سازی سه بعدی و مدیریت پروژه‌های ساختمانی'
    : activeTab.value === 'services'
    ? 'خدمات مهندسی BIM شامل مشاوره، طراحی، نظارت و اجرای پروژه‌های ساختمانی با استفاده از فناوری‌های پیشرفته'
    : 'گواهینامه‌ها، افتخارات و دستاوردهای شرکت در زمینه مهندسی BIM و ساخت و ساز'
  
  document.title = title
  
  // Update meta description
  let metaDescription = document.querySelector('meta[name="description"]')
  if (metaDescription) {
    metaDescription.setAttribute('content', description)
  }
}

// Articles computed properties
const filteredArticles = computed(() => {
  let filtered = articles.value

  if (selectedArticleCategory.value !== 'همه') {
    filtered = filtered.filter(article => article.category === selectedArticleCategory.value)
  }

  if (articleSearchQuery.value) {
    const query = articleSearchQuery.value.toLowerCase()
    filtered = filtered.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.excerpt.toLowerCase().includes(query) ||
      (article.tags && article.tags.some(tag => tag.toLowerCase().includes(query)))
    )
  }

  if (articleSortBy.value === 'popular') {
    filtered = [...filtered].sort((a, b) => (b.viewsNum || 0) - (a.viewsNum || 0))
  } else if (articleSortBy.value === 'latest') {
    filtered = [...filtered].sort((a, b) => b.id - a.id)
  }

  return filtered
})

const paginatedArticles = computed(() => {
  const start = (currentArticlePage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredArticles.value.slice(start, end)
})

const totalArticlePages = computed(() => {
  return Math.ceil(filteredArticles.value.length / itemsPerPage)
})

// Gallery computed properties
const filteredGalleryItems = computed(() => {
  let filtered = galleryItems.value

  if (selectedGalleryCategory.value !== 'همه') {
    filtered = filtered.filter(item => item.category === selectedGalleryCategory.value)
  }

  if (gallerySearchQuery.value) {
    const query = gallerySearchQuery.value.toLowerCase()
    filtered = filtered.filter(item =>
      item.title.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query) ||
      (item.tech && item.tech.some(t => t.toLowerCase().includes(query)))
    )
  }

  return filtered
})

const paginatedGalleryItems = computed(() => {
  const start = (currentGalleryPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredGalleryItems.value.slice(start, end)
})

const totalGalleryPages = computed(() => {
  return Math.ceil(filteredGalleryItems.value.length / itemsPerPage)
})

// Services computed properties
const filteredServices = computed(() => {
  let filtered = services.value

  if (selectedServiceCategory.value !== 'همه') {
    filtered = filtered.filter(service => service.category === selectedServiceCategory.value)
  }

  if (servicesSearchQuery.value) {
    const query = servicesSearchQuery.value.toLowerCase()
    filtered = filtered.filter(service =>
      service.title.toLowerCase().includes(query) ||
      service.description.toLowerCase().includes(query) ||
      (service.tags && service.tags.some(tag => tag.toLowerCase().includes(query)))
    )
  }

  return filtered
})

const paginatedServices = computed(() => {
  const start = (currentServicePage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredServices.value.slice(start, end)
})

const totalServicePages = computed(() => {
  return Math.ceil(filteredServices.value.length / itemsPerPage)
})

// Certificates computed properties
const filteredCertificates = computed(() => {
  let filtered = certificates.value

  if (selectedCertificateCategory.value !== 'همه') {
    filtered = filtered.filter(cert => cert.category === selectedCertificateCategory.value)
  }

  if (certificatesSearchQuery.value) {
    const query = certificatesSearchQuery.value.toLowerCase()
    filtered = filtered.filter(cert =>
      cert.title.toLowerCase().includes(query) ||
      cert.description.toLowerCase().includes(query) ||
      (cert.tags && cert.tags.some(tag => tag.toLowerCase().includes(query)))
    )
  }

  return filtered
})

const paginatedCertificates = computed(() => {
  const start = (currentCertificatePage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredCertificates.value.slice(start, end)
})

const totalCertificatePages = computed(() => {
  return Math.ceil(filteredCertificates.value.length / itemsPerPage)
})

// Enrich article with slider images
const enrichArticleWithSlider = async (article) => {
  if (article.slider_id) {
    try {
      const sliderResponse = await getSlider(article.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...article,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (article.image && !article.images) {
    return {
      ...article,
      images: [article.image]
    }
  }
  return article
}

// Enrich gallery item with slider images
const enrichGalleryItemWithSlider = async (item) => {
  if (item.slider_id) {
    try {
      const sliderResponse = await getSlider(item.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...item,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (item.image && !item.images) {
    return {
      ...item,
      images: [item.image]
    }
  }
  return item
}

// Enrich service with slider images
const enrichServiceWithSlider = async (service) => {
  if (service.slider_id) {
    try {
      const sliderResponse = await getSlider(service.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...service,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (service.image && !service.images) {
    return {
      ...service,
      images: [service.image]
    }
  }
  return service
}

// Enrich certificate with slider images
const enrichCertificateWithSlider = async (cert) => {
  if (cert.slider_id) {
    try {
      const sliderResponse = await getSlider(cert.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...cert,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (cert.image && !cert.images) {
    return {
      ...cert,
      images: [cert.image]
    }
  }
  return cert
}

// Fetch articles from API
const fetchArticles = async () => {
  try {
    articlesLoading.value = true
    articlesError.value = null
    const response = await getArticles({ page: 1, limit: 100 })
    let items = response.data || []
    
    items = await Promise.all(items.map(article => enrichArticleWithSlider(article)))
    
    articles.value = items
    
    const cats = ['همه', ...new Set(articles.value.map(a => a.category))]
    articleCategories.value = cats
  } catch (err) {
    console.error('Error fetching articles:', err)
    articlesError.value = 'خطا در بارگیری مقالات'
  } finally {
    articlesLoading.value = false
  }
}

// Fetch gallery items from API
const fetchGalleryItems = async () => {
  try {
    galleryLoading.value = true
    galleryError.value = null
    const response = await getGalleryItems({ page: 1, limit: 100 })
    let items = response.data || []
    
    items = await Promise.all(items.map(item => enrichGalleryItemWithSlider(item)))
    
    galleryItems.value = items
    
    const cats = ['همه', ...new Set(galleryItems.value.map(i => i.category))]
    galleryCategories.value = cats
  } catch (err) {
    console.error('Error fetching gallery items:', err)
    galleryError.value = 'خطا در بارگیری پروژه‌ها'
  } finally {
    galleryLoading.value = false
  }
}

// Fetch services from API
const fetchServices = async () => {
  try {
    servicesLoading.value = true
    servicesError.value = null
    const response = await getServices()
    let items = response.data || []
    
    items = await Promise.all(items.map(service => enrichServiceWithSlider(service)))
    
    services.value = items
    
    const cats = ['همه', ...new Set(services.value.map(s => s.category))]
    serviceCategories.value = cats
  } catch (err) {
    console.error('Error fetching services:', err)
    servicesError.value = 'خطا در بارگیری خدمات'
  } finally {
    servicesLoading.value = false
  }
}

// Fetch certificates from API
const fetchCertificates = async () => {
  try {
    certificatesLoading.value = true
    certificatesError.value = null
    const response = await getCertificates()
    let items = response.data || []
    
    items = await Promise.all(items.map(cert => enrichCertificateWithSlider(cert)))
    
    certificates.value = items
    
    const cats = ['همه', ...new Set(certificates.value.map(c => c.category))]
    certificateCategories.value = cats
  } catch (err) {
    console.error('Error fetching certificates:', err)
    certificatesError.value = 'خطا در بارگیری گواهینامه‌ها'
  } finally {
    certificatesLoading.value = false
  }
}

// Initialize from URL query
onMounted(() => {
  // Check URL query for active tab
  if (route.query.tab === 'gallery') {
    activeTab.value = 'gallery'
  } else if (route.query.tab === 'services') {
    activeTab.value = 'services'
  } else if (route.query.tab === 'certificates') {
    activeTab.value = 'certificates'
  }
  
  fetchArticles()
  fetchGalleryItems()
  fetchServices()
  fetchCertificates()
  updateMetaTags()
})

// Watch for tab changes to update meta tags
watch(activeTab, () => {
  updateMetaTags()
})
</script>

<style scoped>
/* Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.media-archive-page {
  min-height: 100vh;
  background: white;
  color: #1a1a1a;
}

.dark-mode.media-archive-page {
  background: #1a1a1a;
  color: #ffffff;
}

.archive-hero {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  padding: 8rem 0 4rem;
  text-align: center;
  color: white;
}

.dark-mode .archive-hero {
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.breadcrumb {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.breadcrumb a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb a:hover {
  color: white;
}

.separator {
  color: rgba(255, 255, 255, 0.6);
}

.current {
  color: white;
  font-weight: 600;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.page-description {
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

/* Tab Switcher */
.tab-switcher {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.tab-btn {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: white;
  color: #0ea5e9;
  border-color: white;
}

.dark-mode .tab-btn.active {
  background: #2d2d2d;
  color: white;
  border-color: #2d2d2d;
}

/* Archive Content */
.archive-content {
  padding: 4rem 0;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.1);
  border-top-color: #0ea5e9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state p {
  color: #e74c3c;
  font-size: 1.1rem;
}

/* Search and Filter Controls */
.archive-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 250px;
  position: relative;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

.search-input {
  width: 100%;
  padding: 0.8rem 3rem 0.8rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #1a1a1a;
}

.dark-mode .search-input {
  background: #2d2d2d;
  color: white;
  border-color: #444;
}

.search-input:focus {
  outline: none;
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-tabs,
.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.6rem 1.2rem;
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.dark-mode .filter-btn {
  background: #2d2d2d;
  color: #ccc;
  border-color: #444;
}

.filter-btn:hover {
  border-color: #0ea5e9;
  color: #0ea5e9;
}

.filter-btn.active {
  background: #0ea5e9;
  color: white;
  border-color: #0ea5e9;
}

.active-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: white;
  border-radius: 2px;
}

.sort-select {
  padding: 0.6rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.3s;
}

.dark-mode .sort-select {
  background: #2d2d2d;
  color: white;
  border-color: #444;
}

.sort-select:focus {
  outline: none;
  border-color: #0ea5e9;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
  background: white;
  padding: 0.3rem;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.dark-mode .view-toggle {
  background: #2d2d2d;
  border-color: #444;
}

.view-toggle button {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.2rem;
}

.view-toggle button.active {
  background: #0ea5e9;
  color: white;
}

.results-info {
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.dark-mode .results-info {
  color: #ccc;
}

/* Articles Grid */
.articles-archive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.article-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  text-decoration: none;
  color: inherit;
  display: block;
}

.dark-mode .article-card {
  background: #2d2d2d;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.article-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.article-badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.article-category,
.featured-badge {
  padding: 0.4rem 0.8rem;
  background: rgba(102, 126, 234, 0.9);
  color: white;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.featured-badge {
  background: rgba(231, 76, 60, 0.9);
}

.article-content {
  padding: 1.5rem;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #999;
}

.article-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #1a1a1a;
  line-height: 1.4;
}

.dark-mode .article-title {
  color: white;
}

.article-excerpt {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dark-mode .article-excerpt {
  color: #ccc;
}

.article-tags-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag-mini {
  padding: 0.3rem 0.6rem;
  background: #f0f0f0;
  color: #666;
  border-radius: 4px;
  font-size: 0.75rem;
}

.dark-mode .tag-mini {
  background: #3d3d3d;
  color: #ccc;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.dark-mode .article-footer {
  border-color: #444;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #0ea5e9;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.author-name {
  font-size: 0.9rem;
  color: #666;
}

.dark-mode .author-name {
  color: #ccc;
}

.read-more {
  color: #0ea5e9;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.arrow {
  transition: transform 0.3s;
}

.article-card:hover .arrow {
  transform: translateX(-3px);
}

/* Gallery Grid */
.gallery-archive-grid {
  display: grid;
  gap: 2rem;
  margin-bottom: 3rem;
}

.gallery-archive-grid.grid {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.gallery-archive-grid.list {
  grid-template-columns: 1fr;
}

.gallery-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  text-decoration: none;
  color: inherit;
  display: block;
}

.dark-mode .gallery-card {
  background: #2d2d2d;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.gallery-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.gallery-card:hover .card-overlay {
  opacity: 1;
}

.card-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.gallery-archive-grid.list .card-image {
  height: 300px;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 40%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.overlay-content {
  text-align: center;
}

.view-btn {
  padding: 0.8rem 1.5rem;
  background: white;
  color: #0ea5e9;
  border-radius: 8px;
  font-weight: 600;
  display: inline-block;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.4rem 0.8rem;
  background: rgba(102, 126, 234, 0.9);
  color: white;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.card-content {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #1a1a1a;
}

.dark-mode .card-title {
  color: white;
}

.card-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dark-mode .card-description {
  color: #ccc;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #999;
}

.card-tech {
  display: flex;
  gap: 0.5rem;
}

.tech-tag {
  padding: 0.3rem 0.6rem;
  background: #f0f0f0;
  color: #666;
  border-radius: 4px;
  font-size: 0.75rem;
}

.dark-mode .tech-tag {
  background: #3d3d3d;
  color: #ccc;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 3rem;
}

.pagination-btn,
.page-btn {
  padding: 0.6rem 1.2rem;
  background: white;
  color: #0ea5e9;
  border: 2px solid #0ea5e9;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.dark-mode .pagination-btn,
.dark-mode .page-btn {
  background: #2d2d2d;
  color: white;
  border-color: #0ea5e9;
}

.pagination-btn:hover:not(:disabled),
.page-btn:hover {
  background: #0ea5e9;
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn.active {
  background: #0ea5e9;
  color: white;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.service-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  text-decoration: none;
  color: inherit;
  display: block;
}

.dark-mode .service-card {
  background: #2d2d2d;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.service-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.service-image {
  width: 100%;
  height: 200px;
  border-radius: 12px 12px 0 0;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.service-content {
  flex: 1;
}

.service-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #1a1a1a;
}

.dark-mode .service-title {
  color: white;
}

.service-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.dark-mode .service-description {
  color: #ccc;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #999;
}

.service-category {
  padding: 0.3rem 0.6rem;
  background: #f0f0f0;
  color: #666;
  border-radius: 4px;
  font-size: 0.75rem;
}

.dark-mode .service-category {
  background: #3d3d3d;
  color: #ccc;
}

/* Certificates Grid */
.certificates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.certificate-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  text-decoration: none;
  color: inherit;
  display: block;
}

.dark-mode .certificate-card {
  background: #2d2d2d;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.certificate-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.certificate-image {
  width: 100%;
  height: 200px;
  border-radius: 16px 16px 0 0;
  overflow: hidden;
}

.certificate-content {
  padding: 1.5rem;
}

.certificate-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #1a1a1a;
}

.dark-mode .certificate-title {
  color: white;
}

.certificate-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dark-mode .certificate-description {
  color: #ccc;
}

.certificate-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #999;
}

.certificate-category {
  padding: 0.3rem 0.6rem;
  background: #f0f0f0;
  color: #666;
  border-radius: 4px;
  font-size: 0.75rem;
}

.dark-mode .certificate-category {
  background: #3d3d3d;
  color: #ccc;
}

.certificate-date {
  color: #0ea5e9;
  font-weight: 600;
}

.pagination-pages {
  display: flex;
  gap: 0.5rem;
}

/* Transitions */
.article-list-move,
.article-list-enter-active,
.article-list-leave-active,
.gallery-list-move,
.gallery-list-enter-active,
.gallery-list-leave-active {
  transition: all 0.5s ease;
}

.article-list-enter-from,
.gallery-list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.article-list-leave-to,
.gallery-list-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.article-list-leave-active,
.gallery-list-leave-active {
  position: absolute;
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .tab-switcher {
    flex-direction: column;
  }
  
  .archive-controls {
    flex-direction: column;
  }
  
  .articles-archive-grid,
  .gallery-archive-grid.grid {
    grid-template-columns: 1fr;
  }
  
  .pagination-pages {
    flex-wrap: wrap;
  }
  
  .filter-tabs,
  .filter-buttons {
    width: 100%;
    justify-content: center;
  }
}
</style>
