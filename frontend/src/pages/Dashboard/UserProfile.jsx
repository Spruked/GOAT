import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  User,
  Mail,
  Calendar,
  Shield,
  ShieldOff,
  Edit,
  ArrowLeft,
  RefreshCw,
  Trash2,
  Ban,
  CheckCircle
} from 'lucide-react'

export function UserProfile() {
  const { userId } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [isEditing, setIsEditing] = useState(false)
  const [editForm, setEditForm] = useState({
    full_name: '',
    email: '',
    role: 'user'
  })

  // Get user details
  const { data: userData, isLoading } = useQuery({
    queryKey: ['admin-user', userId],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get(`/api/v1/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    },
    enabled: !!userId
  })

  // Update user mutation
  const updateUserMutation = useMutation({
    mutationFn: async (userData) => {
      const token = localStorage.getItem('token')
      const { data } = await axios.put(`/api/v1/admin/users/${userId}`, userData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-user', userId])
      queryClient.invalidateQueries(['admin-users'])
      setIsEditing(false)
    }
  })

  // Block/Unblock user mutation
  const toggleBlockMutation = useMutation({
    mutationFn: async (action) => {
      const token = localStorage.getItem('token')
      const endpoint = action === 'block' ? 'block' : 'unblock'
      await axios.put(`/api/v1/admin/users/${userId}/${endpoint}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-user', userId])
      queryClient.invalidateQueries(['admin-users'])
    }
  })

  // Delete user mutation
  const deleteUserMutation = useMutation({
    mutationFn: async () => {
      const token = localStorage.getItem('token')
      await axios.delete(`/api/v1/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    },
    onSuccess: () => {
      navigate('/dashboard/users')
    }
  })

  useEffect(() => {
    if (userData?.user) {
      setEditForm({
        full_name: userData.user.full_name || '',
        email: userData.user.email || '',
        role: userData.user.role || 'user'
      })
    }
  }, [userData])

  const handleEditSubmit = (e) => {
    e.preventDefault()
    updateUserMutation.mutate(editForm)
  }

  const handleToggleBlock = () => {
    const action = userData?.user?.is_blocked ? 'unblock' : 'block'
    toggleBlockMutation.mutate(action)
  }

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      deleteUserMutation.mutate()
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    )
  }

  if (!userData?.user) {
    return (
      <div className="text-center py-12">
        <User className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">User Not Found</h3>
        <p className="text-gray-500 dark:text-gray-400">The requested user could not be found.</p>
        <button
          onClick={() => navigate('/dashboard/users')}
          className="mt-4 bg-goat-primary hover:bg-goat-primary/80 text-white px-4 py-2 rounded-lg"
        >
          Back to Users
        </button>
      </div>
    )
  }

  const user = userData.user

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/dashboard/users')}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">User Profile</h1>
            <p className="text-gray-500 dark:text-gray-400">Manage user details and permissions</p>
          </div>
        </div>
        <div className="flex gap-2">
          {!isEditing && (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
              >
                <Edit className="w-4 h-4" />
                Edit
              </button>
              <button
                onClick={handleToggleBlock}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  user.is_blocked
                    ? 'bg-green-600 hover:bg-green-700 text-white'
                    : 'bg-orange-600 hover:bg-orange-700 text-white'
                }`}
                disabled={toggleBlockMutation.isPending}
              >
                {user.is_blocked ? (
                  <>
                    <CheckCircle className="w-4 h-4" />
                    Unblock
                  </>
                ) : (
                  <>
                    <Ban className="w-4 h-4" />
                    Block
                  </>
                )}
              </button>
              <button
                onClick={handleDelete}
                className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
                disabled={deleteUserMutation.isPending}
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </>
          )}
        </div>
      </div>

      {/* User Info Card */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="p-6">
          <div className="flex items-start gap-6">
            <div className="w-20 h-20 bg-goat-primary rounded-full flex items-center justify-center">
              <User className="w-10 h-10 text-white" />
            </div>
            <div className="flex-1">
              {isEditing ? (
                <form onSubmit={handleEditSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Full Name
                      </label>
                      <input
                        type="text"
                        value={editForm.full_name}
                        onChange={(e) => setEditForm({...editForm, full_name: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Email
                      </label>
                      <input
                        type="email"
                        value={editForm.email}
                        onChange={(e) => setEditForm({...editForm, email: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Role
                      </label>
                      <select
                        value={editForm.role}
                        onChange={(e) => setEditForm({...editForm, role: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      >
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                      </select>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      className="bg-goat-primary hover:bg-goat-primary/80 text-white px-4 py-2 rounded-lg transition-colors"
                      disabled={updateUserMutation.isPending}
                    >
                      {updateUserMutation.isPending ? 'Saving...' : 'Save Changes'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {user.full_name || 'No name provided'}
                    </h2>
                    <div className="flex items-center gap-2 mt-1">
                      <Mail className="w-4 h-4 text-gray-400" />
                      <span className="text-gray-600 dark:text-gray-400">{user.email}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="flex items-center gap-2">
                      <Shield className={`w-4 h-4 ${user.role === 'admin' ? 'text-purple-500' : 'text-gray-400'}`} />
                      <span className="text-sm text-gray-600 dark:text-gray-400">Role:</span>
                      <span className={`text-sm font-medium ${user.role === 'admin' ? 'text-purple-600 dark:text-purple-400' : 'text-gray-900 dark:text-white'}`}>
                        {user.role}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">Joined:</span>
                      <span className="text-sm text-gray-900 dark:text-white">
                        {new Date(user.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      {user.is_blocked ? (
                        <ShieldOff className="w-4 h-4 text-red-500" />
                      ) : (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      )}
                      <span className="text-sm text-gray-600 dark:text-gray-400">Status:</span>
                      <span className={`text-sm font-medium ${user.is_blocked ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'}`}>
                        {user.is_blocked ? 'Blocked' : 'Active'}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Additional User Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Files</h3>
          <p className="text-2xl font-bold text-goat-primary">{user.files_count || 0}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">Total files uploaded</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Storage</h3>
          <p className="text-2xl font-bold text-goat-primary">{user.storage_used || '0 MB'}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">Storage used</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Last Login</h3>
          <p className="text-2xl font-bold text-goat-primary">
            {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">Last activity</p>
        </div>
      </div>
    </div>
  )
}