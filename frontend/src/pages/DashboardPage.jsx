import React, { useState, useEffect } from 'react';
import { 
  Users, Activity, DollarSign, Settings, Database, AlertCircle, 
  TrendingUp, FileText, LogOut, Shield, Server, Eye, Check, X,
  Mic, BookOpen, Headphones, GraduationCap, Radio, Sparkles, Heart
} from 'lucide-react';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({
    totalUsers: 247,
    activeUsers: 89,
    totalProjects: 1523,
    revenue: 24750,
    serverStatus: 'healthy',
    apiCalls: 45230,
    // Product breakdown
    products: {
      podcasts: { active: 47, inProgress: 12, published: 35 },
      books: { active: 23, inProgress: 18, published: 5 },
      audiobooks: { active: 15, inProgress: 9, published: 6 },
      courses: { active: 31, inProgress: 22, published: 9 },
      masterclass: { active: 8, inProgress: 5, published: 3 },
      audioCourse: { active: 19, inProgress: 14, published: 5 },
      custom: { active: 67, completed: 54, pending: 13 },
      legacy: { created: 142, archived: 142, privateOnly: true }
    }
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    setUser(userData);

    // Simulate loading stats - replace with actual API calls
    // TODO: Fetch real stats from backend
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  const isAdmin = user.isAdmin;

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'products', label: 'Products', icon: Sparkles },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'commerce', label: 'Commerce', icon: DollarSign },
    { id: 'operations', label: 'Operations', icon: Server },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <img src="/Goatvault256.png" alt="GOAT" className="w-10 h-10 rounded-full mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Master Control Center</h1>
                {isAdmin && <span className="text-xs text-slate-600 flex items-center mt-0.5"><Shield className="w-3 h-3 mr-1 text-slate-500" />Foundational Access</span>}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Admin: {user.email}</span>
              <button
                onClick={handleLogout}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <LogOut className="w-5 h-5 mr-1" />
                Logout
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex space-x-1 -mb-px">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center px-6 py-3 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Product Breakdown Panel */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-slate-700" />
                Product Activity
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <Mic className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Podcasts</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.podcasts.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.podcasts.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <BookOpen className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Books</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.books.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.books.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <Headphones className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Audiobooks</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.audiobooks.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.audiobooks.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <GraduationCap className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Courses</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.courses.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.courses.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <TrendingUp className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Masterclass</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.masterclass.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.masterclass.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <Radio className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Audio Course</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.audioCourse.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.audioCourse.published} published</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <Sparkles className="w-4 h-4 mr-2 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">Client Projects</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.custom.active}</p>
                  <p className="text-xs text-slate-600 mt-1">{stats.products.custom.completed} completed</p>
                </div>
                <div className="p-4 bg-slate-900/5 rounded-lg border border-slate-300/50">
                  <div className="flex items-center mb-2">
                    <Heart className="w-4 h-4 mr-2 text-slate-700" />
                    <span className="text-sm font-medium text-slate-800">Legacy Assemblies</span>
                  </div>
                  <p className="text-2xl font-bold text-slate-900">{stats.products.legacy.created}</p>
                  <p className="text-xs text-slate-700 mt-1">Archives preserved (Private)</p>
                </div>
              </div>
              <p className="text-xs text-slate-500 mt-4">8 specialized products. Each with its own reverence.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 text-sm">Total Users</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalUsers}</p>
                    <p className="text-green-600 text-sm mt-1">↑ 12% this month</p>
                  </div>
                  <Users className="w-12 h-12 text-blue-600 opacity-80" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 text-sm">Active Now</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.activeUsers}</p>
                    <p className="text-gray-500 text-sm mt-1">{Math.round(stats.activeUsers/stats.totalUsers*100)}% of total</p>
                  </div>
                  <Activity className="w-12 h-12 text-green-600 opacity-80" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 text-sm">Total Projects</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalProjects}</p>
                    <p className="text-blue-600 text-sm mt-1">Across all users</p>
                  </div>
                  <FileText className="w-12 h-12 text-purple-600 opacity-80" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 text-sm">Revenue (MRR)</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">${stats.revenue.toLocaleString()}</p>
                    <p className="text-green-600 text-sm mt-1">↑ 23% this month</p>
                  </div>
                  <DollarSign className="w-12 h-12 text-green-600 opacity-80" />
                </div>
              </div>
            </div>

            {/* System Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Server className="w-5 h-5 mr-2 text-blue-600" />
                  System Health
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-emerald-50/50 rounded border border-emerald-200/50">
                    <span className="flex items-center"><Check className="w-4 h-4 mr-2 text-emerald-600" />API Server</span>
                    <span className="text-emerald-700 font-medium">Healthy</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-emerald-50/50 rounded border border-emerald-200/50">
                    <span className="flex items-center"><Check className="w-4 h-4 mr-2 text-emerald-600" />Database</span>
                    <span className="text-emerald-700 font-medium">Connected</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-emerald-50/50 rounded border border-emerald-200/50">
                    <span className="flex items-center"><Check className="w-4 h-4 mr-2 text-emerald-600" />Storage</span>
                    <span className="text-emerald-700 font-medium">67% Used</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-amber-50/50 rounded border border-amber-200/50">
                    <span className="flex items-center"><AlertCircle className="w-4 h-4 mr-2 text-amber-600" />Cache</span>
                    <span className="text-amber-700 font-medium">Warming</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                  Recent Activity
                </h3>
                <div className="space-y-3">
                  <div className="flex items-start p-3 border-l-4 border-slate-400 bg-slate-50/50">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-800">New user registration</p>
                      <p className="text-xs text-slate-600">user@example.com - 2 min ago</p>
                    </div>
                  </div>
                  <div className="flex items-start p-3 border-l-4 border-emerald-400 bg-emerald-50/50">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-800">Podcast published</p>
                      <p className="text-xs text-slate-600">"Tech Talk Ep 12" - 15 min ago</p>
                    </div>
                  </div>
                  <div className="flex items-start p-3 border-l-4 border-slate-400 bg-slate-50/50">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-800">Legacy Assembly created</p>
                      <p className="text-xs text-slate-600">Archive preserved (Private) - 1 hour ago</p>
                    </div>
                  </div>
                  <div className="flex items-start p-3 border-l-4 border-amber-400 bg-amber-50/50">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-800">Storage threshold notice</p>
                      <p className="text-xs text-slate-600">70% capacity - 2 hours ago</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-6">Product Analytics</h3>
              <div className="space-y-6">
                {/* Commercial Products */}
                <div>
                  <h4 className="text-sm font-medium text-slate-600 mb-3">Content Production</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><Mic className="w-4 h-4 mr-2 text-slate-600" />Podcast Engine</span>
                        <span className="text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded">Flagship</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.podcasts.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.podcasts.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.podcasts.published}</span></div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><BookOpen className="w-4 h-4 mr-2 text-slate-600" />Books</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.books.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.books.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.books.published}</span></div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><Headphones className="w-4 h-4 mr-2 text-slate-600" />Audiobooks</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.audiobooks.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.audiobooks.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.audiobooks.published}</span></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Content Products */}
                <div>
                  <h4 className="text-sm font-medium text-slate-600 mb-3">Content & Authority</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><GraduationCap className="w-4 h-4 mr-2 text-slate-600" />Digital Course</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.courses.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.courses.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.courses.published}</span></div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><TrendingUp className="w-4 h-4 mr-2 text-slate-600" />Masterclass</span>
                        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">Premium</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.masterclass.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.masterclass.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.masterclass.published}</span></div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><Radio className="w-4 h-4 mr-2 text-slate-600" />Audio Course</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.audioCourse.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">In Progress:</span><span className="font-medium">{stats.products.audioCourse.inProgress}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Published:</span><span className="font-medium">{stats.products.audioCourse.published}</span></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Special Products */}
                <div>
                  <h4 className="text-sm font-medium text-slate-600 mb-3">Specialized Services</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><Sparkles className="w-4 h-4 mr-2 text-slate-600" />Client Projects</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-600">Active:</span><span className="font-medium">{stats.products.custom.active}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Pending:</span><span className="font-medium">{stats.products.custom.pending}</span></div>
                        <div className="flex justify-between"><span className="text-slate-600">Completed:</span><span className="font-medium">{stats.products.custom.completed}</span></div>
                      </div>
                    </div>
                    <div className="p-4 bg-slate-900/5 border border-slate-300 rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <span className="flex items-center"><Heart className="w-4 h-4 mr-2 text-slate-700" />Legacy Assemblies</span>
                        <span className="text-xs bg-slate-200 text-slate-700 px-2 py-1 rounded">Moral Center</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between"><span className="text-slate-700">Created:</span><span className="font-medium text-slate-900">{stats.products.legacy.created}</span></div>
                        <div className="flex justify-between"><span className="text-slate-700">Archives:</span><span className="font-medium text-slate-900">{stats.products.legacy.archived}</span></div>
                        <div className="flex justify-between"><span className="text-slate-700">Privacy:</span><span className="font-medium text-slate-900">Protected</span></div>
                      </div>
                      <p className="text-xs text-slate-600 mt-3 border-t border-slate-300 pt-3">No revenue tracking. Private-only. Reverence over monetization.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b flex justify-between items-center">
              <h3 className="text-lg font-semibold">User Management</h3>
              <input
                type="search"
                placeholder="Search users..."
                className="px-4 py-2 border rounded-lg"
              />
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Projects</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  <tr>
                    <td className="px-6 py-4">John Doe</td>
                    <td className="px-6 py-4">john@example.com</td>
                    <td className="px-6 py-4">12</td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">Pro</span></td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">Active</span></td>
                    <td className="px-6 py-4"><button className="text-blue-600 hover:underline text-sm">View</button></td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4">Jane Smith</td>
                    <td className="px-6 py-4">jane@example.com</td>
                    <td className="px-6 py-4">5</td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">Free</span></td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">Active</span></td>
                    <td className="px-6 py-4"><button className="text-blue-600 hover:underline text-sm">View</button></td>
                  </tr>
                  <tr>
                    <td colSpan="6" className="px-6 py-4 text-center py-8 text-gray-500">
                      Real user data will load from API
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}



        {/* Commerce Tab */}
        {activeTab === 'commerce' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-500 text-sm">Monthly Recurring Revenue</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">${stats.revenue.toLocaleString()}</p>
                <p className="text-green-600 text-sm mt-1">↑ 23% vs last month</p>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-500 text-sm">Annual Run Rate</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">${(stats.revenue * 12).toLocaleString()}</p>
                <p className="text-gray-500 text-sm mt-1">Projected yearly</p>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-500 text-sm">Avg Revenue Per User</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">${Math.round(stats.revenue / stats.totalUsers)}</p>
                <p className="text-gray-500 text-sm mt-1">Per month</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">Revenue analytics and charts will display here</h3>
              <p className="text-gray-500">Integration with payment processor pending</p>
            </div>
          </div>
        )}

        {/* Operations Tab */}
        {activeTab === 'operations' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">API Usage</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-gray-500 text-sm">Total API Calls</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.apiCalls.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm">Avg Response Time</p>
                  <p className="text-2xl font-bold text-gray-900">127ms</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm">Error Rate</p>
                  <p className="text-2xl font-bold text-green-600">0.3%</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm">Uptime</p>
                  <p className="text-2xl font-bold text-green-600">99.9%</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">Recent Errors</h3>
              <p className="text-gray-500">Error logs and monitoring dashboard</p>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-6">Platform Settings</h3>
            <div className="space-y-6">
              <div>
                <h4 className="font-medium mb-2">Feature Flags</h4>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-2" defaultChecked />
                    <span>New user signups enabled</span>
                  </label>
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-2" defaultChecked />
                    <span>Payment processing enabled</span>
                  </label>
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-2" />
                    <span>Beta features access</span>
                  </label>
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">System Configuration</h4>
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Manage Configuration
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}