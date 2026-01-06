import { useState } from 'react'
import { Upload, FileText, CheckCircle, Clock, Star, TrendingUp } from 'lucide-react'

export function HomeTab({ user, filesStats }) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      // Handle file upload here
      console.log("Files dropped:", e.dataTransfer.files)
    }
  }

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      // Handle file upload here
      console.log("Files selected:", e.target.files)
    }
  }

  return (
    <div className="space-y-8">
      {/* Welcome Hero */}
      <div className="goat-card">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <img
              src={user.profile_image || "/defaults/avatar-goat.png"}
              alt={user.display_name}
              className="w-20 h-20 rounded-full border-4 border-goat-primary"
            />
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Welcome back, <span className="text-goat-primary">{user.display_name || "@goat"}!</span>
              </h1>
              <p className="text-xl text-slate-400">
                You've processed <strong className="text-goat-primary">{filesStats?.processed_files || 0}</strong> files like a legend.
              </p>
              {user.bio && (
                <p className="text-slate-300 mt-2 italic">"{user.bio}"</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          icon={<FileText className="w-8 h-8" />}
          title="Total Files"
          value={filesStats?.total_files || 0}
          color="from-blue-500 to-cyan-500"
        />
        <StatCard
          icon={<CheckCircle className="w-8 h-8" />}
          title="Processed"
          value={filesStats?.processed_files || 0}
          color="from-green-500 to-emerald-500"
        />
        <StatCard
          icon={<Star className="w-8 h-8" />}
          title="Favorites"
          value={filesStats?.favorites || 0}
          color="from-yellow-500 to-orange-500"
        />
        <StatCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="This Week"
          value={filesStats?.recent_uploads || 0}
          color="from-purple-500 to-pink-500"
        />
      </div>

      {/* Upload Zone */}
      <div
        className={`goat-card border-2 border-dashed transition-colors ${
          dragActive
            ? 'border-goat-primary bg-goat-primary/10'
            : 'border-slate-600 hover:border-goat-primary/50'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="text-center py-12">
          <Upload className={`w-16 h-16 mx-auto mb-4 ${dragActive ? 'text-goat-primary' : 'text-slate-400'}`} />
          <h3 className="text-2xl font-bold mb-2">
            {dragActive ? 'Drop your files here!' : 'Drop files here or click to upload'}
          </h3>
          <p className="text-slate-400 mb-6 max-w-md mx-auto">
            We'll organize, enhance, and GOAT-ify them instantly. Supports PDFs, images, documents, and more.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <label className="bg-goat-primary text-slate-900 px-6 py-3 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors cursor-pointer">
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.gif,.txt"
              />
              Choose Files
            </label>
            <button className="border border-slate-600 text-slate-300 px-6 py-3 rounded-lg font-medium hover:bg-slate-700 transition-colors">
              Browse Folders
            </button>
          </div>

          <div className="mt-6 text-sm text-slate-500">
            <p>Supported formats: PDF, DOC, DOCX, JPG, PNG, GIF, TXT</p>
            <p>Maximum file size: 50MB per file</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="goat-card">
        <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>

        <div className="space-y-4">
          {/* Sample recent activities - in real app, this would come from API */}
          <ActivityItem
            icon={<CheckCircle className="text-green-400" />}
            title="Resume.pdf processed successfully"
            time="2 hours ago"
            status="completed"
          />
          <ActivityItem
            icon={<Clock className="text-blue-400" />}
            title="Business Plan.docx processing"
            time="4 hours ago"
            status="processing"
          />
          <ActivityItem
            icon={<Star className="text-yellow-400" />}
            title="Portfolio.pdf marked as favorite"
            time="1 day ago"
            status="favorited"
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
      <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm text-slate-400">{title}</div>
    </div>
  )
}

function ActivityItem({ icon, title, time, status }) {
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
        status === 'completed' ? 'bg-green-500/20 text-green-400' :
        status === 'processing' ? 'bg-blue-500/20 text-blue-400' :
        'bg-yellow-500/20 text-yellow-400'
      }`}>
        {status}
      </div>
    </div>
  )
}