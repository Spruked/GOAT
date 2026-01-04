import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { Header } from './components/Header'
import { ProtectedRoute } from './components/ProtectedRoute'
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { SignupPage } from './pages/SignupPage'
import { CollectorPage } from './pages/CollectorPage'
import { TeacherPage } from './pages/TeacherPage'
import { VaultPage } from './pages/VaultPage'
import { ProfilePage } from './pages/ProfilePage'
import { VaultForgePage } from './pages/VaultForgePage'

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-slate-900 text-white">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/collect" element={
                <ProtectedRoute>
                  <CollectorPage />
                </ProtectedRoute>
              } />
              <Route path="/learn" element={
                <ProtectedRoute>
                  <TeacherPage />
                </ProtectedRoute>
              } />
              <Route path="/vault" element={
                <ProtectedRoute>
                  <VaultPage />
                </ProtectedRoute>
              } />
              <Route path="/vault-forge" element={
                <ProtectedRoute>
                  <VaultForgePage />
                </ProtectedRoute>
              } />
              <Route path="/profile/:username" element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
