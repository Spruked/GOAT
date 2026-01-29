import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import {
  BookOpen,
  FileText,
  Download,
  Eye,
  Edit,
  Trash2,
  RefreshCw,
  Plus,
  Search,
  Filter
} from 'lucide-react'

export function BooksTab() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedBook, setSelectedBook] = useState(null)
  const queryClient = useQueryClient()

  // Get books stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['books-stats'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/books/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data
    }
  })

  // Get books list
  const { data: books, isLoading: booksLoading } = useQuery({
    queryKey: ['books-list'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const { data } = await axios.get('/api/v1/admin/books', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return data.books || []
    }
  })

  const filteredBooks = books?.filter(book =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.author.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  if (statsLoading || booksLoading) {
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
          <BookOpen className="w-6 h-6" />
          Books Management
        </h2>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
            <Plus className="w-4 h-4" />
            Add Book
          </button>
          <button
            onClick={() => queryClient.invalidateQueries(['books-stats', 'books-list'])}
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
              <p className="text-gray-400 text-sm">Total Books</p>
              <p className="text-2xl font-bold text-white">{stats?.total_books || 0}</p>
            </div>
            <BookOpen className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Published</p>
              <p className="text-2xl font-bold text-white">{stats?.published_books || 0}</p>
            </div>
            <FileText className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Downloads</p>
              <p className="text-2xl font-bold text-white">{stats?.total_downloads || 0}</p>
            </div>
            <Download className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Revenue</p>
              <p className="text-2xl font-bold text-white">${stats?.total_revenue || 0}</p>
            </div>
            <Eye className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <input
          type="text"
          placeholder="Search books..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Books List */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Books ({filteredBooks.length})</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {filteredBooks.map((book) => (
            <div key={book.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-16 bg-gray-600 rounded-lg flex items-center justify-center">
                    <BookOpen className="w-6 h-6 text-gray-300" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{book.title}</h4>
                    <p className="text-gray-400">by {book.author}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>{book.genre}</span>
                      <span>{book.pages} pages</span>
                      <span>{book.downloads} downloads</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        book.status === 'published' ? 'bg-green-100 text-green-800' :
                        book.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {book.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-2 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-gray-600">
                    <Eye className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-green-400 hover:text-green-300 rounded-lg hover:bg-gray-600">
                    <Edit className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-red-400 hover:text-red-300 rounded-lg hover:bg-gray-600">
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
          {filteredBooks.length === 0 && (
            <div className="p-6 text-center text-gray-400">
              No books found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}