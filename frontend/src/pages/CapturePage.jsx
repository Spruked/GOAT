import React, { useState, useEffect } from 'react';
import { Mic, Square, Play, Pause, BookOpen, GraduationCap, Archive } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function CapturePage() {
  const [isRecording, setIsRecording] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [duration, setDuration] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [title, setTitle] = useState('');
  const [participants, setParticipants] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    let interval;
    if (isRecording) {
      interval = setInterval(() => {
        setDuration(d => d + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const startRecording = async () => {
    try {
      const response = await fetch('/capture/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: null,
          title: title || 'Untitled Recording',
          participants: participants
        })
      });

      const data = await response.json();
      setSessionId(data.session_id);
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = async () => {
    if (!sessionId) return;

    try {
      const response = await fetch(`/capture/stop/${sessionId}`, {
        method: 'POST'
      });

      const data = await response.json();
      setIsRecording(false);
      setTranscript('Processing transcript...');

      // Poll for transcript
      pollTranscript(data.session_id);
    } catch (error) {
      console.error('Failed to stop recording:', error);
    }
  };

  const pollTranscript = async (sid) => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`/capture/status/${sid}`);
        const data = await response.json();

        if (data.transcript_length > 0) {
          setTranscript(`Transcript: ${data.transcript_length} words processed`);
        }

        if (data.status === 'completed') {
          // Load full transcript
          setTranscript('Transcript completed and saved to vault');
        } else {
          setTimeout(checkStatus, 2000);
        }
      } catch (error) {
        console.error('Failed to check status:', error);
      }
    };

    checkStatus();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
            GOAT Capture Studio
          </h1>
          <p className="text-slate-300">
            Record your knowledge, stories, and expertise
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 mb-6">
          <div className="mb-6">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Session Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter session title..."
              className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              disabled={isRecording}
            />
          </div>

          <div className="text-center mb-8">
            <div className="text-6xl font-mono text-cyan-400 mb-4">
              {formatDuration(duration)}
            </div>

            <div className="flex justify-center space-x-4">
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 px-8 py-4 rounded-full text-white font-semibold transition-colors"
                >
                  <Mic className="w-6 h-6" />
                  <span>Start Recording</span>
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="flex items-center space-x-2 bg-gray-500 hover:bg-gray-600 px-8 py-4 rounded-full text-white font-semibold transition-colors"
                >
                  <Square className="w-6 h-6" />
                  <span>Stop Recording</span>
                </button>
              )}
            </div>
          </div>

          {isRecording && (
            <div className="text-center mb-6">
              <div className="inline-flex items-center space-x-2 bg-red-500/20 border border-red-500/50 rounded-lg px-4 py-2">
                <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                <span className="text-red-400 font-medium">Recording Live</span>
              </div>
            </div>
          )}

          {transcript && (
            <div className="bg-slate-700/50 rounded-lg p-4 mt-6">
              <h3 className="text-lg font-semibold text-cyan-400 mb-2">Recording Complete!</h3>
              <p className="text-slate-300 mb-4">Your content has been processed and is ready for transformation.</p>
              
              <div className="flex flex-wrap gap-3">
                <button 
                  onClick={() => navigate('/book-builder')}
                  className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                >
                  <BookOpen className="w-4 h-4 mr-2" />
                  Create Book
                </button>
                <button 
                  onClick={() => navigate('/podcast-engine')}
                  className="bg-purple-500 hover:bg-purple-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                >
                  <GraduationCap className="w-4 h-4 mr-2" />
                  Masterclass
                </button>
                <button 
                  onClick={() => navigate('/vault')}
                  className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                >
                  <Archive className="w-4 h-4 mr-2" />
                  View in Vault
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
            <h3 className="text-xl font-semibold text-cyan-400 mb-4">Recording Tips</h3>
            <ul className="space-y-2 text-slate-300">
              <li>• Speak clearly and at a normal pace</li>
              <li>• Use a good microphone for best results</li>
              <li>• Take breaks if needed - recording saves automatically</li>
              <li>• Your content is processed by AI for summaries and chapters</li>
            </ul>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
            <h3 className="text-xl font-semibold text-purple-400 mb-4">What Happens Next</h3>
            <ul className="space-y-2 text-slate-300">
              <li>• Auto-transcription and summarization</li>
              <li>• Chapter detection and timestamps</li>
              <li>• Vault storage with blockchain anchoring</li>
              <li>• Ready for book, podcast, or video content creation</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}