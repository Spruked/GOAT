import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  Award,
  RefreshCw,
  Download,
  Eye,
  Plus,
  Search,
  Calendar,
  User
} from 'lucide-react'

export function CertificatesTab() {
  const [searchTerm, setSearchTerm] = useState('')
  const queryClient = useQueryClient()

  // Get certificates stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['certificates-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/certificates/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get certificates list
  const { data: certificates, isLoading: certificatesLoading } = useQuery({
    queryKey: ['certificates-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/certificates', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.certificates || []
    }
  })

  const filteredCertificates = certificates?.filter(cert =>
    cert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cert.recipient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cert.recipient_email.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  if (statsLoading || certificatesLoading) {
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
          <Award className="w-6 h-6" />
          Certificates Management
        </h2>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
            <Plus className="w-4 h-4" />
            Issue Certificate
          </button>
          <button
            onClick={() => queryClient.invalidateQueries(['certificates-stats', 'certificates-list'])}
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
              <p className="text-gray-400 text-sm">Total Certificates</p>
              <p className="text-2xl font-bold text-white">{stats?.total_certificates || 0}</p>
            </div>
            <Award className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Issued This Month</p>
              <p className="text-2xl font-bold text-white">{stats?.issued_this_month || 0}</p>
            </div>
            <Calendar className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Certificates</p>
              <p className="text-2xl font-bold text-white">{stats?.active_certificates || 0}</p>
            </div>
            <User className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Downloads</p>
              <p className="text-2xl font-bold text-white">{stats?.total_downloads || 0}</p>
            </div>
            <Download className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <input
          type="text"
          placeholder="Search certificates..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Certificates List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Certificates ({filteredCertificates.length})</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {filteredCertificates.map((cert) => (
            <div key={cert.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Award className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{cert.title}</h4>
                    <p className="text-gray-400">Issued to: {cert.recipient_name}</p>
                    <p className="text-gray-400">{cert.recipient_email}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>Issued: {new Date(cert.issued_at).toLocaleDateString()}</span>
                      <span>Type: {cert.certificate_type}</span>
                      <span>Status: {cert.status}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        cert.status === 'active' ? 'bg-green-100 text-green-800' :
                        cert.status === 'revoked' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {cert.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
                    <Eye className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-green-400 hover:text-green-300 rounded-lg hover:bg-gray-600">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
          {filteredCertificates.length === 0 && (
            <div className="p-6 text-center text-gray-400">
              No certificates found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}