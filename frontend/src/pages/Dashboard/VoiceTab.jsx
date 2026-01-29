import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Cpu,
  Volume2,
  Mic,
  Settings,
  RefreshCw,
  Play,
  Pause,
  BarChart3,
  Zap
} from 'lucide-react'

export function VoiceTab() {
  const [selectedVoice, setSelectedVoice] = useState(null)
  const queryClient = useQueryClient()

  // Get voice systems stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['voice-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/voice/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get voice systems
  const { data: voices, isLoading: voicesLoading } = useQuery({
    queryKey: ['voice-systems'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/voice/systems', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.voices || []
    }
  })

  if (statsLoading || voicesLoading) {
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
          <Cpu className="w-6 h-6" />
          Voice Systems Management
        </h2>
        <button
          onClick={() => queryClient.invalidateQueries(['voice-stats', 'voice-systems'])}
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
              <p className="text-gray-400 text-sm">Active Voices</p>
              <p className="text-2xl font-bold text-white">{stats?.active_voices || 0}</p>
            </div>
            <Mic className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Generations</p>
              <p className="text-2xl font-bold text-white">{stats?.total_generations || 0}</p>
            </div>
            <Volume2 className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg. Quality</p>
              <p className="text-2xl font-bold text-white">{stats?.avg_quality || '0%'}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Processing Time</p>
              <p className="text-2xl font-bold text-white">{stats?.avg_processing_time || '0s'}</p>
            </div>
            <Zap className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Voice Systems List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Voice Systems</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {voices?.map((voice) => (
            <div key={voice.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Mic className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{voice.name}</h4>
                    <p className="text-gray-400">{voice.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>Engine: {voice.engine}</span>
                      <span>Language: {voice.language}</span>
                      <span>Quality: {voice.quality}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        voice.status === 'active' ? 'bg-green-100 text-green-800' :
                        voice.status === 'training' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {voice.status}
                      </span>
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
              No voice systems found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}