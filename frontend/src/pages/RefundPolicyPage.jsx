import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, DollarSign } from 'lucide-react';

export default function RefundPolicyPage() {
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
          <DollarSign className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Refund Policy</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Overview</h2>
            <p className="text-slate-300 leading-relaxed">
              GOAT is committed to providing high-quality content preparation services. This Refund Policy outlines when and how you can request refunds for our services. Our policy is designed to be fair and transparent, reflecting our "preparation, not publishing" business model.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>Key Principle</strong>: GOAT provides per-project content preparation services. Refunds are available when we fail to deliver the promised service or when you cancel before substantial work begins.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Refund Eligibility</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Automatic Refunds</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Failure</strong>: Full refund if we cannot deliver the service due to our technical issues</li>
              <li><strong>Project Cancellation Before Start</strong>: Full refund if you cancel before we begin processing</li>
              <li><strong>Payment Processing Errors</strong>: Full refund for duplicate or erroneous charges</li>
              <li><strong>System Outages</strong>: Pro-rated refund for extended service unavailability (24+ hours)</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Discretionary Refunds</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Quality Issues</strong>: Partial or full refund if output doesn't meet professional standards</li>
              <li><strong>Timeline Delays</strong>: Partial refund for significant delays beyond estimated completion</li>
              <li><strong>Feature Unavailability</strong>: Refund for promised features that become unavailable</li>
              <li><strong>Exceptional Circumstances</strong>: Case-by-case review for unique situations</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Non-Refundable Items</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Completed Projects</strong>: No refunds for successfully completed projects</li>
              <li><strong>Downloaded Content</strong>: No refunds once deliverables have been downloaded</li>
              <li><strong>Third-Party Services</strong>: No refunds for integrated third-party services</li>
              <li><strong>Account Fees</strong>: No refunds for account maintenance or storage fees</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. Refund Timeframes</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Request Windows</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Pre-Processing</strong>: Full refund available before project processing begins</li>
              <li><strong>During Processing</strong>: Partial refund available during active processing (prorated)</li>
              <li><strong>Post-Delivery</strong>: Refund requests must be made within 7 days of delivery</li>
              <li><strong>Quality Issues</strong>: Refund requests for quality issues within 14 days of delivery</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Processing Time</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Automatic Refunds</strong>: Processed within 1-2 business days</li>
              <li><strong>Review Required</strong>: Discretionary refunds reviewed within 5-7 business days</li>
              <li><strong>Complex Cases</strong>: Extended review period of up to 14 days for complex disputes</li>
              <li><strong>Payment Method</strong>: Refunds issued to original payment method</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. Refund Amounts</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Full Refunds</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Unavailable</strong>: 100% refund for technical failures preventing service delivery</li>
              <li><strong>Cancellation Before Processing</strong>: 100% refund for projects cancelled before work begins</li>
              <li><strong>Payment Errors</strong>: 100% refund for duplicate or incorrect charges</li>
              <li><strong>Material Breach</strong>: 100% refund if we materially breach this agreement</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Partial Refunds</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Quality Deficiencies</strong>: 25-75% refund based on severity of quality issues</li>
              <li><strong>Timeline Delays</strong>: 10-50% refund based on delay duration and impact</li>
              <li><strong>Feature Reduction</strong>: Pro-rated refund for removed or unavailable features</li>
              <li><strong>Processing Interruptions</strong>: Pro-rated refund for service interruptions</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">No Refunds</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Completed Work</strong>: No refund for work that meets specifications</li>
              <li><strong>Change of Mind</strong>: No refund for buyer's remorse or change of requirements</li>
              <li><strong>Third-Party Issues</strong>: No refund for issues caused by third-party services</li>
              <li><strong>External Factors</strong>: No refund for delays caused by factors beyond our control</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. How to Request a Refund</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Refund Request Process</h3>
            <ol className="list-decimal list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Contact Support</strong>: Email refunds@goatvault.io with your request</li>
              <li><strong>Provide Details</strong>: Include project ID, payment confirmation, and reason for refund</li>
              <li><strong>Submit Evidence</strong>: Provide screenshots, files, or other evidence supporting your claim</li>
              <li><strong>Allow Review Time</strong>: Wait for our review (typically 5-7 business days)</li>
              <li><strong>Receive Decision</strong>: Get notification of approval or denial with explanation</li>
            </ol>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Required Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Account Email</strong>: Email address associated with your GOAT account</li>
              <li><strong>Project Details</strong>: Project name, ID, or description</li>
              <li><strong>Payment Information</strong>: Date, amount, and payment method used</li>
              <li><strong>Reason for Refund</strong>: Detailed explanation of why you're requesting a refund</li>
              <li><strong>Supporting Evidence</strong>: Screenshots, error messages, or examples of issues</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Refund Review Process</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Initial Review</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Automated Checks</strong>: System verifies refund eligibility automatically</li>
              <li><strong>Documentation Review</strong>: Support team reviews submitted evidence</li>
              <li><strong>Technical Assessment</strong>: Technical team evaluates technical claims</li>
              <li><strong>Timeline Verification</strong>: Project timelines and status are verified</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Quality Assessment</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Output Review</strong>: Delivered content is reviewed against specifications</li>
              <li><strong>Standards Compliance</strong>: Content is checked against professional standards</li>
              <li><strong>Technical Quality</strong>: Technical aspects (formatting, functionality) are evaluated</li>
              <li><strong>Customer Feedback</strong>: Your specific concerns are addressed</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Appeal Process</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Initial Decision</strong>: Most refund requests resolved at first review</li>
              <li><strong>Appeal Right</strong>: You can appeal denied refunds within 14 days</li>
              <li><strong>Escalation Review</strong>: Appeals reviewed by senior support management</li>
              <li><strong>Final Resolution</strong>: Appeal decisions are final</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Refund Methods and Timing</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Refund Methods</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Original Payment Method</strong>: Refunds issued to the same payment method used</li>
              <li><strong>Credit Card</strong>: 3-5 business days for credit card refunds</li>
              <li><strong>Bank Transfer</strong>: 5-10 business days for bank transfer refunds</li>
              <li><strong>Digital Wallets</strong>: 1-3 business days for wallet refunds</li>
              <li><strong>Cryptocurrency</strong>: 1-2 business days for crypto refunds</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Processing Timeframes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Automatic Refunds</strong>: Processed within 24-48 hours of approval</li>
              <li><strong>Review Required</strong>: Processed within 2-5 business days after approval</li>
              <li><strong>Banking Delays</strong>: Additional time may be needed for banking processing</li>
              <li><strong>Holiday Impact</strong>: Processing may be delayed during holidays</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Special Circumstances</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Technical Issues</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>System Outages</strong>: Pro-rated refunds for extended outages affecting your project</li>
              <li><strong>Data Loss</strong>: Full refund if we lose your data due to our systems</li>
              <li><strong>Security Breaches</strong>: Full refund if your data is compromised due to our security failures</li>
              <li><strong>Feature Bugs</strong>: Partial refunds for bugs affecting project completion</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Service Changes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Feature Removal</strong>: Pro-rated refund if promised features are removed</li>
              <li><strong>API Changes</strong>: Refunds for integrations broken by our API changes</li>
              <li><strong>Service Deprecation</strong>: Migration assistance and potential refunds for deprecated services</li>
              <li><strong>Performance Degradation</strong>: Refunds for significant performance issues</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">External Factors</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Force Majeure</strong>: Extended deadlines, no refunds for uncontrollable events</li>
              <li><strong>Third-Party Issues</strong>: No refunds for problems caused by third-party services</li>
              <li><strong>Regulatory Changes</strong>: Adjustments made for legal requirement changes</li>
              <li><strong>Market Conditions</strong>: No refunds for general market or economic conditions</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Refund Records and Reporting</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Refund Tracking</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Refund History</strong>: All refund requests tracked in your account</li>
              <li><strong>Status Updates</strong>: Regular updates on refund request status</li>
              <li><strong>Confirmation Emails</strong>: Email confirmations for all refund decisions</li>
              <li><strong>Transaction Records</strong>: Complete records of all refund transactions</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Reporting Requirements</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Tax Documentation</strong>: Refund amounts reported on tax documents if applicable</li>
              <li><strong>Regulatory Reporting</strong>: Refunds reported to regulatory authorities as required</li>
              <li><strong>Audit Trail</strong>: Complete audit trail maintained for all refund decisions</li>
              <li><strong>Data Retention</strong>: Refund records retained for legal and compliance purposes</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Dispute Resolution</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Refund Disputes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Internal Review</strong>: Denied refunds can be appealed internally</li>
              <li><strong>Mediation</strong>: Mediation available for unresolved refund disputes</li>
              <li><strong>Arbitration</strong>: Binding arbitration for disputes over $5,000</li>
              <li><strong>Court Action</strong>: Court action available as final resort</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Consumer Protection</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Consumer Rights</strong>: You retain all applicable consumer protection rights</li>
              <li><strong>Regulatory Agencies</strong>: You can escalate to relevant regulatory agencies</li>
              <li><strong>Small Claims</strong>: Small claims court available for disputes under threshold</li>
              <li><strong>Legal Aid</strong>: Access to legal aid services for valid claims</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Policy Updates</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this Refund Policy to reflect changes in our services or legal requirements. Updates will be:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Posted on our website with clear notice</li>
              <li>Sent via email to registered users</li>
              <li>Applied prospectively to maintain fairness</li>
              <li>Reviewed to ensure they don't reduce existing refund rights</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Contact Information</h2>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Refund Team</p>
              <p className="text-slate-300">Email: refunds@goatvault.io</p>
              <p className="text-slate-300 mt-2">Phone: 1-800-GOAT-REFUND (Available 9 AM - 6 PM EST)</p>
              <p className="text-slate-300 mt-2">For general inquiries: support@goatvault.io</p>
            </div>
            <p className="text-slate-300 mt-4 text-sm">
              <strong>Response Time</strong>: We aim to respond to all refund requests within 24 hours during business days.
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