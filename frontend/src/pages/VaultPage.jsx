import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Shield, Search, ExternalLink } from 'lucide-react'
import axios from 'axios'

export function VaultPage() {
  const [searchId, setSearchId] = useState('')
  const [selectedGlyph, setSelectedGlyph] = useState(null)

  const { data: glyphs } = useQuery({
    queryKey: ['glyphs'],
    queryFn: async () => {
      const { data } = await axios.get('/api/vault/list?limit=50')
      return data
    }
  })

  const { data: proof } = useQuery({
    queryKey: ['proof', selectedGlyph],
    queryFn: async () => {
      const { data } = await axios.get(`/api/vault/proof/${selectedGlyph}`)
      return data
    },
    enabled: !!selectedGlyph
  })

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Glyph Vault</h1>
        <p className="text-slate-400">
          Cryptographic provenance for all knowledge data
        </p>
      </div>

      {/* Search */}
      <div className="goat-card">
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Search by Glyph ID (0x...)"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            className="goat-input flex-1"
          />
          <button
            onClick={() => setSelectedGlyph(searchId)}
            className="goat-button"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Glyph List */}
      <div className="goat-card">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
          <Shield className="w-6 h-6 text-goat-primary" />
          Recent Glyphs
        </h2>
        
        <div className="space-y-2">
          {glyphs?.glyphs?.map((glyph) => (
            <div
              key={glyph.id}
              onClick={() => setSelectedGlyph(glyph.id)}
              className="bg-slate-700 rounded-lg p-4 cursor-pointer hover:bg-slate-600 transition"
            >
              <div className="flex items-center gap-4">
                <img 
                  src={`/glyph/svg/${glyph.id}`} 
                  alt="Glyph"
                  className="w-12 h-12 rounded"
                />
                <div className="flex-1">
                  <div className="font-mono text-sm text-goat-primary break-all">
                    {glyph.id}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    {glyph.source} • {new Date(glyph.timestamp * 1000).toLocaleString()}
                  </div>
                </div>
                {glyph.verified && (
                  <div className="glyph-badge">
                    Verified
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Proof Details */}
      {proof && (
        <div className="goat-card bg-slate-700 bg-opacity-50">
          <h2 className="text-2xl font-bold mb-4">Cryptographic Proof</h2>
          
          <div className="space-y-4 font-mono text-sm">
            <ProofField label="Glyph ID" value={proof.glyph_id} />
            <ProofField label="Data Hash" value={proof.data_hash} />
            <ProofField label="Source" value={proof.source} />
            <ProofField label="Signer" value={proof.signer} />
            <ProofField 
              label="Signature" 
              value={proof.signature}
              truncate 
            />
            <ProofField 
              label="Signature Valid" 
              value={proof.signature_valid ? '✓ Valid' : '✗ Invalid'}
              highlight={proof.signature_valid}
            />
            <ProofField 
              label="Timestamp" 
              value={new Date(proof.timestamp * 1000).toLocaleString()}
            />
          </div>

          {proof.audit_trail && proof.audit_trail.length > 0 && (
            <div className="mt-6">
              <h3 className="font-bold mb-3">Audit Trail</h3>
              <div className="space-y-2">
                {proof.audit_trail.map((entry, idx) => (
                  <div key={idx} className="bg-slate-800 rounded p-3 text-xs">
                    <div className="flex justify-between">
                      <span className="text-goat-primary">{entry.action}</span>
                      <span className="text-slate-400">
                        {new Date(entry.timestamp * 1000).toLocaleString()}
                      </span>
                    </div>
                    <div className="text-slate-400 mt-1">
                      Actor: {entry.actor}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="mt-6">
            <a 
              href={`/glyph/badge/${proof.glyph_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="goat-button inline-flex items-center gap-2"
            >
              <ExternalLink className="w-4 h-4" />
              View Badge
            </a>
          </div>
        </div>
      )}
    </div>
  )
}

function ProofField({ label, value, truncate, highlight }) {
  return (
    <div>
      <div className="text-slate-400 text-xs mb-1">{label}</div>
      <div className={`${truncate ? 'truncate' : 'break-all'} ${highlight ? 'text-green-500' : 'text-white'}`}>
        {value}
      </div>
    </div>
  )
}
