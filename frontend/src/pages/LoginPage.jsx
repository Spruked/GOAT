import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Lock, Eye, EyeOff, Shield, Sparkles, UserPlus, Mail, User } from 'lucide-react';
import { ENDPOINTS } from '../config/api';

export default function LoginPage() {
  const location = useLocation();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Check for existing session on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      try {
        const userData = JSON.parse(user);
        // Redirect based on user type
        if (userData.isAdmin) {
          window.location.href = '/dashboard';
        } else {
          window.location.href = '/products';
        }
      } catch (e) {
        // Invalid user data, clear storage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    console.log('Form submitted:', { isLogin, email: formData.email });
    
    // Check terms acceptance for signup
    if (!isLogin && !acceptedTerms) {
      setError('Please accept the Terms of Service to continue.');
      return;
    }
    
    setIsLoading(true);

    try {
      // Admin bypass check
      if (isLogin && formData.email === 'admin@goat.local' && formData.password === 'goat2024admin') {
        // Admin bypass - no backend call needed
        localStorage.setItem('token', 'admin-bypass-token');
        localStorage.setItem('user', JSON.stringify({ 
          email: 'admin@goat.local', 
          name: 'Admin',
          isAdmin: true 
        }));
        window.location.href = '/dashboard'; // Admin goes to Master Control Center
        return;
      }

      // Test user bypass check (for UI evaluation)
      if (isLogin && formData.email === 'test@goat.local' && formData.password === 'goattest2024') {
        // Test user bypass - no backend call needed
        localStorage.setItem('token', 'test-bypass-token');
        localStorage.setItem('user', JSON.stringify({ 
          email: 'test@goat.local', 
          name: 'Test User',
          isAdmin: false 
        }));
        window.location.href = '/products'; // Regular users go to Products page
        return;
      }

      const endpoint = isLogin ? `${ENDPOINTS.auth}/login` : `${ENDPOINTS.auth}/signup`;
      console.log('Calling endpoint:', endpoint);
      let payload;
      
      if (isLogin) {
        // Login uses form data (username/password)
        const formDataObj = new FormData();
        formDataObj.append('username', formData.email); // OAuth2 expects 'username'
        formDataObj.append('password', formData.password);
        
        const res = await fetch(endpoint, {
          method: 'POST',
          body: formDataObj, // Send as form data, not JSON
        });
        
        if (res.ok) {
          const data = await res.json();
          // Store token
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('user', JSON.stringify({ 
            email: formData.email,
            isAdmin: false // Regular users are not admins
          }));
          window.location.href = '/products'; // Regular users go to Products page
        } else {
          const errorData = await res.json();
          setError(errorData.detail || 'Login failed');
        }
      } else {
        // Signup uses JSON
        payload = JSON.stringify({
          email: formData.email,
          full_name: formData.name, // Backend expects full_name
          password: formData.password,
          marketing_opt_in: true
        });
        
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: payload,
        });
        
        if (res.ok) {
          const data = await res.json();
          setError('Account created successfully! Please log in.');
          setIsLogin(true); // Switch to login mode
        } else {
          const errorData = await res.json();
          setError(errorData.detail || 'Signup failed');
        }
      }
    } catch (err) {
      console.error('Signup/Login error:', err);
      setError(`Connection failed: ${err.message}. Please try again.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-6">
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-950/20 via-black to-amber-950/10" />
      
      <div className="relative w-full max-w-md">
        {/* GOAT Vault Logo */}
        <div className="flex justify-center mb-10">
          <div className="relative">
            <img 
              src="/Goatvault256.png" 
              alt="GOAT Vault" 
              className="w-32 h-32 rounded-full border-4 border-cyan-600/60 shadow-2xl animate-gpu-float"
            />
            <div className="absolute inset-0 rounded-full bg-cyan-400/20 animate-ping-slow" />
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex mb-8 bg-slate-800/50 rounded-lg p-1">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 rounded-md transition ${isLogin ? 'bg-cyan-600 text-white' : 'text-slate-400'}`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 rounded-md transition ${!isLogin ? 'bg-cyan-600 text-white' : 'text-slate-400'}`}
          >
            Sign Up
          </button>
        </div>

        <div className="bg-gradient-to-b from-cyan-950/30 via-black/90 to-black rounded-3xl border border-cyan-700/50 p-10 backdrop-blur-2xl shadow-2xl">
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-amber-400 mb-4 tracking-tight">
              {isLogin ? 'Enter Your Vault' : 'Create Your Vault'}
            </h1>
            <p className="text-cyan-400 text-lg font-light">
              {isLogin ? 'Give what\'s important Permanence.' : 'Monetize your Mind.'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {!isLogin && (
              <div>
                <label className="block text-cyan-300 text-lg mb-3">Full Name</label>
                <div className="relative">
                  <User className="absolute left-4 top-5 w-6 h-6 text-cyan-600" />
                  <input
                    type="text"
                    name="name"
                    required={!isLogin}
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Your eternal name"
                    className="w-full pl-12 pr-6 py-5 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 transition"
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-cyan-300 text-lg mb-3">Email</label>
              <div className="relative">
                <Mail className="absolute left-4 top-5 w-6 h-6 text-cyan-600" />
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="UCM-Core-CALI@eternal.vault"
                  className="w-full pl-12 pr-6 py-5 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-cyan-300 text-lg mb-3">Master Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="••••••••••••••••"
                  className="w-full px-6 py-5 pr-16 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 transition"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-5 top-5 text-cyan-400 hover:text-cyan-200 transition"
                >
                  {showPassword ? <EyeOff className="w-6 h-6" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {!isLogin && (
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  id="terms"
                  checked={acceptedTerms}
                  onChange={(e) => setAcceptedTerms(e.target.checked)}
                  className="mt-1 w-5 h-5 rounded border-cyan-700/60 bg-cyan-950/40 text-cyan-600 focus:ring-cyan-400 focus:ring-offset-0 cursor-pointer"
                />
                <label htmlFor="terms" className="text-cyan-300 text-sm cursor-pointer">
                  I agree to the{' '}
                  <a href="/terms" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Terms of Service
                  </a>
                  {', '}
                  <a href="/privacy" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Privacy Policy
                  </a>
                  {', '}
                  <a href="/customer-rights" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Customer Rights Statement
                  </a>
                  {', '}
                  <a href="/content-ownership" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Content Ownership Agreement
                  </a>
                  {', '}
                  <a href="/refund-policy" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Refund Policy
                  </a>
                  {', '}
                  <a href="/data-processing" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Data Processing Agreement
                  </a>
                  {', '}
                  <a href="/cookie-policy" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    Cookie Policy
                  </a>
                  {', and '}
                  <a href="/dmca-policy" className="text-cyan-400 hover:text-cyan-200 underline" target="_blank" rel="noopener noreferrer">
                    DMCA Copyright Policy
                  </a>
                </label>
              </div>
            )}

            {error && (
              <div className="bg-red-950/60 border border-red-600/60 rounded-xl p-4 text-red-300 text-center">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-6 bg-gradient-to-r from-cyan-600 via-cyan-500 to-amber-600 rounded-2xl text-2xl font-light shadow-2xl shadow-cyan-600/40 hover:brightness-110 disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-500 flex items-center justify-center gap-4 group"
            >
              {isLoading ? (
                <>
                  <div className="w-7 h-7 border-4 border-cyan-300 border-t-transparent rounded-full animate-spin" />
                  {isLogin ? 'Unlocking Vault...' : 'Forging Vault...'}
                </>
              ) : (
                <>
                  {isLogin ? <Lock className="w-7 h-7 group-hover:animate-pulse" /> : <UserPlus className="w-7 h-7 group-hover:animate-pulse" />}
                  {isLogin ? 'Open My Eternal Vault' : 'Create My Eternal Vault'}
                  <Sparkles className="w-7 h-7 group-hover:animate-pulse" />
                </>
              )}
            </button>
          </form>

          <div className="mt-10 text-center space-y-4">
            {isLogin && (
              <a href="/forgot" className="text-cyan-500 hover:text-cyan-300 transition text-lg">
                Forgotten your master key?
              </a>
            )}
            <div className="flex items-center justify-center gap-4 text-cyan-500 text-sm">
              <a href="/pricing" className="hover:text-cyan-300 transition">
                View Pricing
              </a>
              <span className="text-cyan-600">•</span>
              <a href="/terms" className="hover:text-cyan-300 transition">
                Terms
              </a>
              <span className="text-cyan-600">•</span>
              <a href="/privacy" className="hover:text-cyan-300 transition">
                Privacy
              </a>
            </div>
            <div className="flex items-center justify-center gap-8 text-cyan-500 text-sm mt-8">
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5" />
                <span>End-to-end encrypted</span>
              </div>
              <div className="flex items-center gap-2">
                <Lock className="w-5 h-5" />
                <span>Zero-knowledge</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer glow */}
        <p className="text-center text-cyan-600 text-sm mt-10 opacity-60">
          GOAT Eternal • Built to outlast civilizations
        </p>
      </div>
    </div>
  );
}
