import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Shield } from 'lucide-react';

export default function CustomerRightsPage() {
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
            <h1 className="text-4xl font-bold text-cyan-400">Customer Rights Statement</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Introduction</h2>
            <p className="text-slate-300 leading-relaxed">
              GOAT ("we," "us," or "our") is committed to transparency and protecting your rights as a customer. This Customer Rights Statement explains your rights when using our content preparation services. GOAT is a **preparation service only** - we help you create professional content, but we do not publish, distribute, or monetize your work.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Content Ownership Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">You Own Your Content</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>100% Ownership</strong>: You retain complete and exclusive ownership of all content you upload, create, or generate through GOAT</li>
              <li><strong>No Transfer of Rights</strong>: GOAT does not acquire any ownership rights to your content</li>
              <li><strong>No Publishing Rights</strong>: GOAT does not obtain publishing, distribution, or commercialization rights to your content</li>
              <li><strong>No Restrictions</strong>: You can use your content however you wish</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">What GOAT Does</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Preparation Services</strong>: We provide AI-powered tools to prepare, format, and enhance your content</li>
              <li><strong>Technical Processing</strong>: We process your content to create professional deliverables (PDFs, audio files, etc.)</li>
              <li><strong>Quality Enhancement</strong>: We improve formatting, structure, and presentation of your content</li>
              <li><strong>Blockchain Preparation</strong>: We prepare content metadata for blockchain integration (when applicable)</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">What GOAT Does Not Do</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>No Publishing</strong>: We do not publish, distribute, or make your content publicly available</li>
              <li><strong>No Monetization</strong>: We do not monetize, license, or sell your content</li>
              <li><strong>No Third-Party Sharing</strong>: We do not share your content with third parties without your explicit consent</li>
              <li><strong>No AI Training</strong>: We do not use your content to train AI models</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. Data Privacy Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Your Data Control</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Access Rights</strong>: You can access all your content and data at any time</li>
              <li><strong>Export Rights</strong>: You can export your content and data in standard formats</li>
              <li><strong>Deletion Rights</strong>: You can request complete deletion of your account and all associated data</li>
              <li><strong>Portability Rights</strong>: You can transfer your data to other services</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Security</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Zero-Knowledge Architecture</strong>: Your content is encrypted and we cannot access it</li>
              <li><strong>Secure Storage</strong>: All data is stored with industry-standard encryption</li>
              <li><strong>No Data Mining</strong>: We do not analyze or mine your content for commercial purposes</li>
              <li><strong>Minimal Data Collection</strong>: We collect only essential data needed to provide services</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. Service Usage Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Fair Usage</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Unlimited Preparation</strong>: You can prepare unlimited content within our service limits</li>
              <li><strong>Multiple Formats</strong>: You can generate content in all supported formats</li>
              <li><strong>Quality Assurance</strong>: You receive professional-quality output for all projects</li>
              <li><strong>Technical Support</strong>: You have access to customer support for service-related issues</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Service Boundaries</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Per-Project Model</strong>: Each project is a separate service engagement</li>
              <li><strong>No Subscription Lock-in</strong>: You are not bound by recurring subscriptions</li>
              <li><strong>Cancellation Rights</strong>: You can cancel projects at any time before completion</li>
              <li><strong>Refund Eligibility</strong>: You may be eligible for refunds under our Refund Policy</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Intellectual Property Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Your IP Protection</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Copyright Protection</strong>: Your original content remains protected under copyright law</li>
              <li><strong>Trademark Protection</strong>: Your trademarks and branding remain your exclusive property</li>
              <li><strong>Patent Protection</strong>: Any patented processes or inventions remain your property</li>
              <li><strong>Trade Secret Protection</strong>: Your confidential information remains protected</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">AI-Generated Content</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Ownership of Output</strong>: You own the final output generated by GOAT's AI tools</li>
              <li><strong>No AI Rights Retention</strong>: GOAT does not retain any rights to AI-generated content</li>
              <li><strong>Commercial Usage</strong>: You can commercially use, license, or sell AI-enhanced content</li>
              <li><strong>Attribution Rights</strong>: You are not required to attribute GOAT for AI-generated content</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Quality and Performance Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Service Quality Guarantees</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Professional Output</strong>: All deliverables meet professional publishing standards</li>
              <li><strong>Technical Accuracy</strong>: Content processing maintains accuracy and integrity</li>
              <li><strong>Format Compliance</strong>: Output files meet industry standards for their formats</li>
              <li><strong>Delivery Timelines</strong>: Projects are completed within estimated timeframes</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Issue Resolution</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Bug Fixes</strong>: We fix any technical issues with our processing</li>
              <li><strong>Reprocessing</strong>: We reprocess content if quality standards are not met</li>
              <li><strong>Compensation</strong>: We provide appropriate compensation for service failures</li>
              <li><strong>Escalation Support</strong>: You can escalate issues to our senior support team</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Privacy and Security Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Privacy Protections</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Data Minimization</strong>: We collect only essential information</li>
              <li><strong>Purpose Limitation</strong>: Your data is used only for service provision</li>
              <li><strong>Consent Requirements</strong>: We obtain consent before any data processing</li>
              <li><strong>Privacy by Design</strong>: Privacy protections are built into our systems</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Security Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Encryption Standards</strong>: All data is encrypted in transit and at rest</li>
              <li><strong>Access Controls</strong>: Strict internal access controls protect your data</li>
              <li><strong>Breach Notification</strong>: You will be notified of any security breaches</li>
              <li><strong>Incident Response</strong>: We have 24/7 incident response capabilities</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Transparency and Communication Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Information Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Transparency</strong>: You receive clear information about our processes</li>
              <li><strong>Pricing Transparency</strong>: All fees and costs are clearly disclosed</li>
              <li><strong>Terms Clarity</strong>: Our terms and policies are written in plain language</li>
              <li><strong>Contact Information</strong>: You have direct access to our support team</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Communication Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Regular Updates</strong>: You receive updates about your projects</li>
              <li><strong>Support Access</strong>: You can contact support through multiple channels</li>
              <li><strong>Feedback Opportunities</strong>: You can provide feedback on our services</li>
              <li><strong>Survey Participation</strong>: You can participate in service improvement surveys</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Legal and Compliance Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Regulatory Compliance</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>GDPR Compliance</strong>: We comply with EU data protection regulations</li>
              <li><strong>CCPA Compliance</strong>: We comply with California privacy laws</li>
              <li><strong>Industry Standards</strong>: We follow industry best practices for data security</li>
              <li><strong>Legal Updates</strong>: We update our policies to comply with new regulations</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Dispute Resolution</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Fair Resolution</strong>: We resolve disputes fairly and transparently</li>
              <li><strong>Mediation Options</strong>: We offer mediation for unresolved disputes</li>
              <li><strong>Legal Compliance</strong>: We comply with applicable consumer protection laws</li>
              <li><strong>Court Access</strong>: You retain the right to pursue legal action if necessary</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Future Rights and Updates</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Service Evolution</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Feature Additions</strong>: You benefit from new features and improvements</li>
              <li><strong>Backward Compatibility</strong>: Existing content remains accessible</li>
              <li><strong>Migration Support</strong>: We help migrate content between service versions</li>
              <li><strong>Legacy Support</strong>: We maintain support for legacy content formats</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Rights Preservation</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>No Rights Erosion</strong>: Your rights do not diminish over time</li>
              <li><strong>Policy Improvements</strong>: Policy updates can only enhance your rights</li>
              <li><strong>Retroactive Protection</strong>: New protections apply to existing users</li>
              <li><strong>Contract Stability</strong>: Your rights remain stable across service updates</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Contact and Enforcement</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Exercising Your Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Support Contact</strong>: Contact our support team to exercise any rights</li>
              <li><strong>Documentation</strong>: Provide necessary documentation for rights requests</li>
              <li><strong>Timely Response</strong>: We respond to rights requests within required timeframes</li>
              <li><strong>Appeal Process</strong>: You can appeal decisions about your rights</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Contact Information</h3>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Customer Rights Team</p>
              <p className="text-slate-300">Email: rights@goatvault.io</p>
              <p className="text-slate-300 mt-2">For general inquiries: support@goatvault.io</p>
            </div>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Updates to This Statement</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this Customer Rights Statement to reflect changes in our services or legal requirements. Updates will be:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Posted on our website with clear notice</li>
              <li>Sent via email to registered users</li>
              <li>Applied prospectively to maintain your existing rights</li>
              <li>Reviewed for consistency with our "preparation, not publishing" philosophy</li>
            </ul>
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

        {/* Copyright */}
        <div className="mt-8 text-center text-slate-400 text-sm">
          <p>Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}