import React, { useState, useEffect } from 'react';
import { Heart, Upload, Lock, Calendar, Users, Music, CheckCircle, X } from 'lucide-react';
import axios from 'axios';

export default function LegacyAssembliesPage() {
  const [step, setStep] = useState('input');
  const [showOrientation, setShowOrientation] = useState(true);
  const [formData, setFormData] = useState({
    assemblyTitle: '',
    personName: '',
    relationship: '',
    birthDate: '',
    significantDate: '',
    assemblyType: 'chronological',
    includeMusic: false,
    musicSelection: '',
    personalMessage: '',
    contextNotes: ''
  });
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const dismissed = localStorage.getItem('legacy_orientation_dismissed');
    if (dismissed) {
      setShowOrientation(false);
    }
  }, []);

  const dismissOrientation = () => {
    setShowOrientation(false);
    localStorage.setItem('legacy_orientation_dismissed', 'true');
  };

  const relationships = [
    'Father',
    'Mother',
    'Partner',
    'Child',
    'Sibling',
    'Friend',
    'Mentor',
    'Pet',
    'Other'
  ];

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    setUploadedFiles(prev => [...prev, ...files.map(file => ({
      file,
      name: file.name,
      type: file.type,
      size: file.size
    }))]);
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const assembleArchive = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const submitData = new FormData();
      
      Object.entries(formData).forEach(([key, value]) => {
        submitData.append(key, value);
      });

      uploadedFiles.forEach(item => {
        submitData.append('files', item.file);
      });

      const response = await axios.post('/api/legacy/assemble', submitData, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setStep('threshold');
    } catch (error) {
      console.error('Assembly failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-800 via-slate-900 to-slate-950 text-slate-200">
      <div className="max-w-5xl mx-auto px-4 py-12">
        
        {/* Header */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 mx-auto bg-slate-700/50 rounded-full flex items-center justify-center mb-6 border-2 border-slate-600">
            <Heart className="w-10 h-10 text-slate-400" />
          </div>
          <h1 className="text-4xl font-light text-slate-300 mb-3">
            Legacy Assemblies
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto font-light">
            Preserve cherished memories with dignity and care. Assemble meaningful tributes for those who matter most.
          </p>
          <div className="flex items-center justify-center gap-3 mt-4 text-slate-500 text-sm">
            <Lock className="w-4 h-4" />
            <span>Private archive only · Never public</span>
            <span className="text-slate-700">·</span>
            <button className="text-slate-500 hover:text-slate-400 underline transition">
              Ensure this archive endures
            </button>
          </div>
        </div>

        {/* Gentle Orientation */}
        {showOrientation && step === 'input' && (
          <div className="bg-slate-800/30 border border-slate-700/40 rounded-lg p-4 mb-8">
            <div className="flex items-start justify-between">
              <p className="text-slate-400 font-light text-sm">
                This space is private and unhurried. Upload what matters, in your own time.
              </p>
              <button
                onClick={dismissOrientation}
                className="text-slate-600 hover:text-slate-400 transition ml-4 flex-shrink-0"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {step === 'input' && (
          <div className="space-y-8">
            
            {/* Person Details */}
            <div className="bg-slate-800/40 p-8 rounded-lg border border-slate-700/50">
              <div className="flex items-center mb-6">
                <Users className="w-5 h-5 mr-3 text-slate-400" />
                <h2 className="text-2xl font-light text-slate-300">Who This Preserves</h2>
              </div>
              
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                    Assembly Title60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 placeholder-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Relationship
                    </label>60 border border-slate-700/7
                    <select
                      value={formData.relationship}
                      onChange={(e) => setFormData({...formData, relationship: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-700/7
                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Full Name
                    </label>
                    <input
                      type="text"
                      placeholder="John Robert Smith"
                      value={formData.personName}
                      onChange={(e) => setFormData({...formData, personName: e.target.value})}
                      className="w-full bg-slate-900/50 border border-slate-700 rounded px-4 py-3 text-slate-200 placeholder-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Relationship
                    </label>
                    <select
                      value={formData.relationship}
                      onChange={(e) => setFormData({...formData, relationship: e.target.value})}
                      className="w-full bg-slate-900/50 border border-slate-700 rounded px-4 py-3 text-slate-200 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    >
                      <option value="">Select relationship...</option>
                      {relationships.map(rel => (
                        <option key={rel} value={rel}>{rel}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Birth Date (optional)
                    </label>
                    <input
                      type="date"
                      value={formData.birthDate}
                      onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Significant Date (optional)
                    </label>
                    <input
                      type="date"
                      value={formData.significantDate}
                      onChange={(e) => setFormData({...formData, significantDate: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Assembly Structure */}
            <div className="bg-slate-800/40 p-8 rounded-lg border border-slate-700/50">
              <div className="flex items-center mb-6">
                <Calendar className="w-5 h-5 mr-3 text-slate-400" />
                <h2 className="text-2xl font-light text-slate-300">Assembly Structure</h2>
              </div>

              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-light text-slate-400 mb-3 uppercase tracking-wide">
                    Arrangement Type
                  </label>
                  <div className="grid md:grid-cols-2 gap-4">
                    <button
                      onClick={() => setFormData({...formData, assemblyType: 'chronological'})}
                      className={`p-5 rounded border-2 transition text-left ${
                        formData.assemblyType === 'chronological'
                          ? 'border-slate-500 bg-slate-700/30'
                          : 'border-slate-700 hover:border-slate-600'
                      }`}
                    >
                      <h3 className="font-normal text-slate-200 mb-1">Chronological</h3>
                      <p className="text-sm text-slate-500 font-light">Arranged by time and date</p>
                    </button>

                    <button
                      onClick={() => setFormData({...formData, assemblyType: 'thematic'})}
                      className={`p-5 rounded border-2 transition text-left ${
                        formData.assemblyType === 'thematic'
                          ? 'border-slate-500 bg-slate-700/30'
                          : 'border-slate-700 hover:border-slate-600'
                      }`}
                    >
                      <h3 className="font-normal text-slate-200 mb-1">Thematic</h3>
                      <p className="text-sm text-slate-500 font-light">Arranged by meaning and context</p>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Upload Media */}
            <div className="bg-slate-800/40 p-8 rounded-lg border border-slate-700/50">
              <div className="flex items-center mb-6">
                <Upload className="w-5 h-5 mr-3 text-slate-400" />
                <h2 className="text-2xl font-light text-slate-300">Media to Preserve</h2>
              </div>

              <div className="space-y-5">
                <div className="border-2 border-dashed border-slate-700 rounded-lg p-8 text-center hover:border-slate-600 transition">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-slate-600" />
                  <label className="cursor-pointer">
                    <span className="text-slate-400 font-light">Upload photos, videos, audio, or documents</span>
                    <input
                      type="file"
                      multiple
                      accept="image/*,video/*,audio/*,.pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>
                  <p className="text-sm text-slate-600 mt-2 font-light">All formats accepted · No limit</p>
                </div>

                {uploadedFiles.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400 uppercase tracking-wide font-light">
                      {uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''} ready to preserve
                    </p>
                    <div className="space-y-2">
                      {uploadedFiles.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-slate-900/50 rounded border border-slate-700/50">
                          <span className="text-slate-300 text-sm font-light truncate flex-1">{item.name}</span>
                          <button
                            onClick={() => removeFile(index)}
                            className="text-slate-500 hover:text-slate-300 text-sm ml-4"
                          >
                            Remove
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                <p className="text-slate-500 text-sm font-light mt-2 ml-1">
                  Music, if used, should remain secondary to voices.
                </p>
                )}
              </div>
            </div>

            {/* Optional Music */}
            <div className="bg-slate-800/40 p-8 rounded-lg border border-slate-700/50">
              <div className="flex items-center mb-6">
                <Music className="w-5 h-5 mr-3 text-slate-400" />
                <h2 className="text-2xl font-light text-slate-300">Background Music (Optional)</h2>
              </div>

              <div className="space-y-5">
                <label className="flex items-center space-x-3 p-4 bg-slate-900/30 rounded cursor-pointer hover:bg-slate-900/50 transition">
                  <input
                    type="checkbox"
                    checked={formData.includeMusic}
                    onChange={(e) => setFormData({...formData, includeMusic: e.target.checked})}
                    className="w-4 h-4 rounded border-slate-600"
                  />
                  <span className="text-slate-300 font-light">Include background music</span>
                </label>

                {formData.includeMusic && (
                  <div>
                    <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                      Music Preference
                    </label>
                    <input
                      type="text"
                      placeholder="Classical, peaceful instrumental, or specific song preference"
                      value={formData.musicSelection}
                      onChange={(e) => setFormData({...formData, musicSelection: e.target.value})}
                      className="w-full bg-slate-900/60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 placeholder-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition"
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Context & Message */}
            <div className="bg-slate-800/40 p-8 rounded-lg border border-slate-700/50">
              <h2 className="text-2xl font-light text-slate-300 mb-6">Context & Personal Message</h2>

              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                    Personal Message (optional)
                  </label>
                  <textarea
                    placeholder="Words you'd like to include..."
                    value={formData.personalMessage}
                    onChange={(e) => setFormData({...formData, personalMessage: e.target.value})}
                    rows={5}
                    className="w-full bg-slate-900/60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 placeholder-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition resize-none font-light"
                  />
                </div>

                <div>
                  <label className="block text-sm font-light text-slate-400 mb-2 uppercase tracking-wide">
                    Context Notes (optional)
                  </label>
                  <textarea
                    placeholder="Timeline details, location names, or other context that helps organize the materials..."
                    value={formData.contextNotes}
                    onChange={(e) => setFormData({...formData, contextNotes: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-900/60 border border-slate-700/70 rounded px-4 py-3 text-slate-200 placeholder-slate-600 focus:border-slate-500 focus:ring-1 focus:ring-slate-500 transition resize-none font-light"
                  />
                </div>
              </div>
            </div>

            {/* Privacy Notice */}
            <div className="bg-slate-700/20 p-6 rounded-lg border border-slate-600/30">
              <div className="flex items-start space-x-3">
                <Lock className="w-5 h-5 text-slate-400 mt-0.5 flex-shrink-0" />
                <div>
                  <h3 className="text-slate-300 font-normal mb-1">Private Archive</h3>
                  <p className="text-sm text-slate-400 font-light leading-relaxed">
                    This assembly will remain completely private. Only you can access it. 
                    It will never be made public, shared, or used for any purpose beyond preservation.
                  </p>
                </div>
              </div>
            </div>

            {/* Submit */}
            <div className="text-center pt-4">
              <button
                onClick={assembleArchive}
                disabled={loading || !formData.assemblyTitle || !formData.personName || uploadedFiles.length === 0}
                className="bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed px-10 py-4 rounded font-light text-lg text-slate-200 transition"
              >
                {loading ? 'Assembling...' : 'Assemble Private Archive'}
              </button>
              {(!formData.personName || uploadedFiles.length === 0) && (
                <p className="text-slate-500 text-sm mt-3 font-light">
                  Please provide a name and upload at least one file
                </p>
              )}
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-6 py-16">
            <div className="animate-spin w-16 h-16 border-2 border-slate-600 border-t-slate-400 rounded-full mx-auto"></div>
            <h2 className="text-2xl font-light text-slate-300">Assembling Your Archive</h2>
            <p className="text-slate-500 font-light">Handling your materials with care...</p>
          </div>threshold' && (
          <div className="text-center space-y-8 py-20">
            <h2 className="text-3xl font-light text-slate-300">Your archive is ready.</h2>
            <p className="text-slate-400 font-light">This space is private and preserved.</p>
            <button
              onClick={() => setStep('complete')}
              className="bg-slate-700 hover:bg-slate-600 px-8 py-3 rounded font-light text-slate-200 transition mt-8"
            >
              Open Archive
            </button>
          </div>
        )}

        {step === '
        )}

        {step === 'complete' && (
          <div className="text-center space-y-6 py-16">
            <CheckCircle className="w-16 h-16 text-slate-400 mx-auto" />
            <h2 className="text-3xl font-light text-slate-300">Archive Assembled</h2>
            <p className="text-slate-400 font-light">Your private archive has been preserved</p>
            <div className="flex items-center justify-center gap-2 text-slate-500 text-sm mt-4">
              <Lock className="w-4 h-4" />
              <span>Stored securely · Private only</span>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
