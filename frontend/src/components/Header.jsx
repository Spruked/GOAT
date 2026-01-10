import { Link } from 'react-router-dom'
import { BookOpen, Database, GraduationCap, Shield, Archive, Package, FileText } from 'lucide-react'

export function Header() {
  return (
    <header className="bg-slate-800 border-b border-slate-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <img 
              src="/Goatvault64.ico" 
              alt="GOAT Vault" 
              className="w-10 h-10 rounded-full"
            />
            <div>
              <h1 className="text-xl font-bold tracking-tight">GOAT v2.1</h1>
              <p className="text-xs text-slate-400">The master of legacy preservation</p>
            </div>
          </Link>
          
          <nav className="flex items-center gap-6">
            <Link to="/" className="flex items-center gap-2 hover:text-goat-primary transition font-semibold">
              <span>Home</span>
            </Link>
            <Link to="/collector" className="flex items-center gap-2 hover:text-goat-primary transition">
              <Database size={18} />
              <span>Collect</span>
            </Link>
            <Link to="/packages" className="flex items-center gap-2 hover:text-goat-primary transition">
              <Package size={18} />
              <span>Products</span>
            </Link>
            <Link to="/vault" className="flex items-center gap-2 hover:text-goat-primary transition">
              <Shield size={18} />
              <span>Vault</span>
            </Link>
            <Link to="/profile" className="flex items-center gap-2 hover:text-goat-primary transition">
              <BookOpen size={18} />
              <span>Profile</span>
            </Link>
            <Link to="/book-builder" className="flex items-center gap-2 hover:text-goat-primary transition">
              <FileText size={18} />
              <span>Book Builder</span>
            </Link>
            <Link to="/project-panel" className="flex items-center gap-2 hover:text-goat-primary transition">
              <Archive size={18} />
              <span>Project</span>
            </Link>
            <Link to="/cart" className="flex items-center gap-2 hover:text-goat-primary transition font-semibold">
              <span role="img" aria-label="cart">🛒</span>
              <span>Cart</span>
            </Link>
            <Link to="/checkout" className="flex items-center gap-2 hover:text-goat-primary transition font-semibold">
              <span role="img" aria-label="checkout">💳</span>
              <span>Checkout</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
