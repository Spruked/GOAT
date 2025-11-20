import { useState } from 'react'
import axios from 'axios'

export function VaultForgePage() {
  const [projectName, setProjectName] = useState('')
  const [tier, setTier] = useState('basic')
  const [autoUpload, setAutoUpload] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const tiers = [
    { id: 'basic', name: 'Vault Basic', price: '$29', desc: 'IPFS only', features: ['IPFS storage', 'Basic metadata'] },
    { id: 'pro', name: 'Vault Pro', price: '$69', desc: 'IPFS + Arweave', features: ['IPFS + Arweave', 'Multi-gateway pins', 'Compression'] },
    { id: 'immortal', name: 'Vault Immortal', price: '$129', desc: 'IPFS + Arweave + Filecoin', features: ['All chains', '10+ year Filecoin deal', '3-node backup'] },
    { id: 'dynasty', name: 'Vault Dynasty', price: '$299', desc: 'All + TrueMark GDIS', features: ['Everything above', 'TrueMark .go domain', 'GDIS identity linking', 'White-label vault'] }
  ]

  const handleCreate = async () => {
    if (!projectName.trim()) return

    setLoading(true)
    try {
      const { data } = await axios.post('/api/vault-forge/create', {
        project_name: projectName,
        tier,
        deliverables_path: './deliverables',
        auto_upload: autoUpload
      })
      setResult(data)
    } catch (error) {
      console.error('Vault creation failed:', error)
      setResult({ success: false, message: 'Failed to create vault' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">GOAT Vault Forge</h1>
        <p className="text-xl text-slate-300">Make Your Empire Immortal</p>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Turn your GOAT-created masterclass, audiobook, or coaching empire into an immutable,
          CertSig-ready, TrueMark-linked legacy package.
        </p>
      </div>

      <div className="goat-card max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-6">Create Your Legacy Vault</h2>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Project Name</label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="e.g., My Masterclass Empire"
              className="goat-input w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-4">Vault Tier</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {tiers.map((t) => (
                <div
                  key={t.id}
                  onClick={() => setTier(t.id)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    tier === t.id
                      ? 'border-goat-primary bg-goat-primary/10'
                      : 'border-slate-600 hover:border-slate-500'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold">{t.name}</h3>
                    <span className="text-goat-primary font-bold">{t.price}</span>
                  </div>
                  <p className="text-sm text-slate-400 mb-2">{t.desc}</p>
                  <ul className="text-xs text-slate-500 space-y-1">
                    {t.features.map((feature, i) => (
                      <li key={i}>• {feature}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {(tier !== 'basic') && (
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="autoUpload"
                checked={autoUpload}
                onChange={(e) => setAutoUpload(e.target.checked)}
                className="rounded"
              />
              <label htmlFor="autoUpload" className="text-sm">
                Auto-upload to permanent storage (IPFS, Arweave, Filecoin)
              </label>
            </div>
          )}

          <button
            onClick={handleCreate}
            disabled={loading || !projectName.trim()}
            className="goat-button w-full disabled:opacity-50"
          >
            {loading ? 'Forging Vault...' : 'Forge Immortal Vault'}
          </button>
        </div>

        {result && (
          <div className={`mt-6 p-4 rounded-lg ${
            result.success ? 'bg-green-900/20 border border-green-500' : 'bg-red-900/20 border border-red-500'
          }`}>
            <h3 className={`font-bold ${result.success ? 'text-green-400' : 'text-red-400'}`}>
              {result.success ? 'Vault Created!' : 'Error'}
            </h3>
            <p className="text-sm mt-2">{result.message}</p>
            {result.vault_zip && (
              <p className="text-sm mt-2">Download: {result.vault_zip}</p>
            )}
            {result.auto_upload && (
              <p className="text-sm mt-2 text-blue-400">Auto-upload enabled - permanent storage initiated</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}