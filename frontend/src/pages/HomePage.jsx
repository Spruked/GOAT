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
      {/* Hero Section */}
      <div className="text-center space-y-4 py-12">
        <div className="w-24 h-24 mx-auto bg-gradient-to-r from-goat-primary to-goat-secondary rounded-full flex items-center justify-center">
          <span className="text-5xl font-bold text-slate-900">G</span>
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-goat-primary to-goat-secondary bg-clip-text text-transparent">
          GOAT v2.1
        </h1>
        <p className="text-2xl text-slate-300">The Proven Teacher</p>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Turn any NFT into a self-improving, AI-powered teacher that verifies learning on-chain.
          Every lesson is signed. Every skill is provable. Every teacher is accountable.
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <FeatureCard
          icon={<Database className="w-8 h-8" />}
          title="Glyph IDs"
          description="Unique, cryptographically signed identifiers for every piece of knowledge"
          color="from-blue-500 to-cyan-500"
        />
        <FeatureCard
          icon={<Shield className="w-8 h-8" />}
          title="Immutable Vault"
          description="AES-256 encrypted storage with complete audit trails"
          color="from-purple-500 to-pink-500"
        />
        <FeatureCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="On-Chain Anchoring"
          description="Merkle roots anchored on Polygon for trustless verification"
          color="from-orange-500 to-red-500"
        />
        <FeatureCard
          icon={<GraduationCap className="w-8 h-8" />}
          title="Adaptive Teaching"
          description="AI-powered personalized learning paths and quizzes"
          color="from-green-500 to-emerald-500"
        />
      </div>

      {/* Stats */}
      {health && (
        <div className="goat-card">
          <h2 className="text-2xl font-bold mb-4">Platform Stats</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              label="Total Glyphs"
              value={health.vault?.total_glyphs || 0}
            />
            <StatCard
              label="Verified"
              value={health.vault?.verified_count || 0}
            />
            <StatCard
              label="Status"
              value={health.status}
              highlight
            />
            <StatCard
              label="Version"
              value="2.1.0"
            />
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="goat-card">
        <h2 className="text-2xl font-bold mb-4">Quick Start</h2>
        <div className="grid md:grid-cols-4 gap-4">
          <QuickAction
            title="Collect NFT Knowledge"
            description="Ingest NFTs from IPFS, OpenSea, or on-chain"
            link="/collect"
            buttonText="Start Collecting"
          />
          <QuickAction
            title="Start Learning"
            description="Get personalized AI-powered lessons and quizzes"
            link="/learn"
            buttonText="Begin Learning"
          />
          <QuickAction
            title="Explore Vault"
            description="View cryptographic proofs and glyph provenance"
            link="/vault"
            buttonText="Open Vault"
          />
          <QuickAction
            title="Forge Immortal Vault"
            description="Create permanent, immutable storage packages"
            link="/vault-forge"
            buttonText="Forge Vault"
          />
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description, color }) {
  return (
    <div className="goat-card hover:scale-105 transition-transform cursor-pointer">
      <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-slate-400 text-sm">{description}</p>
    </div>
  )
}

function StatCard({ label, value, highlight }) {
  return (
    <div className="text-center">
      <div className={`text-2xl font-bold ${highlight ? 'text-goat-primary' : 'text-white'}`}>
        {value}
      </div>
      <div className="text-sm text-slate-400">{label}</div>
    </div>
  )
}

function QuickAction({ title, description, link, buttonText }) {
  return (
    <div className="bg-slate-700 rounded-lg p-4 space-y-3">
      <h3 className="font-bold">{title}</h3>
      <p className="text-sm text-slate-400">{description}</p>
      <a href={link}>
        <button className="goat-button w-full">
          {buttonText}
        </button>
      </a>
    </div>
  )
}
