import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import {
  CreditCard,
  RefreshCw,
  DollarSign,
  TrendingUp,
  Users,
  Receipt,
  Calendar
} from 'lucide-react'

export function PaymentsTab() {
  const [selectedTransaction, setSelectedTransaction] = useState(null)

  // Get payments stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['payments-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/payments/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get recent transactions
  const { data: transactions, isLoading: transactionsLoading } = useQuery({
    queryKey: ['payments-transactions'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/payments/transactions', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.transactions || []
    }
  })

  if (statsLoading || transactionsLoading) {
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
          <CreditCard className="w-6 h-6" />
          Payments Management
        </h2>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Revenue</p>
              <p className="text-2xl font-bold text-white">${stats?.total_revenue || 0}</p>
              <p className="text-sm text-green-500 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                +{stats?.revenue_growth || 0}%
              </p>
            </div>
            <DollarSign className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Transactions</p>
              <p className="text-2xl font-bold text-white">{stats?.total_transactions || 0}</p>
              <p className="text-sm text-gray-400">All time</p>
            </div>
            <Receipt className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Subscribers</p>
              <p className="text-2xl font-bold text-white">{stats?.active_subscribers || 0}</p>
              <p className="text-sm text-gray-400">Monthly</p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg Transaction</p>
              <p className="text-2xl font-bold text-white">${stats?.avg_transaction || 0}</p>
              <p className="text-sm text-gray-400">Per transaction</p>
            </div>
            <CreditCard className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Recent Transactions</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {transactions?.map((transaction) => (
            <div key={transaction.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-gray-600 rounded-lg flex items-center justify-center">
                    <CreditCard className="w-5 h-5 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">
                      ${transaction.amount} - {transaction.description}
                    </h4>
                    <p className="text-gray-400">User: {transaction.user_email}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>{new Date(transaction.created_at).toLocaleString()}</span>
                      <span>Method: {transaction.payment_method}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        transaction.status === 'completed' ? 'bg-green-100 text-green-800' :
                        transaction.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        transaction.status === 'failed' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {transaction.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-white">${transaction.amount}</p>
                  <p className="text-sm text-gray-400">{transaction.currency}</p>
                </div>
              </div>
            </div>
          )) || (
            <div className="p-6 text-center text-gray-400">
              No transactions found
            </div>
          )}
        </div>
      </div>

      {/* Subscription Overview */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Subscription Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-500">{stats?.monthly_subscribers || 0}</div>
            <div className="text-sm text-gray-400">Monthly Subscribers</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-500">{stats?.yearly_subscribers || 0}</div>
            <div className="text-sm text-gray-400">Yearly Subscribers</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-500">{stats?.lifetime_subscribers || 0}</div>
            <div className="text-sm text-gray-400">Lifetime Subscribers</div>
          </div>
        </div>
      </div>
    </div>
  )
}