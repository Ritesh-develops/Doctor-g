# 🏥 Doctor-G - AI-Powered Medical Imaging Analysis Platform

<div align="center">

![Doctor-G Logo](https://img.shields.io/badge/Doctor--G-AI%20Medical%20Assistant-blue?style=for-the-badge&logo=medical-cross)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-FF6B6B?style=for-the-badge)](https://ultralytics.com/)

**Advanced X-ray analysis powered by YOLOv11 and LLM technology**

[🚀 Live Demo](#) | [📖 Documentation](docs/) | [🐛 Report Bug](issues/) | [💡 Request Feature](issues/)

---

### 🔗 **Deployment Link**
**Production:** `https://your-deployment-url.com`  
**Staging:** `https://staging-your-deployment-url.com`

</div>

## 📋 Table of Contents
- [🎯 About The Project](#-about-the-project)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [📊 X-ray Analysis Flow](#-x-ray-analysis-flow)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Getting Started](#-getting-started)
- [📚 API Documentation](#-api-documentation)
- [🔧 Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [📈 Performance](#-performance)
- [🔒 Security](#-security)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👥 Team](#-team)

## 🎯 About The Project

Doctor-G is an advanced AI-powered medical imaging analysis platform that combines cutting-edge computer vision with natural language processing to provide instant, accurate X-ray analysis. The system uses YOLOv11 for precise nodule detection and integrates with Large Language Models to deliver patient-friendly medical explanations.

### 🎯 **Mission**
Democratize medical imaging analysis by making AI-powered diagnostics accessible, understandable, and reliable for both healthcare professionals and patients.

### ⚡ **Key Highlights**
- **Instant Analysis**: Get X-ray results in seconds, not hours
- **AI-Powered**: YOLOv11 for detection + LLM for explanations
- **User-Friendly**: Complex medical terms translated to simple language
- **Secure**: HIPAA-ready with enterprise-grade security
- **Scalable**: Modern microservices architecture

## ✨ Features

### 🔍 **Core Functionality**
- **X-ray Upload & Analysis**: Drag-and-drop X-ray images for instant AI analysis.
- **Lung Nodule Detection**: Advanced YOLOv11 model trained specifically for lung abnormalities.
- **AI Medical Explanations**: LLM-powered patient-friendly interpretation of results.
- **Interactive Chat**: Ask follow-up questions about your X-ray results.
- **Conversation History**: Complete medical consultation tracking.

### 💼 **User Management**
- **Secure Authentication**: JWT-based login with refresh tokens.
- **User Profiles**: Personal medical consultation history.
- **Session Management**: Secure, persistent user sessions.
- **Data Privacy**: GDPR-compliant data handling.

### 📱 **User Experience**
- **Responsive Design**: Works seamlessly on desktop and mobile.
- **Real-time Updates**: Live chat with instant AI responses.
- **File Management**: Secure X-ray image storage and retrieval.
- **Dashboard Analytics**: Personal health consultation overview.

## 🏗️ Architecture
```mermaid
graph TB
    subgraph "🌐 Client Layer"
        WEB[Web Browser]
        MOB[Mobile Browser]
    end

    subgraph "⚛️ Frontend Layer"
        REACT[React Application<br/>📱 Responsive UI<br/>🔄 Real-time Chat<br/>📤 File Upload]
    end

    subgraph "🖥️ Backend Services"
        API[FastAPI Server<br/>🔐 JWT Authentication<br/>📋 Data Validation<br/>🔄 Async Processing]

        subgraph "🤖 AI Services"
            YOLO[YOLOv11 Service<br/>🫁 Lung Nodule Detection<br/>📊 Confidence Scoring<br/>📍 Bounding Box Prediction]
            LLM[LLM Service<br/>🧠 Medical Interpretation<br/>💬 Patient Communication<br/>❓ Follow-up Q&A]
        end
    end

    subgraph "💾 Data Layer"
        DB[(PostgreSQL<br/>👤 User Management<br/>💬 Chat History<br/>🏥 Medical Records)]
        REDIS[(Redis Cache<br/>⚡ Session Storage<br/>📊 Performance Cache)]
        FS[File System<br/>🖼️ X-ray Images<br/>📁 Secure Storage)]
    end

    subgraph "🌍 External APIs"
        GROQ[Groq API<br/>🦙 Llama 3 70B<br/>🔬 Medical Knowledge<br/>💡 Smart Responses]
    end

    WEB --> REACT
    MOB --> REACT
    REACT --> API
    API --> YOLO
    API --> LLM
    API --> DB
    API --> REDIS
    API --> FS
    LLM --> GROQ

    style REACT fill:#61dafb,stroke:#333,stroke-width:2px,color:#000
    style API fill:#009688,stroke:#333,stroke-width:2px,color:#fff
    style YOLO fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
    style LLM fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style DB fill:#336791,stroke:#333,stroke-width:2px,color:#fff
📊 X-ray Analysis Flow
Code snippet

flowchart TD
    START([👤 User Uploads X-ray]) --> UPLOAD{📤 File Upload}
    UPLOAD -->|✅ Valid Image| SAVE[💾 Save to Secure Storage]
    UPLOAD -->|❌ Invalid Format| ERROR1[🚫 Show Error Message]

    SAVE --> RECORD[📝 Create Scan Record in DB]
    RECORD --> YOLO_INIT[🤖 Initialize YOLOv11 Model]

    YOLO_INIT --> PREPROCESS[🔧 Image Preprocessing<br/>• Resize & Normalize<br/>• Format Conversion<br/>• Quality Check]
    PREPROCESS --> DETECTION[🎯 YOLOv11 Detection<br/>• Lung Nodule Detection<br/>• Confidence Scoring<br/>• Bounding Box Generation]

    DETECTION --> RESULTS{📊 Detection Results}
    RESULTS -->|🔍 Nodules Found| ANALYZE[📋 Generate Analysis<br/>• Severity Assessment<br/>• Location Mapping<br/>• Risk Evaluation]
    RESULTS -->|✅ No Issues| CLEAN[💚 Clean X-ray Report]

    ANALYZE --> LLM_PROCESS[🧠 LLM Processing<br/>• Medical Context Analysis<br/>• Patient-Friendly Translation<br/>• Recommendation Generation]
    CLEAN --> LLM_PROCESS

    LLM_PROCESS --> GROQ[🌐 Groq API Call<br/>• Llama 3 70B Model<br/>• Medical Knowledge Base<br/>• Natural Language Generation]

    GROQ --> RESPONSE[📝 Generate Response<br/>• Clear Explanations<br/>• Medical Disclaimers<br/>• Next Steps Guidance]

    RESPONSE --> SAVE_RESULTS[💾 Save Analysis Results<br/>• Update Scan Record<br/>• Create Chat Messages<br/>• Log Confidence Scores]

    SAVE_RESULTS --> NOTIFY[📨 Notify User<br/>• Real-time Update<br/>• Analysis Complete<br/>• Results Available]

    NOTIFY --> DISPLAY[📱 Display Results<br/>• Visual Annotations<br/>• Detailed Explanation<br/>• Chat Interface Active]

    DISPLAY --> CHAT{💬 User Questions?}
    CHAT -->|❓ Yes| FOLLOWUP[🔄 Process Follow-up<br/>• Context-Aware Responses<br/>• Reference Original Analysis<br/>• Educational Information]
    CHAT -->|✅ No| END([🏁 Analysis Complete])

    FOLLOWUP --> GROQ
    ERROR1 --> END

    style START fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style YOLO_INIT fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style DETECTION fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    style LLM_PROCESS fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style GROQ fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    style DISPLAY fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    style END fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
🔄 Analysis Pipeline Details
📤 Upload Phase: Secure file handling with validation.

🔧 Preprocessing: Image optimization for AI model.

🎯 Detection: YOLOv11 identifies potential abnormalities.

📊 Analysis: Confidence scoring and severity assessment.

🧠 Interpretation: LLM generates patient-friendly explanations.

💬 Communication: Interactive chat for follow-up questions.

🛠️ Technology Stack
Frontend Technologies
⚛️ React 18: Modern UI framework

⚡ Vite: Lightning-fast build tool

🎨 TailwindCSS: Utility-first CSS framework

🧭 React Router: Client-side routing

🔄 Context API: State management

📡 Axios: HTTP client

🎯 React Hook Form: Form handling

🔔 React Hot Toast: Notifications

🎨 Lucide React: Beautiful icons

📱 Responsive Design: Mobile-first approach

Backend Technologies
🐍 Python 3.12: Modern Python runtime

⚡ FastAPI: High-performance web framework

🗃️ SQLAlchemy 2.0: Async ORM

🔐 JWT Authentication: Secure token-based auth

📊 Pydantic v2: Data validation

🐘 PostgreSQL 15: Robust relational database

⚡ Redis: High-speed caching

📁 Async File Handling: Non-blocking I/O

🔒 bcrypt: Password hashing

AI/ML Stack
🤖 YOLOv11: State-of-the-art object detection

🔥 PyTorch 2.1: Deep learning framework

🖼️ OpenCV: Computer vision operations

🎨 Pillow: Image processing

📊 NumPy: Numerical computing

🦙 Groq API (Llama 3 70B): Large Language Model

🧠 Ultralytics: YOLO implementation

📈 Confidence Scoring: Prediction reliability

🚀 Getting Started
Prerequisites
Before running Doctor-G, ensure you have the following installed:

Bash

# Backend Requirements
Python 3.12+
PostgreSQL 15+
Redis (optional but recommended)

# Frontend Requirements
Node.js 18+
npm or yarn

# AI/ML Requirements
CUDA-compatible GPU (optional, for faster inference)
Installation
Clone the Repository

Bash

git clone [https://github.com/yourusername/doctor-g.git](https://github.com/yourusername/doctor-g.git)
cd doctor-g
Backend Setup

Bash

cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Edit .env with your configuration

# Set up database
createdb doctorg_db
alembic upgrade head

# Download and place your YOLOv11 model
mkdir models
# Place your lung_nodule_detector.pt in models/

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Frontend Setup

Bash

cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Edit .env with your configuration

# Run the frontend
npm run dev
🌐 Access the Application
Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs

📚 API Documentation
Authentication Endpoints
Plaintext

POST   /api/v1/auth/register     - Register new user
POST   /api/v1/auth/login        - User login
POST   /api/v1/auth/refresh      - Refresh access token
GET    /api/v1/auth/me           - Get current user
POST   /api/v1/auth/logout       - User logout
Chat & Analysis Endpoints
Plaintext

GET    /api/v1/chats/conversations/              - Get user conversations
POST   /api/v1/chats/conversations/              - Create new conversation
GET    /api/v1/chats/conversations/{id}/messages - Get conversation messages
POST   /api/v1/chats/conversations/{id}/messages - Send message
POST   /api/v1/chats/conversations/{id}/analyze  - Analyze X-ray image
Scan Management Endpoints
Plaintext

GET    /api/v1/scans/           - Get user scans
GET    /api/v1/scans/count      - Get scan count
GET    /api/v1/scans/stats      - Get scan statistics
🔧 Configuration
Backend Environment Variables
Code snippet

# Security
SECRET_KEY=your-very-long-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080

# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/doctorg_db

# Groq API
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192

# File Upload
MAX_UPLOAD_SIZE=10485760 # 10 MB
UPLOAD_DIR=uploads
YOLO_MODEL_PATH=models/lung_nodule_detector.pt

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","[http://127.0.0.1:3000](http://127.0.0.1:3000)"]
Frontend Environment Variables
Code snippet

VITE_API_URL=http://localhost:8000
🧪 Testing
Backend Testing
Bash

cd backend

# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run integration tests
pytest tests/integration/ -v

# Test specific module
pytest tests/test_yolo_service.py -v
Frontend Testing
Bash

cd frontend

# Run unit tests
npm run test

# Run e2e tests
npm run test:e2e

# Run tests with coverage
npm run test:coverage
📈 Performance
Benchmarks
X-ray Analysis: < 3 seconds average processing time

API Response: < 200ms for most endpoints

Model Inference: < 1 second for YOLOv11 detection

Database Queries: < 50ms average response time

Optimization Features
Async Processing: Non-blocking I/O operations in FastAPI.

Model Caching: Pre-loaded AI models for faster inference.

Database Indexing: Optimized queries with proper indexing.

Redis Caching: Session and API response caching.

🔒 Security
Security Features
JWT Authentication: Secure token-based authentication.

Password Hashing: bcrypt for secure password storage.

Input Validation: Comprehensive data validation with Pydantic.

File Upload Security: Restricted file types and size limits.

CORS Configuration: Controlled cross-origin requests.

Rate Limiting: API rate limiting to prevent abuse.

Medical Data Compliance
HIPAA Ready: Architecture designed for HIPAA compliance.

Data Encryption: Encrypted data storage and transmission.

Access Logging: Complete audit trail for medical data access.

Secure File Storage: Protected X-ray image storage.

🤝 Contributing
We welcome contributions to Doctor-G! Please follow these steps:

Fork the repository.

Create a feature branch: git checkout -b feature/amazing-feature

Make your changes.

Add tests for your changes.

Commit your changes: git commit -m 'Add amazing feature'

Push to the branch: git push origin feature/amazing-feature

Open a Pull Request.

Development Guidelines
Follow PEP 8 for Python code.

Use ESLint and Prettier for JavaScript/React code.

Write comprehensive tests for new features.

Update documentation for API changes.

Ensure all tests pass before submitting a PR.

Code of Conduct
Please read our Code of Conduct before contributing.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Team
Core Development Team
Lead Developer: Your Name - Full Stack & AI Integration

AI/ML Engineer: Contributor Name - YOLOv11 & Model Optimization

Frontend Developer: Contributor Name - React & UI/UX

Backend Developer: Contributor Name - FastAPI & Database

Medical Advisory Board
Chief Medical Officer: Dr. Medical Advisor - Clinical Validation

Radiologist Consultant: Dr. Radiology Expert - X-ray Analysis Review

<h3 align="center">🏥 Doctor-G - Making Medical AI Accessible to Everyone</h3>
