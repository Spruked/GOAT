import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import {
  BarChart3,
  RefreshCw,
  TrendingUp,
  Users,
  Activity,
  Database,
  Clock
} from 'lucide-react'

export function AnalyticsTab() {
  const [timeRange, setTimeRange] = useState('7d')

  // Get analytics data
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics', timeRange],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get(`/api/v1/admin/analytics?range=${timeRange}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  if (isLoading) {
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
          <BarChart3 className="w-6 h-6" />
          System Analytics
        </h2>
        <div className="flex items-center gap-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Users</p>
              <p className="text-2xl font-bold text-white">{analytics?.total_users || 0}</p>
              <p className="text-sm text-green-500 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                +{analytics?.user_growth || 0}%
              </p>
            </div>
            <Users className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Sessions</p>
              <p className="text-2xl font-bold text-white">{analytics?.active_sessions || 0}</p>
              <p className="text-sm text-gray-400">Current</p>
            </div>
            <Activity className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">API Calls</p>
              <p className="text-2xl font-bold text-white">{analytics?.api_calls || 0}</p>
              <p className="text-sm text-gray-400">This period</p>
            </div>
            <Database className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg Response Time</p>
              <p className="text-2xl font-bold text-white">{analytics?.avg_response_time || '0ms'}</p>
              <p className="text-sm text-gray-400">API</p>
            </div>
            <Clock className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* User Activity Chart */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">User Activity</h3>
          <div className="h-64 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <BarChart3 className="w-12 h-12 mx-auto mb-2" />
              <p>Activity chart would be displayed here</p>
              <p className="text-sm">Integration with charting library needed</p>
            </div>
          </div>
        </div>

        {/* System Performance */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">System Performance</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">CPU Usage</span>
              <span className="text-white">{analytics?.cpu_usage || '0'}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full"
                style={{ width: `${analytics?.cpu_usage || 0}%` }}
              ></div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-400">Memory Usage</span>
              <span className="text-white">{analytics?.memory_usage || '0'}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-green-500 h-2 rounded-full"
                style={{ width: `${analytics?.memory_usage || 0}%` }}
              ></div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-400">Storage Usage</span>
              <span className="text-white">{analytics?.storage_usage || '0'}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-purple-500 h-2 rounded-full"
                style={{ width: `${analytics?.storage_usage || 0}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Recent Activity</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {analytics?.recent_activity?.map((activity, index) => (
            <div key={index} className="p-4 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white">{activity.description}</p>
                  <p className="text-sm text-gray-400">{activity.timestamp}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  activity.type === 'user' ? 'bg-blue-100 text-blue-800' :
                  activity.type === 'system' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {activity.type}
                </span>
              </div>
            </div>
          )) || (
            <div className="p-6 text-center text-gray-400">
              No recent activity
            </div>
          )}
        </div>
      </div>
    </div>
  )
}