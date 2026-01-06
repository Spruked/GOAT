import { Menu, X, LogOut, Upload } from 'lucide-react'

export function DashboardLayout({
  user,
  activeTab,
  setActiveTab,
  tabs,
  sidebarOpen,
  setSidebarOpen,
  theme,
  toggleTheme,
  onLogout,
  filesStats,
  children
}) {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-slate-800 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex flex-col h-full">
          {/* Logo/Brand */}
          <div className="flex items-center justify-center h-16 px-4 bg-gradient-to-r from-goat-primary to-goat-secondary">
            <h1 className="text-xl font-bold">GOAT</h1>
          </div>

          {/* User Info */}
          <div className="p-4 border-b border-slate-700">
            <div className="flex items-center space-x-3">
              <img
                src={user.profile_image || "/defaults/avatar-goat.png"}
                alt={user.display_name}
                className="w-10 h-10 rounded-full"
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user.display_name}</p>
                <p className="text-xs text-slate-400 truncate">@{user.username || user.email}</p>
              </div>
            </div>

            {/* Quick Stats */}
            {filesStats && (
              <div className="mt-3 grid grid-cols-2 gap-2 text-center">
                <div className="bg-slate-700 rounded p-2">
                  <div className="text-lg font-bold text-goat-primary">{filesStats.total_files}</div>
                  <div className="text-xs text-slate-400">Files</div>
                </div>
                <div className="bg-slate-700 rounded p-2">
                  <div className="text-lg font-bold text-green-400">{filesStats.processed_files}</div>
                  <div className="text-xs text-slate-400">Processed</div>
                </div>
              </div>
            )}
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-2 py-4 space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setSidebarOpen(false)
                  }}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-goat-primary text-slate-900'
                      : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                  }`}
                >
                  <Icon size={18} className="mr-3" />
                  {tab.label}
                </button>
              )
            })}
          </nav>

          {/* Quick Upload Button */}
          <div className="p-4 border-t border-slate-700">
            <button className="w-full bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors flex items-center justify-center">
              <Upload size={16} className="mr-2" />
              Quick Upload
            </button>
          </div>

          {/* Logout */}
          <div className="p-4 border-t border-slate-700">
            <button
              onClick={onLogout}
              className="w-full flex items-center px-3 py-2 text-sm font-medium text-slate-300 rounded-lg hover:bg-slate-700 hover:text-white transition-colors"
            >
              <LogOut size={18} className="mr-3" />
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="lg:pl-64">
        {/* Top Bar */}
        <div className="sticky top-0 z-30 bg-slate-900 border-b border-slate-700">
          <div className="flex items-center justify-between h-16 px-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg hover:bg-slate-700"
            >
              <Menu size={20} />
            </button>

            <div className="flex items-center space-x-4">
              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg hover:bg-slate-700 transition-colors"
              >
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>

              {/* User Menu */}
              <div className="flex items-center space-x-2">
                <img
                  src={user.profile_image || "/defaults/avatar-goat.png"}
                  alt={user.display_name}
                  className="w-8 h-8 rounded-full"
                />
                <span className="hidden md:block text-sm font-medium">{user.display_name}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}