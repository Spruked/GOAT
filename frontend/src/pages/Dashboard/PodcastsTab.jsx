import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Mic,
  Play,
  Pause,
  Radio,
  Users,
  TrendingUp,
  RefreshCw,
  Plus,
  Settings,
  BarChart3
} from 'lucide-react'

export function PodcastsTab() {
  const [selectedPodcast, setSelectedPodcast] = useState(null)
  const queryClient = useQueryClient()

  // Get podcasts stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['podcasts-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/podcasts/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get podcasts list
  const { data: podcasts, isLoading: podcastsLoading } = useQuery({
    queryKey: ['podcasts-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/podcasts', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.podcasts || []
    }
  })

  if (statsLoading || podcastsLoading) {
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
          <Mic className="w-6 h-6" />
          Podcasts Management
        </h2>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
            <Plus className="w-4 h-4" />
            Create Podcast
          </button>
          <button
            onClick={() => queryClient.invalidateQueries(['podcasts-stats', 'podcasts-list'])}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Podcasts</p>
              <p className="text-2xl font-bold text-white">{stats?.total_podcasts || 0}</p>
            </div>
            <Radio className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Episodes</p>
              <p className="text-2xl font-bold text-white">{stats?.total_episodes || 0}</p>
            </div>
            <Mic className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Listens</p>
              <p className="text-2xl font-bold text-white">{stats?.total_listens || 0}</p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg. Engagement</p>
              <p className="text-2xl font-bold text-white">{stats?.avg_engagement || '0%'}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Podcasts List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Podcasts</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {podcasts?.map((podcast) => (
            <div key={podcast.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Mic className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{podcast.title}</h4>
                    <p className="text-gray-400">{podcast.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>{podcast.episodes} episodes</span>
                      <span>{podcast.total_listens} listens</span>
                      <span>{podcast.subscribers} subscribers</span>
                      <span>Last updated: {new Date(podcast.last_updated).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
                    <Play className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-green-400 hover:text-green-300 rounded-lg hover:bg-gray-600">
                    <BarChart3 className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-gray-300 rounded-lg hover:bg-gray-600">
                    <Settings className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          )) || (
            <div className="p-6 text-center text-gray-400">
              No podcasts found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}