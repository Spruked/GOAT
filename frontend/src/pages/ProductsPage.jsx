import React, { useState, useEffect } from 'react';
import { 
  Mic, BookOpen, Headphones, GraduationCap, TrendingUp, Radio, 
  Sparkles, Heart, FileText, Activity, Check, LogOut 
} from 'lucide-react';

export default function ProductsPage() {
  const [user, setUser] = useState(null);
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
      description: 'Module-based learning with text, video, and resources',
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
      description: 'Mobile-first spoken learning series',
      route: '/audio-course'
    },
    { 
      id: 'custom', 
      name: 'Custom Projects', 
      icon: Sparkles, 
      description: 'Platform-specific ads and promotional content',
      route: '/custom'
    },
    { 
      id: 'legacy', 
      name: 'Legacy Assemblies', 
      icon: Heart, 
      description: 'Private archives of voices, memories, and meaning',
      badge: 'Private',
      route: '/legacy',
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
          <p className="text-gray-600">Select a product to begin creating</p>
        </div>

        {/* Product Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {products.map((product) => {
            const Icon = product.icon;
            return (
              <a
                key={product.id}
                href={product.route}
                className={`block p-6 rounded-lg border-2 transition-all hover:shadow-lg ${
                  product.special
                    ? 'bg-slate-900/5 border-slate-300 hover:border-slate-400'
                    : 'bg-white border-gray-200 hover:border-blue-500'
                }`}
              >
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
              </a>
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
    </div>
  );
}
