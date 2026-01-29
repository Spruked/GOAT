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
import BookBuilderPage from './pages/BookBuilderPage';
import OrganizerPage from './pages/OrganizerPage';
import { ProfilePage } from './pages/ProfilePage';
import { VaultForgePage } from './pages/VaultForgePage';
import AudiobookPage from './pages/AudiobookPage';
import CoursePage from './pages/CoursePage';
import MasterclassPage from './pages/MasterclassPage';
import MintingPage from './pages/MintingPage';
import CustomerRightsPage from './pages/CustomerRightsPage';
import ContentOwnershipPage from './pages/ContentOwnershipPage';
import RefundPolicyPage from './pages/RefundPolicyPage';
import DataProcessingPage from './pages/DataProcessingPage';
import CookiePolicyPage from './pages/CookiePolicyPage';
import DMCAPage from './pages/DMCAPage';
import PricingPage from './pages/PricingPage';
import { PackagesPage } from './pages/PackagesPage';
import { UserProfile } from './pages/Dashboard/UserProfile';
import { CaleonProvider, CaleonOverlay } from './components/CaleonOverlay';
import './App.css';

function App() {
  return (
    <CaleonProvider>
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
            <Route path="/dashboard/users/:userId" element={<UserProfile />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/podcast" element={<PodcastEnginePage />} />
            <Route path="/menu" element={<MenuPage />} />
            <Route path="/start" element={<StartPage />} />
            <Route path="/actions" element={<StartActionsPage />} />
            <Route path="/terms" element={<TermsPage />} />
            <Route path="/privacy" element={<PrivacyPage />} />
            <Route path="/orb-only" element={<OrbOnly />} />
            <Route path="/book-builder" element={<BookBuilderPage />} />
            <Route path="/organizer" element={<OrganizerPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/vault-forge" element={<VaultForgePage />} />
            <Route path="/audiobook" element={<AudiobookPage />} />
            <Route path="/course" element={<CoursePage />} />
            <Route path="/masterclass" element={<MasterclassPage />} />
            <Route path="/minting" element={<MintingPage />} />
            <Route path="/customer-rights" element={<CustomerRightsPage />} />
            <Route path="/content-ownership" element={<ContentOwnershipPage />} />
            <Route path="/refund-policy" element={<RefundPolicyPage />} />
            <Route path="/data-processing" element={<DataProcessingPage />} />
            <Route path="/cookie-policy" element={<CookiePolicyPage />} />
            <Route path="/dmca" element={<DMCAPage />} />
            <Route path="/pricing" element={<PricingPage />} />
            <Route path="/packages" element={<PackagesPage />} />
          </Routes>
        </BrowserRouter>
        <CaleonOverlay />
      </div>
    </CaleonProvider>
  );
}

export default App;
