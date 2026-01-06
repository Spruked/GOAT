import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Lock } from 'lucide-react';

export default function PrivacyPage() {
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
          <Lock className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Privacy Policy</h1>
            <p className="text-slate-400 mt-2">Last Updated: December 15, 2025</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Introduction</h2>
            <p className="text-slate-300 leading-relaxed">
              GOAT Vault ("we," "us," or "our") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Service. By using GOAT Vault, you consent to the practices described in this policy.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Information We Collect</h2>
            
            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Personal Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Name and email address</li>
              <li>Account credentials (encrypted passwords)</li>
              <li>Payment information (processed securely by third-party providers)</li>
              <li>Profile information you choose to provide</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Content Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Content you create, upload, or store in the Service</li>
              <li>Files, documents, and media you upload</li>
              <li>Messages and communications within the platform</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Usage Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Device information (browser type, operating system)</li>
              <li>IP address and location data</li>
              <li>Usage patterns and feature interactions</li>
              <li>Error logs and performance data</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. How We Use Your Information</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We use the collected information to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Provide, maintain, and improve our Service</li>
              <li>Process transactions and send related information</li>
              <li>Send technical notices and security alerts</li>
              <li>Respond to your comments and questions</li>
              <li>Monitor and analyze trends, usage, and activities</li>
              <li>Detect and prevent fraud and security issues</li>
              <li>Personalize and improve your experience</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. Data Security</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We implement robust security measures to protect your information:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>End-to-End Encryption:</strong> Your content is encrypted in transit and at rest</li>
              <li><strong>Zero-Knowledge Architecture:</strong> We cannot access your encrypted content</li>
              <li><strong>Secure Password Storage:</strong> Passwords are hashed using industry-standard algorithms</li>
              <li><strong>Regular Security Audits:</strong> We conduct regular security assessments</li>
              <li><strong>Access Controls:</strong> Strict internal access policies and monitoring</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              However, no method of transmission over the Internet is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Information Sharing</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We do not sell your personal information. We may share information with:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Providers:</strong> Third parties who perform services on our behalf (hosting, analytics, payment processing)</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect our rights</li>
              <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets</li>
              <li><strong>With Your Consent:</strong> When you explicitly authorize us to share information</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Data Retention</h2>
            <p className="text-slate-300 leading-relaxed">
              We retain your information for as long as your account is active or as needed to provide services. You may request deletion of your account and data at any time. We will retain certain information as required by law or for legitimate business purposes, such as fraud prevention and record-keeping.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Your Privacy Rights</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You have the right to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Access:</strong> Request a copy of your personal information</li>
              <li><strong>Correction:</strong> Update or correct inaccurate information</li>
              <li><strong>Deletion:</strong> Request deletion of your account and data</li>
              <li><strong>Portability:</strong> Export your data in a machine-readable format</li>
              <li><strong>Opt-Out:</strong> Unsubscribe from marketing communications</li>
              <li><strong>Restriction:</strong> Limit how we use your information</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              To exercise these rights, contact us at privacy@goatvault.io
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Cookies and Tracking</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We use cookies and similar technologies to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Maintain your session and keep you logged in</li>
              <li>Remember your preferences and settings</li>
              <li>Analyze site usage and performance</li>
              <li>Provide personalized features</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              You can control cookies through your browser settings. Note that disabling cookies may affect Service functionality.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Third-Party Links</h2>
            <p className="text-slate-300 leading-relaxed">
              Our Service may contain links to third-party websites. We are not responsible for the privacy practices of these sites. We encourage you to review their privacy policies before providing any information.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Children's Privacy</h2>
            <p className="text-slate-300 leading-relaxed">
              Our Service is not intended for children under 13. We do not knowingly collect personal information from children. If you believe we have collected information from a child, please contact us immediately.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. International Data Transfers</h2>
            <p className="text-slate-300 leading-relaxed">
              Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place to protect your information in accordance with this Privacy Policy.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Changes to This Policy</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this Privacy Policy from time to time. We will notify you of material changes via email or through the Service. The "Last Updated" date at the top indicates when the policy was last revised.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">13. Contact Us</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              If you have questions about this Privacy Policy or our privacy practices, please contact us:
            </p>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Vault Privacy Team</p>
              <p className="text-slate-300">Email: privacy@goatvault.io</p>
              <p className="text-slate-300 mt-2">For general inquiries: support@goatvault.io</p>
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
