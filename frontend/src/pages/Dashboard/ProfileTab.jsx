import { useState, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  User,
  Camera,
  Save,
  X,
  Check,
  Calendar,
  FileText,
  Star,
  TrendingUp
} from 'lucide-react'
import axios from 'axios'

export function ProfileTab({ user }) {
  const [editMode, setEditMode] = useState(false)
  const [profileData, setProfileData] = useState({
    display_name: user?.display_name || '',
    username: user?.username || '',
    bio: user?.bio || '',
    profile_image: user?.profile_image || '/defaults/avatar-goat.png',
    cover_image: user?.cover_image || null
  })
  const fileInputRef = useRef(null)
  const queryClient = useQueryClient()

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async (profile) => {
      const { data } = await axios.patch('/api/user/profile', profile)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-profile'])
      setEditMode(false)
    }
  })

  const handleInputChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }))
  }

  const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      // In a real app, you'd upload to a server and get back a URL
      const reader = new FileReader()
      reader.onload = (e) => {
        handleInputChange('profile_image', e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const saveProfile = () => {
    updateProfileMutation.mutate(profileData)
  }

  const cancelEdit = () => {
    setProfileData({
      display_name: user?.display_name || '',
      username: user?.username || '',
      bio: user?.bio || '',
      profile_image: user?.profile_image || '/defaults/avatar-goat.png',
      cover_image: user?.cover_image || null
    })
    setEditMode(false)
  }

  return (
    <div className="space-y-8">
      {/* Profile Header */}
      <div className="goat-card">
        {/* Cover Image */}
        <div className="h-32 bg-gradient-to-r from-goat-primary to-goat-secondary rounded-t-lg relative overflow-hidden">
          {profileData.cover_image && (
            <img
              src={profileData.cover_image}
              alt="Cover"
              className="w-full h-full object-cover"
            />
          )}
          {editMode && (
            <button className="absolute top-4 right-4 bg-slate-800/80 text-white p-2 rounded-lg hover:bg-slate-700/80 transition-colors">
              <Camera size={16} />
            </button>
          )}
        </div>

        {/* Profile Info */}
        <div className="px-6 pb-6">
          <div className="flex items-end space-x-4 -mt-16">
            {/* Profile Picture */}
            <div className="relative">
              <img
                src={profileData.profile_image}
                alt={profileData.display_name}
                className="w-32 h-32 rounded-full border-4 border-slate-800 bg-slate-800"
              />
              {editMode && (
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="absolute bottom-0 right-0 bg-goat-primary text-slate-900 p-2 rounded-full hover:bg-goat-primary/80 transition-colors"
                >
                  <Camera size={16} />
                </button>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />
            </div>

            {/* Name and Actions */}
            <div className="flex-1 pb-4">
              <div className="flex items-center justify-between">
                <div>
                  {editMode ? (
                    <input
                      type="text"
                      value={profileData.display_name}
                      onChange={(e) => handleInputChange('display_name', e.target.value)}
                      className="text-2xl font-bold bg-transparent border-b border-goat-primary focus:outline-none"
                      placeholder="Your display name"
                    />
                  ) : (
                    <h1 className="text-2xl font-bold">{profileData.display_name || 'Anonymous GOAT'}</h1>
                  )}
                  {profileData.username && (
                    <p className="text-goat-primary">@{profileData.username}</p>
                  )}
                </div>

                <div className="flex space-x-2">
                  {editMode ? (
                    <>
                      <button
                        onClick={saveProfile}
                        disabled={updateProfileMutation.isLoading}
                        className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors disabled:opacity-50"
                      >
                        <Save size={16} className="mr-2" />
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="bg-slate-700 text-slate-300 px-4 py-2 rounded-lg hover:bg-slate-600 transition-colors"
                      >
                        <X size={16} className="mr-2" />
                        Cancel
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => setEditMode(true)}
                      className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors"
                    >
                      Edit Profile
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Bio */}
          <div className="mt-4">
            {editMode ? (
              <textarea
                value={profileData.bio}
                onChange={(e) => handleInputChange('bio', e.target.value)}
                rows={3}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:border-goat-primary resize-none"
                placeholder="Tell the world about yourself..."
              />
            ) : (
              <p className="text-slate-300">{profileData.bio || 'No bio yet. Click edit to add one!'}</p>
            )}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          icon={<FileText className="w-6 h-6" />}
          title="Files Uploaded"
          value={user?.stats?.total_files || 0}
          color="from-blue-500 to-cyan-500"
        />
        <StatCard
          icon={<Check className="w-6 h-6" />}
          title="Files Processed"
          value={user?.stats?.processed_files || 0}
          color="from-green-500 to-emerald-500"
        />
        <StatCard
          icon={<Star className="w-6 h-6" />}
          title="Favorites"
          value={user?.stats?.favorites || 0}
          color="from-yellow-500 to-orange-500"
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6" />}
          title="This Week"
          value={user?.stats?.recent_uploads || 0}
          color="from-purple-500 to-pink-500"
        />
      </div>

      {/* Account Information */}
      <div className="goat-card">
        <h2 className="text-xl font-bold mb-6">Account Information</h2>

        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Email</label>
              <div className="bg-slate-700 px-3 py-2 rounded-lg text-slate-300">
                {user?.email}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Member Since</label>
              <div className="bg-slate-700 px-3 py-2 rounded-lg text-slate-300 flex items-center">
                <Calendar size={16} className="mr-2 text-slate-400" />
                {user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                }) : 'Unknown'}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Last Active</label>
            <div className="bg-slate-700 px-3 py-2 rounded-lg text-slate-300 flex items-center">
              <Calendar size={16} className="mr-2 text-slate-400" />
              {user?.last_active_at ? new Date(user.last_active_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              }) : 'Recently'}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="goat-card">
        <h2 className="text-xl font-bold mb-6">Recent Activity</h2>

        <div className="space-y-4">
          {/* Mock activity data - in real app, this would come from API */}
          <ActivityItem
            icon={<FileText className="text-blue-400" />}
            title="Uploaded 'Resume.pdf'"
            time="2 hours ago"
            type="upload"
          />
          <ActivityItem
            icon={<Check className="text-green-400" />}
            title="'Business Plan.docx' processed successfully"
            time="1 day ago"
            type="processed"
          />
          <ActivityItem
            icon={<Star className="text-yellow-400" />}
            title="Marked 'Portfolio.pdf' as favorite"
            time="2 days ago"
            type="favorite"
          />
          <ActivityItem
            icon={<FileText className="text-blue-400" />}
            title="Downloaded 'Resume 2025.pdf'"
            time="3 days ago"
            type="download"
          />
        </div>

        <div className="mt-6 text-center">
          <button className="text-goat-primary hover:text-goat-primary/80 transition-colors">
            View All Activity →
          </button>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, title, value, color }) {
  return (
    <div className="goat-card">
      <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <div className="text-xl font-bold">{value}</div>
      <div className="text-sm text-slate-400">{title}</div>
    </div>
  )
}

function ActivityItem({ icon, title, time, type }) {
  return (
    <div className="flex items-center space-x-4 p-3 bg-slate-700 rounded-lg">
      <div className="flex-shrink-0">
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium">{title}</p>
        <p className="text-xs text-slate-400">{time}</p>
      </div>
      <div className={`px-2 py-1 rounded-full text-xs font-medium ${
        type === 'processed' ? 'bg-green-500/20 text-green-400' :
        type === 'upload' ? 'bg-blue-500/20 text-blue-400' :
        type === 'favorite' ? 'bg-yellow-500/20 text-yellow-400' :
        'bg-slate-500/20 text-slate-400'
      }`}>
        {type}
      </div>
    </div>
  )
}