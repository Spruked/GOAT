import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Shield } from 'lucide-react';

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Back Button */}
        <Link to="/login" className="inline-flex items-center text-cyan-400 hover:text-cyan-300 mb-8">
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Login
        </Link>

        {/* Header */}
        <div className="flex items-center mb-8">
          <Shield className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Terms of Service</h1>
            <p className="text-slate-400 mt-2">Last Updated: December 15, 2025</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Acceptance of Terms</h2>
            <p className="text-slate-300 leading-relaxed">
              By accessing and using GOAT Vault ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to these terms, please do not use the Service.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Description of Service</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              GOAT Vault is a legacy preservation and content creation platform that allows users to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Create and store personal legacies, books, podcasts, and content</li>
              <li>Organize knowledge and information</li>
              <li>Generate structured content with AI assistance</li>
              <li>Preserve digital assets for future generations</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. User Accounts</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You are responsible for:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Maintaining the confidentiality of your account credentials</li>
              <li>All activities that occur under your account</li>
              <li>Notifying us immediately of any unauthorized use</li>
              <li>Ensuring your account information is accurate and up-to-date</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. User Content</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You retain all rights to your content. By using our Service, you grant us a limited license to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Store and process your content to provide the Service</li>
              <li>Create backups and derivatives necessary for functionality</li>
              <li>Use anonymized, aggregated data for service improvement</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              You are solely responsible for the content you create and must not upload content that violates any laws or third-party rights.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Prohibited Uses</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You may not use the Service to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Violate any laws or regulations</li>
              <li>Infringe upon intellectual property rights</li>
              <li>Transmit malware, viruses, or harmful code</li>
              <li>Harass, abuse, or harm others</li>
              <li>Engage in unauthorized access or data mining</li>
              <li>Impersonate others or provide false information</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Intellectual Property</h2>
            <p className="text-slate-300 leading-relaxed">
              The Service, including its original content, features, and functionality, is owned by GOAT Vault and is protected by international copyright, trademark, and other intellectual property laws. You may not copy, modify, or distribute our intellectual property without explicit permission.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Payments and Subscriptions</h2>
            <p className="text-slate-300 leading-relaxed">
              Certain features may require payment. All fees are non-refundable unless otherwise stated. We reserve the right to change pricing with 30 days notice. Subscriptions automatically renew unless cancelled before the renewal date.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Termination</h2>
            <p className="text-slate-300 leading-relaxed">
              We may terminate or suspend your account immediately, without prior notice, for conduct that we believe violates these Terms or is harmful to other users, us, or third parties, or for any other reason at our sole discretion.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Disclaimer of Warranties</h2>
            <p className="text-slate-300 leading-relaxed">
              THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. WE DO NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED, SECURE, OR ERROR-FREE.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Limitation of Liability</h2>
            <p className="text-slate-300 leading-relaxed">
              IN NO EVENT SHALL GOAT VAULT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF YOUR USE OF THE SERVICE.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Governing Law</h2>
            <p className="text-slate-300 leading-relaxed">
              These Terms shall be governed by and construed in accordance with the laws of the United States, without regard to its conflict of law provisions.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Changes to Terms</h2>
            <p className="text-slate-300 leading-relaxed">
              We reserve the right to modify these Terms at any time. We will notify users of any material changes via email or through the Service. Your continued use after such modifications constitutes acceptance of the updated Terms.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">13. Contact Information</h2>
            <p className="text-slate-300 leading-relaxed">
              If you have any questions about these Terms, please contact us at:
            </p>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Vault Support</p>
              <p className="text-slate-300">Email: legal@goatvault.io</p>
            </div>
          </section>
        </div>

        {/* Back to Login */}
        <div className="mt-12 text-center">
          <Link
            to="/login"
            className="inline-flex items-center bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-700 hover:to-purple-700 text-white font-bold py-3 px-8 rounded-lg transition-all duration-200"
          >
            Return to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
