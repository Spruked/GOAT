import React, { useState, useEffect } from 'react';
import { Mic, Headphones, Waves, Radio, Users, Music, FileText, Settings, Sparkles, CheckCircle, Clock, TrendingUp, Zap } from 'lucide-react';
import axios from 'axios';
import { ProductWalkthrough } from '../components/ProductWalkthrough';
import { useProductWalkthrough } from '../hooks/useProductWalkthrough';

export default function PodcastPage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    // Show Identity
    showTitle: '',
    showTagline: '',
    showDescription: '',
    showCategory: '',
    
    // Episode Details
    episodeTitle: '',
    episodeNumber: '',
    seasonNumber: '',
    episodeType: '',
    episodeDuration: '',
    releaseSchedule: 'single',
    
    // Voice & Performance
    hostVoice: '',
    hostName: '',
    coHostVoice: '',
    coHostName: '',
    hasCoHost: false,
    guestVoice: '',
    guestName: '',
    hasGuest: false,
    
    // Tone & Style
    conversationStyle: '',
    pacing: '',
    energyLevel: '',
    formality: '',
    
    // Audio Production
    introMusicStyle: '',
    outroMusicStyle: '',
    transitionStyle: '',
    includeIntro: true,
    includeOutro: true,
    includeMusicBed: false,
    soundEffects: false,
    
    // Content Structure
    episodeOutline: '',
    keyTalkingPoints: '',
    openingHook: '',
    closingStatement: '',
    researchSources: '',
    
    // Audience & Messaging
    targetAudience: '',
    targetListenerLevel: '',
    callToAction: '',
    sponsorMention: '',
    
    // Distribution
    distributionChannels: [],
    explicitContent: false,
    episodeTags: ''
  });
  const [voices, setVoices] = useState([]);
  const [loading, setLoading] = useState(false);

  // Product walkthrough hook
  const {
    showWalkthrough,
    completeWalkthrough,
    skipWalkthrough
  } = useProductWalkthrough('podcast');

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

  const episodeTypes = [
    { value: 'solo_monologue', label: 'Solo Monologue', desc: 'Single host deep-dive', icon: Mic },
    { value: 'interview', label: 'Interview', desc: 'Host + guest Q&A', icon: Users },
    { value: 'cohosted_conversation', label: 'Co-Hosted Discussion', desc: 'Two hosts conversing', icon: Headphones },
    { value: 'panel_roundtable', label: 'Panel Roundtable', desc: 'Multiple expert voices', icon: Radio },
    { value: 'narrative_storytelling', label: 'Narrative Story', desc: 'Scripted documentary style', icon: FileText },
    { value: 'news_commentary', label: 'News & Commentary', desc: 'Current events analysis', icon: TrendingUp }
  ];

  const showCategories = [
    'Business & Entrepreneurship',
    'Technology & Innovation',
    'Education & Knowledge',
    'Health & Wellness',
    'Arts & Culture',
    'News & Politics',
    'Science & Research',
    'Personal Development',
    'Comedy & Entertainment',
    'True Crime & Mystery',
    'Sports & Recreation',
    'Society & Culture'
  ];

  const durations = [
    { value: '5-10', label: '5-10 minutes', desc: 'Quick insights' },
    { value: '15-20', label: '15-20 minutes', desc: 'Commute-friendly' },
    { value: '30-40', label: '30-40 minutes', desc: 'Standard episode' },
    { value: '45-60', label: '45-60 minutes', desc: 'Long-form discussion' },
    { value: '60-90', label: '60-90 minutes', desc: 'Deep dive session' },
    { value: '90+', label: '90+ minutes', desc: 'Extended conversation' }
  ];

  const conversationStyles = [
    'Casual & Friendly',
    'Professional & Polished',
    'Educational & Informative',
    'Entertaining & Humorous',
    'Investigative & Analytical',
    'Inspirational & Motivational',
    'Debate & Discussion',
    'Storytelling & Narrative'
  ];

  const pacingOptions = ['Relaxed', 'Moderate', 'Brisk', 'Dynamic'];
  const energyLevels = ['Calm', 'Balanced', 'Energetic', 'High-Energy'];
  const formalityLevels = ['Informal', 'Semi-Formal', 'Professional', 'Academic'];

  const musicStyles = [
    'Modern Electronic',
    'Upbeat Indie',
    'Corporate Professional',
    'Jazz & Lounge',
    'Cinematic Orchestral',
    'Ambient Atmospheric',
    'Rock & Guitar',
    'Hip Hop Beats',
    'None'
  ];

  const transitionStyles = [
    'Smooth Fade',
    'Quick Cut',
    'Music Sting',
    'Sound Effect',
    'None'
  ];

  const listenerLevels = [
    'Beginner (No prior knowledge)',
    'Intermediate (Some familiarity)',
    'Advanced (Industry professionals)',
    'Mixed (All levels welcome)'
  ];

  const distributionOptions = [
    'Apple Podcasts',
    'Spotify',
    'YouTube',
    'Google Podcasts',
    'Amazon Music',
    'RSS Feed Only'
  ];

  const createPodcast = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/podcast/create', formData, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      setTimeout(() => {
        setStep('complete');
      }, 2000);
    } catch (error) {
      console.error('Podcast creation failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  const toggleDistribution = (channel) => {
    setFormData(prev => ({
      ...prev,
      distributionChannels: prev.distributionChannels.includes(channel)
        ? prev.distributionChannels.filter(c => c !== channel)
        : [...prev.distributionChannels, channel]
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-slate-900 to-indigo-950 text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        
        {/* Premium Header */}
        <div className="text-center mb-12">
          <div className="relative inline-block mb-6">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full blur-xl opacity-50 animate-pulse"></div>
            <div className="relative w-24 h-24 mx-auto bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center shadow-2xl border-4 border-purple-400/30">
              <Mic className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-300 via-pink-300 to-purple-300 bg-clip-text text-transparent mb-3">
            Professional Podcast Studio
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto font-light leading-relaxed">
            Broadcast-quality podcast production with AI-powered scripting, multi-voice synthesis, and studio-grade audio mastering
          </p>
          <div className="flex items-center justify-center gap-4 mt-6 text-sm text-purple-300">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              <span>Professional Audio</span>
            </div>
            <span className="text-purple-700">•</span>
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              <span>Multi-Voice Support</span>
            </div>
            <span className="text-purple-700">•</span>
            <div className="flex items-center gap-2">
              <Radio className="w-4 h-4" />
              <span>Distribution Ready</span>
            </div>
          </div>
        </div>

        {step === 'input' && (
          <div className="space-y-8">
            
            {/* 1. Show Identity */}
            <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 p-8 rounded-2xl border border-purple-500/30 shadow-2xl">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mr-4">
                  <Radio className="w-6 h-6 text-purple-300" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-purple-200">Show Identity</h2>
                  <p className="text-purple-400 text-sm mt-1">Brand your podcast for recognition</p>
                </div>
              </div>
              
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-semibold text-purple-200 mb-2 uppercase tracking-wide">Show Title</label>
                  <input
                    type="text"
                    placeholder="The Innovation Podcast"
                    value={formData.showTitle}
                    onChange={(e) => setFormData({...formData, showTitle: e.target.value})}
                    className="w-full bg-slate-900/60 border border-purple-500/40 rounded-lg px-5 py-3 text-white placeholder-slate-500 text-lg focus:border-purple-400 focus:ring-2 focus:ring-purple-400/30 transition"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-purple-200 mb-2 uppercase tracking-wide">Show Tagline</label>
                  <input
                    type="text"
                    placeholder="Exploring breakthrough ideas that shape tomorrow"
                    value={formData.showTagline}
                    onChange={(e) => setFormData({...formData, showTagline: e.target.value})}
                    className="w-full bg-slate-900/60 border border-purple-500/40 rounded-lg px-5 py-3 text-white placeholder-slate-500 focus:border-purple-400 focus:ring-2 focus:ring-purple-400/30 transition"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-purple-200 mb-2 uppercase tracking-wide">Show Description</label>
                  <textarea
                    placeholder="Weekly conversations with visionaries, entrepreneurs, and thought leaders about the innovations shaping our future..."
                    value={formData.showDescription}
                    onChange={(e) => setFormData({...formData, showDescription: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-900/60 border border-purple-500/40 rounded-lg px-5 py-3 text-white placeholder-slate-500 focus:border-purple-400 focus:ring-2 focus:ring-purple-400/30 transition resize-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-purple-200 mb-2 uppercase tracking-wide">Show Category</label>
                  <select
                    value={formData.showCategory}
                    onChange={(e) => setFormData({...formData, showCategory: e.target.value})}
                    className="w-full bg-slate-900/60 border border-purple-500/40 rounded-lg px-5 py-3 text-white focus:border-purple-400 focus:ring-2 focus:ring-purple-400/30 transition"
                  >
                    <option value="">Select category...</option>
                    {showCategories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* 2. Episode Details */}
            <div className="bg-gradient-to-r from-slate-900/60 to-purple-900/40 p-8 rounded-2xl border border-slate-700/50 shadow-2xl">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-pink-500/20 rounded-xl flex items-center justify-center mr-4">
                  <FileText className="w-6 h-6 text-pink-300" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-pink-200">Episode Configuration</h2>
                  <p className="text-pink-400 text-sm mt-1">Structure and format details</p>
                </div>
              </div>

              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-semibold text-slate-200 mb-2 uppercase tracking-wide">Episode Title</label>
                  <input
                    type="text"
                    placeholder="How AI is Reshaping Creative Work"
                    value={formData.episodeTitle}
                    onChange={(e) => setFormData({...formData, episodeTitle: e.target.value})}
                    className="w-full bg-slate-900/60 border border-slate-600 rounded-lg px-5 py-3 text-white placeholder-slate-500 text-lg focus:border-pink-400 focus:ring-2 focus:ring-pink-400/30 transition"
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold text-slate-200 mb-2 uppercase tracking-wide">Episode Number</label>
                    <input
                      type="text"
                      placeholder="42"
                      value={formData.episodeNumber}
                      onChange={(e) => setFormData({...formData, episodeNumber: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-600 rounded-lg px-5 py-3 text-white placeholder-slate-500 focus:border-pink-400 focus:ring-2 focus:ring-pink-400/30 transition"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-200 mb-2 uppercase tracking-wide">Season Number (optional)</label>
                    <input
                      type="text"
                      placeholder="2"
                      value={formData.seasonNumber}
                      onChange={(e) => setFormData({...formData, seasonNumber: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-600 rounded-lg px-5 py-3 text-white placeholder-slate-500 focus:border-pink-400 focus:ring-2 focus:ring-pink-400/30 transition"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-200 mb-3 uppercase tracking-wide">Episode Format</label>
                  <div className="grid md:grid-cols-3 gap-3">
                    {episodeTypes.map((type) => {
                      const Icon = type.icon;
                      return (
                        <button
                          key={type.value}
                          onClick={() => setFormData({...formData, episodeType: type.value})}
                          className={`p-5 rounded-xl border-2 transition text-left ${
                            formData.episodeType === type.value
                              ? 'border-pink-500 bg-pink-500/20 shadow-lg shadow-pink-500/20'
                              : 'border-slate-700 hover:border-slate-600 bg-slate-900/40'
                          }`}
                        >
                          <Icon className={`w-6 h-6 mb-2 ${formData.episodeType === type.value ? 'text-pink-400' : 'text-slate-500'}`} />
                          <h3 className="font-bold text-base mb-1">{type.label}</h3>
                          <p className="text-xs text-slate-400">{type.desc}</p>
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-200 mb-3 uppercase tracking-wide">Episode Duration</label>
                  <div className="grid md:grid-cols-3 gap-3">
                    {durations.map((dur) => (
                      <button
                        key={dur.value}
                        onClick={() => setFormData({...formData, episodeDuration: dur.value})}
                        className={`p-4 rounded-lg border-2 transition text-left ${
                          formData.episodeDuration === dur.value
                            ? 'border-pink-500 bg-pink-500/20'
                            : 'border-slate-700 hover:border-slate-600 bg-slate-900/40'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <h3 className="font-bold text-sm">{dur.label}</h3>
                          <Clock className="w-4 h-4 text-slate-500" />
                        </div>
                        <p className="text-xs text-slate-400">{dur.desc}</p>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* 3. Voice Configuration - Continued in next part due to length... */}

            <div className="text-center pt-6">
              <button
                onClick={createPodcast}
                disabled={loading || !formData.showTitle || !formData.episodeType || !formData.hostVoice}
                className="group relative bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 hover:from-purple-700 hover:via-pink-700 hover:to-purple-700 disabled:opacity-40 disabled:cursor-not-allowed px-12 py-5 rounded-xl font-bold text-xl shadow-2xl transition-all duration-300 transform hover:scale-105 hover:shadow-purple-500/50"
              >
                <span className="relative z-10 flex items-center justify-center gap-3">
                  <Sparkles className="w-6 h-6" />
                  {loading ? 'Producing Podcast...' : 'Produce Professional Podcast'}
                </span>
              </button>
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-8 py-20">
            <div className="relative">
              <div className="animate-spin w-20 h-20 border-4 border-purple-500/30 border-t-purple-500 rounded-full mx-auto"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Waves className="w-8 h-8 text-purple-400 animate-pulse" />
              </div>
            </div>
            <div>
              <h2 className="text-4xl font-bold text-purple-300 mb-3">Producing Your Podcast</h2>
              <p className="text-slate-400 font-light">Professional audio engineering and mastering in progress...</p>
            </div>
          </div>
        )}

        {step === 'complete' && (
          <div className="text-center space-y-8 py-20">
            <CheckCircle className="w-24 h-24 text-green-400 mx-auto" />
            <h2 className="text-5xl font-bold text-green-300">Podcast Ready!</h2>
            <p className="text-xl text-slate-400">Your professional podcast episode is ready to publish</p>
          </div>
        )}

      </div>

      {/* Product Walkthrough */}
      <ProductWalkthrough
        productId="podcast"
        productName="Podcast Engine"
        isVisible={showWalkthrough}
        onComplete={completeWalkthrough}
        onSkip={skipWalkthrough}
      />
    </div>
  );
}
