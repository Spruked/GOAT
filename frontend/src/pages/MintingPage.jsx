import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Shield, CheckCircle, ExternalLink, Crown, Download, Info, Zap } from 'lucide-react';
import axios from 'axios';

export default function PartnerReferralPage() {
  const [searchParams] = useSearchParams();
  const legacyId = searchParams.get('legacyId');
  const [legacy, setLegacy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPartner, setSelectedPartner] = useState('alpha_certsig');
  const [packageReady, setPackageReady] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

  useEffect(() => {
    if (legacyId) {
      loadLegacy();
    }
  }, [legacyId]);

  const loadLegacy = async () => {
    try {
      const [userId, productType] = legacyId.split('_');
      const response = await axios.get(`/api/legacy/${userId}/${productType}`, {
        headers: { 'Authorization': 'Bearer goat_api_key' }
      });
      setLegacy(response.data.legacy);
    } catch (error) {
      alert('Failed to load legacy: ' + error.response?.data?.detail || error.message);
    }
    setLoading(false);
  };

  const preparePackage = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/legacy/prepare-mint-package', {
        legacy_id: legacyId,
        partner: selectedPartner
      }, {
        headers: { 'Authorization': 'Bearer goat_api_key' }
      });
      
      setPackageReady(true);
      setDownloadUrl(response.data.download_url);
    } catch (error) {
      alert('Failed to prepare package: ' + error.response?.data?.detail || error.message);
    }
    setLoading(false);
  };

  const partners = {
    alpha_certsig: {
      name: "Alpha CertSig Mint",
      description: "Multi-chain blockchain minting with IPFS pinning",
      url: "https://alphamint.certsig.io?ref=GOAT30",
      standardPrice: "$0.08 ETH",
      goatPrice: "$0.056 ETH",
      savings: "30% OFF",
      features: [
        "ERC-721/ERC-1155 minting",
        "Multi-chain (Ethereum, Polygon, Base, Arbitrum)",
        "IPFS pinning included",
        "ChaCha24/128/256 encryption upgrades",
        "Permanent authorship proof",
        "Fast and simple process"
      ],
      recommended: "Content Creators"
    },
    truemark: {
      name: "TrueMark Mint",
      description: "Identity-linked permanent blockchain records",
      url: "https://mint.truemark.com?ref=GOAT30",
      standardPrice: "$0.15 ETH",
      goatPrice: "$0.105 ETH",
      savings: "30% OFF",
      features: [
        "Identity-linked minting",
        ".go domain integration",
        "GDIS identity verification",
        "Royalty tracking built-in",
        "Multi-chain support",
        "White-label branding options",
        "ChaCha24/128/256 encryption upgrades",
        "Enterprise compliance ready"
      ],
      recommended: "Professional Brands"
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p>Preparing your package...</p>
        </div>
      </div>
    );
  }

  if (!legacy) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Legacy Not Found</h1>
          <p className="text-slate-400">The requested legacy could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full flex items-center justify-center shadow-2xl mb-6">
            <Crown className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
            Make Your Creation Immortal
          </h1>
          <p className="text-xl text-slate-300 mb-4">
            GOAT has prepared your blockchain package. Choose a partner to mint.
          </p>
          <div className="bg-goat-primary/10 border border-goat-primary/30 rounded-lg p-4 inline-block">
            <p className="text-goat-primary font-bold text-lg">
              🎁 Exclusive GOAT Discount: 30% OFF at both partners!
            </p>
          </div>
        </div>

        {/* Legacy Preview */}
        <div className="bg-slate-800/50 p-8 rounded-lg border border-slate-700 mb-8">
          <h2 className="text-2xl font-bold text-cyan-300 mb-4">{legacy.content.title}</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-purple-300 mb-2">Details</h3>
              <p className="text-slate-300"><span className="text-slate-400">Type:</span> {legacy.product_type}</p>
              <p className="text-slate-300"><span className="text-slate-400">Author:</span> {legacy.nft_metadata.attributes.find(a => a.trait_type === 'Author')?.value}</p>
              <p className="text-slate-300"><span className="text-slate-400">Created:</span> {new Date(legacy.generated_at).toLocaleDateString()}</p>
            </div>
            <div>
              <h3 className="font-semibold text-purple-300 mb-2">Package Ready</h3>
              <p className="text-green-400">✅ Cryptographic signatures</p>
              <p className="text-green-400">✅ Content verification hash</p>
              <p className="text-green-400">✅ Blockchain-ready metadata</p>
              <p className="text-green-400">✅ IPFS preparation complete</p>
            </div>
          </div>
        </div>

        {/* Why Mint Section */}
        <div className="bg-gradient-to-r from-purple-900/20 to-cyan-900/20 p-8 rounded-lg border border-purple-600/30 mb-8">
          <div className="flex items-center mb-4">
            <Info className="w-6 h-6 mr-3 text-purple-400" />
            <h2 className="text-2xl font-bold text-purple-300">Why Mint on the Blockchain?</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-slate-300">
            <div>
              <p className="mb-2">✅ <strong>Permanent Proof of Authorship</strong> - Timestamped, verifiable, immutable</p>
              <p className="mb-2">✅ <strong>Decentralized Storage</strong> - IPFS/Arweave ensures your work can't be deleted</p>
              <p className="mb-2">✅ <strong>Transferable Ownership</strong> - Sell, gift, or license your creation</p>
            </div>
            <div>
              <p className="mb-2">✅ <strong>Royalty Tracking</strong> - Earn from secondary sales (TrueMark)</p>
              <p className="mb-2">✅ <strong>Cannot Be Altered</strong> - Original preserved forever</p>
              <p className="mb-2">✅ <strong>Protects IP Rights</strong> - Legal proof you created it first</p>
            </div>
          </div>
        </div>

        {/* Partner Selection */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-center mb-6">Choose Your Minting Partner</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {Object.entries(partners).map(([key, partner]) => (
              <div
                key={key}
                onClick={() => setSelectedPartner(key)}
                className={`p-6 rounded-lg border-2 cursor-pointer transition-all ${
                  selectedPartner === key
                    ? 'border-goat-primary bg-goat-primary/10'
                    : 'border-slate-600 hover:border-slate-500 bg-slate-800/30'
                }`}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-white mb-1">{partner.name}</h3>
                    <p className="text-sm text-slate-400">{partner.description}</p>
                  </div>
                  {selectedPartner === key && (
                    <CheckCircle className="w-6 h-6 text-goat-primary" />
                  )}
                </div>

                <div className="mb-4">
                  <div className="flex items-baseline gap-2 mb-1">
                    <span className="text-2xl font-bold text-goat-primary">{partner.goatPrice}</span>
                    <span className="text-sm text-slate-400 line-through">{partner.standardPrice}</span>
                    <span className="text-sm font-bold text-green-400">{partner.savings}</span>
                  </div>
                  <p className="text-xs text-slate-500">+ gas fees</p>
                </div>

                <div className="mb-4">
                  <p className="text-xs text-purple-300 font-semibold mb-2">Best for: {partner.recommended}</p>
                </div>

                <div className="space-y-2">
                  {partner.features.map((feature, idx) => (
                    <p key={idx} className="text-sm text-slate-300">• {feature}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="bg-slate-800/50 p-8 rounded-lg border border-slate-700">
          <div className="text-center mb-6">
            <h3 className="text-xl font-bold mb-2">Ready to Mint with {partners[selectedPartner].name}?</h3>
            <p className="text-slate-400">Follow these simple steps:</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="w-12 h-12 mx-auto bg-cyan-500/20 rounded-full flex items-center justify-center mb-3">
                <Download className="w-6 h-6 text-cyan-400" />
              </div>
              <h4 className="font-semibold mb-2">1. Download Package</h4>
              <p className="text-sm text-slate-400">Get your blockchain-ready ZIP</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 mx-auto bg-purple-500/20 rounded-full flex items-center justify-center mb-3">
                <ExternalLink className="w-6 h-6 text-purple-400" />
              </div>
              <h4 className="font-semibold mb-2">2. Visit Partner</h4>
              <p className="text-sm text-slate-400">30% discount auto-applied</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 mx-auto bg-green-500/20 rounded-full flex items-center justify-center mb-3">
                <Zap className="w-6 h-6 text-green-400" />
              </div>
              <h4 className="font-semibold mb-2">3. Upload & Mint</h4>
              <p className="text-sm text-slate-400">Process takes ~5 minutes</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {!packageReady ? (
              <button
                onClick={preparePackage}
                disabled={loading}
                className="goat-button-primary px-8 py-4 text-lg"
              >
                {loading ? 'Preparing Package...' : 'Prepare Download Package'}
              </button>
            ) : (
              <>
                <a
                  href={downloadUrl}
                  download
                  className="goat-button-primary px-8 py-4 text-lg inline-flex items-center justify-center"
                >
                  <Download className="w-5 h-5 mr-2" />
                  Download ZIP Package
                </a>
                <a
                  href={partners[selectedPartner].url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="goat-button-secondary px-8 py-4 text-lg inline-flex items-center justify-center"
                >
                  <ExternalLink className="w-5 h-5 mr-2" />
                  Go to {partners[selectedPartner].name}
                </a>
              </>
            )}
          </div>

          {packageReady && (
            <div className="mt-6 text-center">
              <p className="text-sm text-slate-400 mb-2">
                Your discount code <strong className="text-goat-primary">GOAT30</strong> is automatically applied at checkout
              </p>
              <p className="text-xs text-slate-500">
                After minting, you'll receive a certificate, transaction hash, and IPFS CID
              </p>
            </div>
          )}
        </div>

        {/* Revenue Model Explanation */}
        <div className="mt-8 bg-slate-900/50 border border-slate-700 rounded-lg p-6 text-center">
          <h3 className="text-lg font-semibold mb-2 text-purple-300">Three-Way Revenue Partnership</h3>
          <p className="text-sm text-slate-400 mb-4">
            GOAT prepares your content • Partners handle blockchain minting • Everyone benefits
          </p>
          <div className="flex justify-center gap-8 text-sm">
            <div>
              <p className="text-goat-primary font-bold">GOAT</p>
              <p className="text-slate-500">Content creation</p>
            </div>
            <div className="text-slate-600">+</div>
            <div>
              <p className="text-cyan-400 font-bold">Alpha CertSig</p>
              <p className="text-slate-500">Blockchain minting</p>
            </div>
            <div className="text-slate-600">+</div>
            <div>
              <p className="text-purple-400 font-bold">TrueMark</p>
              <p className="text-slate-500">Identity linking</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
            </div>
          </div>
        </div>

        {/* Minting Options */}
        {!mintResult && (
          <div className="grid md:grid-cols-2 gap-8 mb-8">
            {/* CertSig */}
            <div className="bg-gradient-to-br from-blue-900/20 to-cyan-900/20 p-6 rounded-lg border border-blue-600/30">
              <div className="flex items-center space-x-3 mb-4">
                <Shield className="w-8 h-8 text-blue-400" />
                <h3 className="text-xl font-bold text-blue-300">CertSig</h3>
              </div>
              <p className="text-slate-300 mb-4">
                Permanent authorship and ownership proof with cryptographic verification.
              </p>
              <ul className="space-y-2 text-sm text-slate-400 mb-6">
                <li>• Timestamped creation records</li>
                <li>• Blockchain-verified authenticity</li>
                <li>• Decentralized storage</li>
                <li>• Royalty tracking ready</li>
              </ul>
              <button
                onClick={() => mintLegacy('certsig')}
                disabled={minting}
                className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 px-6 py-3 rounded-lg font-semibold transition"
              >
                {minting ? 'Minting...' : 'Mint with CertSig'}
              </button>
            </div>

            {/* TrueMark */}
            <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 p-6 rounded-lg border border-purple-600/30">
              <div className="flex items-center space-x-3 mb-4">
                <CheckCircle className="w-8 h-8 text-purple-400" />
                <h3 className="text-xl font-bold text-purple-300">TrueMark</h3>
              </div>
              <p className="text-slate-300 mb-4">
                Identity-linked permanent records with advanced verification features.
              </p>
              <ul className="space-y-2 text-sm text-slate-400 mb-6">
                <li>• Identity verification</li>
                <li>• Multi-chain support</li>
                <li>• Enhanced metadata</li>
                <li>• Commercial licensing tools</li>
              </ul>
              <button
                onClick={() => mintLegacy('truemark')}
                disabled={minting}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 px-6 py-3 rounded-lg font-semibold transition"
              >
                {minting ? 'Minting...' : 'Mint with TrueMark'}
              </button>
            </div>
          </div>
        )}

        {/* Mint Result */}
        {mintResult && (
          <div className="bg-gradient-to-r from-green-900/20 to-cyan-900/20 p-8 rounded-lg border border-green-600/30">
            <div className="text-center mb-6">
              <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-green-300 mb-2">Legacy Minted Successfully!</h2>
              <p className="text-slate-300">{mintResult.message}</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-cyan-300 mb-3">Mint Details</h3>
                <div className="space-y-2 text-sm">
                  <p><span className="text-slate-400">Engine:</span> {mintResult.mint_result.engine_details.name}</p>
                  <p><span className="text-slate-400">Token ID:</span> {mintResult.mint_result.token_id}</p>
                  <p><span className="text-slate-400">Transaction:</span> {mintResult.mint_result.transaction_hash.substring(0, 20)}...</p>
                  <p><span className="text-slate-400">Contract:</span> {mintResult.mint_result.contract_address.substring(0, 20)}...</p>
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-cyan-300 mb-3">What's Next?</h3>
                <ul className="space-y-2 text-sm text-slate-300">
                  <li>• Your work is now permanently preserved</li>
                  <li>• Authorship is cryptographically verified</li>
                  <li>• Share, sell, or license with confidence</li>
                  <li>• Build upon your legacy anytime</li>
                </ul>
              </div>
            </div>

            <div className="mt-6 p-4 bg-slate-800/50 rounded-lg">
              <p className="text-slate-300 italic">"{mintResult.caleon_message}"</p>
              <p className="text-slate-400 text-sm mt-2">— Caleon</p>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12">
          <p className="text-slate-400">
            Minting creates permanent, unalterable proof of your authorship.
            Your legacy will outlive you and be verifiable by anyone, anywhere.
          </p>
        </div>
      </div>
    </div>
  );
}