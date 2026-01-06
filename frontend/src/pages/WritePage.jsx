import React, { useState, useEffect } from 'react';
import { Save, FileText, Zap, BookOpen, GraduationCap, Archive } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function WritePage() {
  const [sessionId, setSessionId] = useState(null);
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [contentType, setContentType] = useState('article');
  const [isSaving, setIsSaving] = useState(false);
  const [wordCount, setWordCount] = useState(0);
  const [lastSaved, setLastSaved] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Auto-save every 30 seconds
    const autoSaveInterval = setInterval(() => {
      if (content && sessionId) {
        saveContent(true);
      }
    }, 30000);

    return () => clearInterval(autoSaveInterval);
  }, [content, sessionId]);

  useEffect(() => {
    setWordCount(content.trim().split(/\s+/).filter(word => word.length > 0).length);
  }, [content]);

  const startSession = async () => {
    try {
      const response = await fetch('/write/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: null,
          title: title || 'Untitled',
          content_type: contentType,
          initial_content: content
        })
      });

      const result = await response.json();
      setSessionId(result.session_id);
    } catch (error) {
      console.error('Failed to start session:', error);
    }
  };

  const saveContent = async (autoSave = false) => {
    if (!sessionId) return;

    setIsSaving(true);
    try {
      const response = await fetch(`/write/save/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: content,
          auto_save: autoSave
        })
      });

      const result = await response.json();
      setLastSaved(new Date().toLocaleTimeString());
    } catch (error) {
      console.error('Failed to save:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const processContent = async () => {
    if (!sessionId) return;

    try {
      await fetch(`/write/process/${sessionId}`, {
        method: 'POST'
      });
      alert('Content processing started. Check back in a few moments for AI suggestions.');
    } catch (error) {
      console.error('Failed to process:', error);
    }
  };

  const contentTypes = [
    { value: 'article', label: 'Article', icon: FileText },
    { value: 'book', label: 'Book Chapter', icon: BookOpen },
    { value: 'course', label: 'Course Content', icon: GraduationCap },
    { value: 'notes', label: 'Personal Notes', icon: Archive }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-400 bg-clip-text text-transparent mb-4">
            GOAT Writer
          </h1>
          <p className="text-slate-300">
            Write, save, and transform your content with AI assistance
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-6 mb-6">
          {/* Session Setup */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 sticky top-6">
              <h3 className="text-lg font-semibold text-orange-400 mb-4">Session Setup</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">
                    Title
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Enter title..."
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Content Type
                  </label>
                  <div className="space-y-2">
                    {contentTypes.map((type) => {
                      const Icon = type.icon;
                      return (
                        <label key={type.value} className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="radio"
                            name="contentType"
                            value={type.value}
                            checked={contentType === type.value}
                            onChange={(e) => setContentType(e.target.value)}
                            className="text-orange-500 focus:ring-orange-500"
                          />
                          <Icon className="w-4 h-4 text-slate-400" />
                          <span className="text-sm text-slate-300">{type.label}</span>
                        </label>
                      );
                    })}
                  </div>
                </div>

                {!sessionId ? (
                  <button
                    onClick={startSession}
                    className="w-full bg-orange-500 hover:bg-orange-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors text-sm"
                  >
                    Start Writing Session
                  </button>
                ) : (
                  <div className="space-y-2">
                    <button
                      onClick={() => saveContent(false)}
                      disabled={isSaving}
                      className="w-full bg-green-500 hover:bg-green-600 disabled:bg-slate-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors text-sm flex items-center justify-center"
                    >
                      <Save className="w-4 h-4 mr-2" />
                      {isSaving ? 'Saving...' : 'Save Now'}
                    </button>

                    <button
                      onClick={processContent}
                      className="w-full bg-purple-500 hover:bg-purple-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors text-sm flex items-center justify-center"
                    >
                      <Zap className="w-4 h-4 mr-2" />
                      Process with AI
                    </button>
                  </div>
                )}
              </div>

              {sessionId && (
                <div className="mt-6 pt-4 border-t border-slate-600">
                  <div className="text-xs text-slate-400 space-y-1">
                    <div>Session ID: <span className="font-mono text-cyan-400">{sessionId.slice(0, 8)}...</span></div>
                    {lastSaved && <div>Last saved: {lastSaved}</div>}
                    <div>Words: {wordCount}</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Writing Area */}
          <div className="lg:col-span-3">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
              <div className="mb-4 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-orange-400">
                  {title || 'Untitled Document'}
                </h2>
                <div className="text-sm text-slate-400">
                  {wordCount} words
                </div>
              </div>

              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Start writing your content here... Your work is automatically saved to the vault."
                className="w-full h-96 px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
                style={{ minHeight: '400px' }}
              />

              {sessionId && (
                <div className="mt-6 pt-4 border-t border-slate-600">
                  <h3 className="text-lg font-semibold text-cyan-400 mb-4">Transform Your Content</h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    <button 
                      onClick={() => navigate('/book-builder')}
                      className="bg-blue-500 hover:bg-blue-600 px-4 py-3 rounded-lg text-white font-semibold transition-colors flex items-center justify-center"
                    >
                      <BookOpen className="w-5 h-5 mr-2" />
                      Create Book
                    </button>
                    <button 
                      onClick={() => navigate('/podcast-engine')}
                      className="bg-purple-500 hover:bg-purple-600 px-4 py-3 rounded-lg text-white font-semibold transition-colors flex items-center justify-center"
                    >
                      <GraduationCap className="w-5 h-5 mr-2" />
                      Masterclass
                    </button>
                    <button 
                      onClick={() => navigate('/vault')}
                      className="bg-green-500 hover:bg-green-600 px-4 py-3 rounded-lg text-white font-semibold transition-colors flex items-center justify-center"
                    >
                      <Archive className="w-5 h-5 mr-2" />
                      Legacy Archive
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tips */}
        <div className="bg-slate-800/30 backdrop-blur-sm rounded-xl p-6">
          <h3 className="text-lg font-semibold text-orange-400 mb-4">Writing Tips</h3>
          <div className="grid md:grid-cols-2 gap-6 text-sm text-slate-300">
            <div>
              <h4 className="font-semibold text-white mb-2">Auto-Save & Vault Storage</h4>
              <p>Your content is automatically saved every 30 seconds and stored securely in your personal vault with blockchain anchoring.</p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">AI Processing</h4>
              <p>Click "Process with AI" to get suggestions for structure, key points, and content improvements powered by GOAT's knowledge engine.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}