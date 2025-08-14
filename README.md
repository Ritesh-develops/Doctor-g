# 🏥 Doctor-G - AI-Powered Medical Imaging Analysis Platform

<div align="center">

![Doctor-G Logo](https://img.shields.io/badge/Doctor--G-AI%20Medical%20Assistant-blue?style=for-the-badge&logo=medical-cross)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-FF6B6B?style=for-the-badge&logo=yolo&logoColor=white)](https://ultralytics.com/)

**Advanced X-ray analysis powered by YOLOv11 and LLM technology**

[🚀 Live Demo](#) | [📖 Documentation](docs/) | [🐛 Report Bug](issues/) | [💡 Request Feature](issues/)


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
- **X-ray Upload & Analysis**: Drag-and-drop X-ray images for instant AI analysis
- **Lung Nodule Detection**: Advanced YOLOv11 model trained specifically for lung abnormalities
- **AI Medical Explanations**: LLM-powered patient-friendly interpretation of results
- **Interactive Chat**: Ask follow-up questions about your X-ray results
- **Conversation History**: Complete medical consultation tracking

### 💼 **User Management**
- **Secure Authentication**: JWT-based login with refresh tokens
- **User Profiles**: Personal medical consultation history
- **Session Management**: Secure, persistent user sessions
- **Data Privacy**: GDPR-compliant data handling

### 📱 **User Experience**
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Updates**: Live chat with instant AI responses
- **File Management**: Secure X-ray image storage and retrieval
- **Dashboard Analytics**: Personal health consultation overview

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
