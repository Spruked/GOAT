import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Headphones,
  Play,
  Pause,
  Volume2,
  Settings,
  RefreshCw,
  BookOpen,
  Clock,
  Users,
  TrendingUp
} from 'lucide-react'

export function AudiobooksTab() {
  const [selectedAudiobook, setSelectedAudiobook] = useState(null)
  const queryClient = useQueryClient()

  // Get audiobooks stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['audiobooks-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/audiobooks/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get audiobooks list
  const { data: audiobooks, isLoading: audiobooksLoading } = useQuery({
    queryKey: ['audiobooks-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/audiobooks', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.audiobooks || []
    }
  })

  if (statsLoading || audiobooksLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <Headphones className="w-6 h-6" />
          Audiobooks Management
        </h2>
        <button
          onClick={() => queryClient.invalidateQueries(['audiobooks-stats', 'audiobooks-list'])}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Audiobooks</p>
              <p className="text-2xl font-bold text-white">{stats?.total_audiobooks || 0}</p>
            </div>
            <BookOpen className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Plays</p>
              <p className="text-2xl font-bold text-white">{stats?.total_plays || 0}</p>
            </div>
            <Play className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Users</p>
              <p className="text-2xl font-bold text-white">{stats?.active_users || 0}</p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg. Listen Time</p>
              <p className="text-2xl font-bold text-white">{stats?.avg_listen_time || '0h'}</p>
            </div>
            <Clock className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Audiobooks List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Audiobooks</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {audiobooks?.map((audiobook) => (
            <div key={audiobook.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Headphones className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{audiobook.title}</h4>
                    <p className="text-gray-400">{audiobook.author}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>{audiobook.duration}</span>
                      <span>{audiobook.plays} plays</span>
                      <span>{audiobook.rating} ★</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
                    <Play className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-gray-300 rounded-lg hover:bg-gray-600">
                    <Settings className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          )) || (
            <div className="p-6 text-center text-gray-400">
              No audiobooks found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}