import { Link, useNavigate } from 'react-router-dom'
import { BookOpen, Database, GraduationCap, Shield, LogIn, LogOut, User } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export function Header() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="bg-slate-800 border-b border-slate-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-r from-goat-primary to-goat-secondary rounded-full flex items-center justify-center font-bold text-xl text-slate-900">
              G
            </div>
            <div>
              <h1 className="text-xl font-bold">GOAT v2.1</h1>
              <p className="text-xs text-slate-400">The Proven Teacher</p>
            </div>
          </Link>
          
          <nav className="flex items-center gap-6">
            {isAuthenticated && (
              <>
                <Link to="/collect" className="flex items-center gap-2 hover:text-goat-primary transition">
                  <Database size={18} />
                  <span>Collect</span>
                </Link>
                <Link to="/learn" className="flex items-center gap-2 hover:text-goat-primary transition">
                  <GraduationCap size={18} />
                  <span>Learn</span>
                </Link>
                <Link to="/vault" className="flex items-center gap-2 hover:text-goat-primary transition">
                  <Shield size={18} />
                  <span>Vault</span>
                </Link>
                <Link to={`/profile/${user?.username}`} className="flex items-center gap-2 hover:text-goat-primary transition">
                  <User size={18} />
                  <span>Profile</span>
                </Link>
              </>
            )}
            
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 hover:text-goat-primary transition"
              >
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            ) : (
              <Link to="/login" className="flex items-center gap-2 hover:text-goat-primary transition">
                <LogIn size={18} />
                <span>Login</span>
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
