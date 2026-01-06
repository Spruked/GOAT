import React, { useState } from 'react';
import { UserPlus, Copy, Mail, Calendar, Clock } from 'lucide-react';

export default function GuestPage() {
  const [inviteForm, setInviteForm] = useState({
    host_name: '',
    guest_email: '',
    guest_name: '',
    session_title: '',
    description: '',
    scheduled_time: ''
  });
  const [inviteResult, setInviteResult] = useState(null);
  const [sessions, setSessions] = useState([]);

  const handleInputChange = (field, value) => {
    setInviteForm(prev => ({ ...prev, [field]: value }));
  };

  const createInvite = async () => {
    try {
      const response = await fetch('/guest/invite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inviteForm)
      });

      const result = await response.json();
      setInviteResult(result);

      // Refresh sessions list
      loadSessions();
    } catch (error) {
      console.error('Failed to create invite:', error);
      alert('Failed to create invite. Please try again.');
    }
  };

  const loadSessions = async () => {
    try {
      const response = await fetch('/guest/sessions');
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const copyInviteLink = () => {
    if (inviteResult?.invite_url) {
      navigator.clipboard.writeText(window.location.origin + inviteResult.invite_url);
      alert('Invite link copied to clipboard!');
    }
  };

  React.useEffect(() => {
    loadSessions();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
            Guest Interviews
          </h1>
          <p className="text-slate-300">
            Invite guests for collaborative recording sessions
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Create Invite Form */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
            <h2 className="text-xl font-semibold text-purple-400 mb-6 flex items-center">
              <UserPlus className="w-6 h-6 mr-2" />
              Create Guest Invite
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Your Name (Host)
                </label>
                <input
                  type="text"
                  value={inviteForm.host_name}
                  onChange={(e) => handleInputChange('host_name', e.target.value)}
                  placeholder="Enter your name"
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Guest Email (Optional)
                </label>
                <input
                  type="email"
                  value={inviteForm.guest_email}
                  onChange={(e) => handleInputChange('guest_email', e.target.value)}
                  placeholder="guest@example.com"
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Guest Name
                </label>
                <input
                  type="text"
                  value={inviteForm.guest_name}
                  onChange={(e) => handleInputChange('guest_name', e.target.value)}
                  placeholder="Enter guest name"
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Session Title
                </label>
                <input
                  type="text"
                  value={inviteForm.session_title}
                  onChange={(e) => handleInputChange('session_title', e.target.value)}
                  placeholder="Interview: AI in Education"
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Description
                </label>
                <textarea
                  value={inviteForm.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="Brief description of the interview topic..."
                  rows={3}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Scheduled Time (Optional)
                </label>
                <input
                  type="datetime-local"
                  value={inviteForm.scheduled_time}
                  onChange={(e) => handleInputChange('scheduled_time', e.target.value)}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <button
                onClick={createInvite}
                disabled={!inviteForm.host_name || !inviteForm.guest_name || !inviteForm.session_title}
                className="w-full bg-purple-500 hover:bg-purple-600 disabled:bg-slate-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg text-white font-semibold transition-colors"
              >
                Create Invite Link
              </button>
            </div>
          </div>

          {/* Invite Result & Sessions */}
          <div className="space-y-6">
            {inviteResult && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
                <h3 className="text-lg font-semibold text-green-400 mb-4 flex items-center">
                  <Mail className="w-5 h-5 mr-2" />
                  Invite Created Successfully
                </h3>

                <div className="space-y-3">
                  <div>
                    <span className="text-slate-400">Invite Link:</span>
                    <div className="flex items-center space-x-2 mt-1">
                      <code className="flex-1 bg-slate-700 px-3 py-2 rounded text-sm text-cyan-400 font-mono">
                        {window.location.origin}{inviteResult.invite_url}
                      </code>
                      <button
                        onClick={copyInviteLink}
                        className="p-2 bg-slate-600 hover:bg-slate-500 rounded transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div>
                    <span className="text-slate-400">Expires:</span>
                    <span className="ml-2 text-white">
                      {new Date(inviteResult.expires_at).toLocaleString()}
                    </span>
                  </div>

                  <div className="pt-2">
                    <p className="text-sm text-slate-300">
                      Share this link with your guest. They can join the interview session without creating an account.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Sessions List */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
              <h3 className="text-lg font-semibold text-cyan-400 mb-4">
                Recent Sessions
              </h3>

              {sessions.length === 0 ? (
                <p className="text-slate-400 text-center py-8">
                  No sessions yet. Create your first guest invite!
                </p>
              ) : (
                <div className="space-y-3">
                  {sessions.map((session, index) => (
                    <div key={index} className="bg-slate-700/50 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-white">{session.session_title}</h4>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          session.status === 'active' ? 'bg-green-500/20 text-green-400' :
                          session.status === 'completed' ? 'bg-blue-500/20 text-blue-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {session.status}
                        </span>
                      </div>
                      <div className="text-sm text-slate-400 space-y-1">
                        <div>Host: {session.host_name}</div>
                        <div>Created: {new Date(session.created_at).toLocaleString()}</div>
                        <div>Expires: {new Date(session.expires_at).toLocaleString()}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}