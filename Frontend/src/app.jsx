import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ChatPage from './pages/ChatPage'
import HistoryPage from './pages/HistoryPage'

function App() {
  const { user, loading } = useAuth()

  // 🔥 DEVELOPMENT MODE - Remove auth guards
  const DEVELOPMENT_MODE = true // Set to false when backend is ready

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="pt-16">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <LoginPage />} 
          />
          <Route 
            path="/dashboard" 
            element={DEVELOPMENT_MODE ? <DashboardPage /> : (user ? <DashboardPage /> : <Navigate to="/login" />)} 
          />
          <Route 
            path="/chat" 
            element={DEVELOPMENT_MODE ? <ChatPage /> : (user ? <ChatPage /> : <Navigate to="/login" />)} 
          />
          <Route 
            path="/chat/:conversationId" 
            element={DEVELOPMENT_MODE ? <ChatPage /> : (user ? <ChatPage /> : <Navigate to="/login" />)} 
          />
          <Route 
            path="/history" 
            element={DEVELOPMENT_MODE ? <HistoryPage /> : (user ? <HistoryPage /> : <Navigate to="/login" />)} 
          />
        </Routes>
      </main>
    </div>
  )
}

export default App