import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, GraduationCap, FileText, Archive, Package, Zap, Star, CheckCircle, ExternalLink, Award, Users, DollarSign } from 'lucide-react';

export function LearningPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 py-20">
          <div className="text-center space-y-8">
            <div className="w-32 h-32 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full flex items-center justify-center shadow-2xl p-2">
              <img
                src="/Goatvault256.png"
                alt="GOAT Vault"
                className="w-full h-full rounded-full object-cover"
              />
            </div>
            <h1 className="text-6xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
              GOAT Pricing & Packages
            </h1>
            <p className="text-2xl text-slate-300 font-light max-w-4xl mx-auto">
              GOAT is your Legacy Engine — the system that transforms your knowledge, story, skills, or creative work into structured, publishable material.
            </p>
            <p className="text-lg text-slate-400 max-w-3xl mx-auto">
              Every package below uses the same core process: <strong className="text-cyan-400">creation → refinement → export</strong>
            </p>
          </div>
        </div>
      </div>

      {/* GOAT Essentials */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-cyan-400 mb-4">⚡ GOAT Essentials (Base Products)</h2>
          <p className="text-xl text-slate-300">Everything GOAT can do without entering the NFT/minting layer</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8 mb-16">
          {/* Book Builder */}
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 hover:border-cyan-500/50 transition-all duration-300">
            <div className="flex items-center mb-6">
              <BookOpen className="w-8 h-8 text-cyan-400 mr-3" />
              <h3 className="text-2xl font-bold text-cyan-300">GOAT Book Builder</h3>
            </div>
            <div className="text-4xl font-bold text-white mb-4">$199<span className="text-lg text-slate-400"> – One-Time</span></div>
            <ul className="space-y-3 mb-6 text-slate-300">
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Full book structuring (chapter layout + narrative flow)
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                AI-guided writing assistance
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                GOAT Draft Engine (auto-builds missing sections)
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Export to Word, PDF, print-ready formats
              </li>
            </ul>
            <p className="text-sm text-slate-400 mb-6"><strong>Best For:</strong> Authors, memoir creators, business books, technical books</p>
            <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Get Book Builder
            </button>
          </div>

          {/* Content Series Builder */}
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 hover:border-cyan-500/50 transition-all duration-300">
            <div className="flex items-center mb-6">
              <GraduationCap className="w-8 h-8 text-cyan-400 mr-3" />
              <h3 className="text-2xl font-bold text-cyan-300">GOAT Content Series Builder</h3>
            </div>
            <div className="text-4xl font-bold text-white mb-4">$149<span className="text-lg text-slate-400"> – One-Time</span></div>
            <ul className="space-y-3 mb-6 text-slate-300">
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Full content structure (modules, episodes, scripts)
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                PDF content outline
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Video script generation
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Workbook & checklist templates
              </li>
            </ul>
            <p className="text-sm text-slate-400 mb-6"><strong>Best For:</strong> Creators, coaches, experts wanting structured content series</p>
            <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Get Content Series Builder
            </button>
          </div>

          {/* Framework Builder */}
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 hover:border-cyan-500/50 transition-all duration-300">
            <div className="flex items-center mb-6">
              <FileText className="w-8 h-8 text-cyan-400 mr-3" />
              <h3 className="text-2xl font-bold text-cyan-300">GOAT Framework Builder</h3>
            </div>
            <div className="text-4xl font-bold text-white mb-4">$99<span className="text-lg text-slate-400"> – One-Time</span></div>
            <ul className="space-y-3 mb-6 text-slate-300">
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Creates content frameworks or systems
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Includes diagrams, definitions, and use-cases
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Export to printable PDF or slide deck format
              </li>
            </ul>
            <p className="text-sm text-slate-400 mb-6"><strong>Best For:</strong> Entrepreneurs, consultants, public speakers</p>
            <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Get Framework Builder
            </button>
          </div>

          {/* Personal Archive Builder */}
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 hover:border-cyan-500/50 transition-all duration-300">
            <div className="flex items-center mb-6">
              <Archive className="w-8 h-8 text-cyan-400 mr-3" />
              <h3 className="text-2xl font-bold text-cyan-300">GOAT Personal Archive Builder</h3>
            </div>
            <div className="text-4xl font-bold text-white mb-4">$79<span className="text-lg text-slate-400"> – One-Time</span></div>
            <ul className="space-y-3 mb-6 text-slate-300">
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Organizes personal documents, thoughts, writings
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Bundles into clean archives for family or legacy
              </li>
              <li className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                Creates exportable PDFs for printing or saving
              </li>
            </ul>
            <p className="text-sm text-slate-400 mb-6"><strong>Best For:</strong> Family histories, memoirs, personal legacies</p>
            <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Get Archive Builder
            </button>
          </div>
        </div>
      </div>

      {/* GOAT Bundles */}
      <div className="bg-slate-800/30 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-purple-400 mb-4">🔥 GOAT Bundles (Best Value)</h2>
            <p className="text-xl text-slate-300">Premium packages for complete legacy creation</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {/* Author's Package */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border-2 border-cyan-500/30 p-6 hover:border-cyan-400 transition-all duration-300 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Star className="w-6 h-6 text-yellow-400" />
              </div>
              <h3 className="text-xl font-bold text-cyan-300 mb-2 text-center">The Author's Package</h3>
              <div className="text-3xl font-bold text-white mb-4 text-center">$399</div>
              <p className="text-sm text-slate-400 mb-4 text-center">Full Book Package</p>
              <ul className="space-y-2 text-sm text-slate-300 mb-6">
                <li>• Book Builder</li>
                <li>• Chapter refinement</li>
                <li>• Author bio + foreword</li>
                <li>• Table of contents</li>
                <li>• Print & e-book formatting</li>
                <li>• 3 rounds of revision</li>
              </ul>
              <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 text-sm">
                Get Author's Package
              </button>
            </div>

            {/* Educator's Package */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border-2 border-purple-500/30 p-6 hover:border-purple-400 transition-all duration-300 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Star className="w-6 h-6 text-yellow-400" />
              </div>
              <h3 className="text-xl font-bold text-purple-300 mb-2 text-center">The Creator's Package</h3>
              <div className="text-3xl font-bold text-white mb-4 text-center">$299</div>
              <p className="text-sm text-slate-400 mb-4 text-center">Content Series + Workbook</p>
              <ul className="space-y-2 text-sm text-slate-300 mb-6">
                <li>• Content Series Builder</li>
                <li>• Full episode scripts</li>
                <li>• Workbook PDF</li>
                <li>• Slides text</li>
                <li>• Quiz questions</li>
                <li>• Certification outline</li>
              </ul>
              <button className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 text-sm">
                Get Creator's Package
              </button>
            </div>

            {/* Legacy Package */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border-2 border-amber-500/30 p-6 hover:border-amber-400 transition-all duration-300 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Star className="w-6 h-6 text-yellow-400" />
              </div>
              <h3 className="text-xl font-bold text-amber-300 mb-2 text-center">The Legacy Package</h3>
              <div className="text-3xl font-bold text-white mb-4 text-center">$499</div>
              <p className="text-sm text-slate-400 mb-4 text-center">Everything for Personal History</p>
              <ul className="space-y-2 text-sm text-slate-300 mb-6">
                <li>• Full life-story processing</li>
                <li>• Family tree section</li>
                <li>• Letters & stories</li>
                <li>• Archive formatting</li>
                <li>• Legacy book</li>
                <li>• Audiobook script</li>
              </ul>
              <button className="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 text-sm">
                Get Legacy Package
              </button>
            </div>

            {/* GOAT Complete */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border-2 border-green-500/30 p-6 hover:border-green-400 transition-all duration-300 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Award className="w-6 h-6 text-yellow-400" />
              </div>
              <h3 className="text-xl font-bold text-green-300 mb-2 text-center">The GOAT Complete</h3>
              <div className="text-3xl font-bold text-white mb-4 text-center">$799</div>
              <p className="text-sm text-slate-400 mb-4 text-center">All-In-One Creation Engine</p>
              <ul className="space-y-2 text-sm text-slate-300 mb-6">
                <li>• Full book</li>
                <li>• Content series</li>
                <li>• Workbook</li>
                <li>• Framework</li>
                <li>• Personal Archive</li>
                <li>• Every export format</li>
              </ul>
              <button className="w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 text-sm">
                Get GOAT Complete
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Add-Ons */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-slate-300 mb-4">📚 Optional Add-Ons</h2>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-800/50 rounded-lg p-6 text-center">
            <Zap className="w-8 h-8 text-yellow-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-yellow-300 mb-2">FastTrack</h3>
            <div className="text-2xl font-bold text-white mb-2">+$99</div>
            <p className="text-sm text-slate-400">48-Hour Priority Processing</p>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 text-center">
            <Users className="w-8 h-8 text-blue-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-blue-300 mb-2">Deep Editing Pass</h3>
            <div className="text-2xl font-bold text-white mb-2">+$149</div>
            <p className="text-sm text-slate-400">Human-Level Polish & Editing</p>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 text-center">
            <FileText className="w-8 h-8 text-purple-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-purple-300 mb-2">Audiobook Script</h3>
            <div className="text-2xl font-bold text-white mb-2">+$49</div>
            <p className="text-sm text-slate-400">Conversion for Audio Recording</p>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 text-center">
            <Package className="w-8 h-8 text-green-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-green-300 mb-2">Chapter Expansion</h3>
            <div className="text-2xl font-bold text-white mb-2">+$39</div>
            <p className="text-sm text-slate-400">Per 5 Chapters</p>
          </div>
        </div>
      </div>

      {/* Minting Options */}
      <div className="bg-slate-800/30 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-slate-300 mb-4">🌐 Minting Options (Upgrade Path)</h2>
            <p className="text-xl text-slate-400">Not included in GOAT pricing, but available for permanent blockchain preservation</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-cyan-900/50 to-blue-900/50 rounded-xl border border-cyan-500/30 p-8 text-center">
              <Award className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-cyan-300 mb-4">TrueMark Mint</h3>
              <p className="text-slate-300 mb-6">Authorship & Proof-of-Work NFTs for permanent ownership verification</p>
              <Link to="/mint" className="inline-flex items-center bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
                Learn About TrueMark
                <ExternalLink className="w-4 h-4 ml-2" />
              </Link>
            </div>

            <div className="bg-gradient-to-r from-purple-900/50 to-pink-900/50 rounded-xl border border-purple-500/30 p-8 text-center">
              <CheckCircle className="w-12 h-12 text-purple-400 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-purple-300 mb-4">CertSig Mint</h3>
              <p className="text-slate-300 mb-6">Certificates, timestamped knowledge, and smart contracts</p>
              <Link to="/mint" className="inline-flex items-center bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
                Learn About CertSig
                <ExternalLink className="w-4 h-4 ml-2" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Web3 Identity & Digital Publishing Extras */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-slate-300 mb-4">✨ Web3 Identity & Digital Publishing Extras</h2>
          <p className="text-xl text-slate-400">Optional upgrades to enhance your digital presence and legacy</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Web3 NFT Domains */}
          <div className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 rounded-xl border border-indigo-500/30 p-8 text-center hover:border-indigo-400 transition-all duration-300">
            <div className="w-16 h-16 mx-auto bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center mb-6">
              <span className="text-2xl font-bold text-white">W</span>
            </div>
            <h3 className="text-2xl font-bold text-indigo-300 mb-4">Web3 NFT Domains (GDIS)</h3>
            <p className="text-slate-300 mb-6">Own a permanent digital identity built on Web3. Perfect for authors, creators, coaches, and anyone who wants a decentralized home base.</p>
            <div className="text-sm text-slate-400 mb-6">
              <div>• web.firstname-lastname</div>
              <div>• gdi.firstname-lastname</div>
              <div>• yourname.gdis</div>
              <div>• custom.projectname</div>
              <div className="mt-2 font-medium">*no renewal fees — lifetime ownership*</div>
            </div>
            <div className="text-2xl font-bold text-white mb-6">$39 – $99</div>
            <button className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Get My Web3 Domain
            </button>
          </div>

          {/* CertSig Mint Discount */}
          <div className="bg-gradient-to-br from-emerald-900/50 to-teal-900/50 rounded-xl border border-emerald-500/30 p-8 text-center hover:border-emerald-400 transition-all duration-300">
            <CheckCircle className="w-16 h-16 text-emerald-400 mx-auto mb-6" />
            <h3 className="text-2xl font-bold text-emerald-300 mb-4">CertSig Mint – 50% OFF</h3>
            <p className="text-slate-300 mb-6">Turn your GOAT project into a certified digital record. Perfect for certificates, contracts, knowledge anchors, and proof-of-work signatures.</p>
            <div className="bg-emerald-900/30 rounded-lg p-4 mb-6">
              <div className="text-emerald-300 font-semibold mb-2">GOAT Creator Discount</div>
              <div className="text-2xl font-bold text-white">50% OFF</div>
              <div className="text-sm text-slate-400">Any CertSig NFT mint</div>
            </div>
            <button className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Redeem CertSig Discount
            </button>
          </div>

          {/* TrueMark Mint Discount */}
          <div className="bg-gradient-to-br from-amber-900/50 to-orange-900/50 rounded-xl border border-amber-500/30 p-8 text-center hover:border-amber-400 transition-all duration-300">
            <Award className="w-16 h-16 text-amber-400 mx-auto mb-6" />
            <h3 className="text-2xl font-bold text-amber-300 mb-4">TrueMark Mint – 25% OFF</h3>
            <p className="text-slate-300 mb-6">Mint authorship, editions, and creator tokens. Perfect for authorship NFTs, editioned works, content certificates, and creator badges.</p>
            <div className="bg-amber-900/30 rounded-lg p-4 mb-6">
              <div className="text-amber-300 font-semibold mb-2">GOAT Creator Discount</div>
              <div className="text-2xl font-bold text-white">25% OFF</div>
              <div className="text-sm text-slate-400">Any TrueMark NFT mint</div>
            </div>
            <button className="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200">
              Use My TrueMark Discount
            </button>
          </div>
        </div>
      </div>

      {/* Distribution Links */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-slate-300 mb-4">📦 Where to Publish & Distribute</h2>
          <p className="text-xl text-slate-400">Every GOAT export is formatted for these platforms</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-6">
          {[
            { name: 'Amazon KDP', color: 'hover:bg-orange-600' },
            { name: 'Lulu Press', color: 'hover:bg-blue-600' },
            { name: 'Barnes & Noble', color: 'hover:bg-red-600' },
            { name: 'IngramSpark', color: 'hover:bg-green-600' },
            { name: 'Draft2Digital', color: 'hover:bg-purple-600' },
            { name: 'Kobo', color: 'hover:bg-cyan-600' },
            { name: 'Apple Books', color: 'hover:bg-gray-600' },
            { name: 'Google Play', color: 'hover:bg-blue-500' },
            { name: 'Blurb', color: 'hover:bg-pink-600' },
            { name: 'BookBaby', color: 'hover:bg-indigo-600' },
            { name: 'Lightning Source', color: 'hover:bg-yellow-600' },
            { name: 'Printify', color: 'hover:bg-teal-600' }
          ].map((platform, index) => (
            <div key={index} className={`bg-slate-800/50 rounded-lg p-4 text-center hover:bg-slate-700 transition-all duration-200 cursor-pointer ${platform.color} hover:text-white`}>
              <ExternalLink className="w-6 h-6 mx-auto mb-2 text-slate-400" />
              <p className="text-sm font-medium text-slate-300">{platform.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-gradient-to-r from-cyan-900/50 to-purple-900/50 py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Start Building Your Legacy Today</h2>
          <p className="text-xl text-slate-300 mb-8">
            Transform your knowledge into publishable content with GOAT's AI-powered creation engine.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/login"
              className="bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
            >
              <span>Start Your Legacy</span>
              <BookOpen className="w-5 h-5" />
            </Link>
            <Link
              to="/menu"
              className="border-2 border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white font-semibold py-4 px-8 rounded-lg transition-all duration-200"
            >
              Explore All Features
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
