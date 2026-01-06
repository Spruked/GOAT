import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Folder,
  FileText,
  Image,
  File,
  Search,
  Filter,
  Grid,
  List,
  Star,
  Download,
  Trash2,
  Edit,
  CheckCircle,
  Clock,
  AlertCircle,
  Upload
} from 'lucide-react'
import axios from 'axios'
import { FileTable } from '../../components/FileTable'

export function FilesTab({ user }) {
  const [viewMode, setViewMode] = useState('table') // 'table' or 'grid'
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedFilter, setSelectedFilter] = useState('all')
  const [selectedFiles, setSelectedFiles] = useState([])
  const queryClient = useQueryClient()

  // Get user files stats for filters
  const { data: filesData, isLoading } = useQuery({
    queryKey: ['user-files-stats'],
    queryFn: async () => {
      const { data } = await axios.get('/api/user/files?limit=1')
      return data
    }
  })

  // Toggle favorite mutation
  const toggleFavoriteMutation = useMutation({
    mutationFn: async (fileId) => {
      const { data } = await axios.post(`/api/user/files/${fileId}/favorite`)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-files-infinite'])
      queryClient.invalidateQueries(['user-files-stats'])
    }
  })

  // Delete file mutation
  const deleteFileMutation = useMutation({
    mutationFn: async (fileId) => {
      await axios.delete(`/api/user/files/${fileId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-files-infinite'])
      queryClient.invalidateQueries(['user-files-stats'])
      setSelectedFiles([])
    }
  })

  const filters = [
    { id: 'all', label: 'All Files', count: filesData?.stats?.total_files || 0 },
    { id: 'processed', label: 'Processed', count: filesData?.stats?.processed_files || 0 },
    { id: 'unprocessed', label: 'Unprocessed', count: (filesData?.stats?.total_files || 0) - (filesData?.stats?.processed_files || 0) },
    { id: 'favorites', label: 'Favorites', count: filesData?.stats?.favorites || 0 },
    { id: 'pdf', label: 'PDFs', icon: FileText },
    { id: 'image', label: 'Images', icon: Image },
    { id: 'document', label: 'Documents', icon: File }
  ]

  const handleFileSelect = (fileId, selected) => {
    if (selected) {
      setSelectedFiles(prev => [...prev, fileId])
    } else {
      setSelectedFiles(prev => prev.filter(id => id !== fileId))
    }
  }

  const handleBulkDelete = () => {
    if (selectedFiles.length > 0 && confirm(`Delete ${selectedFiles.length} selected files?`)) {
      selectedFiles.forEach(fileId => deleteFileMutation.mutate(fileId))
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">My Files</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="goat-card animate-pulse">
              <div className="h-32 bg-slate-700 rounded mb-3"></div>
              <div className="h-4 bg-slate-700 rounded mb-2"></div>
              <div className="h-3 bg-slate-700 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">My Files</h1>
        <div className="flex items-center space-x-4">
          <button className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors flex items-center">
            <Upload size={16} className="mr-2" />
            Upload
          </button>
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex items-center justify-end space-x-2">
        <button
          onClick={() => setViewMode('table')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            viewMode === 'table' ? 'bg-goat-primary text-slate-900' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          Table View
        </button>
        <button
          onClick={() => setViewMode('grid')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            viewMode === 'grid' ? 'bg-goat-primary text-slate-900' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          Grid View
        </button>
      </div>

      {/* File Table or Grid */}
      {viewMode === 'table' ? (
        <FileTable user={user} />
      ) : (
        <div className="space-y-6">
          {/* Search and Filters */}
          <div className="goat-card">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search files..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:border-goat-primary"
                />
              </div>

              {/* View Toggle */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded-lg ${viewMode === 'grid' ? 'bg-goat-primary text-slate-900' : 'bg-slate-700 text-slate-400'}`}
                >
                  <Grid size={16} />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded-lg ${viewMode === 'list' ? 'bg-goat-primary text-slate-900' : 'bg-slate-700 text-slate-400'}`}
                >
                  <List size={16} />
                </button>
              </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex flex-wrap gap-2 mt-4">
              {filters.map((filter) => (
                <button
                  key={filter.id}
                  onClick={() => setSelectedFilter(filter.id)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center ${
                    selectedFilter === filter.id
                      ? 'bg-goat-primary text-slate-900'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {filter.icon && <filter.icon size={14} className="mr-2" />}
                  {filter.label}
                  <span className="ml-2 px-2 py-0.5 bg-slate-600 rounded-full text-xs">
                    {filter.count}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Bulk Actions */}
          {selectedFiles.length > 0 && (
            <div className="goat-card bg-goat-primary/10 border-goat-primary/30">
              <div className="flex items-center justify-between">
                <span className="text-goat-primary font-medium">
                  {selectedFiles.length} file{selectedFiles.length !== 1 ? 's' : ''} selected
                </span>
                <div className="flex items-center space-x-2">
                  <button className="bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors">
                    <Download size={16} className="mr-2" />
                    Download
                  </button>
                  <button
                    onClick={handleBulkDelete}
                    className="bg-red-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors"
                  >
                    <Trash2 size={16} className="mr-2" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Files Grid/List - Keeping the old implementation for grid view */}
          <div className="text-center py-10">
            <p className="text-slate-400">Grid view temporarily disabled. Use Table View for full functionality.</p>
          </div>
        </div>
      )}
    </div>
  )
}