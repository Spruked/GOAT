import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  User,
  Folder,
  FileText,
  Settings,
  Download,
  Upload,
  LogOut,
  Menu,
  X,
  Sun,
  Moon,
  Palette,
  Network
} from 'lucide-react'
import axios from 'axios'

// Import dashboard components
import { DashboardLayout } from './DashboardLayout'
import { HomeTab } from './HomeTab'
import { FilesTab } from './FilesTab'
import { ProductsTab } from './ProductsTab'
import { PreferencesTab } from './PreferencesTab'
import { ProfileTab } from './ProfileTab'

export function Dashboard() {
  const [activeTab, setActiveTab] = useState('home')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [theme, setTheme] = useState('dark')
  const navigate = useNavigate()

  // Get current user
  const { data: user, isLoading: userLoading } = useQuery({
    queryKey: ['user-profile'],
    queryFn: async () => {
      const { data } = await axios.get('/api/user/profile')
      return data
    },
    onError: () => {
      // If not authenticated, redirect to login
      navigate('/login')
    }
  })

  // Get user files stats
  const { data: filesData } = useQuery({
    queryKey: ['user-files-stats'],
    queryFn: async () => {
      const { data } = await axios.get('/api/user/files?limit=1')
      return data.stats
    },
    enabled: !!user
  })

  const tabs = [
    { id: 'home', label: 'Home', icon: User },
    { id: 'files', label: 'Files', icon: Folder },
    { id: 'products', label: 'Products', icon: Download },
    { id: 'graph-demo', label: 'Knowledge Graphs', icon: Network },
    { id: 'preferences', label: 'Preferences', icon: Settings },
    { id: 'profile', label: 'Profile', icon: User }
  ]

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout')
      navigate('/login')
    } catch (error) {
      // Even if logout fails, clear local state
      navigate('/login')
    }
  }

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    document.documentElement.className = newTheme
  }

  useEffect(() => {
    // Set initial theme
    document.documentElement.className = theme
  }, [theme])

  if (userLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-goat-primary"></div>
      </div>
    )
  }

  if (!user) {
    return null // Will redirect in useQuery onError
  }

  return (
    <DashboardLayout
      user={user}
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      tabs={tabs}
      sidebarOpen={sidebarOpen}
      setSidebarOpen={setSidebarOpen}
      theme={theme}
      toggleTheme={toggleTheme}
      onLogout={handleLogout}
      filesStats={filesData}
    >
      {activeTab === 'home' && <HomeTab user={user} filesStats={filesData} />}
      {activeTab === 'files' && <FilesTab user={user} />}
      {activeTab === 'products' && <ProductsTab user={user} />}
      {activeTab === 'graph-demo' && (
        <div className="space-y-6">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Network className="text-goat-primary" />
              Knowledge Graph Demo
            </h2>
            <p className="text-gray-300 mb-4">
              Explore interactive visualizations of concepts, characters, and story relationships.
            </p>
            <button
              onClick={() => navigate('/graph-demo')}
              className="bg-goat-primary hover:bg-goat-primary/80 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Launch Graph Demo
            </button>
          </div>
        </div>
      )}
      {activeTab === 'preferences' && <PreferencesTab user={user} theme={theme} setTheme={setTheme} />}
      {activeTab === 'profile' && <ProfileTab user={user} />}
    </DashboardLayout>
  )
}