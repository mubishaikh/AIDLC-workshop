# Unit 1: Idea Submission & Management - Code Generation Plan

## Overview
This plan guides the Code Generation stage for Unit 1. The goal is to generate production-ready code for backend, frontend, database, and tests.

---

## Code Generation Checklist

- [ ] Backend Project Setup
- [ ] Frontend Project Setup
- [ ] Database Schema & Migrations
- [ ] API Endpoints Implementation
- [ ] Frontend Components Implementation
- [ ] Authentication & Authorization
- [ ] Business Logic Implementation
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] API Documentation
- [ ] Deployment Configuration

---

## 1. Backend Project Setup

### Technology Stack
- Language: Python 3.9+
- Framework: Django 4.0+ or FastAPI 0.95+
- ORM: Django ORM or SQLAlchemy
- Database: PostgreSQL 12+
- Caching: Redis 6+
- Task Queue: Celery 5.0+

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── settings.py              # Configuration
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point (for async)
├── ideas/
│   ├── migrations/              # Database migrations
│   ├── models.py                # Domain models
│   ├── views.py                 # API views/endpoints
│   ├── serializers.py           # Request/response serialization
│   ├── services.py              # Business logic
│   ├── permissions.py           # Authorization
│   ├── tests.py                 # Unit tests
│   └── urls.py                  # App-specific URLs
├── contributors/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── tests.py
├── campaigns/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── tests.py
├── documents/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── tests.py
├── auth/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── permissions.py
│   └── tests.py
├── common/
│   ├── exceptions.py            # Custom exceptions
│   ├── middleware.py            # Custom middleware
│   ├── decorators.py            # Custom decorators
│   ├── utils.py                 # Utility functions
│   └── constants.py             # Constants
├── celery_tasks/
│   ├── __init__.py
│   ├── submission_tasks.py      # Submission-related tasks
│   ├── file_tasks.py            # File processing tasks
│   ├── notification_tasks.py    # Notification tasks
│   └── tests.py
├── tests/
│   ├── conftest.py              # Pytest configuration
│   ├── factories.py             # Test data factories
│   ├── integration/             # Integration tests
│   └── e2e/                     # End-to-end tests
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
└── docker-compose.yml           # Local development setup
```

### Dependencies

```
# requirements.txt
Django==4.0.0
djangorestframework==3.13.0
django-cors-headers==3.11.0
django-filter==21.1
django-extensions==3.1.1
psycopg2-binary==2.9.1
redis==4.1.0
celery==5.2.0
gunicorn==20.1.0
python-dotenv==0.19.0
pydantic==1.9.0
requests==2.27.0
pytest==6.2.5
pytest-django==4.5.2
pytest-cov==3.0.0
factory-boy==3.2.1
faker==10.0.0
```

---

## 2. Frontend Project Setup

### Technology Stack
- Framework: React 18+
- State Management: Redux or Context API
- UI Library: Material-UI or Ant Design
- HTTP Client: Axios
- Build Tool: Vite or Create React App
- Testing: Jest + React Testing Library

### Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── index.js
│   ├── App.jsx
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Navigation.jsx
│   │   ├── ideas/
│   │   │   ├── IdeaList.jsx
│   │   │   ├── IdeaCard.jsx
│   │   │   ├── IdeaDetail.jsx
│   │   │   ├── IdeaForm.jsx
│   │   │   └── IdeaSubmission.jsx
│   │   ├── contributors/
│   │   │   ├── ContributorList.jsx
│   │   │   ├── ContributorForm.jsx
│   │   │   └── ContributorCard.jsx
│   │   ├── auth/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   └── common/
│   │       ├── Loading.jsx
│   │       ├── Error.jsx
│   │       └── Modal.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── IdeaPage.jsx
│   │   ├── SubmitIdeaPage.jsx
│   │   ├── MyIdeasPage.jsx
│   │   ├── DashboardPage.jsx
│   │   └── NotFoundPage.jsx
│   ├── services/
│   │   ├── api.js              # API client
│   │   ├── ideaService.js      # Idea API calls
│   │   ├── authService.js      # Auth API calls
│   │   ├── contributorService.js
│   │   └── documentService.js
│   ├── store/
│   │   ├── index.js            # Redux store
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── ideaSlice.js
│   │   │   ├── uiSlice.js
│   │   │   └── errorSlice.js
│   │   └── middleware/
│   │       └── errorHandler.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useIdeas.js
│   │   └── useFetch.js
│   ├── utils/
│   │   ├── constants.js
│   │   ├── validators.js
│   │   ├── formatters.js
│   │   └── helpers.js
│   ├── styles/
│   │   ├── index.css
│   │   ├── variables.css
│   │   └── components.css
│   └── tests/
│       ├── components/
│       ├── services/
│       └── utils/
├── package.json
├── vite.config.js              # or webpack.config.js
├── .env.example
└── .eslintrc.json
```

### Dependencies

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^6.0.0",
    "@reduxjs/toolkit": "^1.8.0",
    "react-redux": "^8.0.0",
    "@mui/material": "^5.0.0",
    "@mui/icons-material": "^5.0.0",
    "axios": "^0.27.0",
    "formik": "^2.2.0",
    "yup": "^0.32.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^1.0.0",
    "vite": "^2.0.0",
    "jest": "^27.0.0",
    "@testing-library/react": "^12.0.0",
    "@testing-library/jest-dom": "^5.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-react": "^7.0.0"
  }
}
```

---

## 3. Database Schema & Migrations

### Core Tables

**ideas**:
- id (UUID, PK)
- title (VARCHAR 200)
- description (TEXT)
- expected_impact (ENUM: HIGH, MEDIUM, LOW)
- submitter_id (UUID, FK)
- campaign_id (UUID, FK)
- status (ENUM: DRAFT, SUBMITTED, UNDER_EVALUATION, EVALUATED, RECOGNIZED)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- submitted_at (TIMESTAMP, nullable)
- recognized_at (TIMESTAMP, nullable)

**contributors**:
- id (UUID, PK)
- idea_id (UUID, FK)
- user_id (UUID, FK)
- role (ENUM: SUBMITTER, CONTRIBUTOR)
- added_at (TIMESTAMP)

**documents**:
- id (UUID, PK)
- idea_id (UUID, FK)
- file_name (VARCHAR 255)
- file_path (VARCHAR 500)
- file_size (INTEGER)
- file_type (VARCHAR 50)
- uploaded_at (TIMESTAMP)
- virus_scan_status (ENUM: PENDING, CLEAN, INFECTED)

**campaigns**:
- id (UUID, PK)
- name (VARCHAR 200)
- description (TEXT)
- status (ENUM: PLANNING, ACTIVE, CLOSED)
- start_date (DATE)
- end_date (DATE)
- created_at (TIMESTAMP)

**users**:
- id (UUID, PK)
- email (VARCHAR 255, UNIQUE)
- first_name (VARCHAR 100)
- last_name (VARCHAR 100)
- role (ENUM: EMPLOYEE, PANEL_MEMBER, ADMIN)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)

---

## 4. API Endpoints

### Ideas Endpoints

```
POST   /api/v1/ideas                    # Submit idea
GET    /api/v1/ideas                    # List all ideas
GET    /api/v1/ideas/{id}               # Get idea details
PUT    /api/v1/ideas/{id}               # Update idea
DELETE /api/v1/ideas/{id}               # Delete idea
GET    /api/v1/ideas/my                 # Get user's ideas
POST   /api/v1/ideas/{id}/submit        # Submit draft idea
POST   /api/v1/ideas/{id}/contributors  # Add contributor
GET    /api/v1/ideas/{id}/contributors  # List contributors
DELETE /api/v1/ideas/{id}/contributors/{user_id}  # Remove contributor
POST   /api/v1/ideas/{id}/documents     # Upload document
GET    /api/v1/ideas/{id}/documents     # List documents
DELETE /api/v1/ideas/{id}/documents/{doc_id}  # Delete document
```

### Authentication Endpoints

```
POST   /api/v1/auth/login               # Login
POST   /api/v1/auth/logout              # Logout
POST   /api/v1/auth/refresh             # Refresh token
GET    /api/v1/auth/me                  # Get current user
```

### Campaign Endpoints

```
GET    /api/v1/campaigns                # List campaigns
GET    /api/v1/campaigns/{id}           # Get campaign details
POST   /api/v1/campaigns                # Create campaign (admin)
PUT    /api/v1/campaigns/{id}           # Update campaign (admin)
DELETE /api/v1/campaigns/{id}           # Delete campaign (admin)
```

---

## 5. Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Backend project setup
- [ ] Frontend project setup
- [ ] Database schema and migrations
- [ ] Authentication system
- [ ] API documentation

### Phase 2: Idea Management (Week 2)
- [ ] Idea submission API
- [ ] Idea listing and filtering
- [ ] Idea detail view
- [ ] Draft management
- [ ] Contributor management

### Phase 3: File Management (Week 2-3)
- [ ] File upload API
- [ ] Virus scanning integration
- [ ] File storage (S3)
- [ ] File download/preview

### Phase 4: Frontend UI (Week 3-4)
- [ ] Login/authentication UI
- [ ] Idea submission form
- [ ] Idea list view
- [ ] Idea detail view
- [ ] My ideas page

### Phase 5: Testing & Deployment (Week 4)
- [ ] Unit tests
- [ ] Integration tests
- [ ] API documentation
- [ ] Docker setup
- [ ] Kubernetes deployment

---

## 6. Testing Strategy

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Target: > 80% code coverage

### Integration Tests
- Test API endpoints
- Test database interactions
- Test service layer

### End-to-End Tests
- Test complete workflows
- Test user interactions
- Test error scenarios

### Test Tools
- Backend: pytest, pytest-django, pytest-cov
- Frontend: Jest, React Testing Library

---

## 7. Code Quality Standards

### Backend
- PEP 8 compliance
- Type hints for all functions
- Docstrings for all modules/classes/functions
- Code review: 100% of code reviewed
- Cyclomatic complexity: < 10

### Frontend
- ESLint compliance
- PropTypes or TypeScript
- JSDoc comments
- Code review: 100% of code reviewed

---

## 8. Documentation

### API Documentation
- OpenAPI/Swagger specification
- Request/response examples
- Error codes and messages
- Authentication details

### Code Documentation
- README with setup instructions
- Architecture documentation
- Database schema documentation
- Deployment guide

---

## 9. Deployment

### Development
- Docker Compose setup
- Local database
- Hot reload enabled

### Staging
- Kubernetes deployment
- AWS RDS database
- Redis cache
- Monitoring enabled

### Production
- Kubernetes deployment
- Multi-AZ database
- Redis cluster
- Full monitoring and alerting

---

## Timeline

- **Week 1**: Backend setup, frontend setup, database, authentication
- **Week 2**: Idea management, file management
- **Week 3**: Frontend UI, additional features
- **Week 4**: Testing, deployment, documentation

**Total Duration**: 4 weeks for complete implementation

---

## Success Criteria

- [ ] All API endpoints implemented and tested
- [ ] Frontend UI complete and responsive
- [ ] Unit test coverage > 80%
- [ ] Integration tests passing
- [ ] API documentation complete
- [ ] Deployment to staging successful
- [ ] Performance targets met (< 1 second response time)
- [ ] Security requirements met (encryption, auth, validation)

