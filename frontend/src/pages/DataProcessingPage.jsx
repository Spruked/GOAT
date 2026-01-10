import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Database } from 'lucide-react';

export default function DataProcessingPage() {
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
          <Database className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Data Processing Agreement</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Introduction</h2>
            <p className="text-slate-300 leading-relaxed">
              This Data Processing Agreement ("DPA") governs the processing of personal data by GOAT on behalf of our customers. GOAT is committed to compliance with global data protection regulations including GDPR, CCPA, and other applicable privacy laws.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>Key Principle</strong>: GOAT processes personal data only as necessary to provide content preparation services. We maintain strict controls to protect your data and ensure compliance with all applicable regulations.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Definitions</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Key Terms</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>"Personal Data"</strong>: Any information relating to an identified or identifiable natural person</li>
              <li><strong>"Processing"</strong>: Any operation performed on personal data, including collection, storage, use, disclosure, and deletion</li>
              <li><strong>"Data Subject"</strong>: The individual whose personal data is being processed</li>
              <li><strong>"Controller"</strong>: The entity that determines the purposes and means of processing personal data</li>
              <li><strong>"Processor"</strong>: The entity that processes personal data on behalf of the controller</li>
              <li><strong>"Sub-processor"</strong>: Third parties engaged by the processor to assist with processing</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Roles and Responsibilities</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>You as Controller</strong>: You determine how your content and any personal data within it is processed</li>
              <li><strong>GOAT as Processor</strong>: We process personal data only according to your instructions</li>
              <li><strong>Shared Responsibility</strong>: We both have obligations to protect data subject rights</li>
              <li><strong>Independent Compliance</strong>: Each party maintains its own compliance with applicable laws</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. Scope of Processing</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Processing Activities</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Content Preparation</strong>: Processing content to create professional deliverables</li>
              <li><strong>Format Conversion</strong>: Converting content between different formats</li>
              <li><strong>Quality Enhancement</strong>: Improving content structure and presentation</li>
              <li><strong>Technical Processing</strong>: Applying AI tools and algorithms to content</li>
              <li><strong>Storage and Backup</strong>: Secure storage during processing</li>
              <li><strong>Delivery</strong>: Secure transmission of processed content to you</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Categories</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Content Data</strong>: Text, images, audio, video, and other media content</li>
              <li><strong>Metadata</strong>: Technical metadata about content files</li>
              <li><strong>Account Data</strong>: Basic account information for service provision</li>
              <li><strong>Usage Data</strong>: Non-personal service usage statistics</li>
              <li><strong>Communication Data</strong>: Support communications (if containing personal data)</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Processing Purposes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Delivery</strong>: To provide content preparation services</li>
              <li><strong>Quality Assurance</strong>: To ensure output meets professional standards</li>
              <li><strong>Technical Support</strong>: To provide customer support</li>
              <li><strong>Security</strong>: To maintain system and data security</li>
              <li><strong>Legal Compliance</strong>: To comply with legal obligations</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. Data Protection Obligations</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">GOAT's Obligations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Lawful Processing</strong>: Process personal data only on your documented instructions</li>
              <li><strong>Purpose Limitation</strong>: Process data only for specified purposes</li>
              <li><strong>Data Minimization</strong>: Process only data necessary for service provision</li>
              <li><strong>Accuracy</strong>: Ensure personal data is accurate and up-to-date</li>
              <li><strong>Storage Limitation</strong>: Retain data only as long as necessary</li>
              <li><strong>Security</strong>: Implement appropriate technical and organizational measures</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Security Measures</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Encryption</strong>: Data encrypted in transit and at rest</li>
              <li><strong>Access Controls</strong>: Strict access controls and authentication</li>
              <li><strong>Network Security</strong>: Firewalls, intrusion detection, and monitoring</li>
              <li><strong>Physical Security</strong>: Secure data center facilities</li>
              <li><strong>Incident Response</strong>: 24/7 incident response capabilities</li>
              <li><strong>Regular Audits</strong>: Security audits and vulnerability assessments</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Data Subject Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Assisting with Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Right to Information</strong>: Provide information about processing activities</li>
              <li><strong>Right of Access</strong>: Assist you in providing data subjects access to their data</li>
              <li><strong>Right to Rectification</strong>: Assist with correcting inaccurate personal data</li>
              <li><strong>Right to Erasure</strong>: Assist with deleting personal data when required</li>
              <li><strong>Right to Restriction</strong>: Assist with restricting processing of personal data</li>
              <li><strong>Right to Portability</strong>: Assist with data portability requests</li>
              <li><strong>Right to Object</strong>: Assist with objections to processing</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Response Timeframes</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>GDPR Requests</strong>: Respond within 30 days (extendable by 60 days)</li>
              <li><strong>CCPA Requests</strong>: Respond within 45 days</li>
              <li><strong>Urgent Requests</strong>: Priority handling for urgent data protection requests</li>
              <li><strong>Complex Requests</strong>: Extended timeframes for complex or numerous requests</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Sub-Processing</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Authorized Sub-Processors</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Cloud Infrastructure</strong>: AWS, Google Cloud, or Microsoft Azure</li>
              <li><strong>AI Services</strong>: Approved AI processing providers</li>
              <li><strong>Security Services</strong>: Security monitoring and compliance services</li>
              <li><strong>Support Services</strong>: Customer support and helpdesk services</li>
              <li><strong>Analytics</strong>: Non-personal analytics and monitoring services</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Sub-Processor Requirements</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Written Agreement</strong>: Sub-processors bound by same data protection obligations</li>
              <li><strong>Security Standards</strong>: Meet same security and compliance standards</li>
              <li><strong>Location Restrictions</strong>: Data processing in approved jurisdictions</li>
              <li><strong>Audit Rights</strong>: Allow audits and inspections</li>
              <li><strong>Termination Rights</strong>: Ability to terminate for non-compliance</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Notification Requirements</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>New Sub-Processors</strong>: 30-day advance notice before engagement</li>
              <li><strong>Objection Period</strong>: 30-day window to object to new sub-processors</li>
              <li><strong>Termination Option</strong>: Right to terminate if you object to sub-processor</li>
              <li><strong>Current List</strong>: Maintain current list of all sub-processors</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. International Data Transfers</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Transfer Mechanisms</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Adequacy Decisions</strong>: Transfers to countries with adequacy decisions</li>
              <li><strong>Standard Contractual Clauses</strong>: EU Standard Contractual Clauses</li>
              <li><strong>Binding Corporate Rules</strong>: BCRs for intra-group transfers</li>
              <li><strong>Certification</strong>: Privacy Shield or similar certification schemes</li>
              <li><strong>Other Safeguards</strong>: Approved codes of conduct or certification mechanisms</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Location</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Primary Processing</strong>: Data processed in EU/EEA for European users</li>
              <li><strong>Backup Locations</strong>: Secure backup locations with appropriate safeguards</li>
              <li><strong>Regional Compliance</strong>: Processing locations chosen for regulatory compliance</li>
              <li><strong>Transfer Documentation</strong>: Documentation of all transfer mechanisms</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. Data Breach Notification</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Breach Response</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Immediate Notification</strong>: Notify you within 24 hours of becoming aware of breach</li>
              <li><strong>Investigation</strong>: Conduct thorough investigation of breach circumstances</li>
              <li><strong>Impact Assessment</strong>: Assess potential impact on data subjects and you</li>
              <li><strong>Regulatory Notification</strong>: Notify relevant supervisory authorities if required</li>
              <li><strong>Communication Plan</strong>: Assist with data subject notifications</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Breach Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Nature of Breach</strong>: Description of the personal data affected</li>
              <li><strong>Number of Individuals</strong>: Approximate number of data subjects affected</li>
              <li><strong>Potential Impact</strong>: Likely consequences of the breach</li>
              <li><strong>Measures Taken</strong>: Steps taken to mitigate the breach</li>
              <li><strong>Recommendations</strong>: Suggested actions to protect affected individuals</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Audit and Inspection</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Audit Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Annual Audits</strong>: Right to conduct audits once per year</li>
              <li><strong>Reasonable Notice</strong>: Provide reasonable notice before audits</li>
              <li><strong>Non-Disruptive</strong>: Audits conducted in non-disruptive manner</li>
              <li><strong>Confidentiality</strong>: Audit findings kept confidential</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Audit Methods</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Independent Auditor</strong>: Use qualified independent auditor</li>
              <li><strong>Certification Reports</strong>: Rely on SOC 2, ISO 27001 certifications</li>
              <li><strong>Self-Audits</strong>: Conduct internal audits with results shared</li>
              <li><strong>Regulatory Audits</strong>: Allow participation in regulatory audits</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Data Deletion and Return</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Deletion Obligations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>End of Processing</strong>: Delete all personal data at end of processing</li>
              <li><strong>Account Closure</strong>: Delete data upon account termination</li>
              <li><strong>Secure Deletion</strong>: Use secure deletion methods preventing recovery</li>
              <li><strong>Verification</strong>: Provide verification of complete deletion</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Return</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Export Rights</strong>: Provide data in portable format upon request</li>
              <li><strong>Return vs Delete</strong>: Return data or delete based on your instructions</li>
              <li><strong>Format Options</strong>: Return in commonly used, machine-readable formats</li>
              <li><strong>No Retention</strong>: Do not retain copies after return/deletion</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Liability and Indemnification</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Liability Limits</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Proportional Liability</strong>: Liability proportional to each party's responsibility</li>
              <li><strong>Direct Damages Only</strong>: Liability limited to direct damages</li>
              <li><strong>Reasonable Caps</strong>: Liability capped at reasonable amounts</li>
              <li><strong>Insurance Requirements</strong>: Maintain appropriate insurance coverage</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Indemnification</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Data Breach Indemnity</strong>: Indemnify for breaches caused by our negligence</li>
              <li><strong>Regulatory Fines</strong>: Indemnify for fines resulting from our non-compliance</li>
              <li><strong>Third-Party Claims</strong>: Indemnify for claims arising from our processing</li>
              <li><strong>Legal Costs</strong>: Cover reasonable legal costs and expenses</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Termination</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Termination Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Material Breach</strong>: Either party can terminate for material breach</li>
              <li><strong>Insolvency</strong>: Termination if either party becomes insolvent</li>
              <li><strong>Regulatory Changes</strong>: Termination if processing becomes illegal</li>
              <li><strong>Mutual Agreement</strong>: Termination by mutual written agreement</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Post-Termination Obligations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Data Deletion</strong>: Delete all personal data within 30 days</li>
              <li><strong>Return Data</strong>: Return all data in your possession</li>
              <li><strong>Certification</strong>: Provide certification of deletion</li>
              <li><strong>Sub-Processor Termination</strong>: Terminate all sub-processor agreements</li>
              <li><strong>Confidentiality</strong>: Maintain confidentiality of processing activities</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">13. Governing Law</h2>
            <p className="text-slate-300 leading-relaxed">
              This DPA shall be governed by and construed in accordance with the laws of the jurisdiction where GOAT is established, without regard to conflict of law principles. Any disputes arising from this DPA shall be resolved through binding arbitration in accordance with the rules of the applicable arbitration association.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              This governing law provision ensures consistent interpretation and enforcement of data protection obligations across different jurisdictions.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">14. Contact Information</h2>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">GOAT Data Protection Officer</p>
              <p className="text-slate-300">Email: dpo@goatvault.io</p>
              <p className="text-slate-300 mt-2">Privacy Team: privacy@goatvault.io</p>
              <p className="text-slate-300 mt-2">Legal Department: legal@goatvault.io</p>
            </div>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">15. Updates to This Agreement</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this DPA to reflect changes in applicable data protection laws or our processing practices. Updates will be:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Communicated to you at least 30 days in advance</li>
              <li>Posted on our website with clear version history</li>
              <li>Applied prospectively to maintain legal compliance</li>
              <li>Reviewed to ensure they enhance rather than reduce protections</li>
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