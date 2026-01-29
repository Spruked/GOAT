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
  Network,
  Mail,
  BookOpen,
  Mic,
  Headphones,
  Cpu,
  Database,
  Search,
  BarChart3,
  CreditCard,
  Award,
  Zap
} from 'lucide-react'
import axios from 'axios'

// Import dashboard components
import { DashboardLayout } from './DashboardLayout'
import { HomeTab } from './HomeTab'
import { FilesTab } from './FilesTab'
import { ProductsTab } from './ProductsTab'
import { PreferencesTab } from './PreferencesTab'
import { ProfileTab } from './ProfileTab'
import { UsersTab } from './UsersTab'
import { MarketingTab } from './MarketingTab'
import { AudiobooksTab } from './AudiobooksTab'
import { BooksTab } from './BooksTab'
import { PodcastsTab } from './PodcastsTab'
import { VoiceTab } from './VoiceTab'
import { DistillersTab } from './DistillersTab'
import { CollectorsTab } from './CollectorsTab'
import { GOATFieldTab } from './GOATFieldTab'
import { AnalyticsTab } from './AnalyticsTab'
import { PaymentsTab } from './PaymentsTab'
import { CertificatesTab } from './CertificatesTab'

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
    { id: 'profile', label: 'Profile', icon: User },
    ...(user?.isAdmin ? [
      { id: 'users', label: 'Users', icon: User },
      { id: 'marketing', label: 'Marketing', icon: Mail },
      { id: 'audiobooks', label: 'Audiobooks', icon: Headphones },
      { id: 'books', label: 'Books', icon: BookOpen },
      { id: 'podcasts', label: 'Podcasts', icon: Mic },
      { id: 'voice', label: 'Voice Systems', icon: Cpu },
      { id: 'distillers', label: 'Distillers', icon: Database },
      { id: 'collectors', label: 'Collectors', icon: Search },
      { id: 'goat-field', label: 'GOAT Field', icon: Zap },
      { id: 'analytics', label: 'Analytics', icon: BarChart3 },
      { id: 'payments', label: 'Payments', icon: CreditCard },
      { id: 'certificates', label: 'Certificates', icon: Award }
    ] : [])
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
      {activeTab === 'users' && user?.isAdmin && <UsersTab user={user} />}
      {activeTab === 'marketing' && user?.isAdmin && <MarketingTab user={user} />}
      {activeTab === 'audiobooks' && user?.isAdmin && <AudiobooksTab user={user} />}
      {activeTab === 'books' && user?.isAdmin && <BooksTab user={user} />}
      {activeTab === 'podcasts' && user?.isAdmin && <PodcastsTab user={user} />}
      {activeTab === 'voice' && user?.isAdmin && <VoiceTab user={user} />}
      {activeTab === 'distillers' && user?.isAdmin && <DistillersTab user={user} />}
      {activeTab === 'collectors' && user?.isAdmin && <CollectorsTab user={user} />}
      {activeTab === 'goat-field' && user?.isAdmin && <GOATFieldTab user={user} />}
      {activeTab === 'analytics' && user?.isAdmin && <AnalyticsTab user={user} />}
      {activeTab === 'payments' && user?.isAdmin && <PaymentsTab user={user} />}
      {activeTab === 'certificates' && user?.isAdmin && <CertificatesTab user={user} />}
    </DashboardLayout>
  )
}