import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Header } from './components/Header'
import { HomePage } from './pages/HomePage'
import { CollectorPage } from './pages/CollectorPage'
import { TeacherPage } from './pages/TeacherPage'
import { VaultPage } from './pages/VaultPage'
import { ProfilePage } from './pages/ProfilePage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-900 text-white">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/collect" element={<CollectorPage />} />
            <Route path="/learn" element={<TeacherPage />} />
            <Route path="/vault" element={<VaultPage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
