import React, { useState, useEffect } from 'react';
import { Crown, Star, Award, Sparkles, CheckCircle, Users } from 'lucide-react';
import axios from 'axios';

export default function MasterclassPage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    masterclassTitle: '',
    expertName: '',
    expertCredentials: '',
    masterclassDescription: '',
    duration: '',
    numberOfSessions: '',
    deliveryFormat: '',
    includeWorkbook: false,
    includeTemplates: false,
    includeOneOnOne: false,
    includeCommunityAccess: false,
    coreTeachings: '',
    expertStories: '',
    actionableSteps: '',
    bonusMaterials: '',
    pricePoint: '',
    exclusivityLevel: ''
  });
  const [loading, setLoading] = useState(false);

  const durations = ['Half-day Intensive', 'Full-day Workshop', '2-day Immersive', 'Week-long Program', 'Month-long Mentorship'];
  const formats = ['Live Virtual Sessions', 'Pre-recorded Premium Content', 'Hybrid (Live + Recorded)', 'In-person Style Experience'];
  const exclusivity = ['Public', 'Limited Cohort (50 students)', 'Exclusive (25 students)', 'VIP (10 students)', 'One-on-One'];

  const createMasterclass = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/masterclass/create', formData, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setStep('complete');
    } catch (error) {
      console.error('Masterclass creation failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-16">
        
        <div className="text-center mb-16">
          <div className="w-24 h-24 mx-auto bg-gradient-to-r from-purple-500 via-pink-500 to-yellow-500 rounded-full flex items-center justify-center shadow-2xl mb-6 animate-pulse">
            <Crown className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-yellow-400 bg-clip-text text-transparent mb-4">
            Premium Masterclass
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Create an exclusive, high-ticket masterclass that commands premium pricing with unparalleled expertise and transformational content
          </p>
          <div className="flex items-center justify-center gap-2 mt-4">
            <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
            <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
            <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
            <span className="text-yellow-400 font-semibold ml-2">Premium Offering</span>
          </div>
        </div>

        {step === 'input' && (
          <div className="space-y-12">
            
            <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 p-8 rounded-2xl border-2 border-purple-500/50 shadow-2xl">
              <div className="flex items-center mb-6">
                <Award className="w-6 h-6 mr-3 text-purple-300" />
                <h2 className="text-3xl font-bold text-purple-200">Masterclass Identity</h2>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-purple-100 mb-3">Masterclass Title</label>
                  <input
                    type="text"
                    placeholder="The CEO's Blueprint to 10X Growth"
                    value={formData.masterclassTitle}
                    onChange={(e) => setFormData({...formData, masterclassTitle: e.target.value})}
                    className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-purple-100 mb-3">Expert Name (You)</label>
                    <input
                      type="text"
                      placeholder="Dr. Jane Smith"
                      value={formData.expertName}
                      onChange={(e) => setFormData({...formData, expertName: e.target.value})}
                      className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                    />
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-purple-100 mb-3">Credentials & Authority</label>
                    <input
                      type="text"
                      placeholder="20+ years, Built 3 $100M companies..."
                      value={formData.expertCredentials}
                      onChange={(e) => setFormData({...formData, expertCredentials: e.target.value})}
                      className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-purple-100 mb-3">Masterclass Description</label>
                  <textarea
                    placeholder="The transformational experience that will revolutionize your approach to..."
                    value={formData.masterclassDescription}
                    onChange={(e) => setFormData({...formData, masterclassDescription: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-indigo-900/40 to-purple-900/40 p-8 rounded-2xl border-2 border-indigo-500/50">
              <div className="flex items-center mb-6">
                <Sparkles className="w-6 h-6 mr-3 text-indigo-300" />
                <h2 className="text-3xl font-bold text-indigo-200">Premium Experience Design</h2>
              </div>

              <div className="space-y-6">
                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Duration</label>
                    <select
                      value={formData.duration}
                      onChange={(e) => setFormData({...formData, duration: e.target.value})}
                      className="w-full bg-slate-900/70 border-2 border-indigo-500/50 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select duration...</option>
                      {durations.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Number of Sessions</label>
                    <input
                      type="number"
                      placeholder="6"
                      value={formData.numberOfSessions}
                      onChange={(e) => setFormData({...formData, numberOfSessions: e.target.value})}
                      className="w-full bg-slate-900/70 border-2 border-indigo-500/50 rounded-lg px-6 py-4 text-white text-lg"
                    />
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Exclusivity Level</label>
                    <select
                      value={formData.exclusivityLevel}
                      onChange={(e) => setFormData({...formData, exclusivityLevel: e.target.value})}
                      className="w-full bg-slate-900/70 border-2 border-indigo-500/50 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select...</option>
                      {exclusivity.map(ex => <option key={ex} value={ex}>{ex}</option>)}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Delivery Format</label>
                  <select
                    value={formData.deliveryFormat}
                    onChange={(e) => setFormData({...formData, deliveryFormat: e.target.value})}
                    className="w-full bg-slate-900/70 border-2 border-indigo-500/50 rounded-lg px-6 py-4 text-white text-lg"
                  >
                    <option value="">Select format...</option>
                    {formats.map(f => <option key={f} value={f}>{f}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Price Point (USD)</label>
                  <input
                    type="number"
                    placeholder="2997"
                    value={formData.pricePoint}
                    onChange={(e) => setFormData({...formData, pricePoint: e.target.value})}
                    className="w-full bg-slate-900/70 border-2 border-indigo-500/50 rounded-lg px-6 py-4 text-white text-lg"
                  />
                  <p className="text-slate-400 text-sm mt-2">Premium masterclasses typically range from $997 - $25,000+</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-purple-900/40 to-indigo-900/40 p-8 rounded-2xl border-2 border-purple-500/50">
              <div className="flex items-center mb-6">
                <Users className="w-6 h-6 mr-3 text-purple-300" />
                <h2 className="text-3xl font-bold text-purple-200">Transformational Content</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-purple-100 mb-3">Core Teachings & Framework</label>
                  <textarea
                    placeholder="The proprietary system you've developed...&#10;Step 1: Foundation&#10;Step 2: Implementation&#10;Step 3: Optimization"
                    value={formData.coreTeachings}
                    onChange={(e) => setFormData({...formData, coreTeachings: e.target.value})}
                    rows={10}
                    className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-purple-100 mb-3">Expert Stories & Case Studies</label>
                  <textarea
                    placeholder="Real examples from your experience, client success stories, lessons learned..."
                    value={formData.expertStories}
                    onChange={(e) => setFormData({...formData, expertStories: e.target.value})}
                    rows={6}
                    className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-purple-100 mb-3">Actionable Steps & Implementation</label>
                  <textarea
                    placeholder="Exactly what participants will DO during and after the masterclass..."
                    value={formData.actionableSteps}
                    onChange={(e) => setFormData({...formData, actionableSteps: e.target.value})}
                    rows={6}
                    className="w-full bg-slate-900/70 border-2 border-purple-500/50 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-yellow-900/30 to-purple-900/40 p-8 rounded-2xl border-2 border-yellow-500/50">
              <h2 className="text-3xl font-bold text-yellow-300 mb-6">Premium Bonuses & Extras</h2>

              <div className="space-y-4">
                <label className="flex items-center space-x-3 p-4 bg-slate-900/50 rounded-lg border border-yellow-500/30">
                  <input
                    type="checkbox"
                    checked={formData.includeWorkbook}
                    onChange={(e) => setFormData({...formData, includeWorkbook: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Premium Workbook & Implementation Guide</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-900/50 rounded-lg border border-yellow-500/30">
                  <input
                    type="checkbox"
                    checked={formData.includeTemplates}
                    onChange={(e) => setFormData({...formData, includeTemplates: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Done-For-You Templates & Resources</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-900/50 rounded-lg border border-yellow-500/30">
                  <input
                    type="checkbox"
                    checked={formData.includeOneOnOne}
                    onChange={(e) => setFormData({...formData, includeOneOnOne: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">1-on-1 Session with Expert (VIP Add-on)</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-900/50 rounded-lg border border-yellow-500/30">
                  <input
                    type="checkbox"
                    checked={formData.includeCommunityAccess}
                    onChange={(e) => setFormData({...formData, includeCommunityAccess: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Private Community Access & Lifetime Support</span>
                </label>
              </div>
            </div>

            <div className="text-center pt-8">
              <button
                onClick={createMasterclass}
                disabled={loading || !formData.masterclassTitle || !formData.coreTeachings}
                className="bg-gradient-to-r from-purple-600 via-pink-600 to-yellow-600 hover:from-purple-700 hover:via-pink-700 hover:to-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed px-12 py-6 rounded-xl font-bold text-2xl shadow-2xl transition transform hover:scale-105 border-2 border-yellow-400/50"
              >
                {loading ? 'Creating Your Masterclass...' : '✨ Create Premium Masterclass ✨'}
              </button>
              {!formData.coreTeachings && (
                <p className="text-yellow-400 text-sm mt-3">Please provide your core teachings</p>
              )}
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-8">
            <div className="animate-spin w-20 h-20 border-4 border-purple-500 border-t-transparent rounded-full mx-auto"></div>
            <h2 className="text-3xl font-bold text-purple-300">Crafting Your Premium Masterclass</h2>
            <p className="text-slate-400">Building transformational content...</p>
          </div>
        )}

        {step === 'complete' && (
          <div className="text-center space-y-8">
            <CheckCircle className="w-20 h-20 text-yellow-400 mx-auto" />
            <h2 className="text-4xl font-bold text-yellow-300">Masterclass Ready!</h2>
            <p className="text-slate-400">Your premium masterclass is ready to launch</p>
          </div>
        )}

      </div>
    </div>
  );
}
