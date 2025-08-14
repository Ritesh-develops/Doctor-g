# 🏥 Doctor-G - AI-Powered Medical Imaging Analysis Platform

<div align="center">

![Doctor-G Logo](https://img.shields.io/badge/Doctor--G-AI%20Medical%20Assistant-blue?style=for-the-badge&logo=medical-cross)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-FF6B6B?style=for-the-badge)](https://ultralytics.com/)

**Advanced X-ray analysis powered by YOLOv11 and LLM technology**
[📖 Documentation](docs/) | [🐛 Report Bug](issues/) | [💡 Request Feature](issues/)

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
