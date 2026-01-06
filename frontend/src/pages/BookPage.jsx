import React, { useState } from 'react';
import { BookOpen, FileText, Layers, Target, Lightbulb, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { ProductWalkthrough } from '../components/ProductWalkthrough';
import { useProductWalkthrough } from '../hooks/useProductWalkthrough';

export default function BookPage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    bookTitle: '',
    subtitle: '',
    bookType: '',
    genre: '',
    targetWordCount: '',
    numberOfChapters: '',
    targetAudience: '',
    readingLevel: '',
    narrative Voice: '',
    writingStyle: '',
    premise: '',
    mainThemes: '',
    characterNotes: '',
    plotOutline: '',
    researchMaterials: '',
    coreMessage: '',
    includeIndex: false,
    includeBibliography: false,
    includeGlossary: false
  });
  const [loading, setLoading] = useState(false);

  // Product walkthrough hook
  const {
    showWalkthrough,
    completeWalkthrough,
    skipWalkthrough
  } = useProductWalkthrough('book');

  const bookTypes = [
    { value: 'fiction', label: 'Fiction Novel', desc: 'Creative storytelling' },
    { value: 'nonfiction', label: 'Non-Fiction', desc: 'Educational/Informational' },
    { value: 'memoir', label: 'Memoir', desc: 'Personal story' },
    { value: 'biography', label: 'Biography', desc: 'Life story of another' },
    { value: 'howto', label: 'How-To Guide', desc: 'Instructional manual' },
    { value: 'selfhelp', label: 'Self-Help', desc: 'Personal development' }
  ];

  const wordCounts = [
    { value: 'novella', label: 'Novella (20,000-40,000 words)', count: '20k-40k' },
    { value: 'short', label: 'Short Novel (40,000-60,000 words)', count: '40k-60k' },
    { value: 'standard', label: 'Standard Novel (70,000-90,000 words)', count: '70k-90k' },
    { value: 'long', label: 'Long Novel (100,000-120,000 words)', count: '100k-120k' },
    { value: 'epic', label: 'Epic (150,000+ words)', count: '150k+' }
  ];

  const writingStyles = ['Descriptive', 'Concise', 'Poetic', 'Academic', 'Conversational', 'Journalistic'];
  const narrativeVoices = ['First Person', 'Third Person Limited', 'Third Person Omniscient', 'Second Person'];
  const readingLevels = ['General Audience', 'Young Adult', 'Academic', 'Professional', 'Elementary'];

  const createBook = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/book/create', formData, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      setStep('complete');
    } catch (error) {
      console.error('Book creation failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-900 via-slate-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-16">
        
        {/* Header */}
        <div className="text-center mb-16">
          <div className="w-24 h-24 mx-auto bg-gradient-to-r from-amber-500 to-orange-500 rounded-full flex items-center justify-center shadow-2xl mb-6">
            <BookOpen className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent mb-4">
            Professional Book Writing
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Transform your ideas into a complete, professionally structured manuscript with AI-assisted writing and developmental editing
          </p>
        </div>

        {step === 'input' && (
          <div className="space-y-12">
            
            {/* Book Identity */}
            <div className="bg-gradient-to-r from-amber-900/30 to-orange-900/30 p-8 rounded-2xl border border-amber-500/30">
              <div className="flex items-center mb-6">
                <FileText className="w-6 h-6 mr-3 text-amber-400" />
                <h2 className="text-3xl font-bold text-amber-300">Book Identity</h2>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-amber-200 mb-3">Book Title</label>
                  <input
                    type="text"
                    placeholder="The Art of Timeless Wisdom"
                    value={formData.bookTitle}
                    onChange={(e) => setFormData({...formData, bookTitle: e.target.value})}
                    className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-amber-200 mb-3">Subtitle (optional)</label>
                  <input
                    type="text"
                    placeholder="Lessons from History's Greatest Minds"
                    value={formData.subtitle}
                    onChange={(e) => setFormData({...formData, subtitle: e.target.value})}
                    className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            {/* Book Structure */}
            <div className="bg-gradient-to-r from-slate-900/50 to-amber-900/30 p-8 rounded-2xl border border-slate-700">
              <div className="flex items-center mb-6">
                <Layers className="w-6 h-6 mr-3 text-orange-400" />
                <h2 className="text-3xl font-bold text-orange-300">Book Structure</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-4">Book Type</label>
                  <div className="grid md:grid-cols-3 gap-4">
                    {bookTypes.map((type) => (
                      <button
                        key={type.value}
                        onClick={() => setFormData({...formData, bookType: type.value})}
                        className={`p-6 rounded-xl border-2 transition text-left ${
                          formData.bookType === type.value
                            ? 'border-orange-500 bg-orange-500/20 shadow-lg shadow-orange-500/30'
                            : 'border-slate-600 hover:border-slate-500 bg-slate-800/30'
                        }`}
                      >
                        <h3 className="font-bold text-lg mb-2">{type.label}</h3>
                        <p className="text-sm text-slate-400">{type.desc}</p>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Target Length</label>
                    <select
                      value={formData.targetWordCount}
                      onChange={(e) => setFormData({...formData, targetWordCount: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select word count...</option>
                      {wordCounts.map(wc => <option key={wc.value} value={wc.value}>{wc.label}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Number of Chapters</label>
                    <input
                      type="number"
                      placeholder="12"
                      min="1"
                      value={formData.numberOfChapters}
                      onChange={(e) => setFormData({...formData, numberOfChapters: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Writing Style */}
            <div className="bg-gradient-to-r from-amber-900/30 to-slate-900/50 p-8 rounded-2xl border border-amber-500/30">
              <div className="flex items-center mb-6">
                <Lightbulb className="w-6 h-6 mr-3 text-amber-400" />
                <h2 className="text-3xl font-bold text-amber-300">Writing Style</h2>
              </div>

              <div className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-amber-200 mb-3">Narrative Voice</label>
                    <select
                      value={formData.narrativeVoice}
                      onChange={(e) => setFormData({...formData, narrativeVoice: e.target.value})}
                      className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select voice...</option>
                      {narrativeVoices.map(nv => <option key={nv} value={nv}>{nv}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-amber-200 mb-3">Writing Style</label>
                    <select
                      value={formData.writingStyle}
                      onChange={(e) => setFormData({...formData, writingStyle: e.target.value})}
                      className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select style...</option>
                      {writingStyles.map(ws => <option key={ws} value={ws}>{ws}</option>)}
                    </select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-amber-200 mb-3">Reading Level</label>
                    <select
                      value={formData.readingLevel}
                      onChange={(e) => setFormData({...formData, readingLevel: e.target.value})}
                      className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select level...</option>
                      {readingLevels.map(rl => <option key={rl} value={rl}>{rl}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-amber-200 mb-3">Genre (optional)</label>
                    <input
                      type="text"
                      placeholder="Science Fiction, Business, Romance..."
                      value={formData.genre}
                      onChange={(e) => setFormData({...formData, genre: e.target.value})}
                      className="w-full bg-slate-800/70 border border-amber-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Content & Story */}
            <div className="bg-gradient-to-r from-slate-900/50 to-amber-900/30 p-8 rounded-2xl border border-slate-700">
              <div className="flex items-center mb-6">
                <Target className="w-6 h-6 mr-3 text-orange-400" />
                <h2 className="text-3xl font-bold text-orange-300">Content & Story</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Book Premise / Core Concept</label>
                  <textarea
                    placeholder="What is your book fundamentally about? The central idea, conflict, or thesis..."
                    value={formData.premise}
                    onChange={(e) => setFormData({...formData, premise: e.target.value})}
                    rows={5}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Main Themes (one per line)</label>
                  <textarea
                    placeholder="Resilience&#10;Personal transformation&#10;The power of community"
                    value={formData.mainThemes}
                    onChange={(e) => setFormData({...formData, mainThemes: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Plot Outline / Chapter Breakdown</label>
                  <textarea
                    placeholder="Chapter 1: Introduction to the problem&#10;Chapter 2: Historical context&#10;Chapter 3: Modern applications..."
                    value={formData.plotOutline}
                    onChange={(e) => setFormData({...formData, plotOutline: e.target.value})}
                    rows={10}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Character Notes (for fiction) / Key Figures (for non-fiction)</label>
                  <textarea
                    placeholder="Main characters, their backgrounds, motivations, arcs..."
                    value={formData.characterNotes}
                    onChange={(e) => setFormData({...formData, characterNotes: e.target.value})}
                    rows={6}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Target Audience</label>
                  <input
                    type="text"
                    placeholder="Young professionals seeking career guidance"
                    value={formData.targetAudience}
                    onChange={(e) => setFormData({...formData, targetAudience: e.target.value})}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Core Message / Takeaway</label>
                  <textarea
                    placeholder="What should readers think, feel, or do after reading your book?"
                    value={formData.coreMessage}
                    onChange={(e) => setFormData({...formData, coreMessage: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            {/* Additional Elements */}
            <div className="bg-gradient-to-r from-amber-900/30 to-slate-900/50 p-8 rounded-2xl border border-amber-500/30">
              <h2 className="text-3xl font-bold text-amber-300 mb-6">Additional Elements</h2>

              <div className="space-y-4">
                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeIndex}
                    onChange={(e) => setFormData({...formData, includeIndex: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include Index</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeBibliography}
                    onChange={(e) => setFormData({...formData, includeBibliography: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include Bibliography / References</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeGlossary}
                    onChange={(e) => setFormData({...formData, includeGlossary: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include Glossary</span>
                </label>
              </div>
            </div>

            {/* Submit */}
            <div className="text-center pt-8">
              <button
                onClick={createBook}
                disabled={loading || !formData.bookTitle || !formData.bookType || !formData.premise}
                className="bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 disabled:opacity-50 disabled:cursor-not-allowed px-12 py-5 rounded-xl font-bold text-xl shadow-2xl transition transform hover:scale-105"
              >
                {loading ? 'Writing Your Book...' : 'Create Professional Book'}
              </button>
              {(!formData.bookType || !formData.premise) && (
                <p className="text-yellow-400 text-sm mt-3">Please select book type and provide premise</p>
              )}
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-8">
            <div className="animate-spin w-20 h-20 border-4 border-amber-500 border-t-transparent rounded-full mx-auto"></div>
            <h2 className="text-3xl font-bold text-amber-300">Writing Your Manuscript</h2>
            <p className="text-slate-400">AI author is crafting your book...</p>
          </div>
        )}

        {step === 'complete' && (
          <div className="text-center space-y-8">
            <CheckCircle className="w-20 h-20 text-green-400 mx-auto" />
            <h2 className="text-4xl font-bold text-green-300">Book Complete!</h2>
            <p className="text-slate-400">Your manuscript is ready for review</p>
          </div>
        )}

      </div>

      {/* Product Walkthrough */}
      <ProductWalkthrough
        productId="book"
        productName="Book Builder"
        isVisible={showWalkthrough}
        onComplete={completeWalkthrough}
        onSkip={skipWalkthrough}
      />
    </div>
  );
}
