import { useQuery } from '@tanstack/react-query'
import { Shield, Database, GraduationCap, TrendingUp } from 'lucide-react'
import axios from 'axios'

export function HomePage() {
  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await axios.get('/api/health')
      return data
    }
  })

  return (
    <div className="space-y-8">
      {/* HERO SECTION */}
      <div className="text-center space-y-4 py-12">
        <div className="w-24 h-24 mx-auto bg-gradient-to-r from-goat-primary to-goat-secondary rounded-full flex items-center justify-center overflow-hidden">
          <img src="/GOAT%20icons/goaticon1024.png" alt="GOAT Icon" className="w-full h-full object-cover" />
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-goat-primary to-goat-secondary bg-clip-text text-transparent tracking-tight">
          GOAT
        </h1>
        <p className="text-3xl text-slate-300 font-semibold">The Master of Legacy Preservation</p>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Teach it once. Own it forever.
          Your story. Your knowledge. Your voice. Your legacy.
          Captured. Organized. Transformed. Preserved for generations.
        </p>
        <div className="flex justify-center space-x-4 mt-8">
          <button
            onClick={() => window.location.href = '/start-actions'}
            className="bg-goat-primary text-slate-900 px-8 py-3 rounded-lg font-semibold hover:bg-goat-primary/80 transition-colors"
          >
            Get Started
          </button>
          <button
            onClick={() => window.location.href = '/menu'}
            className="border border-goat-primary text-goat-primary px-8 py-3 rounded-lg font-semibold hover:bg-goat-primary/10 transition-colors"
          >
            Watch Demo
          </button>
        </div>
      </div>

      {/* SECTION 1 — The Problem */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">Most people die twice.</h2>
        <div className="text-center space-y-4">
          <p className="text-xl text-slate-300">Once when their heart stops…</p>
          <p className="text-xl text-slate-300">And again when their knowledge disappears.</p>
          <p className="text-slate-400 max-w-2xl mx-auto mt-6">
            Your wisdom, your stories, your perspective — all of it fades when you're gone.
            Cloud platforms won't save it. Social media buries it. AI companies steal it.
            Your legacy deserves better.
          </p>
        </div>
      </div>

      {/* SECTION 2 — The GOAT Solution */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">Your Life. Digitized. Immortalized. Owned by YOU.</h2>
        <p className="text-center text-slate-400 mb-6">
          GOAT is the world's first Legacy Preservation Engine — a system that transforms everything you know into structured, timeless, exportable knowledge.
        </p>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-goat-primary">Upload anything:</h3>
            <ul className="text-slate-300 space-y-1">
              <li>• Video</li>
              <li>• Audio</li>
              <li>• Journals</li>
              <li>• Phone recordings</li>
              <li>• Notes</li>
              <li>• Letters</li>
              <li>• Interviews</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-goat-primary">GOAT processes it into:</h3>
            <ul className="text-slate-300 space-y-1">
              <li>• A book</li>
              <li>• A masterclass</li>
              <li>• A podcast</li>
              <li>• A personal archive</li>
              <li>• A life timeline</li>
              <li>• A symbolic legacy record</li>
              <li>• An NFT-backed inheritance asset</li>
            </ul>
          </div>
        </div>
        <p className="text-center text-slate-400 mt-6">All automatically. All beautifully organized. All owned by you.</p>
      </div>

      {/* SECTION 3 — Why GOAT is Unlike Anything Else */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">Why GOAT is Unlike Anything Else</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-goat-primary">1. It captures your voice — and keeps it.</h3>
              <p className="text-slate-400">GOAT builds content in your tone, not generic AI fluff.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-goat-primary">2. It creates multiple products from one upload.</h3>
              <p className="text-slate-400">One file → full legacy ecosystem.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-goat-primary">3. It lives on your machine, not in the cloud.</h3>
              <p className="text-slate-400">Your knowledge stays private, encrypted, local.</p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-goat-primary">4. It works with CertSig and DALS for absolute authenticity.</h3>
              <p className="text-slate-400">Every asset GOAT creates can be timestamped, sealed, and cryptographically anchored.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-goat-primary">5. It becomes part of your family.</h3>
              <p className="text-slate-400">Your descendants inherit a clean, organized record of your life — your way of thinking, your stories, your wisdom.</p>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 4 — Who GOAT Is For */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">Who GOAT Is For</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-slate-700 rounded-lg">
            <h3 className="font-bold text-goat-primary mb-2">Creators</h3>
            <p className="text-sm text-slate-400">Turn your ideas into books and content that last forever.</p>
          </div>
          <div className="text-center p-4 bg-slate-700 rounded-lg">
            <h3 className="font-bold text-goat-primary mb-2">Entrepreneurs</h3>
            <p className="text-sm text-slate-400">Preserve your hard-earned knowledge as company assets.</p>
          </div>
          <div className="text-center p-4 bg-slate-700 rounded-lg">
            <h3 className="font-bold text-goat-primary mb-2">Families</h3>
            <p className="text-sm text-slate-400">Capture stories, wisdom, and history before they're gone.</p>
          </div>
          <div className="text-center p-4 bg-slate-700 rounded-lg">
            <h3 className="font-bold text-goat-primary mb-2">Leaders</h3>
            <p className="text-sm text-slate-400">Ensure your vision, philosophy, and playbook survive.</p>
          </div>
        </div>
        <p className="text-center text-slate-400 mt-6">Anyone who refuses to be forgotten.</p>
      </div>

      {/* SECTION 5 — What GOAT Can Build for You */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">From a single video, GOAT creates:</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <ul className="text-slate-300 space-y-1">
              <li>• Full written book</li>
              <li>• Chapter summaries</li>
              <li>• Audiobook files</li>
              <li>• Masterclass modules</li>
              <li>• Podcast episode</li>
              <li>• Quote cards</li>
              <li>• Legacy archive entry</li>
            </ul>
          </div>
          <div className="space-y-2">
            <ul className="text-slate-300 space-y-1">
              <li>• NFT identity certificate</li>
            </ul>
          </div>
        </div>
        <p className="text-center text-slate-400 mt-6">This is more than content creation. It's knowledge multiplication.</p>
      </div>

      {/* SECTION 6 — The Future-Proof Engine */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">The Future-Proof Engine</h2>
        <p className="text-center text-slate-400 mb-6">GOAT integrates with:</p>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <ul className="text-slate-300 space-y-1">
              <li>• DALS (Digital Asset Logistics System)</li>
              <li>• CertSig NFT Engine</li>
              <li>• UCM + Caleon AI</li>
            </ul>
          </div>
          <div className="space-y-2">
            <p className="text-slate-400">This gives you:</p>
            <ul className="text-slate-300 space-y-1">
              <li>• Absolute ownership</li>
              <li>• Time-anchored authenticity</li>
              <li>• Encrypted storage</li>
              <li>• Immutable legacy records</li>
            </ul>
          </div>
        </div>
        <p className="text-center text-slate-400 mt-6">No cloud. No data mining. No expiration date.</p>
      </div>

      {/* SECTION 7 — Plans & Pricing */}
      <div className="goat-card">
        <h2 className="text-3xl font-bold mb-6 text-center">Plans & Pricing</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-6 bg-slate-700 rounded-lg text-center">
            <h3 className="text-xl font-bold text-goat-primary mb-2">GOAT Starter</h3>
            <p className="text-2xl font-bold mb-4">$129</p>
            <p className="text-sm text-slate-400 mb-4">Perfect for creators and storytellers.</p>
            <ul className="text-sm text-slate-300 space-y-1 mb-4">
              <li>• Book builder</li>
              <li>• Transcript processor</li>
              <li>• Export to PDF</li>
            </ul>
            <button className="goat-button w-full">Choose Plan</button>
          </div>
          <div className="p-6 bg-slate-700 rounded-lg text-center">
            <h3 className="text-xl font-bold text-goat-primary mb-2">GOAT Creator Pro</h3>
            <p className="text-2xl font-bold mb-4">$499</p>
            <p className="text-sm text-slate-400 mb-4">Your full content engine.</p>
            <ul className="text-sm text-slate-300 space-y-1 mb-4">
              <li>• Masterclass builder</li>
              <li>• Audiobook creation</li>
              <li>• NFT certificates</li>
              <li>• Personal archive</li>
            </ul>
            <button className="goat-button w-full">Choose Plan</button>
          </div>
          <div className="p-6 bg-slate-700 rounded-lg text-center">
            <h3 className="text-xl font-bold text-goat-primary mb-2">GOAT Business Master</h3>
            <p className="text-2xl font-bold mb-4">$999</p>
            <p className="text-sm text-slate-400 mb-4">Turn your knowledge into revenue.</p>
            <ul className="text-sm text-slate-300 space-y-1 mb-4">
              <li>• Licensing tools</li>
              <li>• Brand templates</li>
              <li>• Content packaging</li>
            </ul>
            <button className="goat-button w-full">Choose Plan</button>
          </div>
          <div className="p-6 bg-slate-700 rounded-lg text-center">
            <h3 className="text-xl font-bold text-goat-primary mb-2">GOAT Legacy Builder</h3>
            <p className="text-2xl font-bold mb-4">$2,500</p>
            <p className="text-sm text-slate-400 mb-4">For families, founders, and leaders.</p>
            <ul className="text-sm text-slate-300 space-y-1 mb-4">
              <li>• Whole-life timeline</li>
              <li>• Multi-media vault</li>
              <li>• Heirloom NFT bundle</li>
              <li>• Legacy edition export</li>
            </ul>
            <button className="goat-button w-full">Choose Plan</button>
          </div>
        </div>
        <div className="text-center mt-6">
          <button className="goat-button mr-4">Talk to an Expert</button>
        </div>
      </div>

      {/* SECTION 8 — The Guarantee */}
      <div className="goat-card text-center">
        <h2 className="text-3xl font-bold mb-6">Your Legacy Will Outlive You. Or you don't pay.</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          If GOAT doesn't build a legacy your family or audience would be proud of, we refund you.
          No questions. No conditions. We're not selling software. We're preserving lives.
        </p>
      </div>

      {/* SECTION 9 — Closing Statement */}
      <div className="goat-card text-center">
        <h2 className="text-3xl font-bold mb-6">This isn't about content. This is about immortality.</h2>
        <p className="text-slate-400 max-w-2xl mx-auto mb-6">
          There's only one you. GOAT makes sure the world never loses you.
        </p>
        <button
          onClick={() => window.location.href = '/start-actions'}
          className="bg-goat-primary text-slate-900 px-8 py-3 rounded-lg font-semibold hover:bg-goat-primary/80 transition-colors text-lg"
        >
          Start Building Your Legacy
        </button>
      </div>
    </div>
  )
}
