import React, { useState } from 'react';
import { GraduationCap, BookOpen, Video, FileText, CheckCircle, Layout } from 'lucide-react';
import axios from 'axios';

export default function CoursePage() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    courseTitle: '',
    courseDescription: '',
    instructor: '',
    courseLevel: '',
    courseDuration: '',
    numberOfModules: '',
    deliveryFormat: '',
    includeQuizzes: false,
    includeAssignments: false,
    includeCertificate: false,
    learningObjectives: '',
    moduleBreakdown: '',
    targetAudience: '',
    prerequisites: '',
    courseOutline: '',
    supplementalMaterials: ''
  });
  const [loading, setLoading] = useState(false);

  const levels = ['Beginner', 'Intermediate', 'Advanced', 'All Levels'];
  const durations = ['1-2 weeks', '3-4 weeks', '1-2 months', '3+ months', 'Self-paced'];
  const formats = ['Video Lectures', 'Text-based Modules', 'Mixed Media', 'Interactive Lessons'];

  const createCourse = async () => {
    setLoading(true);
    setStep('processing');

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/course/create', formData, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setStep('complete');
    } catch (error) {
      console.error('Course creation failed:', error);
      setStep('input');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-slate-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-16">
        
        <div className="text-center mb-16">
          <div className="w-24 h-24 mx-auto bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center shadow-2xl mb-6">
            <GraduationCap className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-4">
            Digital Course Creation
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Build comprehensive online courses with structured modules, assessments, and professional course materials
          </p>
        </div>

        {step === 'input' && (
          <div className="space-y-12">
            
            <div className="bg-gradient-to-r from-green-900/30 to-emerald-900/30 p-8 rounded-2xl border border-green-500/30">
              <div className="flex items-center mb-6">
                <BookOpen className="w-6 h-6 mr-3 text-green-400" />
                <h2 className="text-3xl font-bold text-green-300">Course Identity</h2>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Course Title</label>
                  <input
                    type="text"
                    placeholder="Complete Digital Marketing Mastery"
                    value={formData.courseTitle}
                    onChange={(e) => setFormData({...formData, courseTitle: e.target.value})}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Course Description</label>
                  <textarea
                    placeholder="What will students learn and achieve from this course?"
                    value={formData.courseDescription}
                    onChange={(e) => setFormData({...formData, courseDescription: e.target.value})}
                    rows={4}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Instructor Name</label>
                  <input
                    type="text"
                    placeholder="Your name or brand"
                    value={formData.instructor}
                    onChange={(e) => setFormData({...formData, instructor: e.target.value})}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-slate-900/50 to-green-900/30 p-8 rounded-2xl border border-slate-700">
              <div className="flex items-center mb-6">
                <Layout className="w-6 h-6 mr-3 text-emerald-400" />
                <h2 className="text-3xl font-bold text-emerald-300">Course Structure</h2>
              </div>

              <div className="space-y-6">
                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Course Level</label>
                    <select
                      value={formData.courseLevel}
                      onChange={(e) => setFormData({...formData, courseLevel: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select level...</option>
                      {levels.map(l => <option key={l} value={l}>{l}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Course Duration</label>
                    <select
                      value={formData.courseDuration}
                      onChange={(e) => setFormData({...formData, courseDuration: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    >
                      <option value="">Select duration...</option>
                      {durations.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-semibold text-slate-200 mb-3">Number of Modules</label>
                    <input
                      type="number"
                      placeholder="8"
                      value={formData.numberOfModules}
                      onChange={(e) => setFormData({...formData, numberOfModules: e.target.value})}
                      className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-slate-200 mb-3">Delivery Format</label>
                  <select
                    value={formData.deliveryFormat}
                    onChange={(e) => setFormData({...formData, deliveryFormat: e.target.value})}
                    className="w-full bg-slate-800/70 border border-slate-600 rounded-lg px-6 py-4 text-white text-lg"
                  >
                    <option value="">Select format...</option>
                    {formats.map(f => <option key={f} value={f}>{f}</option>)}
                  </select>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-green-900/30 to-slate-900/50 p-8 rounded-2xl border border-green-500/30">
              <div className="flex items-center mb-6">
                <FileText className="w-6 h-6 mr-3 text-green-400" />
                <h2 className="text-3xl font-bold text-green-300">Course Content</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Learning Objectives (one per line)</label>
                  <textarea
                    placeholder="Master social media advertising&#10;Understand SEO fundamentals&#10;Create effective email campaigns"
                    value={formData.learningObjectives}
                    onChange={(e) => setFormData({...formData, learningObjectives: e.target.value})}
                    rows={6}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Complete Course Outline</label>
                  <textarea
                    placeholder="Module 1: Introduction&#10;  - Lesson 1.1: Overview&#10;  - Lesson 1.2: Getting Started&#10;Module 2: Core Concepts..."
                    value={formData.courseOutline}
                    onChange={(e) => setFormData({...formData, courseOutline: e.target.value})}
                    rows={12}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg font-mono"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Target Audience</label>
                  <input
                    type="text"
                    placeholder="Aspiring marketers, small business owners, career switchers..."
                    value={formData.targetAudience}
                    onChange={(e) => setFormData({...formData, targetAudience: e.target.value})}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>

                <div>
                  <label className="block text-lg font-semibold text-green-200 mb-3">Prerequisites (if any)</label>
                  <textarea
                    placeholder="Basic computer skills, No prior experience needed..."
                    value={formData.prerequisites}
                    onChange={(e) => setFormData({...formData, prerequisites: e.target.value})}
                    rows={3}
                    className="w-full bg-slate-800/70 border border-green-500/30 rounded-lg px-6 py-4 text-white placeholder-slate-400 text-lg"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-slate-900/50 to-green-900/30 p-8 rounded-2xl border border-slate-700">
              <h2 className="text-3xl font-bold text-emerald-300 mb-6">Assessment & Certification</h2>

              <div className="space-y-4">
                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeQuizzes}
                    onChange={(e) => setFormData({...formData, includeQuizzes: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include module quizzes</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeAssignments}
                    onChange={(e) => setFormData({...formData, includeAssignments: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Include practical assignments</span>
                </label>

                <label className="flex items-center space-x-3 p-4 bg-slate-800/50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.includeCertificate}
                    onChange={(e) => setFormData({...formData, includeCertificate: e.target.checked})}
                    className="w-5 h-5 rounded border-slate-600"
                  />
                  <span className="text-lg">Provide completion certificate</span>
                </label>
              </div>
            </div>

            <div className="text-center pt-8">
              <button
                onClick={createCourse}
                disabled={loading || !formData.courseTitle || !formData.courseOutline}
                className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed px-12 py-5 rounded-xl font-bold text-xl shadow-2xl transition transform hover:scale-105"
              >
                {loading ? 'Building Your Course...' : 'Create Digital Course'}
              </button>
              {!formData.courseOutline && (
                <p className="text-yellow-400 text-sm mt-3">Please provide course outline</p>
              )}
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="text-center space-y-8">
            <div className="animate-spin w-20 h-20 border-4 border-green-500 border-t-transparent rounded-full mx-auto"></div>
            <h2 className="text-3xl font-bold text-green-300">Building Your Course</h2>
            <p className="text-slate-400">Structuring modules and lessons...</p>
          </div>
        )}

        {step === 'complete' && (
          <div className="text-center space-y-8">
            <CheckCircle className="w-20 h-20 text-green-400 mx-auto" />
            <h2 className="text-4xl font-bold text-green-300">Course Complete!</h2>
            <p className="text-slate-400">Your digital course is ready to publish</p>
          </div>
        )}

      </div>
    </div>
  );
}
