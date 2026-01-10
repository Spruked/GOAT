import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, FileText } from 'lucide-react';

export default function ContentOwnershipPage() {
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
          <FileText className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Content Ownership Agreement</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Agreement Overview</h2>
            <p className="text-slate-300 leading-relaxed">
              This Content Ownership Agreement ("Agreement") governs the relationship between you ("Customer," "you," or "your") and GOAT ("we," "us," or "our") regarding content ownership and usage rights. This Agreement is fundamental to GOAT's "preparation, not publishing" philosophy.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>Key Principle</strong>: GOAT is a content preparation service only. We help you create professional content, but you retain 100% ownership and control of all your content at all times.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Customer Content Ownership</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Complete Ownership Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Exclusive Ownership</strong>: You retain complete and exclusive ownership of all content you upload, create, or generate through GOAT</li>
              <li><strong>No Transfer of Rights</strong>: GOAT does not acquire any ownership rights, including copyright, trademark, or intellectual property rights</li>
              <li><strong>Full Control</strong>: You have complete control over how your content is used, distributed, or monetized</li>
              <li><strong>No Restrictions</strong>: GOAT imposes no restrictions on your use of your content</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Content Types Covered</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Original Content</strong>: Text, images, audio, video, and other media you provide</li>
              <li><strong>AI-Enhanced Content</strong>: Content enhanced or modified using GOAT's AI tools</li>
              <li><strong>Generated Content</strong>: New content created through GOAT's generation tools</li>
              <li><strong>Processed Output</strong>: Professional deliverables (PDFs, audiobooks, etc.) created from your content</li>
              <li><strong>Metadata and Tags</strong>: Blockchain metadata and content tags prepared by GOAT</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. GOAT's Limited License</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Technical Processing License</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Processing Rights</strong>: You grant GOAT a limited, revocable license to process your content for service delivery</li>
              <li><strong>Time-Limited</strong>: This license exists only during active service provision</li>
              <li><strong>Purpose-Specific</strong>: License is limited to preparing your content for your use</li>
              <li><strong>Automatically Terminates</strong>: License terminates immediately upon service completion or account closure</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">What GOAT Can Do With Your Content</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Format Conversion</strong>: Convert content between different formats (text to PDF, text to audio, etc.)</li>
              <li><strong>Quality Enhancement</strong>: Improve formatting, structure, and presentation</li>
              <li><strong>Technical Processing</strong>: Apply AI tools to enhance or generate content as directed</li>
              <li><strong>Storage and Backup</strong>: Store content securely during processing (encrypted and inaccessible)</li>
              <li><strong>Delivery Preparation</strong>: Prepare content for download and delivery to you</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">What GOAT Cannot Do With Your Content</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>No Publishing</strong>: GOAT cannot publish, distribute, or make your content publicly available</li>
              <li><strong>No Monetization</strong>: GOAT cannot monetize, license, or sell your content</li>
              <li><strong>No Third-Party Sharing</strong>: GOAT cannot share your content with third parties without explicit consent</li>
              <li><strong>No AI Training</strong>: GOAT cannot use your content to train AI models</li>
              <li><strong>No Derivative Works</strong>: GOAT cannot create derivative works for its own use</li>
              <li><strong>No Archival Rights</strong>: GOAT cannot retain your content after service completion</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. AI-Generated Content Ownership</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Complete Customer Ownership</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Output Ownership</strong>: You own 100% of all AI-generated or AI-enhanced content output</li>
              <li><strong>No AI Rights Retention</strong>: GOAT retains no rights to AI-generated content</li>
              <li><strong>Commercial Usage</strong>: You can commercially use, license, or sell AI-enhanced content</li>
              <li><strong>No Attribution Required</strong>: You are not required to attribute GOAT for AI-generated content</li>
              <li><strong>Full Exploitation Rights</strong>: You can exploit the content in any way you choose</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">AI Tool Usage</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Tool Access</strong>: GOAT provides access to AI tools for content enhancement</li>
              <li><strong>Customer Direction</strong>: AI tools operate under your direction and control</li>
              <li><strong>Output Control</strong>: You control the parameters and direction of AI generation</li>
              <li><strong>Revision Rights</strong>: You can request unlimited revisions of AI-generated content</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Intellectual Property Protections</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Your IP Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Copyright Protection</strong>: Your original content remains protected under copyright law</li>
              <li><strong>Trademark Protection</strong>: Your trademarks and branding remain your exclusive property</li>
              <li><strong>Patent Protection</strong>: Any patented processes or inventions remain your property</li>
              <li><strong>Trade Secret Protection</strong>: Your confidential information remains protected</li>
              <li><strong>Moral Rights</strong>: You retain all moral rights in your content</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Third-Party Content</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Your Responsibility</strong>: You are responsible for ensuring you have rights to any third-party content</li>
              <li><strong>License Verification</strong>: You must have proper licenses for third-party materials</li>
              <li><strong>Indemnification</strong>: You agree to indemnify GOAT for third-party content claims</li>
              <li><strong>Content Review</strong>: GOAT may refuse to process content with questionable ownership</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Content Security and Privacy</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Zero-Knowledge Architecture</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Encrypted Storage</strong>: All content is encrypted using industry-standard encryption</li>
              <li><strong>Access Prevention</strong>: GOAT personnel cannot access your content</li>
              <li><strong>Secure Processing</strong>: Content is processed in secure, isolated environments</li>
              <li><strong>Automatic Deletion</strong>: Content is automatically deleted after processing completion</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Privacy Protections</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>No Data Mining</strong>: GOAT does not analyze or mine your content</li>
              <li><strong>No Usage Analytics</strong>: GOAT does not track how you use your content</li>
              <li><strong>No Content Sharing</strong>: GOAT does not share content with third parties</li>
              <li><strong>Minimal Metadata</strong>: Only essential processing metadata is retained temporarily</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Content Export and Portability</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Export Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Full Export</strong>: You can export all your content in original and processed formats</li>
              <li><strong>Multiple Formats</strong>: Content available in all supported export formats</li>
              <li><strong>No Export Fees</strong>: Standard export functionality is included in service fees</li>
              <li><strong>Unlimited Downloads</strong>: You can download your content unlimited times</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Portability</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Standard Formats</strong>: Content exported in industry-standard formats</li>
              <li><strong>Metadata Included</strong>: All relevant metadata and tags included in exports</li>
              <li><strong>Third-Party Compatible</strong>: Exported content compatible with other services</li>
              <li><strong>No Vendor Lock-in</strong>: You can easily migrate to other platforms</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Content Deletion and Account Closure</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Deletion Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Complete Deletion</strong>: You can request complete deletion of all your content and data</li>
              <li><strong>Immediate Processing</strong>: Deletion requests are processed immediately</li>
              <li><strong>No Retention</strong>: GOAT does not retain deleted content</li>
              <li><strong>Confirmation</strong>: You receive confirmation when deletion is complete</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Account Closure</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Full Termination</strong>: Account closure terminates all licenses and access rights</li>
              <li><strong>Content Ownership</strong>: Content ownership rights remain with you after closure</li>
              <li><strong>Export Window</strong>: You have a grace period to export content before closure</li>
              <li><strong>No Reversal</strong>: Account closure is permanent but content ownership is preserved</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Breach of Agreement</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">GOAT's Obligations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>License Compliance</strong>: GOAT must comply with all license limitations</li>
              <li><strong>Content Protection</strong>: GOAT must protect your content from unauthorized access</li>
              <li><strong>Privacy Compliance</strong>: GOAT must comply with all privacy obligations</li>
              <li><strong>Immediate Cessation</strong>: Any unauthorized use must cease immediately</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Remedies for Breach</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>License Termination</strong>: Immediate termination of GOAT's limited license</li>
              <li><strong>Content Return</strong>: Return or deletion of all your content</li>
              <li><strong>Damages</strong>: You may be entitled to damages for unauthorized use</li>
              <li><strong>Injunctive Relief</strong>: Court orders to prevent further unauthorized use</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Dispute Resolution</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Ownership Disputes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Good Faith Resolution</strong>: Disputes resolved in good faith</li>
              <li><strong>Evidence-Based</strong>: Resolution based on evidence of ownership</li>
              <li><strong>Independent Review</strong>: Third-party review for complex disputes</li>
              <li><strong>Legal Compliance</strong>: Compliance with applicable intellectual property laws</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Mediation Process</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Voluntary Mediation</strong>: Both parties can agree to mediation</li>
              <li><strong>Neutral Mediator</strong>: Independent mediator for dispute resolution</li>
              <li><strong>Binding Agreements</strong>: Mediation agreements are binding</li>
              <li><strong>Cost Sharing</strong>: Mediation costs shared equally</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Governing Law and Jurisdiction</h2>
            <p className="text-slate-300 leading-relaxed">
              This Agreement shall be governed by and construed in accordance with the laws of the jurisdiction in which GOAT operates, without regard to conflict of law principles. Any disputes arising from this Agreement shall be resolved in the courts of competent jurisdiction in that location.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              This governing law provision ensures consistent interpretation of content ownership rights and protects both parties' interests in intellectual property matters.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Updates and Amendments</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Amendment Process</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Customer Consent</strong>: Material changes require customer consent</li>
              <li><strong>Advance Notice</strong>: Changes communicated 30 days in advance</li>
              <li><strong>Opt-out Rights</strong>: Customers can opt-out of changes affecting ownership rights</li>
              <li><strong>Legal Review</strong>: Changes reviewed for consistency with ownership principles</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Version Control</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Version History</strong>: All versions of this Agreement are maintained</li>
              <li><strong>Effective Dates</strong>: Clear effective dates for all changes</li>
              <li><strong>Customer Rights</strong>: Existing customers' rights protected from adverse changes</li>
              <li><strong>Transparency</strong>: All changes clearly documented and communicated</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">13. Contact Information</h2>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Content Ownership Team</p>
              <p className="text-slate-300">Email: ownership@goatvault.io</p>
              <p className="text-slate-300 mt-2">Legal Department: legal@goatvault.io</p>
              <p className="text-slate-300 mt-2">For general inquiries: support@goatvault.io</p>
            </div>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">14. Entire Agreement</h2>
            <p className="text-slate-300 leading-relaxed">
              This Content Ownership Agreement, together with our Terms of Service and Privacy Policy, constitutes the entire agreement between you and GOAT regarding content ownership and supersedes all prior agreements or understandings. This Agreement cannot be modified except in writing signed by both parties.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>Fundamental Principle</strong>: Your content remains yours. GOAT's role is limited to preparation services only. We do not publish, distribute, or monetize your work.
            </p>
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