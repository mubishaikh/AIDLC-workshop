import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Layout from './components/common/Layout'
import ProtectedRoute from './components/auth/ProtectedRoute'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import SubmitIdeaPage from './pages/SubmitIdeaPage'
import MyIdeasPage from './pages/MyIdeasPage'
import IdeaDetailPage from './pages/IdeaDetailPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  const { isAuthenticated } = useSelector((state) => state.auth)

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        
        <Route
          path="/submit"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <SubmitIdeaPage />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/my-ideas"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <MyIdeasPage />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/ideas/:id"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <IdeaDetailPage />
            </ProtectedRoute>
          }
        />
        
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App
