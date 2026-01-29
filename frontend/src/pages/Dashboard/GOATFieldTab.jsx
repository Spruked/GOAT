import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Zap,
  RefreshCw,
  BarChart3,
  Settings,
  Database,
  Activity,
  Brain,
  TrendingUp
} from 'lucide-react'

export function GOATFieldTab() {
  const [selectedProposal, setSelectedProposal] = useState(null)
  const queryClient = useQueryClient()

  // Get GOAT Field stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['goat-field-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/goat-field/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get pending proposals
  const { data: proposals, isLoading: proposalsLoading } = useQuery({
    queryKey: ['goat-field-proposals'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/field/review/pending', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Approve/Reject proposal
  const proposalMutation = useMutation({
    mutationFn: async ({ proposalId, action, data }) => {
      const token = localStorage.getItem('token')
      const { data: response } = await axios.post(`/api/v1/admin/field/review/${proposalId}/${action}`, data, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['goat-field-proposals'])
    }
  })

  if (statsLoading || proposalsLoading) {
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
          <Brain className="w-6 h-6" />
          GOAT Field Management
        </h2>
        <button
          onClick={() => queryClient.invalidateQueries(['goat-field-stats', 'goat-field-proposals'])}
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
              <p className="text-gray-400 text-sm">Total Nodes</p>
              <p className="text-2xl font-bold text-white">{stats?.total_nodes || 0}</p>
            </div>
            <Database className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Edges</p>
              <p className="text-2xl font-bold text-white">{stats?.active_edges || 0}</p>
            </div>
            <Activity className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Learning Rate</p>
              <p className="text-2xl font-bold text-white">{stats?.learning_rate || '0%'}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Integrity Score</p>
              <p className="text-2xl font-bold text-white">{stats?.integrity_score || '0%'}</p>
            </div>
            <Zap className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Pending Proposals */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Pending Learning Proposals ({proposals?.length || 0})</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {proposals?.map((proposal) => (
            <div key={proposal.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-white">{proposal.title}</h4>
                  <p className="text-gray-400 mt-1">{proposal.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                    <span>Type: {proposal.type}</span>
                    <span>Confidence: {proposal.confidence}%</span>
                    <span>Created: {new Date(proposal.created_at).toLocaleString()}</span>
                    <span className="px-2 py-1 rounded-full text-xs bg-yellow-100 text-yellow-800">
                      Pending Review
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <button
                    onClick={() => proposalMutation.mutate({
                      proposalId: proposal.id,
                      action: 'approve',
                      data: {
                        approved_config: { chunk_size: 1000, pre_filter: "drop_empty_rows" }, // Example config
                        human_rationale: "Chunking improves CSV without affecting accuracy; tested locally."
                      }
                    })}
                    className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => proposalMutation.mutate({
                      proposalId: proposal.proposal_id,
                      action: 'reject',
                      data: {
                        human_rationale: "Optimization conflicts with XLSX merged-cell handling."
                      }
                    })}
                    className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
                  >
                    Reject
                  </button>
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
                    <BarChart3 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          )) || (
            <div className="p-6 text-center text-gray-400">
              No pending proposals
            </div>
          )}
        </div>
      </div>

      {/* Field Health */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Field Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-500">{stats?.clutter_cleaned || 0}</div>
            <div className="text-sm text-gray-400">Clutter Cleaned</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-500">{stats?.patterns_extracted || 0}</div>
            <div className="text-sm text-gray-400">Patterns Extracted</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-500">{stats?.self_repairs || 0}</div>
            <div className="text-sm text-gray-400">Self-Repairs</div>
          </div>
        </div>
      </div>
    </div>
  )
}