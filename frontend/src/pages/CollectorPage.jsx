import { useState } from 'react'
import DumpZone from '../components/DumpZone'
import { useMutation } from '@tanstack/react-query'
import { Upload, Link as LinkIcon, CheckCircle, BookOpen, Plus, X } from 'lucide-react'
import axios from 'axios'

export function CollectorPage() {
  const [ipfsCid, setIpfsCid] = useState('')
  const [contract, setContract] = useState('')
  const [tokenId, setTokenId] = useState('')
  const [result, setResult] = useState(null)
  
  // Manual knowledge entry state
  const [manualKnowledge, setManualKnowledge] = useState({
    name: '',
    category: 'Technical',
    description: '',
    content: '',
    tags: '',
    concepts: [],
    skill_level: 'Beginner'
  })
  const [newConcept, setNewConcept] = useState({ name: '', definition: '', example: '' })

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

  const manualMutation = useMutation({
    mutationFn: async (knowledge) => {
      const { data } = await axios.post('/api/collect/manual', knowledge)
      return data
    },
    onSuccess: (data) => {
      setResult(data)
      setManualKnowledge({
        name: '',
        category: 'Technical',
        description: '',
        content: '',
        tags: '',
        concepts: [],
        skill_level: 'Beginner'
      })
    }
  })

  const addConcept = () => {
    if (newConcept.name && newConcept.definition) {
      setManualKnowledge({
        ...manualKnowledge,
        concepts: [...manualKnowledge.concepts, { ...newConcept }]
      })
      setNewConcept({ name: '', definition: '', example: '' })
    }
  }

  const removeConcept = (index) => {
    setManualKnowledge({
      ...manualKnowledge,
      concepts: manualKnowledge.concepts.filter((_, i) => i !== index)
    })
  }

  // Handler for when Somedaa set upload completes
  const handleSomedaaUpload = () => {
    // Optionally refresh state or show a message
    setResult({ glyph_id: 'SOMEDAA_SET', source: 'Somedaa Set Upload' });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">NFT Collector</h1>
        <p className="text-slate-400">
          Ingest NFT knowledge with cryptographic glyph generation
        </p>
      </div>

      {/* Somedaa Set Drag-and-Drop Ingestion */}
      <div className="goat-card">
        <div className="flex items-center gap-3 mb-4">
          <Upload className="w-6 h-6 text-goat-primary" />
          <h2 className="text-2xl font-bold">Ingest Somedaa Set (Drag & Drop)</h2>
        </div>
        <DumpZone projectId="somedaa" onUploadComplete={handleSomedaaUpload} />
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

      {/* Manual Knowledge Entry */}
      <div className="goat-card">
        <div className="flex items-center gap-3 mb-6">
          <BookOpen className="w-6 h-6 text-goat-primary" />
          <h2 className="text-2xl font-bold">Manual Knowledge Entry</h2>
        </div>

        <div className="space-y-4">
          {/* Knowledge Name */}
          <div>
            <label className="block text-sm font-medium mb-2">Knowledge Name *</label>
            <input
              type="text"
              value={manualKnowledge.name}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, name: e.target.value })}
              placeholder="e.g., Python Basics, HVAC Troubleshooting, Sales Scripts v1"
              className="goat-input w-full"
            />
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium mb-2">Category *</label>
            <select
              value={manualKnowledge.category}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, category: e.target.value })}
              className="goat-input w-full"
            >
              <option>Technical</option>
              <option>Professional</option>
              <option>Personal Development</option>
              <option>Scientific</option>
              <option>Legal</option>
              <option>Art</option>
              <option>Business</option>
              <option>Legacy</option>
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-2">Description *</label>
            <textarea
              value={manualKnowledge.description}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, description: e.target.value })}
              placeholder="Short summary of this knowledge (becomes NFT description)"
              className="goat-input w-full h-24"
            />
          </div>

          {/* Raw Knowledge Content */}
          <div>
            <label className="block text-sm font-medium mb-2">Raw Knowledge Content *</label>
            <textarea
              value={manualKnowledge.content}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, content: e.target.value })}
              placeholder="Enter your expertise, principles, frameworks, processes, instructions, skills..."
              className="goat-input w-full h-48 font-mono text-sm"
            />
            <p className="text-xs text-slate-400 mt-1">
              This is the heart of your knowledge asset. Be thorough and clear.
            </p>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium mb-2">Tags</label>
            <input
              type="text"
              value={manualKnowledge.tags}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, tags: e.target.value })}
              placeholder="comma, separated, tags"
              className="goat-input w-full"
            />
          </div>

          {/* Skill Level */}
          <div>
            <label className="block text-sm font-medium mb-2">Skill Level</label>
            <select
              value={manualKnowledge.skill_level}
              onChange={(e) => setManualKnowledge({ ...manualKnowledge, skill_level: e.target.value })}
              className="goat-input w-full"
            >
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
              <option>Mastery</option>
            </select>
          </div>

          {/* Concepts Section */}
          <div className="border-t border-slate-600 pt-4">
            <h3 className="font-bold mb-3 flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Add Concepts (Optional)
            </h3>
            
            {/* Concept List */}
            {manualKnowledge.concepts.length > 0 && (
              <div className="space-y-2 mb-4">
                {manualKnowledge.concepts.map((concept, idx) => (
                  <div key={idx} className="bg-slate-700 p-3 rounded-lg flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-semibold text-goat-primary">{concept.name}</div>
                      <div className="text-sm text-slate-300">{concept.definition}</div>
                      {concept.example && (
                        <div className="text-xs text-slate-400 mt-1">Example: {concept.example}</div>
                      )}
                    </div>
                    <button
                      onClick={() => removeConcept(idx)}
                      className="text-red-400 hover:text-red-300 ml-2"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Add New Concept */}
            <div className="space-y-2 bg-slate-700 p-4 rounded-lg">
              <input
                type="text"
                value={newConcept.name}
                onChange={(e) => setNewConcept({ ...newConcept, name: e.target.value })}
                placeholder="Concept name"
                className="goat-input w-full text-sm"
              />
              <input
                type="text"
                value={newConcept.definition}
                onChange={(e) => setNewConcept({ ...newConcept, definition: e.target.value })}
                placeholder="Definition"
                className="goat-input w-full text-sm"
              />
              <input
                type="text"
                value={newConcept.example}
                onChange={(e) => setNewConcept({ ...newConcept, example: e.target.value })}
                placeholder="Example (optional)"
                className="goat-input w-full text-sm"
              />
              <button
                onClick={addConcept}
                disabled={!newConcept.name || !newConcept.definition}
                className="goat-button-secondary w-full text-sm disabled:opacity-50"
              >
                Add Concept
              </button>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={() => manualMutation.mutate(manualKnowledge)}
            disabled={!manualKnowledge.name || !manualKnowledge.description || !manualKnowledge.content || manualMutation.isPending}
            className="goat-button w-full disabled:opacity-50"
          >
            {manualMutation.isPending ? 'Generating Glyphs...' : 'Generate Glyphs & Store Knowledge'}
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
          <li>Links to knowledge graph for content creation</li>
        </ol>
      </div>
    </div>
  )
}
