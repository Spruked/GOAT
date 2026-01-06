import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  User,
  Folder,
  FileText,
  Settings,
  Download,
  Palette,
  Moon,
  Sun,
  Upload,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'
import axios from 'axios'

export function ProfilePage() {
  const [activeTab, setActiveTab] = useState('files')
  const [theme, setTheme] = useState('dark')
  const [user, setUser] = useState(null)

  // Get current user info
  const { data: userData } = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const { data } = await axios.get('/api/auth/me')
      return data
    }
  })

  // Get user's files and projects
  const { data: userFiles, isLoading: filesLoading } = useQuery({
    queryKey: ['user-files'],
    queryFn: async () => {
      const { data } = await axios.get('/api/user/files')
      return data
    }
  })

  useEffect(() => {
    if (userData) {
      setUser(userData)
    }
  }, [userData])

  const tabs = [
    { id: 'files', label: 'My Files', icon: Folder },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'downloads', label: 'Downloads', icon: Download }
  ]

  if (!user) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-400">Loading profile...</p>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="goat-card">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 bg-gradient-to-r from-goat-primary to-goat-secondary rounded-full flex items-center justify-center">
            <User className="w-10 h-10 text-slate-900" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">{user.name || user.email}</h1>
            <p className="text-slate-400">{user.email}</p>
            <p className="text-sm text-slate-500 mt-1">
              Member since {new Date(user.signup_date).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="goat-card">
        <div className="flex space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-goat-primary text-slate-900'
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Icon size={18} />
                {tab.label}
              </button>
            )
          })}
        </div>
      </div>

      {/* Tab Content */}
      <div className="goat-card">
        {activeTab === 'files' && <FilesTab files={userFiles} loading={filesLoading} />}
        {activeTab === 'settings' && <SettingsTab theme={theme} setTheme={setTheme} user={user} />}
        {activeTab === 'downloads' && <DownloadsTab />}
      </div>
    </div>
  )
}

function FilesTab({ files, loading }) {
  if (loading) {
    return <div className="text-center py-10">Loading files...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">My Files & Projects</h2>
        <button className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors flex items-center gap-2">
          <Upload size={16} />
          Upload New
        </button>
      </div>

      {/* File Categories */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Processed Files */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <CheckCircle className="text-green-400" size={20} />
            Processed Files
          </h3>
          <div className="space-y-2">
            {files?.processed?.length > 0 ? (
              files.processed.map((file, idx) => (
                <FileItem key={idx} file={file} status="processed" />
              ))
            ) : (
              <p className="text-slate-500 text-sm">No processed files yet</p>
            )}
          </div>
        </div>

        {/* Unprocessed Files */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Clock className="text-yellow-400" size={20} />
            Unprocessed Files
          </h3>
          <div className="space-y-2">
            {files?.unprocessed?.length > 0 ? (
              files.unprocessed.map((file, idx) => (
                <FileItem key={idx} file={file} status="pending" />
              ))
            ) : (
              <p className="text-slate-500 text-sm">No unprocessed files</p>
            )}
          </div>
        </div>
      </div>

      {/* Projects Section */}
      <div className="border-t border-slate-700 pt-6">
        <h3 className="text-lg font-semibold mb-4">Active Projects</h3>
        <div className="grid md:grid-cols-3 gap-4">
          {/* Sample projects - in real app, this would come from API */}
          <ProjectCard
            title="Audiobook: My Story"
            status="processing"
            progress={75}
            type="audiobook"
          />
          <ProjectCard
            title="Course: Advanced Topics"
            status="completed"
            progress={100}
            type="course"
          />
          <ProjectCard
            title="Blog Series"
            status="draft"
            progress={30}
            type="blog"
          />
        </div>
      </div>
    </div>
  )
}

function FileItem({ file, status }) {
  const statusColor = status === 'processed' ? 'text-green-400' : 'text-yellow-400'
  const StatusIcon = status === 'processed' ? CheckCircle : Clock

  return (
    <div className="flex items-center justify-between p-3 bg-slate-700 rounded-lg">
      <div className="flex items-center gap-3">
        <FileText size={16} className="text-slate-400" />
        <div>
          <p className="font-medium">{file.name}</p>
          <p className="text-sm text-slate-400">{file.size} • {file.uploaded}</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <StatusIcon size={16} className={statusColor} />
        <span className={`text-sm ${statusColor}`}>
          {status === 'processed' ? 'Ready' : 'Processing'}
        </span>
      </div>
    </div>
  )
}

function ProjectCard({ title, status, progress, type }) {
  const statusColors = {
    completed: 'text-green-400',
    processing: 'text-blue-400',
    draft: 'text-yellow-400'
  }

  return (
    <div className="bg-slate-700 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-medium">{title}</h4>
        <span className={`text-sm ${statusColors[status]}`}>{status}</span>
      </div>
      <div className="text-sm text-slate-400 mb-3 capitalize">{type}</div>
      <div className="w-full bg-slate-600 rounded-full h-2">
        <div
          className="bg-goat-primary h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="text-xs text-slate-400 mt-1">{progress}% complete</div>
    </div>
  )
}

function SettingsTab({ theme, setTheme, user }) {
  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    marketingEmails: user?.marketing_opt_in || false,
    theme: theme,
    language: 'en'
  })

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({ ...prev, [key]: value }))
    if (key === 'theme') {
      setTheme(value)
    }
  }

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold">Settings & Preferences</h2>

      {/* Theme Settings */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Palette size={20} />
          Appearance
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          <ThemeOption
            icon={<Moon size={24} />}
            title="Dark"
            description="Classic dark theme"
            selected={theme === 'dark'}
            onClick={() => handlePreferenceChange('theme', 'dark')}
          />
          <ThemeOption
            icon={<Sun size={24} />}
            title="Light"
            description="Clean light theme"
            selected={theme === 'light'}
            onClick={() => handlePreferenceChange('theme', 'light')}
          />
          <ThemeOption
            icon={<Palette size={24} />}
            title="Auto"
            description="Follow system"
            selected={theme === 'auto'}
            onClick={() => handlePreferenceChange('theme', 'auto')}
          />
        </div>
      </div>

      {/* Notification Settings */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Notifications</h3>
        <div className="space-y-3">
          <SettingToggle
            label="Email Notifications"
            description="Receive updates about your projects"
            checked={preferences.emailNotifications}
            onChange={(checked) => handlePreferenceChange('emailNotifications', checked)}
          />
          <SettingToggle
            label="Marketing Emails"
            description="Receive news and promotional content"
            checked={preferences.marketingEmails}
            onChange={(checked) => handlePreferenceChange('marketingEmails', checked)}
          />
        </div>
      </div>

      {/* Account Information */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Account Information</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Name</label>
            <input
              type="text"
              value={user?.name || ''}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
              placeholder="Your name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Email</label>
            <input
              type="email"
              value={user?.email || ''}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
              placeholder="your@email.com"
            />
          </div>
        </div>
        <button className="bg-goat-primary text-slate-900 px-6 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors">
          Save Changes
        </button>
      </div>
    </div>
  )
}

function ThemeOption({ icon, title, description, selected, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`p-4 rounded-lg border-2 transition-colors ${
        selected
          ? 'border-goat-primary bg-goat-primary/10'
          : 'border-slate-600 hover:border-slate-500'
      }`}
    >
      <div className="flex flex-col items-center text-center space-y-2">
        {icon}
        <div>
          <h4 className="font-medium">{title}</h4>
          <p className="text-sm text-slate-400">{description}</p>
        </div>
      </div>
    </button>
  )
}

function SettingToggle({ label, description, checked, onChange }) {
  return (
    <div className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
      <div>
        <h4 className="font-medium">{label}</h4>
        <p className="text-sm text-slate-400">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`w-12 h-6 rounded-full transition-colors ${
          checked ? 'bg-goat-primary' : 'bg-slate-600'
        }`}
      >
        <div
          className={`w-5 h-5 bg-white rounded-full transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  )
}

function DownloadsTab() {
  const sampleDownloads = [
    {
      id: 1,
      name: 'My Audiobook - Complete',
      type: 'Audiobook',
      format: 'M4B',
      size: '245 MB',
      status: 'ready',
      created: '2025-11-28'
    },
    {
      id: 2,
      name: 'Course Materials',
      type: 'Course',
      format: 'ZIP',
      size: '89 MB',
      status: 'ready',
      created: '2025-11-25'
    },
    {
      id: 3,
      name: 'Blog Series Draft',
      type: 'Documents',
      format: 'PDF',
      size: '12 MB',
      status: 'processing',
      created: '2025-11-29'
    }
  ]

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">My Downloads</h2>

      <div className="space-y-4">
        {sampleDownloads.map((download) => (
          <div key={download.id} className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-goat-primary/20 rounded-lg flex items-center justify-center">
                <Download size={20} className="text-goat-primary" />
              </div>
              <div>
                <h4 className="font-medium">{download.name}</h4>
                <p className="text-sm text-slate-400">
                  {download.type} • {download.format} • {download.size} • Created {download.created}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {download.status === 'ready' ? (
                <>
                  <CheckCircle size={16} className="text-green-400" />
                  <button className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors">
                    Download
                  </button>
                </>
              ) : (
                <>
                  <Clock size={16} className="text-yellow-400" />
                  <span className="text-yellow-400 text-sm">Processing...</span>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {sampleDownloads.length === 0 && (
        <div className="text-center py-10">
          <Download size={48} className="text-slate-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium mb-2">No downloads yet</h3>
          <p className="text-slate-400">Complete some projects to see your downloads here</p>
        </div>
      )}
    </div>
  )
}
