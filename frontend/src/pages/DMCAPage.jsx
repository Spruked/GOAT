import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ShieldCheck } from 'lucide-react';

export default function DMCAPage() {
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
          <ShieldCheck className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">DMCA Policy</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Introduction</h2>
            <p className="text-slate-300 leading-relaxed">
              GOAT respects the intellectual property rights of others and expects our users to do the same. This Digital Millennium Copyright Act ("DMCA") Policy describes our procedures for handling copyright infringement claims and our commitment to protecting copyright owners' rights.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>DMCA Compliance</strong>: GOAT complies with the DMCA and other applicable copyright laws. We respond to valid copyright infringement notices and take appropriate action to remove or disable access to allegedly infringing content.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Our Content Ownership Philosophy</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Preparation, Not Publishing</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Content Preparation Service</strong>: GOAT provides AI-powered tools to prepare and enhance content</li>
              <li><strong>No Publishing Rights</strong>: We do not publish, distribute, or make content publicly available</li>
              <li><strong>Customer Ownership</strong>: You retain 100% ownership of all content processed through GOAT</li>
              <li><strong>Private Processing</strong>: All content processing occurs in secure, private environments</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Zero-Knowledge Processing</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Encrypted Content</strong>: Your content is encrypted and inaccessible to GOAT personnel</li>
              <li><strong>Automated Processing</strong>: AI tools process content without human review</li>
              <li><strong>No Content Storage</strong>: Content is not stored after processing completion</li>
              <li><strong>Secure Delivery</strong>: Processed content is delivered directly to you</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. Copyright Infringement Reporting</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">DMCA Agent</h3>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT DMCA Agent</p>
              <p className="text-slate-300">Email: dmca@goatvault.io</p>
              <p className="text-slate-300 mt-2">Phone: 1-800-GOAT-DMCA (Available 9 AM - 5 PM EST)</p>
              <p className="text-slate-300 mt-2">Address: [Legal Department Address]</p>
            </div>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Valid DMCA Notice Requirements</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Physical/Electronic Signature</strong>: Signature of copyright owner or authorized representative</li>
              <li><strong>Identification</strong>: Identification of copyrighted work claimed to be infringed</li>
              <li><strong>Location</strong>: Identification of infringing material and its location</li>
              <li><strong>Contact Information</strong>: Your contact information (address, phone, email)</li>
              <li><strong>Good Faith Statement</strong>: Statement that you believe use is not authorized</li>
              <li><strong>Accuracy Statement</strong>: Statement that information is accurate under penalty of perjury</li>
              <li><strong>Authority Statement</strong>: Statement that you are authorized to act on copyright owner's behalf</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. DMCA Takedown Process</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Notice Review</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Receipt Confirmation</strong>: Acknowledge receipt of DMCA notice within 24 hours</li>
              <li><strong>Validity Assessment</strong>: Review notice for completeness and validity</li>
              <li><strong>Content Investigation</strong>: Investigate the alleged infringement</li>
              <li><strong>Action Determination</strong>: Determine appropriate response based on findings</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Takedown Actions</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Content Removal</strong>: Remove or disable access to allegedly infringing content</li>
              <li><strong>User Notification</strong>: Notify the affected user of the takedown</li>
              <li><strong>Forward Notice</strong>: Forward the DMCA notice to the user</li>
              <li><strong>Account Actions</strong>: May suspend or terminate accounts for repeat infringement</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Response Timeframes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Initial Response</strong>: Respond to valid notices within 24 hours</li>
              <li><strong>Content Removal</strong>: Remove infringing content within 10 business days</li>
              <li><strong>User Notification</strong>: Notify affected users within 24 hours of removal</li>
              <li><strong>Counter-Notice Response</strong>: Respond to counter-notices within 14 days</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Counter-Notification Process</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Counter-Notice Requirements</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Physical/Electronic Signature</strong>: Your physical or electronic signature</li>
              <li><strong>Identification</strong>: Identification of material removed and its location</li>
              <li><strong>Good Faith Statement</strong>: Statement under penalty of perjury that material was removed by mistake</li>
              <li><strong>Jurisdiction Consent</strong>: Consent to jurisdiction in federal court for your district</li>
              <li><strong>Contact Information</strong>: Your name, address, phone number, and email</li>
              <li><strong>Accuracy Statement</strong>: Statement that you will accept service of process from complainant</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Counter-Notice Process</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Submission</strong>: Send counter-notice to our designated DMCA agent</li>
              <li><strong>Forwarding</strong>: We forward your counter-notice to the original complainant</li>
              <li><strong>Content Restoration</strong>: May restore content 10-14 days after forwarding</li>
              <li><strong>Legal Notice</strong>: Original complainant may seek court order to prevent restoration</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Repeat Infringer Policy</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Repeat Infringement</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Tracking</strong>: We track DMCA notices and counter-notices</li>
              <li><strong>Pattern Recognition</strong>: Identify users with multiple infringement claims</li>
              <li><strong>Warning System</strong>: Issue warnings for first-time and repeat violations</li>
              <li><strong>Account Termination</strong>: Terminate accounts of repeat infringers</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Termination Process</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Notice</strong>: Provide written notice of termination decision</li>
              <li><strong>Appeal Right</strong>: Allow appeal of termination within 14 days</li>
              <li><strong>Content Deletion</strong>: Delete all user content upon termination</li>
              <li><strong>Reinstatement</strong>: May offer reinstatement after sufficient time and compliance</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Fair Use and Limitations</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Fair Use Defense</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Good Faith</strong>: We consider fair use defenses in good faith</li>
              <li><strong>Factor Analysis</strong>: Evaluate purpose, nature, amount, and market effect</li>
              <li><strong>Restoration</strong>: May restore content if fair use claim is credible</li>
              <li><strong>Legal Referral</strong>: Refer disputed claims to legal counsel when appropriate</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Limitations and Exceptions</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Educational Use</strong>: Consider educational and research purposes</li>
              <li><strong>Parody/Satire</strong>: Evaluate transformative uses and commentary</li>
              <li><strong>News Reporting</strong>: Allow fair use for news and current events</li>
              <li><strong>Library Exceptions</strong>: Respect library and archive preservation rights</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Misrepresentation and Abuse</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">False Claims</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Investigation</strong>: Investigate claims of false or misleading notices</li>
              <li><strong>Penalties</strong>: Pursue legal action against knowingly false claims</li>
              <li><strong>Damages Recovery</strong>: Seek recovery of damages and legal costs</li>
              <li><strong>Account Actions</strong>: May terminate accounts for abuse of DMCA process</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Abuse Prevention</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Pattern Monitoring</strong>: Monitor for patterns of abusive DMCA filings</li>
              <li><strong>Automated Detection</strong>: Use technology to detect potentially abusive notices</li>
              <li><strong>Third-Party Verification</strong>: Consult legal experts for complex cases</li>
              <li><strong>Transparency</strong>: Maintain public records of DMCA actions</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. International Copyright Considerations</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Global Compliance</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Berne Convention</strong>: Respect international copyright standards</li>
              <li><strong>WIPO Cooperation</strong>: Cooperate with World Intellectual Property Organization</li>
              <li><strong>Local Laws</strong>: Comply with copyright laws in relevant jurisdictions</li>
              <li><strong>Cross-Border</strong>: Handle international copyright disputes appropriately</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">International Notices</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Language Support</strong>: Accept notices in major languages</li>
              <li><strong>Translation</strong>: Provide translation services for international notices</li>
              <li><strong>Local Counsel</strong>: Consult local legal experts when needed</li>
              <li><strong>Jurisdiction</strong>: Respect appropriate jurisdictional requirements</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Transparency and Reporting</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">DMCA Reporting</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Annual Reports</strong>: Publish annual DMCA transparency reports</li>
              <li><strong>Notice Statistics</strong>: Report on number of notices received and processed</li>
              <li><strong>Response Times</strong>: Report on average response and processing times</li>
              <li><strong>Outcome Data</strong>: Share data on notice outcomes and appeals</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Public Records</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Notice Archive</strong>: Maintain archive of processed DMCA notices</li>
              <li><strong>Redaction</strong>: Redact personal information from public records</li>
              <li><strong>Searchable Database</strong>: Provide searchable database of actions</li>
              <li><strong>Appeal Records</strong>: Document appeal outcomes and reasoning</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Legal Compliance and Cooperation</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Law Enforcement Cooperation</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Valid Requests</strong>: Respond to valid law enforcement requests</li>
              <li><strong>Preservation Orders</strong>: Preserve evidence when legally required</li>
              <li><strong>Subpoena Compliance</strong>: Comply with properly served subpoenas</li>
              <li><strong>Chain of Custody</strong>: Maintain proper chain of custody for evidence</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Court Orders</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Jurisdiction</strong>: Respect court orders from competent jurisdictions</li>
              <li><strong>Appeal Rights</strong>: Allow time for appeals before compliance</li>
              <li><strong>Scope Limitation</strong>: Comply only with scope of court order</li>
              <li><strong>Documentation</strong>: Maintain detailed records of compliance</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Updates and Amendments</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this DMCA Policy to reflect changes in copyright law, our practices, or legal requirements. Updates will be:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Posted on our website with clear notice</li>
              <li>Sent via email to registered users</li>
              <li>Applied prospectively to maintain fairness</li>
              <li>Reviewed for consistency with copyright law</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">13. Contact Information</h2>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">DMCA Agent</p>
              <p className="text-slate-300">Email: dmca@goatvault.io</p>
              <p className="text-slate-300 mt-2">Phone: 1-800-GOAT-DMCA</p>
              <p className="text-slate-300 mt-2">Legal Department: legal@goatvault.io</p>
            </div>
            <p className="text-slate-300 mt-4 text-sm">
              <strong>Emergency Contact</strong>: For urgent copyright matters outside business hours, call our emergency line.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">14. Disclaimer</h2>
            <p className="text-slate-300 leading-relaxed">
              This DMCA Policy is not legal advice. GOAT is not a law firm and does not provide legal advice. For legal questions about copyright or DMCA, consult qualified legal counsel. This policy describes our procedures but does not create contractual obligations beyond those required by law.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>Limitation of Liability</strong>: GOAT's liability under this DMCA Policy is limited to the requirements of the DMCA and applicable copyright law. We are not liable for indirect, incidental, or consequential damages arising from DMCA compliance.
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