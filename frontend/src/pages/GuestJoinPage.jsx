import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { User, Play, Mic, MicOff } from 'lucide-react';

export default function GuestJoinPage() {
  const { invite_token } = useParams();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [joined, setJoined] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    loadSession();
  }, [invite_token]);

  const loadSession = async () => {
    try {
      const response = await fetch(`/guest/join/${invite_token}`);
      if (!response.ok) {
        throw new Error('Invalid or expired invite');
      }
      const data = await response.json();
      setSession(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const joinSession = async () => {
    try {
      const response = await fetch(`/guest/join/${invite_token}/start`, {
        method: 'POST'
      });
      const data = await response.json();
      setJoined(true);
      setIsRecording(true);
    } catch (err) {
      setError('Failed to join session');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-xl">Loading session...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <User className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold mb-4">Session Not Available</h1>
          <p className="text-slate-400 mb-6">{error}</p>
          <p className="text-sm text-slate-500">
            Please contact the host for a new invite link.
          </p>
        </div>
      </div>
    );
  }

  if (!joined) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="max-w-2xl mx-auto px-4 py-16">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
              <User className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
              Join Interview Session
            </h1>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-white mb-2">{session.session_title}</h2>
                <p className="text-slate-400">Hosted by {session.host_name}</p>
              </div>

              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-400">Status:</span>
                  <span className="ml-2 text-green-400 font-medium capitalize">{session.status}</span>
                </div>
                <div>
                  <span className="text-slate-400">Created:</span>
                  <span className="ml-2 text-white">
                    {new Date(session.created_at).toLocaleString()}
                  </span>
                </div>
                <div className="md:col-span-2">
                  <span className="text-slate-400">Expires:</span>
                  <span className="ml-2 text-white">
                    {new Date(session.expires_at).toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="bg-slate-700/50 rounded-lg p-4">
                <h3 className="font-semibold text-cyan-400 mb-2">What happens next?</h3>
                <ul className="text-sm text-slate-300 space-y-1">
                  <li>• You'll join a live recording session with the host</li>
                  <li>• Your audio will be recorded and transcribed automatically</li>
                  <li>• The content will be processed and saved to the host's vault</li>
                  <li>• No account required - just click join and start talking</li>
                </ul>
              </div>

              <button
                onClick={joinSession}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
              >
                <Play className="w-6 h-6" />
                <span>Join Session</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Recording interface
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white mb-2">{session.session_title}</h1>
          <p className="text-slate-400">Interview with {session.host_name}</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8">
          <div className="text-center mb-8">
            <div className="w-24 h-24 mx-auto mb-4 bg-red-500 rounded-full flex items-center justify-center">
              {isRecording ? (
                <Mic className="w-12 h-12 text-white animate-pulse" />
              ) : (
                <MicOff className="w-12 h-12 text-white" />
              )}
            </div>
            <div className="text-2xl font-mono text-cyan-400 mb-2">00:00:00</div>
            <div className="text-lg text-green-400 font-medium">
              {isRecording ? 'Recording Live' : 'Session Paused'}
            </div>
          </div>

          <div className="bg-slate-700/50 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-cyan-400 mb-4">Live Transcript</h3>
            <div className="h-32 bg-slate-800/50 rounded p-4 text-slate-300 text-sm">
              Transcript will appear here in real-time...
            </div>
          </div>

          <div className="text-center">
            <p className="text-slate-400 text-sm mb-4">
              Your interview is being recorded and will be automatically processed into content.
              The host will receive the final transcript and can create books, courses, or archives from this session.
            </p>
            <div className="text-xs text-slate-500">
              Session ID: {invite_token}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}