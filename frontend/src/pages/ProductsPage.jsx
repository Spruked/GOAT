import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Mic, BookOpen, Headphones, GraduationCap, TrendingUp, Radio, 
  Sparkles, Heart, FileText, Activity, Check, LogOut 
} from 'lucide-react';

export default function ProductsPage() {
  const [user, setUser] = useState(null);
  const [showComingSoon, setShowComingSoon] = useState(false);
  const [comingSoonProduct, setComingSoonProduct] = useState(null);
  const [stats, setStats] = useState({
    yourProjects: 0,
    inProgress: 0,
    completed: 0
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    setUser(userData);

    // TODO: Fetch user's actual project stats from backend
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  const products = [
    { 
      id: 'podcast', 
      name: 'Podcast Engine', 
      icon: Mic, 
      description: 'Professional podcast production with multi-voice support',
      badge: 'Flagship',
      route: '/podcast'
    },
    { 
      id: 'book', 
      name: 'Books', 
      icon: BookOpen, 
      description: 'Structured book creation with chapters and formatting',
      route: '/book'
    },
    { 
      id: 'audiobook', 
      name: 'Audiobooks', 
      icon: Headphones, 
      description: 'Voice-narrated books with biological voice synthesis',
      route: '/audiobook'
    },
    { 
      id: 'course', 
      name: 'Digital Course', 
      icon: GraduationCap, 
      description: 'Module-based content with text, video, and resources',
      route: '/course'
    },
    { 
      id: 'masterclass', 
      name: 'Masterclass', 
      icon: TrendingUp, 
      description: 'Premium authority content for deep expertise',
      badge: 'Premium',
      route: '/masterclass'
    },
    { 
      id: 'audiocourse', 
      name: 'Audio Course', 
      icon: Radio, 
      description: 'Mobile-first spoken content series',
      route: '/course',
      comingSoon: true
    },
    { 
      id: 'custom', 
      name: 'Client Projects', 
      icon: Sparkles, 
      description: 'Platform-specific ads and promotional content',
      route: '/custom',
      comingSoon: true
    },
    { 
      id: 'legacy', 
      name: 'Legacy Assemblies', 
      icon: Heart, 
      description: 'Private archives of voices, memories, and meaning',
      badge: 'Private',
      route: '/legacy',
      comingSoon: true,
      special: true
    }
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
                <h1 className="text-2xl font-bold text-gray-900">GOAT Platform</h1>
                <p className="text-xs text-gray-600">Your Creative Studio</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{user.email}</span>
              <button
                onClick={handleLogout}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <LogOut className="w-5 h-5 mr-1" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Products</h2>
          <p className="text-lg text-gray-700 italic mb-2">Create once. Publish anywhere. Preserve forever.</p>
          <p className="text-gray-600">Select a product to begin creating</p>
        </div>

        {/* Product Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {products.map((product) => {
            const Icon = product.icon;
            const isComingSoon = product.comingSoon;
            
            return (
              <div
                key={product.id}
                className={`block p-6 rounded-lg border-2 transition-all hover:shadow-lg hover:shadow-blue-500/25 hover:-translate-y-1 ${
                  product.special
                    ? 'bg-slate-900/5 border-slate-300 hover:border-slate-400 shadow-md'
                    : isComingSoon
                    ? 'bg-gray-50 border-gray-200 opacity-75 shadow-sm'
                    : 'bg-white border-gray-200 hover:border-blue-500 shadow-md hover:shadow-blue-500/25'
                }`}
                onClick={() => {
                  if (isComingSoon) {
                    setComingSoonProduct(product);
                    setShowComingSoon(true);
                  }
                }}
              >
                {isComingSoon ? (
                  <div className="relative">
                    <div className="flex items-start justify-between mb-4">
                      <Icon className={`w-8 h-8 ${product.special ? 'text-slate-700' : 'text-gray-400'}`} />
                      <span className="text-xs px-2 py-1 rounded bg-orange-100 text-orange-700">
                        Coming Soon
                      </span>
                    </div>
                    <h3 className={`text-xl font-semibold mb-2 ${product.special ? 'text-slate-900' : 'text-gray-900'}`}>
                      {product.name}
                    </h3>
                    <p className={`text-sm ${product.special ? 'text-slate-600' : 'text-gray-600'}`}>
                      {product.description}
                    </p>
                  </div>
                ) : (
                  <Link to={product.route}>
                    <div className="flex items-start justify-between mb-4">
                      <Icon className={`w-8 h-8 ${product.special ? 'text-slate-700' : 'text-blue-600'}`} />
                      {product.badge && (
                        <span className={`text-xs px-2 py-1 rounded ${
                          product.badge === 'Flagship' ? 'bg-blue-100 text-blue-700' :
                          product.badge === 'Premium' ? 'bg-purple-100 text-purple-700' :
                          product.badge === 'Private' ? 'bg-slate-200 text-slate-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {product.badge}
                        </span>
                      )}
                    </div>
                    <h3 className={`text-xl font-semibold mb-2 ${product.special ? 'text-slate-900' : 'text-gray-900'}`}>
                      {product.name}
                    </h3>
                    <p className={`text-sm ${product.special ? 'text-slate-600' : 'text-gray-600'}`}>
                      {product.description}
                    </p>
                  </Link>
                )}
              </div>
            );
          })}
        </div>

        {/* User Stats Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Your Projects</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.yourProjects}</p>
              </div>
              <FileText className="w-12 h-12 text-blue-600 opacity-80" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">In Progress</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.inProgress}</p>
              </div>
              <Activity className="w-12 h-12 text-green-600 opacity-80" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Completed</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.completed}</p>
              </div>
              <Check className="w-12 h-12 text-purple-600 opacity-80" />
            </div>
          </div>
        </div>
      </div>

      {/* Coming Soon Modal */}
      {showComingSoon && comingSoonProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                {React.createElement(comingSoonProduct.icon, { className: "w-8 h-8 text-orange-600" })}
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {comingSoonProduct.name} - Coming Soon
              </h3>
              <p className="text-gray-600 mb-4">
                {comingSoonProduct.description}
              </p>
              <p className="text-sm text-gray-500 mb-6">
                This feature is currently in development. We're working hard to bring you the best experience possible.
              </p>
              <button
                onClick={() => setShowComingSoon(false)}
                className="w-full bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Got it
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
