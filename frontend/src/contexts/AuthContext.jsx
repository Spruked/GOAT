import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  // Configure axios defaults
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }, [token])

  // Load user on mount if token exists
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          // Configure authorization header before making request
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          const { data } = await axios.get('/api/v1/auth/me')
          setUser(data)
        } catch (error) {
          // Token is invalid, remove it
          localStorage.removeItem('token')
          setToken(null)
        }
      }
      setLoading(false)
    }

    loadUser()
  }, [token])

  const login = async (username, password) => {
    const { data } = await axios.post('/api/v1/auth/login', {
      username,
      password
    })
    
    localStorage.setItem('token', data.access_token)
    setToken(data.access_token)
    
    // Set authorization header before fetching user data
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
    
    // Fetch user data
    const { data: userData } = await axios.get('/api/v1/auth/me')
    setUser(userData)
    
    return userData
  }

  const signup = async (username, email, password) => {
    const { data } = await axios.post('/api/v1/auth/signup', {
      username,
      email,
      password
    })
    
    localStorage.setItem('token', data.access_token)
    setToken(data.access_token)
    
    // Set authorization header before fetching user data
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
    
    // Fetch user data
    const { data: userData } = await axios.get('/api/v1/auth/me')
    setUser(userData)
    
    return userData
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
