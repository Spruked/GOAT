import React, { useState, useEffect } from 'react';
import { Mic, BookOpen, GraduationCap, FileText, Upload, Play, CheckCircle, ExternalLink, Download } from 'lucide-react';
import axios from 'axios';

export default function PodcastEnginePage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    topic: '',
    notes: '',
    outputType: 'podcast',
    outputFormat: '',
    audience: '',
    tone: '',
    lengthEstimate: 'medium',
    createAudiobook: false,
    voice: ''
  });
  const [files, setFiles] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [legacy, setLegacy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [caleonMessage, setCaleonMessage] = useState('');
  const [voices, setVoices] = useState([]);

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

  const outputTypes = [
    { 
      value: 'podcast', 
      label: 'Podcast', 
      icon: Mic,
      formats: ['Single Episode', 'Mini-Series (3-5 episodes)', 'Full Season (10+ episodes)'],
      tones: ['Conversational', 'Professional', 'Documentary Style', 'Interview Format']
    },
    { 
      value: 'book', 
      label: 'Book', 
      icon: BookOpen,
      formats: ['Short Book (10-20k words)', 'Standard Book (40-60k words)', 'Epic Book (80k+ words)', 'Novella'],
      tones: ['Narrative', 'Academic', 'How-To Guide', 'Memoir Style']
    },
    { 
      value: 'audiobook', 
      label: 'Audiobook', 
      icon: Play,
      formats: ['Short Form (1-3 hours)', 'Medium (4-6 hours)', 'Long Form (8+ hours)'],
      tones: ['Narrative', 'Conversational', 'Dramatic', 'Educational']
    },
    { 
      value: 'course', 
      label: 'Digital Course', 
      icon: GraduationCap,
      formats: ['Mini Course (3-5 modules)', 'Standard Course (8-12 modules)', 'Masterclass (15+ modules)'],
      tones: ['Beginner Friendly', 'Advanced Technical', 'Workshop Style', 'Certification Track']
    },
    { 
      value: 'content-series', 
      label: 'Content Series', 
      icon: FileText,
      formats: ['Blog Series', 'Email Newsletter Course', 'Social Media Series', 'Video Script Series'],
      tones: ['Engaging', 'Professional', 'Casual', 'Authoritative']
    }
  ];

  const handleFileUpload = async (e) => {
    const uploadedFiles = Array.from(e.target.files);
    setFiles(uploadedFiles);

    // Analyze files with VisiData
    if (uploadedFiles.length > 0) {
      setLoading(true);
      try {
        const analyses = [];
        for (const file of uploadedFiles) {
          const formData = new FormData();
          formData.append('file', file);

          const response = await axios.post('/podcast/analyze-data', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          analyses.push({ file: file.name, ...response.data });
        }
        setAnalysis(analyses);
        setCaleonMessage("I've analyzed your data files. I can see some interesting patterns that would work well for your " + formData.outputType + ". Ready to structure this?");
      } catch (error) {
        console.error('Analysis failed:', error);
        setCaleonMessage("I had trouble analyzing those files, but we can still create something amazing with your notes.");
      }
      setLoading(false);
    }
  };

  const createLegacy = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        window.location.href = '/login';
        return;
      }

      const submitData = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        submitData.append(key, value);
      });

      files.forEach(file => {
        submitData.append('source_files', file);
      });

      const response = await axios.post('/podcast/create-legacy', submitData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });

      setLegacy(response.data);
      setStep('complete');
      setCaleonMessage("Your legacy is complete! This represents your greatest work, structured and ready to share with the world.");

    } catch (error) {
      console.error('Legacy creation failed:', error);
      setCaleonMessage("I encountered an issue creating your legacy. Let's try again with some adjustments.");
      setStep('input');
    }
    setLoading(false);
  };

  const getMintingSuggestions = async () => {
    if (!legacy) return;

    try {
      const response = await axios.get(`/podcast/minting-suggestions/${legacy.artifact.content_type}`);
      // Show minting suggestions
      setCaleonMessage(`If you'd like to preserve this ${legacy.artifact.content_type} permanently, I can connect you with our minting partners.`);
    } catch (error) {
      console.error('Failed to get minting suggestions:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-16">

        {/* Header */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full flex items-center justify-center shadow-2xl mb-6">
            <Mic className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
            Podcast Engine
          </h1>
          <p className="text-xl text-slate-300">
            Transform your knowledge into legacies that outlive you
          </p>
          <p className="text-slate-400 mt-2">
            COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE
          </p>
        </div>

        {/* Host Guidance */}
        {caleonMessage && (
          <div className="bg-gradient-to-r from-purple-900/20 to-cyan-900/20 p-6 rounded-lg border border-purple-600/30 mb-8">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-sm">H</span>
              </div>
              <div>
                <p className="text-slate-300 italic">"{caleonMessage}"</p>
                <p className="text-slate-400 text-sm mt-2">— HOST</p>
              </div>
            </div>
          </div>
        )}

        {/* Input Step */}
        {step === 'input' && (
          <div className="space-y-8">

            {/* Topic & Intent */}
            <div className="space-y-8">
              
              {/* Topic Input */}
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-cyan-300">What is your topic?</h2>
                <input
                  type="text"
                  placeholder="Your greatest work topic..."
                  value={formData.topic}
                  onChange={(e) => setFormData({...formData, topic: e.target.value})}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400"
                />
              </div>

              {/* Output Type Selection */}
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-purple-300">What would you like to create?</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {outputTypes.map((type) => (
                    <button
                      key={type.value}
                      onClick={() => setFormData({...formData, outputType: type.value, outputFormat: '', tone: ''})}
                      className={`p-6 rounded-lg border-2 transition text-left ${
                        formData.outputType === type.value
                          ? 'border-purple-500 bg-purple-500/20 shadow-lg shadow-purple-500/20'
                          : 'border-slate-600 hover:border-slate-500 bg-slate-800/50'
                      }`}
                    >
                      <type.icon className={`w-10 h-10 mb-3 ${formData.outputType === type.value ? 'text-purple-400' : 'text-slate-400'}`} />
                      <h3 className="font-semibold text-lg mb-1">{type.label}</h3>
                    </button>
                  ))}
                </div>
              </div>

              {/* Format & Tone Dropdowns - Only show when output type selected */}
              {formData.outputType && (
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <label className="block text-lg font-semibold text-cyan-300">
                      Choose Format
                    </label>
                    <select
                      value={formData.outputFormat}
                      onChange={(e) => setFormData({...formData, outputFormat: e.target.value})}
                      className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white"
                    >
                      <option value="">Select a format...</option>
                      {outputTypes.find(t => t.value === formData.outputType)?.formats.map((format) => (
                        <option key={format} value={format}>{format}</option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-3">
                    <label className="block text-lg font-semibold text-cyan-300">
                      Choose Tone/Style
                    </label>
                    <select
                      value={formData.tone}
                      onChange={(e) => setFormData({...formData, tone: e.target.value})}
                      className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white"
                    >
                      <option value="">Select a tone...</option>
                      {outputTypes.find(t => t.value === formData.outputType)?.tones.map((tone) => (
                        <option key={tone} value={tone}>{tone}</option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              {/* Audience Input */}
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-cyan-300">Who is your audience?</h2>
                <input
                  type="text"
                  placeholder="Beginners, experts, professionals..."
                  value={formData.audience}
                  onChange={(e) => setFormData({...formData, audience: e.target.value})}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400"
                />
              </div>
            </div>

            {/* Notes */}
            <div>
              <h2 className="text-2xl font-bold text-cyan-300 mb-4">Share your notes and ideas</h2>
              <textarea
                placeholder="Pour out your knowledge, experiences, and insights..."
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows={8}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400"
              />
            </div>

            {/* File Upload */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h2 className="text-2xl font-bold text-cyan-300 mb-4">Upload source materials (optional)</h2>
              <p className="text-slate-400 mb-4">
                CSV, Excel, JSON files with data that can enhance your legacy
              </p>
              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg cursor-pointer transition">
                  <Upload className="w-5 h-5" />
                  <span>Choose Files</span>
                  <input
                    type="file"
                    multiple
                    accept=".csv,.xlsx,.xls,.json"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
                {files.length > 0 && (
                  <span className="text-slate-300">{files.length} file(s) selected</span>
                )}
              </div>
            </div>

            {/* Data Analysis Results */}
            {analysis && (
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-bold text-purple-300 mb-4">Data Analysis Results</h3>
                {analysis.map((result, index) => (
                  <div key={index} className="mb-4 p-4 bg-slate-700/50 rounded">
                    <h4 className="font-semibold text-cyan-300">{result.file}</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2 text-sm">
                      <div>
                        <span className="text-slate-400">Rows:</span> {result.analysis.shape?.[0] || 'N/A'}
                      </div>
                      <div>
                        <span className="text-slate-400">Columns:</span> {result.analysis.columns?.length || 0}
                      </div>
                      <div>
                        <span className="text-slate-400">Themes:</span> {result.analysis.extracted_themes?.length || 0}
                      </div>
                      <div>
                        <span className="text-slate-400">Data Types:</span> {Object.keys(result.analysis.dtypes || {}).length}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Audiobook/Voice Options - Only for certain types */}
            {['podcast', 'audiobook', 'course'].includes(formData.outputType) && (
              <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
                <h2 className="text-2xl font-bold text-purple-300 mb-4">
                  {formData.outputType === 'audiobook' ? 'Voice Narration' : 'Add Voice Narration (Optional)'}
                </h2>
                <p className="text-slate-400 mb-4">
                  {formData.outputType === 'audiobook' 
                    ? 'Choose a voice for your audiobook narration' 
                    : 'Generate audio narration alongside your content'}
                </p>
                
                <div className="flex items-center space-x-4 mb-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={formData.outputType === 'audiobook' ? true : formData.createAudiobook}
                      onChange={(e) => setFormData({...formData, createAudiobook: e.target.checked})}
                      disabled={formData.outputType === 'audiobook'}
                      className="rounded border-slate-600"
                    />
                    <span>{formData.outputType === 'audiobook' ? 'Voice narration included' : 'Add voice narration'}</span>
                  </label>
                </div>

                {(formData.createAudiobook || formData.outputType === 'audiobook') && voices.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Choose Voice ({voices.slice(0, 3).length} available):
                    </label>
                    <select
                      value={formData.voice}
                      onChange={(e) => setFormData({...formData, voice: e.target.value})}
                      className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white"
                    >
                      <option value="">Default voice</option>
                      {voices.slice(0, 3).map((voice, index) => (
                        <option key={voice.id} value={voice.id}>
                          {voice.name} ({voice.gender})
                        </option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
            )}

            <div className="text-center">
              <button
                onClick={createLegacy}
                disabled={loading || !formData.topic || !formData.notes || !formData.outputFormat || !formData.tone}
                className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed px-8 py-4 rounded-lg font-bold text-lg transition"
              >
                {loading ? 'Creating Your Legacy...' : `Create My ${outputTypes.find(t => t.value === formData.outputType)?.label || 'Legacy'}`}
              </button>
              {(!formData.outputFormat || !formData.tone) && (
                <p className="text-yellow-400 text-sm mt-2">Please select format and tone to continue</p>
              )}
            </div>
          </div>
        )}

        {/* Processing Step */}
        {step === 'processing' && (
          <div className="text-center space-y-8">
            <div className="animate-spin w-16 h-16 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto"></div>
            <h2 className="text-2xl font-bold text-cyan-300">Crafting Your Legacy</h2>
            <p className="text-slate-400">COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE</p>
            <div className="space-y-4 text-left max-w-2xl mx-auto">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-400" />
                <span>Analyzing your input and source materials</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                <span>Structuring content with AI guidance</span>
              </div>
              <div className="flex items-center space-x-3 opacity-50">
                <div className="w-6 h-6 border-2 border-slate-600 rounded-full"></div>
                <span>Expanding into full masterpiece</span>
              </div>
              <div className="flex items-center space-x-3 opacity-50">
                <div className="w-6 h-6 border-2 border-slate-600 rounded-full"></div>
                <span>Archiving to your vault</span>
              </div>
            </div>
          </div>
        )}

        {/* Complete Step */}
        {step === 'complete' && legacy && (
          <div className="space-y-8">

            {/* Success Message */}
            <div className="text-center">
              <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-green-300 mb-2">Your Legacy is Complete!</h2>
              <p className="text-slate-400">A {legacy.artifact.content_type} with {legacy.artifact.word_count} words</p>
            </div>

            {/* Legacy Preview */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h3 className="text-xl font-bold text-cyan-300 mb-4">{legacy.artifact.title}</h3>

              <div className="grid md:grid-cols-3 gap-6 mb-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-300">{legacy.artifact.sections.length}</div>
                  <div className="text-slate-400">Sections</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-300">{legacy.artifact.word_count}</div>
                  <div className="text-slate-400">Words</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-300">{legacy.artifact.estimated_time}</div>
                  <div className="text-slate-400">Read Time</div>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="font-semibold text-slate-300">Sections:</h4>
                {legacy.artifact.sections.slice(0, 5).map((section, index) => (
                  <div key={index} className="text-slate-400 text-sm">
                    {section.number}. {section.title}
                  </div>
                ))}
                {legacy.artifact.sections.length > 5 && (
                  <div className="text-slate-400 text-sm">... and {legacy.artifact.sections.length - 5} more</div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="grid md:grid-cols-3 gap-6">

              <button className="bg-slate-700 hover:bg-slate-600 p-6 rounded-lg border border-slate-600 transition">
                <Download className="w-8 h-8 mx-auto mb-2" />
                <h3 className="font-semibold">Download</h3>
                <p className="text-sm text-slate-400">Export your legacy</p>
              </button>

              <button className="bg-slate-700 hover:bg-slate-600 p-6 rounded-lg border border-slate-600 transition">
                <BookOpen className="w-8 h-8 mx-auto mb-2" />
                <h3 className="font-semibold">Edit</h3>
                <p className="text-sm text-slate-400">Refine your work</p>
              </button>

              <button
                onClick={getMintingSuggestions}
                className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 p-6 rounded-lg transition"
              >
                <ExternalLink className="w-8 h-8 mx-auto mb-2" />
                <h3 className="font-semibold">Preserve Forever</h3>
                <p className="text-sm text-slate-400">Mint with partners</p>
              </button>

            </div>

            {/* Minting Suggestions */}
            {legacy.minting_suggestions && (
              <div className="bg-gradient-to-r from-purple-900/20 to-cyan-900/20 p-6 rounded-lg border border-purple-600/30">
                <h3 className="text-xl font-bold text-purple-300 mb-4">Preserve Your Legacy</h3>
                <p className="text-slate-400 mb-4">
                  Make this version permanent and unchangeable with our minting partners:
                </p>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-slate-700/50 p-4 rounded-lg">
                    <h4 className="font-semibold text-cyan-300 mb-2">CertSig</h4>
                    <p className="text-sm text-slate-400 mb-3">{legacy.minting_suggestions.certsig}</p>
                    <button className="w-full bg-cyan-600 hover:bg-cyan-700 px-4 py-2 rounded text-sm transition">
                      Mint with CertSig
                    </button>
                  </div>

                  <div className="bg-slate-700/50 p-4 rounded-lg">
                    <h4 className="font-semibold text-purple-300 mb-2">TrueMark</h4>
                    <p className="text-sm text-slate-400 mb-3">{legacy.minting_suggestions.truemark}</p>
                    <button className="w-full bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-sm transition">
                      Mint with TrueMark
                    </button>
                  </div>
                </div>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}