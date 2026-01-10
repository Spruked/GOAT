import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Shield, Zap, Users, AlertTriangle, ArrowRight } from 'lucide-react';

export default function StartPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
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
              GOAT
            </h1>
            <p className="text-2xl text-slate-300 font-light">
              Greatest Of All Time
            </p>
            <p className="text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
              The Engine That Immortalizes Your Greatest Work. Transform your skill, story, and experience into permanent, publishable legacy through AI-guided creation and blockchain preservation.
            </p>
          </div>
        </div>
      </div>

      {/* Purpose & Capabilities */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12">
          <div className="space-y-8">
            <h2 className="text-3xl font-bold text-cyan-400">What GOAT Does</h2>
            <p className="text-lg text-slate-300 leading-relaxed">
              GOAT is a Legacy Builder, Masterpiece Engine, and Knowledge Extractor. It captures your skill, story, and experience, then structures it into books, masterclasses, courses, frameworks, and archives that become your permanent legacy.
            </p>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <Shield className="w-6 h-6 text-green-400 mt-1" />
                <div>
                  <h3 className="font-semibold text-green-400">Legacy Preservation</h3>
                  <p className="text-slate-400">Your greatest work becomes immortal through blockchain anchoring and decentralized storage.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Zap className="w-6 h-6 text-yellow-400 mt-1" />
                <div>
                  <h3 className="font-semibold text-yellow-400">Scripted Host Creation</h3>
                  <p className="text-slate-400">HOST guides you step-by-step to structure and enhance your masterpiece.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Users className="w-6 h-6 text-blue-400 mt-1" />
                <div>
                  <h3 className="font-semibold text-blue-400">Publish & Monetize</h3>
                  <p className="text-slate-400">Create publishable content you can sell, license, or share with permanent authorship proof.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-8">
            <h2 className="text-3xl font-bold text-purple-400">What GOAT Creates</h2>
            <div className="space-y-6">
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-cyan-300 mb-2">Books & Masterclasses</h3>
                <p className="text-slate-400">Structure your expertise into comprehensive books and masterclass content.</p>
              </div>
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-cyan-300 mb-2">Courses & Frameworks</h3>
                <p className="text-slate-400">Build structured courses and philosophical frameworks from your knowledge.</p>
              </div>
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-cyan-300 mb-2">Permanent Archives</h3>
                <p className="text-slate-400">Create vault artifacts and knowledge sets preserved forever on-chain.</p>
              </div>
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-cyan-300 mb-2">Authorship NFTs</h3>
                <p className="text-slate-400">Mint permanent proof of your authorship and ownership through CertSig and TrueMark.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Limitations */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="bg-amber-900/20 border border-amber-600/30 rounded-lg p-8">
          <div className="flex items-start space-x-4">
            <AlertTriangle className="w-8 h-8 text-amber-400 flex-shrink-0 mt-1" />
            <div>
              <h2 className="text-2xl font-bold text-amber-400 mb-4">Important Limitations</h2>
              <div className="grid md:grid-cols-2 gap-6 text-slate-300">
                <div>
                  <h3 className="font-semibold text-amber-300 mb-2">Blockchain Dependencies</h3>
                  <p>Requires Polygon network connectivity for NFT operations and on-chain anchoring.</p>
                </div>
                <div>
                  <h3 className="font-semibold text-amber-300 mb-2">GPU Requirements</h3>
                  <p>Advanced AI features may require GPU acceleration for optimal performance.</p>
                </div>
                <div>
                  <h3 className="font-semibold text-amber-300 mb-2">Network Connectivity</h3>
                  <p>IPFS and decentralized storage require stable internet connection.</p>
                </div>
                <div>
                  <h3 className="font-semibold text-amber-300 mb-2">Content Creation</h3>
                  <p>Understanding blockchain concepts and NFT mechanics may require initial familiarization.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold text-white mb-6">Ready to Start Creating Content?</h2>
        <p className="text-xl text-slate-400 mb-8">
          Join thousands of creators in the decentralized content revolution.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/start-actions"
            className="bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-8 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <span>Start Creating</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/menu"
            className="border border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200"
          >
            Learn More
          </Link>
        </div>
      </div>
    </div>
  );
}