import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Upload, Link as LinkIcon, CheckCircle } from 'lucide-react'
import axios from 'axios'

export function CollectorPage() {
  const [ipfsCid, setIpfsCid] = useState('')
  const [contract, setContract] = useState('')
  const [tokenId, setTokenId] = useState('')
  const [result, setResult] = useState(null)

  const ipfsMutation = useMutation({
    mutationFn: async (cid) => {
      const { data } = await axios.post('/api/collect/ipfs', {
        cid,
        auto_pin: true
      })
      return data
    },
    onSuccess: (data) => {
      setResult(data)
      setIpfsCid('')
    }
  })

  const onchainMutation = useMutation({
    mutationFn: async ({ contract, token_id }) => {
      const { data } = await axios.post('/api/collect/onchain', {
        contract,
        token_id
      })
      return data
    },
    onSuccess: (data) => {
      setResult(data)
      setContract('')
      setTokenId('')
    }
  })

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">NFT Collector</h1>
        <p className="text-slate-400">
          Ingest NFT knowledge with cryptographic glyph generation
        </p>
      </div>

      {/* IPFS Ingestion */}
      <div className="goat-card">
        <div className="flex items-center gap-3 mb-4">
          <Upload className="w-6 h-6 text-goat-primary" />
          <h2 className="text-2xl font-bold">Ingest from IPFS</h2>
        </div>
        
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Enter IPFS CID (e.g., QmXX...)"
            value={ipfsCid}
            onChange={(e) => setIpfsCid(e.target.value)}
            className="goat-input w-full"
          />
          
          <button
            onClick={() => ipfsMutation.mutate(ipfsCid)}
            disabled={!ipfsCid || ipfsMutation.isPending}
            className="goat-button w-full disabled:opacity-50"
          >
            {ipfsMutation.isPending ? 'Ingesting...' : 'Ingest from IPFS'}
          </button>
        </div>
      </div>

      {/* On-Chain Ingestion */}
      <div className="goat-card">
        <div className="flex items-center gap-3 mb-4">
          <LinkIcon className="w-6 h-6 text-goat-primary" />
          <h2 className="text-2xl font-bold">Ingest from Blockchain</h2>
        </div>
        
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Contract Address (0x...)"
            value={contract}
            onChange={(e) => setContract(e.target.value)}
            className="goat-input w-full"
          />
          
          <input
            type="text"
            placeholder="Token ID"
            value={tokenId}
            onChange={(e) => setTokenId(e.target.value)}
            className="goat-input w-full"
          />
          
          <button
            onClick={() => onchainMutation.mutate({ contract, token_id: tokenId })}
            disabled={!contract || !tokenId || onchainMutation.isPending}
            className="goat-button w-full disabled:opacity-50"
          >
            {onchainMutation.isPending ? 'Ingesting...' : 'Ingest from Blockchain'}
          </button>
        </div>
      </div>

      {/* Result Display */}
      {result && (
        <div className="goat-card bg-green-900 bg-opacity-20 border-green-500">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle className="w-6 h-6 text-green-500" />
            <h3 className="text-xl font-bold">Successfully Ingested!</h3>
          </div>
          
          <div className="space-y-2 font-mono text-sm">
            <div>
              <span className="text-slate-400">Glyph ID:</span>
              <div className="text-goat-primary break-all">{result.glyph_id}</div>
            </div>
            <div>
              <span className="text-slate-400">Source:</span>
              <div className="text-white">{result.source}</div>
            </div>
          </div>
          
          <div className="mt-4">
            <a href={`/vault#${result.glyph_id}`}>
              <button className="goat-button-secondary">
                View in Vault
              </button>
            </a>
          </div>
        </div>
      )}

      {/* Info Section */}
      <div className="goat-card bg-slate-700 bg-opacity-50">
        <h3 className="font-bold mb-3">How It Works</h3>
        <ol className="space-y-2 text-sm text-slate-300 list-decimal list-inside">
          <li>Provide IPFS CID or blockchain contract address</li>
          <li>GOAT downloads and analyzes the NFT metadata</li>
          <li>Generates unique cryptographic Glyph ID</li>
          <li>Stores encrypted in vault with EIP-191 signature</li>
          <li>Links to knowledge graph for teaching</li>
        </ol>
      </div>
    </div>
  )
}
