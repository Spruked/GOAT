import React, { useState, useEffect } from 'react';
import { Headphones, BookOpen, Waves, Clock, CheckCircle } from 'lucide-react';
import axios from 'axios';

export default function AudiobookPage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    audiobookTitle: '',
    author: '',
    narrator: '',
    duration: '',
    chapterCount: '',
    pacing: '',
    emotionalTone: '',
    voiceGender: '',
    voiceAge: '',
    accent: '',
    bookContent: '',
    chapterBreakdown: '',
    pronunciationGuide: '',
    musicBetweenChapters: false,
    soundEffects: false,
    backgroundAmbience: ''
  });
  const [voices, setVoices] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchVoices = async () => {
      try {
        const response = await axios.get('/podcast/voices');
        setVoices(response.data.voices);
      } catch (error) {
        console.error('Failed to fetch voices:', error);
      }
    };
    fetchVoices();
  }, []);

  const durations = ['Under 3 hours', '3-5 hours', '5-8 hours', '8-12 hours', '12+ hours'];
  const pacing = ['Slow & Deliberate', 'Moderate', 'Brisk', 'Fast-paced'];
  const emotionalTones = ['Neutral', 'Warm & Inviting', 'Dramatic', 'Suspenseful', 'Inspirational', 'Authoritative'];
  const accents = ['American', 'British', 'Australian', 'Neutral', 'Regional'];
  const ambience = ['None', 'Light Background', 'Nature Sounds', 'Cafe Atmosphere', 'Library Quiet'];

  const createAudiobook = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/audiobook/create', formData, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setStep('complete');
    } catch (error) {
      console.error('Audiobook creation failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-slate-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-16">
        
        <div className="text-center mb-16">
          <div className="w-24 h-24 mx-auto bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center shadow-2xl mb-6">
            <Headphones className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-4">
            Professional Audiobook Production
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Transform your manuscript into a studio-quality audiobook with professional voice narration and audio engineering
          </p>
        </div>

        {step === 'input' && (
          <div className="space-y-12">
            
            <div className="bg-gradient-to-r from-blue-900/30 to-cyan-900/30 p-8 rounded-2xl border border-blue-500/30">
              <div className="flex items-center mb-6">
                <BookOpen className="w-6 h-6 mr-3 text-blue-400" />
                <h2 className="text-3xl font-bold text-blue-300">Audiobook Details</h2>
              </div>
              
              <div className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-blue-200 mb-3">Audiobook Title</label>
                    <input
                      type="text"
                      placeholder="The Complete Guide to..."
                      value={formData.audiobookTitle}
                      onChange={(e) => setFormData({...formData, audiobookTitle: e.target.value})}
                      className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                    />
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-blue-200 mb-3">Author Name</label>
                    <input
                      type="text"
                      placeholder="John Smith"
                      value={formData.author}
                      onChange={(e) => setFormData({...formData, author: e.target.value})}
                      className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-blue-200 mb-3">Target Duration</label>
                    <select
                      value={formData.duration}
                      onChange={(e) => setFormData({...formData, duration: e.target.value})}
                      className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select duration...</option>
                      {durations.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-blue-200 mb-3">Number of Chapters</label>
                    <input
                      type="number"
                      placeholder="15"
                      value={formData.chapterCount}
                      onChange={(e) => setFormData({...formData, chapterCount: e.target.value})}
                      className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white text-lg"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-slate-900/50 to-blue-900/30 p-8 rounded-2xl border border-slate-700">
              <div className="flex items-center mb-6">
                <Waves className="w-6 h-6 mr-3 text-cyan-400" />
                <h2 className="text-3xl font-bold text-cyan-300">Narration Style</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Professional Narrator Voice</label>
                  <select
                    value={formData.narrator}
                    onChange={(e) => setFormData({...formData, narrator: e.target.value})}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                  >
                    <option value="">Select narrator voice...</option>
                    {voices.map(v => <option key={v.id} value={v.id}>{v.name} ({v.gender})</option>)}
                  </select>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Narration Pacing</label>
                    <select
                      value={formData.pacing}
                      onChange={(e) => setFormData({...formData, pacing: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select pacing...</option>
                      {pacing.map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Emotional Tone</label>
                    <select
                      value={formData.emotionalTone}
                      onChange={(e) => setFormData({...formData, emotionalTone: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select tone...</option>
                      {emotionalTones.map(et => <option key={et} value={et}>{et}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Accent Preference</label>
                    <select
                      value={formData.accent}
                      onChange={(e) => setFormData({...formData, accent: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select accent...</option>
                      {accents.map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-blue-900/30 to-slate-900/50 p-8 rounded-2xl border border-blue-500/30">
              <div className="flex items-center mb-6">
                <Clock className="w-6 h-6 mr-3 text-blue-400" />
                <h2 className="text-3xl font-bold text-blue-300">Content & Script</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-blue-200 mb-3">Full Book Content / Manuscript</label>
                  <textarea
                    placeholder="Paste your complete book manuscript here..."
                    value={formData.bookContent}
                    onChange={(e) => setFormData({...formData, bookContent: e.target.value})}
                    rows={15}
                    className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg font-mono"
                  />
                  <p className="text-slate-400 text-sm mt-2">Pro tip: Upload your document or paste text directly</p>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-blue-200 mb-3">Chapter Breakdown (optional)</label>
                  <textarea
                    placeholder="Chapter 1: Introduction - starts at paragraph 1&#10;Chapter 2: The Beginning - starts at paragraph 15..."
                    value={formData.chapterBreakdown}
                    onChange={(e) => setFormData({...formData, chapterBreakdown: e.target.value})}
                    rows={6}
                    className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-blue-200 mb-3">Pronunciation Guide (optional)</label>
                  <textarea
                    placeholder="Character names, technical terms, foreign words...&#10;Hermione = her-MY-oh-nee&#10;Entrepreneur = on-truh-pruh-NUR"
                    value={formData.pronunciationGuide}
                    onChange={(e) => setFormData({...formData, pronunciationGuide: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-800/70 border border-blue-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-slate-900/50 to-blue-900/30 p-8 rounded-2xl border border-slate-700">
              <h2 className="text-3xl font-bold text-cyan-300 mb-6">Audio Production Options</h2>

              <div className="space-y-4">
                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.musicBetweenChapters}
                    onChange={(e) => setFormData({...formData, musicBetweenChapters: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Add music transitions between chapters</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.soundEffects}
                    onChange={(e) => setFormData({...formData, soundEffects: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include subtle sound effects for immersion</span>
                </label>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Background Ambience</label>
                  <select
                    value={formData.backgroundAmbience}
                    onChange={(e) => setFormData({...formData, backgroundAmbience: e.target.value})}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                  >
                    <option value="">Select ambience...</option>
                    {ambience.map(a => <option key={a} value={a}>{a}</option>)}
                  </select>
                </div>
              </div>
            </div>

            <div className="text-center pt-8">
              <button
                onClick={createAudiobook}
                disabled={loading || !formData.audiobookTitle || !formData.narrator || !formData.bookContent}
                className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed px-12 py-5 rounded-xl font-bold text-xl shadow-2xl transition transform hover:scale-105"
              >
                {loading ? 'Producing Your Audiobook...' : 'Create Professional Audiobook'}
              </button>
              {(!formData.narrator || !formData.bookContent) && (
                <p className="text-yellow-400 text-sm mt-3">Please select narrator and provide manuscript content</p>
              )}
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-8">
            <div className="animate-spin w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
            <h2 className="text-3xl font-bold text-blue-300">Narrating Your Audiobook</h2>
            <p className="text-slate-400">Professional voice recording in progress...</p>
          </div>
        )}

        {step === 'complete' && (
          <div className="text-center space-y-8">
            <CheckCircle className="w-20 h-20 text-green-400 mx-auto" />
            <h2 className="text-4xl font-bold text-green-300">Audiobook Complete!</h2>
            <p className="text-slate-400">Your professional audiobook is ready for distribution</p>
          </div>
        )}

      </div>
    </div>
  );
}
