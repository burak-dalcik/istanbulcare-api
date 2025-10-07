# Istanbul Care API - React Developer Guide

## 🚀 Quick Start

**Base URL:** `http://127.0.0.1:8000`  
**Swagger UI:** `http://127.0.0.1:8000/docs`

## 🔑 Authentication Status
**✅ Authentication is DISABLED for development**  
All endpoints are accessible without authentication tokens.

---

## 📝 Blog API Endpoints

### 1. **Get All Blog Posts (Public)**
```http
GET /api/v1/blog/posts?page=1&size=10&lang=en
```

**Parameters:**
- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 10, max: 100)
- `lang` (optional): Language code - `tr`, `en`, `fr` (default: `en`)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "slug": "dhi-hair-transplant-turkey",
      "author_id": 1,
      "published_date": "2025-10-07T10:30:00",
      "title_tr": "Türkiye'de DHI Saç Ekimi",
      "title_en": "DHI Hair Transplant in Turkey",
      "title_fr": "Greffe de Cheveux DHI en Turquie",
      "description_tr": "Türkiye, gelişmiş tıbbi tesisleri...",
      "description_en": "Turkey has become a top destination...",
      "description_fr": "La Turquie est devenue une destination...",
      "content_tr": "Türkiye, gelişmiş tıbbi tesisleri...",
      "content_en": "Turkey has become a top destination...",
      "content_fr": "La Turquie est devenue une destination...",
      "featured_image_url": "https://example.com/images/dhi-hair-transplant.jpg",
      "gallery_urls": ["https://example.com/images/dhi-1.jpg", "https://example.com/images/dhi-2.jpg"]
    }
  ],
  "total": 3,
  "page": 1,
  "size": 10
}
```

### 2. **Get Single Blog Post (Public)**
```http
GET /api/v1/blog/posts/{slug}?lang=en
```

**Parameters:**
- `slug`: Blog post slug (e.g., "dhi-hair-transplant-turkey")
- `lang` (optional): Language code - `tr`, `en`, `fr` (default: `en`)

**Response:** Single blog post object (same structure as above)

---

## 🛠 Admin Blog Management

### 3. **Get All Blog Posts (Admin)**
```http
GET /admin/blog/posts
```

**Response:** Array of all blog posts (same structure as public API)

### 4. **Get Single Blog Post (Admin)**
```http
GET /admin/blog/posts/{id}
```

### 5. **Create Blog Post**
```http
POST /admin/blog/posts
Content-Type: application/json

{
  "slug": "new-blog-post",
  "author_id": 1,
  "published_date": "2025-10-07T10:30:00",
  "title_tr": "Türkçe Başlık",
  "title_en": "English Title",
  "title_fr": "Titre Français",
  "description_tr": "Türkçe açıklama...",
  "description_en": "English description...",
  "description_fr": "Description française...",
  "content_tr": "Türkçe içerik...",
  "content_en": "English content...",
  "content_fr": "Contenu français...",
  "featured_image_url": "https://example.com/image.jpg",
  "gallery_urls": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
}
```

### 6. **Update Blog Post**
```http
PUT /admin/blog/posts/{id}
Content-Type: application/json

{
  "title_en": "Updated English Title",
  "content_en": "Updated English content..."
}
```

### 7. **Delete Blog Post**
```http
DELETE /admin/blog/posts/{id}
```

---

## 🌐 Language Support

The API supports 3 languages:
- **Turkish (`tr`)**: `title_tr`, `content_tr`, `description_tr`
- **English (`en`)**: `title_en`, `content_en`, `description_en`
- **French (`fr`)**: `title_fr`, `content_fr`, `description_fr`

### React Implementation Example:
```javascript
// Get blog posts in Turkish
const response = await fetch('/api/v1/blog/posts?lang=tr&page=1&size=6');
const data = await response.json();

// Display based on language
const displayTitle = (post, lang) => {
  switch(lang) {
    case 'tr': return post.title_tr || post.title_en;
    case 'fr': return post.title_fr || post.title_en;
    default: return post.title_en;
  }
};
```

---

## 🎨 Frontend Design Integration

Based on your design, here's how to structure the blog cards:

```javascript
// Blog Card Component
const BlogCard = ({ post, language = 'en' }) => {
  const title = post[`title_${language}`] || post.title_en;
  const description = post[`description_${language}`] || post.description_en;
  
  return (
    <div className="blog-card">
      <img src={post.featured_image_url} alt={title} />
      <h3>{title}</h3>
      <p>{description}</p>
      <Link to={`/blog/${post.slug}?lang=${language}`}>
        Read More
      </Link>
    </div>
  );
};

// Usage in your services section
const ServicesSection = () => {
  const [posts, setPosts] = useState([]);
  const [language, setLanguage] = useState('en');
  
  useEffect(() => {
    fetch(`/api/v1/blog/posts?lang=${language}&size=6`)
      .then(res => res.json())
      .then(data => setPosts(data.items));
  }, [language]);
  
  return (
    <div className="services-grid">
      {posts.map(post => (
        <BlogCard key={post.id} post={post} language={language} />
      ))}
    </div>
  );
};
```

---

## 📊 Other Available APIs

### Header Navigation
```http
GET /api/v1/header/columns?lang=en
```

### Services
```http
GET /api/v1/services
GET /api/v1/services/{slug}
```

### Lead Generation
```http
POST /api/v1/leads
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I'm interested in hair transplant"
}
```

---

## 🔧 Development Setup

1. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Create sample data:**
   ```bash
   python create_sample_data.py
   ```

3. **Access Swagger UI:**
   ```
   http://127.0.0.1:8000/docs
   ```

---

## ✅ Ready for React Development!

- ✅ Authentication disabled for easy development
- ✅ Multilingual blog system (TR, EN, FR)
- ✅ Complete CRUD operations
- ✅ Sample hair transplant content
- ✅ Image support for blog posts
- ✅ Pagination support
- ✅ RESTful API design

**Your React developer can now:**
1. Fetch blog posts with language support
2. Create dynamic blog cards matching your design
3. Implement language switching
4. Build admin panels for content management
5. Handle pagination and filtering

**Need help?** Check the Swagger UI at `http://127.0.0.1:8000/docs` for interactive API testing!
