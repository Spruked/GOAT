import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, Upload, UserPlus, PenTool } from 'lucide-react';

export default function StartActionsPage() {
  const navigate = useNavigate();

  const actions = [
    {
      id: 'record',
      title: 'Record',
      description: 'Start recording your session',
      icon: Mic,
      route: '/capture',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'upload',
      title: 'Upload',
      description: 'Upload existing audio/video files',
      icon: Upload,
      route: '/upload',
      color: 'from-green-500 to-emerald-500'
    },
    {
      id: 'invite',
      title: 'Invite',
      description: 'Invite guests for interviews',
      icon: UserPlus,
      route: '/guest',
      color: 'from-purple-500 to-pink-500'
    },
    {
      id: 'write',
      title: 'Write',
      description: 'Start writing your content',
      icon: PenTool,
      route: '/write',
      color: 'from-orange-500 to-red-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
            Start Your Legacy
          </h1>
          <p className="text-xl text-slate-300">
            Choose how you want to begin creating your masterpiece
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {actions.map((action) => {
            const Icon = action.icon;
            return (
              <button
                key={action.id}
                onClick={() => navigate(action.route)}
                className="group relative overflow-hidden bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:bg-slate-800/80 transition-all duration-300 hover:scale-105 hover:shadow-2xl"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${action.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />
                <div className="relative z-10">
                  <div className={`w-16 h-16 mx-auto mb-4 bg-gradient-to-br ${action.color} rounded-full flex items-center justify-center shadow-lg`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{action.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{action.description}</p>
                </div>
              </button>
            );
          })}
        </div>

        <div className="text-center mt-12">
          <p className="text-slate-500">
            Each path leads to professional-quality content creation powered by GOAT's AI
          </p>
        </div>
      </div>
    </div>
  );
}