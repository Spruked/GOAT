import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Database,
  Settings,
  RefreshCw,
  Play,
  Pause,
  BarChart3,
  Zap,
  Activity
} from 'lucide-react'

export function DistillersTab() {
  const [selectedDistiller, setSelectedDistiller] = useState(null)
  const queryClient = useQueryClient()

  // Get distillers stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['distillers-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/distillers/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get distillers list
  const { data: distillers, isLoading: distillersLoading } = useQuery({
    queryKey: ['distillers-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/distillers', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.distillers || []
    }
  })

  // Toggle distiller status
  const toggleMutation = useMutation({
    mutationFn: async ({ distillerId, action }) => {
      const token = localStorage.getItem('token')
      const { data } = await axios.put(`/api/v1/admin/distillers/${distillerId}/${action}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['distillers-list'])
    }
  })

  if (statsLoading || distillersLoading) {
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
          <Database className="w-6 h-6" />
          Distillers Management
        </h2>
        <button
          onClick={() => queryClient.invalidateQueries(['distillers-stats', 'distillers-list'])}
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
              <p className="text-gray-400 text-sm">Total Distillers</p>
              <p className="text-2xl font-bold text-white">{stats?.total_distillers || 0}</p>
            </div>
            <Database className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Distillers</p>
              <p className="text-2xl font-bold text-white">{stats?.active_distillers || 0}</p>
            </div>
            <Activity className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Executions</p>
              <p className="text-2xl font-bold text-white">{stats?.total_executions || 0}</p>
            </div>
            <Play className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg. Performance</p>
              <p className="text-2xl font-bold text-white">{stats?.avg_performance || '0%'}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Distillers List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Distillers</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {distillers?.map((distiller) => (
            <div key={distiller.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Database className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{distiller.name}</h4>
                    <p className="text-gray-400">{distiller.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>Type: {distiller.type}</span>
                      <span>Version: {distiller.version}</span>
                      <span>Executions: {distiller.executions}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        distiller.status === 'active' ? 'bg-green-100 text-green-800' :
                        distiller.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {distiller.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleMutation.mutate({
                      distillerId: distiller.id,
                      action: distiller.status === 'active' ? 'deactivate' : 'activate'
                    })}
                    className={`p-2 rounded-lg hover:bg-gray-600 ${
                      distiller.status === 'active'
                        ? 'text-red-400 hover:text-red-300'
                        : 'text-green-400 hover:text-green-300'
                    }`}
                    title={distiller.status === 'active' ? 'Deactivate' : 'Activate'}
                  >
                    {distiller.status === 'active' ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  </button>
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
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
              No distillers found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}