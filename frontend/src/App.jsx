import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import OrbOnly from './OrbOnly';
import ProductsPage from './pages/ProductsPage';
import LoginPage from './pages/LoginPage';
import OnboardingPage from './pages/OnboardingPage';
import PodcastEnginePage from './pages/PodcastEnginePage';
import MenuPage from './pages/MenuPage';
import StartPage from './pages/StartPage';
import StartActionsPage from './pages/StartActionsPage';
import TermsPage from './pages/TermsPage';
import PrivacyPage from './pages/PrivacyPage';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }}
    >
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/podcast" element={<PodcastEnginePage />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/start" element={<StartPage />} />
        <Route path="/actions" element={<StartActionsPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/orb-only" element={<OrbOnly />} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
