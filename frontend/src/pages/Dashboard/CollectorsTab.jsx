import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Search,
  RefreshCw,
  Play,
  Pause,
  BarChart3,
  Settings,
  Database,
  Activity
} from 'lucide-react'

export function CollectorsTab() {
  const [selectedCollector, setSelectedCollector] = useState(null)
  const queryClient = useQueryClient()

  // Get collectors stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['collectors-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/collectors/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get collectors list
  const { data: collectors, isLoading: collectorsLoading } = useQuery({
    queryKey: ['collectors-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/collectors', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.collectors || []
    }
  })

  // Toggle collector status
  const toggleMutation = useMutation({
    mutationFn: async ({ collectorId, action }) => {
      const token = localStorage.getItem('token')
      const { data } = await axios.put(`/api/v1/admin/collectors/${collectorId}/${action}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['collectors-list'])
    }
  })

  if (statsLoading || collectorsLoading) {
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
          <Search className="w-6 h-6" />
          Collectors Management
        </h2>
        <button
          onClick={() => queryClient.invalidateQueries(['collectors-stats', 'collectors-list'])}
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
              <p className="text-gray-400 text-sm">Total Collectors</p>
              <p className="text-2xl font-bold text-white">{stats?.total_collectors || 0}</p>
            </div>
            <Search className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Collectors</p>
              <p className="text-2xl font-bold text-white">{stats?.active_collectors || 0}</p>
            </div>
            <Activity className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Data Collected</p>
              <p className="text-2xl font-bold text-white">{stats?.total_data_collected || 0}</p>
            </div>
            <Database className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Success Rate</p>
              <p className="text-2xl font-bold text-white">{stats?.success_rate || '0%'}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Collectors List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Collectors</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {collectors?.map((collector) => (
            <div key={collector.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Search className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{collector.name}</h4>
                    <p className="text-gray-400">{collector.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>Source: {collector.source_type}</span>
                      <span>Frequency: {collector.frequency}</span>
                      <span>Last Run: {new Date(collector.last_run).toLocaleString()}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        collector.status === 'active' ? 'bg-green-100 text-green-800' :
                        collector.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                        collector.status === 'error' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {collector.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleMutation.mutate({
                      collectorId: collector.id,
                      action: collector.status === 'active' ? 'stop' : 'start'
                    })}
                    className={`p-2 rounded-lg hover:bg-gray-600 ${
                      collector.status === 'active'
                        ? 'text-red-400 hover:text-red-300'
                        : 'text-green-400 hover:text-green-300'
                    }`}
                    title={collector.status === 'active' ? 'Stop Collector' : 'Start Collector'}
                  >
                    {collector.status === 'active' ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
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
              No collectors found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}