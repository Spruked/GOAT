import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  Download,
  FileText,
  Image,
  Video,
  Music,
  Package,
  ExternalLink,
  Star,
  Calendar,
  CheckCircle,
  Clock
} from 'lucide-react'
import axios from 'axios'

export function ProductsTab({ user }) {
  const [selectedCategory, setSelectedCategory] = useState('all')

  // Mock data for products - in real app, this would come from API
  const products = [
    {
      id: 1,
      title: "Ultimate Resume 2025",
      type: "PDF",
      category: "document",
      description: "AI-enhanced resume with modern design and ATS optimization",
      preview_url: "/previews/resume-123.pdf",
      download_url: "/downloads/resume-123.pdf",
      file_size: "2.3 MB",
      created_at: "2025-11-28T10:30:00Z",
      status: "ready",
      tags: ["resume", "professional", "ATS-optimized"],
      download_count: 42,
      is_favorite: true
    },
    {
      id: 2,
      title: "Business Card Design",
      type: "PNG",
      category: "image",
      description: "Professional business card design with your branding",
      preview_url: "/previews/business-card-456.png",
      download_url: "/downloads/business-card-456.png",
      file_size: "1.8 MB",
      created_at: "2025-11-27T14:20:00Z",
      status: "ready",
      tags: ["business", "branding", "design"],
      download_count: 18,
      is_favorite: false
    },
    {
      id: 3,
      title: "Product Demo Video",
      type: "MP4",
      category: "video",
      description: "AI-generated product demonstration video",
      preview_url: "/previews/demo-video-789.mp4",
      download_url: "/downloads/demo-video-789.mp4",
      file_size: "45.2 MB",
      created_at: "2025-11-26T09:15:00Z",
      status: "processing",
      tags: ["demo", "marketing", "video"],
      download_count: 0,
      is_favorite: false
    },
    {
      id: 4,
      title: "Brand Guidelines PDF",
      type: "PDF",
      category: "document",
      description: "Complete brand guidelines and style guide",
      preview_url: "/previews/brand-guide-101.pdf",
      download_url: "/downloads/brand-guide-101.pdf",
      file_size: "8.7 MB",
      created_at: "2025-11-25T16:45:00Z",
      status: "ready",
      tags: ["branding", "guidelines", "design"],
      download_count: 7,
      is_favorite: true
    }
  ]

  const categories = [
    { id: 'all', label: 'All Products', count: products.length },
    { id: 'document', label: 'Documents', icon: FileText, count: products.filter(p => p.category === 'document').length },
    { id: 'image', label: 'Images', icon: Image, count: products.filter(p => p.category === 'image').length },
    { id: 'video', label: 'Videos', icon: Video, count: products.filter(p => p.category === 'video').length },
    { id: 'audio', label: 'Audio', icon: Music, count: products.filter(p => p.category === 'audio').length }
  ]

  const filteredProducts = selectedCategory === 'all'
    ? products
    : products.filter(p => p.category === selectedCategory)

  const getTypeIcon = (type) => {
    const typeMap = {
      'PDF': FileText,
      'PNG': Image,
      'JPG': Image,
      'MP4': Video,
      'MP3': Music
    }
    return typeMap[type] || Package
  }

  const getStatusColor = (status) => {
    return status === 'ready' ? 'text-green-400' : 'text-blue-400'
  }

  const getStatusIcon = (status) => {
    return status === 'ready' ? CheckCircle : Clock
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">My Products</h1>
          <p className="text-slate-400 mt-1">Generated assets and downloadable content</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-goat-primary">{products.filter(p => p.status === 'ready').length}</div>
          <div className="text-sm text-slate-400">Ready to download</div>
        </div>
      </div>

      {/* Category Filters */}
      <div className="goat-card">
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => {
            const Icon = category.icon
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center ${
                  selectedCategory === category.id
                    ? 'bg-goat-primary text-slate-900'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {Icon && <Icon size={14} className="mr-2" />}
                {category.label}
                <span className="ml-2 px-2 py-0.5 bg-slate-600 rounded-full text-xs">
                  {category.count}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Products Grid */}
      {filteredProducts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map((product) => {
            const TypeIcon = getTypeIcon(product.type)
            const StatusIcon = getStatusIcon(product.status)
            const statusColor = getStatusColor(product.status)

            return (
              <div key={product.id} className="goat-card group">
                {/* Preview */}
                <div className="aspect-video bg-slate-700 rounded-lg mb-4 flex items-center justify-center relative overflow-hidden">
                  {product.preview_url ? (
                    <div className="w-full h-full bg-gradient-to-br from-goat-primary/20 to-goat-secondary/20 flex items-center justify-center">
                      <TypeIcon size={48} className="text-goat-primary" />
                    </div>
                  ) : (
                    <TypeIcon size={48} className="text-slate-400" />
                  )}

                  {/* Favorite */}
                  {product.is_favorite && (
                    <div className="absolute top-2 right-2">
                      <Star size={16} className="text-yellow-400" fill="currentColor" />
                    </div>
                  )}

                  {/* Status */}
                  <div className={`absolute bottom-2 left-2 flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium bg-slate-800/80 ${statusColor}`}>
                    <StatusIcon size={12} />
                    <span className="capitalize">{product.status}</span>
                  </div>
                </div>

                {/* Content */}
                <div className="space-y-3">
                  <div>
                    <h3 className="font-semibold text-lg">{product.title}</h3>
                    <p className="text-sm text-slate-400">{product.description}</p>
                  </div>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1">
                    {product.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-slate-700 text-xs rounded-full text-slate-300"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Meta */}
                  <div className="flex items-center justify-between text-sm text-slate-400">
                    <div className="flex items-center space-x-4">
                      <span>{product.type}</span>
                      <span>{product.file_size}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Download size={14} />
                      <span>{product.download_count}</span>
                    </div>
                  </div>

                  {/* Date */}
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <Calendar size={12} />
                    <span>{new Date(product.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-2 mt-4">
                  {product.status === 'ready' ? (
                    <>
                      <button className="flex-1 bg-goat-primary text-slate-900 px-4 py-2 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors flex items-center justify-center">
                        <Download size={16} className="mr-2" />
                        Download
                      </button>
                      <button className="p-2 bg-slate-700 text-slate-300 rounded-lg hover:bg-slate-600 transition-colors">
                        <ExternalLink size={16} />
                      </button>
                    </>
                  ) : (
                    <div className="w-full bg-slate-700 text-slate-400 px-4 py-2 rounded-lg font-medium flex items-center justify-center">
                      <Clock size={16} className="mr-2" />
                      Processing...
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <EmptyProductsState selectedCategory={selectedCategory} />
      )}

      {/* Usage Stats */}
      <div className="goat-card">
        <h2 className="text-xl font-bold mb-4">Usage Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-goat-primary mb-1">
              {products.reduce((sum, p) => sum + p.download_count, 0)}
            </div>
            <div className="text-sm text-slate-400">Total Downloads</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-400 mb-1">
              {products.filter(p => p.status === 'ready').length}
            </div>
            <div className="text-sm text-slate-400">Ready Products</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-400 mb-1">
              {products.filter(p => p.status === 'processing').length}
            </div>
            <div className="text-sm text-slate-400">In Progress</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function EmptyProductsState({ selectedCategory }) {
  const categoryName = selectedCategory === 'all' ? 'products' : selectedCategory + 's'

  return (
    <div className="text-center py-20">
      <Package size={64} className="text-slate-600 mx-auto mb-4" />
      <h3 className="text-xl font-medium mb-2">No {categoryName} yet</h3>
      <p className="text-slate-400 mb-6">
        Upload some files and let GOAT create amazing {categoryName} for you
      </p>
      <button className="bg-goat-primary text-slate-900 px-6 py-3 rounded-lg font-medium hover:bg-goat-primary/80 transition-colors">
        Start Creating
      </button>
    </div>
  )
}