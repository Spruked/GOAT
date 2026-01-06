
import React, { useState, useEffect } from 'react';
import { HostBubble } from '../components/HostBubble';

export default function OnboardingPage() {
  const [user, setUser] = useState(null);
  const [onboardingComplete, setOnboardingComplete] = useState(false);
  const [onboardingData, setOnboardingData] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    setUser(userData);
  }, []);

  const handleOnboardingComplete = (data) => {
    setOnboardingData(data);
    setOnboardingComplete(true);
    localStorage.setItem('onboarding', JSON.stringify(data));

    // Redirect based on user type
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    window.location.href = userData.isAdmin ? '/dashboard' : '/products';
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (onboardingComplete) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
          <p className="text-green-600">Welcome to GOAT! Setting up your experience...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <img src="/Goatvault256.png" alt="GOAT" className="w-10 h-10 rounded-full mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Welcome to GOAT</h1>
                <p className="text-sm text-gray-600">Let's get you set up for success</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Your Personal GOAT Assistant
            </h2>
            <p className="text-lg text-gray-600">
              I'm here to help you get started. Let's have a quick conversation to understand your goals and set up your experience.
            </p>
          </div>

          {/* Host Bubble will handle the conversational onboarding */}
          <div className="flex justify-center">
            <div className="w-full max-w-2xl">
              <HostBubble
                user={{ ...user, id: user.email }} // Use email as ID for onboarding
                isVisible={true}
                onboardingMode={true}
                onOnboardingComplete={handleOnboardingComplete}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
  