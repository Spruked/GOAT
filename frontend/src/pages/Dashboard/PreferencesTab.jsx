import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Palette,
  Sun,
  Moon,
  Monitor,
  User,
  Bell,
  Shield,
  Download,
  Trash2,
  Save,
  Eye,
  EyeOff
} from 'lucide-react'
import axios from 'axios'

export function PreferencesTab({ user, theme, setTheme }) {
  const [preferences, setPreferences] = useState({
    sidebar_collapsed: false,
    notifications: true,
    auto_preview: true,
    default_download_format: 'pdf'
  })
  const [profileData, setProfileData] = useState({
    display_name: user?.display_name || '',
    username: user?.username || '',
    bio: user?.bio || '',
    email: user?.email || ''
  })
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const queryClient = useQueryClient()

  // Update preferences mutation
  const updatePreferencesMutation = useMutation({
    mutationFn: async (prefs) => {
      const { data } = await axios.post('/api/user/preferences', prefs)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-profile'])
    }
  })

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async (profile) => {
      const { data } = await axios.patch('/api/user/profile', profile)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-profile'])
    }
  })

  useEffect(() => {
    if (user?.preferences) {
      setPreferences(user.preferences)
    }
    if (user) {
      setProfileData({
        display_name: user.display_name || '',
        username: user.username || '',
        bio: user.bio || '',
        email: user.email || ''
      })
    }
  }, [user])

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({ ...prev, [key]: value }))
  }

  const handleProfileChange = (key, value) => {
    setProfileData(prev => ({ ...prev, [key]: value }))
  }

  const savePreferences = () => {
    updatePreferencesMutation.mutate(preferences)
  }

  const saveProfile = () => {
    updateProfileMutation.mutate(profileData)
  }

  const themeOptions = [
    {
      id: 'dark',
      name: 'Dark',
      description: 'Classic dark theme',
      icon: Moon,
      preview: 'bg-slate-900 text-white'
    },
    {
      id: 'light',
      name: 'Light',
      description: 'Clean light theme',
      icon: Sun,
      preview: 'bg-white text-slate-900'
    },
    {
      id: 'auto',
      name: 'Auto',
      description: 'Follow system preference',
      icon: Monitor,
      preview: 'bg-gradient-to-r from-slate-900 to-white'
    }
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Preferences</h1>
        <p className="text-slate-400 mt-1">Customize your GOAT experience</p>
      </div>

      {/* Appearance Settings */}
      <div className="goat-card">
        <div className="flex items-center space-x-2 mb-6">
          <Palette className="text-goat-primary" size={20} />
          <h2 className="text-xl font-bold">Appearance</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-4">Theme</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {themeOptions.map((option) => {
                const Icon = option.icon
                return (
                  <button
                    key={option.id}
                    onClick={() => setTheme(option.id)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      theme === option.id
                        ? 'border-goat-primary bg-goat-primary/10'
                        : 'border-slate-600 hover:border-slate-500'
                    }`}
                  >
                    <div className="flex flex-col items-center space-y-3">
                      <div className={`w-12 h-12 rounded-lg ${option.preview} flex items-center justify-center`}>
                        <Icon size={24} className={theme === option.id ? 'text-goat-primary' : 'text-slate-400'} />
                      </div>
                      <div className="text-center">
                        <h4 className="font-medium">{option.name}</h4>
                        <p className="text-sm text-slate-400">{option.description}</p>
                      </div>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">UI Preferences</h3>
            <div className="space-y-4">
              <PreferenceToggle
                label="Collapsed Sidebar"
                description="Keep the sidebar collapsed by default"
                checked={preferences.sidebar_collapsed}
                onChange={(checked) => handlePreferenceChange('sidebar_collapsed', checked)}
              />
              <PreferenceToggle
                label="Auto Preview"
                description="Automatically show previews for files"
                checked={preferences.auto_preview}
                onChange={(checked) => handlePreferenceChange('auto_preview', checked)}
              />
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={savePreferences}
            disabled={updatePreferencesMutation.isLoading}
            className="bg-goat-primary text-slate-900 px-6 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors disabled:opacity-50"
          >
            <Save size={16} className="mr-2" />
            Save Appearance
          </button>
        </div>
      </div>

      {/* Profile Settings */}
      <div className="goat-card">
        <div className="flex items-center space-x-2 mb-6">
          <User className="text-goat-primary" size={20} />
          <h2 className="text-xl font-bold">Profile</h2>
        </div>

        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Display Name</label>
              <input
                type="text"
                value={profileData.display_name}
                onChange={(e) => handleProfileChange('display_name', e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
                placeholder="Your display name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Username</label>
              <input
                type="text"
                value={profileData.username}
                onChange={(e) => handleProfileChange('username', e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
                placeholder="@username"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Email</label>
            <input
              type="email"
              value={profileData.email}
              onChange={(e) => handleProfileChange('email', e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Bio</label>
            <textarea
              value={profileData.bio}
              onChange={(e) => handleProfileChange('bio', e.target.value)}
              rows={3}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary resize-none"
              placeholder="Tell us about yourself..."
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={saveProfile}
            disabled={updateProfileMutation.isLoading}
            className="bg-goat-primary text-slate-900 px-6 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors disabled:opacity-50"
          >
            <Save size={16} className="mr-2" />
            Save Profile
          </button>
        </div>
      </div>

      {/* Notification Settings */}
      <div className="goat-card">
        <div className="flex items-center space-x-2 mb-6">
          <Bell className="text-goat-primary" size={20} />
          <h2 className="text-xl font-bold">Notifications</h2>
        </div>

        <div className="space-y-4">
          <PreferenceToggle
            label="Email Notifications"
            description="Receive updates about your files and products"
            checked={preferences.notifications}
            onChange={(checked) => handlePreferenceChange('notifications', checked)}
          />
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={savePreferences}
            disabled={updatePreferencesMutation.isLoading}
            className="bg-goat-primary text-slate-900 px-6 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors disabled:opacity-50"
          >
            <Save size={16} className="mr-2" />
            Save Notifications
          </button>
        </div>
      </div>

      {/* Downloads Settings */}
      <div className="goat-card">
        <div className="flex items-center space-x-2 mb-6">
          <Download className="text-goat-primary" size={20} />
          <h2 className="text-xl font-bold">Downloads</h2>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Default Download Format</label>
            <select
              value={preferences.default_download_format}
              onChange={(e) => handlePreferenceChange('default_download_format', e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary"
            >
              <option value="pdf">PDF</option>
              <option value="docx">Word Document</option>
              <option value="png">PNG Image</option>
              <option value="jpg">JPG Image</option>
            </select>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={savePreferences}
            disabled={updatePreferencesMutation.isLoading}
            className="bg-goat-primary text-slate-900 px-6 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors disabled:opacity-50"
          >
            <Save size={16} className="mr-2" />
            Save Downloads
          </button>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="goat-card border-red-500/30">
        <div className="flex items-center space-x-2 mb-6">
          <Shield className="text-red-400" size={20} />
          <h2 className="text-xl font-bold text-red-400">Danger Zone</h2>
        </div>

        <div className="space-y-4">
          <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <h3 className="font-semibold text-red-400 mb-2">Export Your Data</h3>
            <p className="text-sm text-slate-400 mb-4">
              Download a copy of all your data, including files, settings, and activity history.
            </p>
            <button className="bg-slate-700 text-slate-300 px-4 py-2 rounded-lg hover:bg-slate-600 transition-colors">
              <Download size={16} className="mr-2" />
              Export Data
            </button>
          </div>

          {!showDeleteConfirm ? (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
              <h3 className="font-semibold text-red-400 mb-2">Delete Account</h3>
              <p className="text-sm text-slate-400 mb-4">
                Permanently delete your account and all associated data. This action cannot be undone.
              </p>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
              >
                <Trash2 size={16} className="mr-2" />
                Delete Account
              </button>
            </div>
          ) : (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
              <h3 className="font-semibold text-red-400 mb-2">Confirm Account Deletion</h3>
              <p className="text-sm text-slate-400 mb-4">
                Are you sure you want to delete your account? This will permanently remove all your files, settings, and data.
              </p>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="bg-slate-700 text-slate-300 px-4 py-2 rounded-lg hover:bg-slate-600 transition-colors"
                >
                  Cancel
                </button>
                <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
                  <Trash2 size={16} className="mr-2" />
                  Yes, Delete My Account
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function PreferenceToggle({ label, description, checked, onChange }) {
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