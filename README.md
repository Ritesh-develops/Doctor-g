# 🏥 Doctor-G - AI-Powered Medical Imaging Analysis Platform

<div align="center">

![Doctor-G Logo](https://img.shields.io/badge/Doctor--G-AI%20Medical%20Assistant-blue?style=for-the-badge&logo=medical-cross)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-FF6B6B?style=for-the-badge)](https://ultralytics.com/)

**Advanced X-ray analysis powered by YOLOv11 and LLM technology**

---

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
## 📊 X-ray Analysis Flow

```mermaid
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
```

#### 🔄 Analysis Pipeline Details
- **📤 Upload Phase**: Secure file handling with validation.
- **🔧 Preprocessing**: Image optimization for the AI model.
- **🎯 Detection**: YOLOv11 identifies potential abnormalities.
- **📊 Analysis**: Confidence scoring and severity assessment.
- **🧠 Interpretation**: LLM generates patient-friendly explanations.
- **💬 Communication**: Interactive chat for follow-up questions.

## 🛠️ Technology Stack

#### Frontend Technologies
- **⚛️ React 18**: Modern UI framework
- **⚡ Vite**: Lightning-fast build tool
- **🎨 TailwindCSS**: Utility-first CSS framework
- **🧭 React Router**: Client-side routing
- **🔄 Context API**: State management
- **📡 Axios**: HTTP client
- **🎯 React Hook Form**: Form handling
- **🔔 React Hot Toast**: Notifications
- **🎨 Lucide React**: Beautiful icons
- **📱 Responsive Design**: Mobile-first approach

#### Backend Technologies
- **🐍 Python 3.12**: Modern Python runtime
- **⚡ FastAPI**: High-performance web framework
- **🗃️ SQLAlchemy 2.0**: Async ORM
- **🔐 JWT Authentication**: Secure token-based auth
- **📊 Pydantic v2**: Data validation
- **🐘 PostgreSQL 15**: Robust relational database
- **⚡ Redis**: High-speed caching
- **📁 Async File Handling**: Non-blocking I/O
- **🔒 bcrypt**: Password hashing

#### AI/ML Stack
- **🤖 YOLOv11**: State-of-the-art object detection
- **🔥 PyTorch 2.1**: Deep learning framework
- **🖼️ OpenCV**: Computer vision operations
- **🎨 Pillow**: Image processing
- **📊 NumPy**: Numerical computing
- **🦙 Groq API (Llama 3 70B)**: Large Language Model
- **🧠 Ultralytics**: YOLO implementation
- **📈 Confidence Scoring**: Prediction reliability

## 🚀 Getting Started

### Prerequisites
Before running Doctor-G, ensure you have the following installed:
```bash
# Backend Requirements
Python 3.12+
PostgreSQL 15+
Redis (optional but recommended)

# Frontend Requirements
Node.js 18+
npm or yarn

# AI/ML Requirements
CUDA-compatible GPU (optional, for faster inference)
```
### 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/doctor-g.git](https://github.com/yourusername/doctor-g.git)
    cd doctor-g
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    
    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Create and configure your environment file
    cp .env.example .env
    # Edit the .env file with your database URL, secret keys, etc.
    
    # Set up the database
    createdb doctorg_db
    alembic upgrade head
    
    # Create a directory for AI models
    mkdir models
    # Add your trained .pt model file to this directory
    
    # Run the backend server
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    
    # Install dependencies
    npm install
    
    # Create and configure your environment file
    cp .env.example .env
    # Edit the .env file to point to your backend API URL
    
    # Run the frontend development server
    npm run dev
    ```
    ## 🔧 Environment Configuration (.env)

For the application to run correctly, you must create and configure environment files for both the backend and frontend. These files store sensitive information like API keys and database URLs and are kept out of version control for security.

---

### Backend Configuration (`/backend/.env`)

The backend requires keys for database access, JWT security, and external services.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create the `.env` file from the template:**
    ```bash
    cp .env.example .env
    ```
    This command copies the example file to a new `.env` file, which is ignored by Git.

3.  **Edit the `.env` file** and add your specific credentials. It will look like this:
    ```env
    # Security: Generate a long, random string for the secret key
    SECRET_KEY=your-very-long-secret-key-here
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_MINUTES=10080

    # Database: Replace with your actual PostgreSQL connection URL
    DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/<database_name>

    # Groq API: Your API key from Groq
    GROQ_API_KEY=your_groq_api_key_here
    GROQ_MODEL='any groq model you want

    # File Upload & Model Paths
    MAX_UPLOAD_SIZE=10485760
    UPLOAD_DIR=uploads
    YOLO_MODEL_PATH=models/lung_nodule_detector.pt

    # CORS: A list of frontend URLs that are allowed to access the backend
    BACKEND_CORS_ORIGINS=["http://localhost:3000","[http://127.0.0.1:3000](http://127.0.0.1:3000)"]
    ```

---

### Frontend Configuration (`/frontend/.env`)

The frontend needs to know the URL of your backend API.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Create the `.env` file from the template:**
    ```bash
    cp .env.example .env
    ```

3.  **Edit the `.env` file** to point to your running backend server's URL.
    ```env
    # This must be the full URL where your backend is running
    VITE_API_URL=http://localhost:8000
    ```

---

### 🔒 Security Note
Your `.env` files contain sensitive information. The `.gitignore` file is already configured to ignore these files, so you will never accidentally commit them to your repository. **Never share your `.env` files or commit them to version control.**
   ## 📈 Performance

#### Benchmarks
- **X-ray Analysis**: < 3 seconds average processing time
- **API Response**: < 200ms for most endpoints
- **Model Inference**: < 1 second for YOLOv11 detection
- **Database Queries**: < 50ms average response time

#### Optimization Features
- **Async Processing**: Non-blocking I/O operations in FastAPI.
- **Model Caching**: Pre-loaded AI models for faster inference.
- **Database Indexing**: Optimized queries with proper indexing.
- **Redis Caching**: Session and API response caching.

---

## 🔒 Security

#### Security Features
- **JWT Authentication**: Secure token-based authentication.
- **Password Hashing**: `bcrypt` for secure password storage.
- **Input Validation**: Comprehensive data validation with Pydantic.
- **File Upload Security**: Restricted file types and size limits.
- **CORS Configuration**: Controlled cross-origin requests.
- **Rate Limiting**: API rate limiting to prevent abuse.

#### Medical Data Compliance
- **HIPAA Ready**: Architecture designed for HIPAA compliance.
- **Data Encryption**: Encrypted data storage and transmission.
- **Access Logging**: Complete audit trail for medical data access.
- **Secure File Storage**: Protected X-ray image storage.

---

<h3 align="center">🏥 Doctor-G - Making Medical AI Accessible to Everyone</h3>



