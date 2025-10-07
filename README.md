# Istanbul Care API

Modern health tourism API built with FastAPI for managing blog posts, services, and image uploads.

## Features

### 🌍 Multi-language Support
- Turkish (TR)
- English (EN) 
- French (FR)

### 📝 Blog Management
- Create, read blog posts
- Multi-language content (title, content, description)
- Image support (featured image + gallery)
- Pagination support

### 🏥 Services Management
- Hair transplant services (DHI, FUE, Sapphire FUE, etc.)
- Service details with pricing and duration
- Multi-language descriptions

### 📸 Image Upload
- Single and multiple file upload
- Supported formats: JPG, JPEG, PNG, GIF, WEBP
- File validation (max 5MB per file)
- Image serving and management

### 🔧 Additional Features
- Header navigation management
- Lead form submissions
- Swagger UI documentation
- CORS enabled for frontend integration

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (easily replaceable)
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd este-api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Sample Data
```bash
python create_sample_data.py
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```

### 5. Access API
- **Swagger UI:** http://127.0.0.1:8000/docs
- **API Base:** http://127.0.0.1:8000/api/v1/

## API Endpoints

### Blog Posts
- `GET /api/v1/blog/posts` - List blog posts (with pagination & language support)
- `GET /api/v1/blog/posts/{slug}` - Get single blog post
- `POST /api/v1/blog/posts` - Create new blog post

### Services
- `GET /api/v1/services` - List all services
- `GET /api/v1/services/{slug}` - Get single service

### Image Management
- `POST /api/v1/images/upload` - Upload single image
- `POST /api/v1/images/upload-multiple` - Upload multiple images
- `GET /api/v1/images` - List all images
- `GET /api/v1/images/{filename}` - Serve image file
- `DELETE /api/v1/images/{filename}` - Delete image

### Other
- `GET /api/v1/header/columns` - Navigation menu items
- `POST /api/v1/leads` - Submit contact form

## Sample Data

The API comes with pre-populated sample data:

### Blog Posts (15 items)
- **Hair Transplant:** DHI, FUE, Sapphire FUE
- **Dental Treatment:** Hollywood Smile, E-max Veneers, Implant Treatment  
- **Plastic Surgery:** Brazilian Butt Lift, Breast Augmentation, etc.
- **Obesity Treatment:** Sleeve Gastrectomy, Gastric Balloon, etc.

### Services (9 items)
- DHI Hair Transplant (€2,500)
- FUE Hair Transplant (€2,000)
- Sapphire FUE (€3,000)
- Beard Transplant (€1,500)
- And more...

## Usage Examples

### React Integration
```javascript
// Fetch blog posts
const fetchBlogs = async (lang = 'en', size = 10) => {
  const response = await fetch(`/api/v1/blog/posts?lang=${lang}&size=${size}`);
  return response.json();
};

// Upload image
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/api/v1/images/upload', {
    method: 'POST',
    body: formData
  });
  return response.json();
};

// Create blog post
const createBlog = async (blogData) => {
  const response = await fetch('/api/v1/blog/posts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(blogData)
  });
  return response.json();
};
```

## Project Structure

```
este-api/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Configuration
│   ├── db/            # Database setup
│   ├── models/        # SQLAlchemy models
│   └── schemas/       # Pydantic schemas
├── uploads/           # Image storage
├── requirements.txt   # Dependencies
├── create_sample_data.py  # Sample data script
└── README.md
```

## Configuration

The API uses environment variables for configuration. Create a `.env` file:

```env
DATABASE_URL=sqlite:///./istanbul_care.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
"# istanbulcare-api" 
