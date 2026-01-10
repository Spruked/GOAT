import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Cookie } from 'lucide-react';

export default function CookiePolicyPage() {
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
          <Cookie className="w-12 h-12 text-cyan-400 mr-4" />
          <div>
            <h1 className="text-4xl font-bold text-cyan-400">Cookie Policy</h1>
            <p className="text-slate-400 mt-2">Last Updated: January 6, 2026</p>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-cyan max-w-none space-y-8">
          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">1. Introduction</h2>
            <p className="text-slate-300 leading-relaxed">
              This Cookie Policy explains how GOAT uses cookies and similar technologies on our website and services. We are committed to transparency about our use of cookies and respect your privacy choices.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              <strong>What are Cookies?</strong> Cookies are small text files that are stored on your device when you visit our website. They help us provide you with a better experience and allow certain features to work properly.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">2. Types of Cookies We Use</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Essential Cookies</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Authentication</strong>: Keep you logged in during your session</li>
              <li><strong>Security</strong>: Protect against security threats and fraud</li>
              <li><strong>Session Management</strong>: Remember your preferences during your visit</li>
              <li><strong>Load Balancing</strong>: Ensure website performance and availability</li>
            </ul>
            <p className="text-slate-300 mt-3 text-sm">
              <strong>Legal Basis</strong>: These cookies are necessary for the website to function and are set based on legitimate interest.
            </p>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Functional Cookies</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Language Preferences</strong>: Remember your language choice</li>
              <li><strong>Theme Settings</strong>: Save your display preferences</li>
              <li><strong>Form Data</strong>: Remember information you've entered in forms</li>
              <li><strong>Feature Preferences</strong>: Save your choices for optional features</li>
            </ul>
            <p className="text-slate-300 mt-3 text-sm">
              <strong>Legal Basis</strong>: Consent (you can withdraw consent at any time).
            </p>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Analytics Cookies</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Usage Statistics</strong>: Understand how visitors use our website</li>
              <li><strong>Performance Monitoring</strong>: Track website performance and errors</li>
              <li><strong>Conversion Tracking</strong>: Measure effectiveness of our services</li>
              <li><strong>A/B Testing</strong>: Test different versions of our website</li>
            </ul>
            <p className="text-slate-300 mt-3 text-sm">
              <strong>Legal Basis</strong>: Consent (you can withdraw consent at any time).
            </p>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Marketing Cookies</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Advertising</strong>: Show relevant advertisements</li>
              <li><strong>Social Media</strong>: Enable social media sharing features</li>
              <li><strong>Retargeting</strong>: Show relevant content based on your interests</li>
              <li><strong>Affiliate Tracking</strong>: Track referrals from partner websites</li>
            </ul>
            <p className="text-slate-300 mt-3 text-sm">
              <strong>Legal Basis</strong>: Consent (you can withdraw consent at any time).
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">3. Third-Party Cookies</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Analytics Providers</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Google Analytics</strong>: Website usage analytics and reporting</li>
              <li><strong>Mixpanel</strong>: User behavior and conversion tracking</li>
              <li><strong>Hotjar</strong>: Heatmaps and user session recordings</li>
              <li><strong>Amplitude</strong>: Product analytics and user insights</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Customer Support</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Intercom</strong>: Live chat and customer support features</li>
              <li><strong>ZenDesk</strong>: Help desk and ticketing system</li>
              <li><strong>Drift</strong>: Conversational marketing and support</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Payment Processing</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Stripe</strong>: Secure payment processing</li>
              <li><strong>PayPal</strong>: Payment processing and fraud prevention</li>
              <li><strong>Adyen</strong>: Global payment processing</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Content Delivery</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Cloudflare</strong>: Content delivery and security</li>
              <li><strong>Fastly</strong>: Content delivery network</li>
              <li><strong>Akamai</strong>: Global content delivery</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">4. Cookie Management</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Cookie Consent</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Consent Banner</strong>: Clear consent request when you first visit</li>
              <li><strong>Granular Control</strong>: Choose which types of cookies to accept</li>
              <li><strong>Easy Withdrawal</strong>: Change your preferences at any time</li>
              <li><strong>Consent Records</strong>: We keep records of your consent choices</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Managing Cookies</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Browser Settings</strong>: Control cookies through your browser preferences</li>
              <li><strong>Our Cookie Tool</strong>: Use our cookie preference center</li>
              <li><strong>Opt-out Links</strong>: Direct links to opt-out of third-party cookies</li>
              <li><strong>Do Not Track</strong>: Respect Do Not Track signals where supported</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Browser Instructions</h3>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold mb-2">Popular Browsers:</p>
              <ul className="text-slate-300 space-y-1 text-sm">
                <li>• Chrome: Settings → Privacy and security → Cookies and other site data</li>
                <li>• Firefox: Settings → Privacy & Security → Cookies and Site Data</li>
                <li>• Safari: Preferences → Privacy → Manage Website Data</li>
                <li>• Edge: Settings → Cookies and site permissions</li>
              </ul>
            </div>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">5. Data Collection and Use</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Information We Collect</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Device Information</strong>: Browser type, operating system, screen resolution</li>
              <li><strong>Usage Data</strong>: Pages visited, time spent, features used</li>
              <li><strong>Location Data</strong>: General location based on IP address</li>
              <li><strong>Referral Data</strong>: How you found our website</li>
              <li><strong>Interaction Data</strong>: Clicks, scrolls, form interactions</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">How We Use This Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Service Improvement</strong>: Enhance website functionality and user experience</li>
              <li><strong>Performance Monitoring</strong>: Identify and fix technical issues</li>
              <li><strong>Security</strong>: Detect and prevent security threats</li>
              <li><strong>Analytics</strong>: Understand user behavior and preferences</li>
              <li><strong>Personalization</strong>: Provide relevant content and recommendations</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">6. Data Retention</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Cookie Lifespans</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Session Cookies</strong>: Deleted when you close your browser</li>
              <li><strong>Persistent Cookies</strong>: Remain until deleted or expired (typically 30 days to 2 years)</li>
              <li><strong>Essential Cookies</strong>: May remain longer for security and functionality</li>
              <li><strong>Analytics Cookies</strong>: Typically expire after 26 months</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Data Deletion</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Automatic Deletion</strong>: Cookies expire based on their lifespan</li>
              <li><strong>Manual Deletion</strong>: You can delete cookies through browser settings</li>
              <li><strong>Account Deletion</strong>: Cookies associated with your account are deleted</li>
              <li><strong>Data Minimization</strong>: We retain only necessary data for our purposes</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">7. Your Rights</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Privacy Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Access</strong>: Request information about cookies and data we collect</li>
              <li><strong>Rectification</strong>: Correct inaccurate data associated with cookies</li>
              <li><strong>Erasure</strong>: Request deletion of data collected via cookies</li>
              <li><strong>Restriction</strong>: Limit how we process cookie data</li>
              <li><strong>Portability</strong>: Receive your data in a portable format</li>
              <li><strong>Objection</strong>: Object to processing of your data via cookies</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Cookie-Specific Rights</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Withdraw Consent</strong>: Change your cookie preferences at any time</li>
              <li><strong>Block Cookies</strong>: Use browser settings to block cookies</li>
              <li><strong>Opt-out</strong>: Use industry opt-out tools for advertising cookies</li>
              <li><strong>Do Not Track</strong>: Request that we not track your activity</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">8. International Transfers</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Data Transfer Safeguards</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Adequacy Decisions</strong>: Transfers to countries with EU adequacy status</li>
              <li><strong>Standard Contractual Clauses</strong>: EU-approved transfer mechanisms</li>
              <li><strong>Privacy Shield</strong>: For transfers to US-based providers</li>
              <li><strong>Binding Corporate Rules</strong>: Internal data transfer policies</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Third-Party Compliance</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Vendor Assessment</strong>: We evaluate third-party cookie providers</li>
              <li><strong>Contractual Protections</strong>: Require appropriate safeguards in contracts</li>
              <li><strong>Ongoing Monitoring</strong>: Monitor third-party compliance</li>
              <li><strong>Incident Response</strong>: Respond to data breaches involving cookies</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">9. Children's Privacy</h2>
            <p className="text-slate-300 leading-relaxed">
              Our services are not intended for children under 13 (or the applicable age in your jurisdiction). We do not knowingly collect personal information from children. If we become aware that we have collected personal information from a child, we will take steps to delete such information.
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              For cookie purposes, we recommend that parents and guardians monitor their children's internet usage and help them understand how to manage cookie preferences.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">10. Updates to This Policy</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this Cookie Policy to reflect changes in our practices or applicable laws. When we make material changes, we will:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li>Notify you via email or website notification</li>
              <li>Update the "Last Updated" date at the top of this policy</li>
              <li>Provide a summary of key changes</li>
              <li>Give you time to review and update your preferences</li>
            </ul>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">11. Contact Us</h2>
            <div className="mt-4 p-4 bg-slate-900/50 rounded-lg">
              <p className="text-cyan-400 font-semibold">Cookie and Privacy Questions</p>
              <p className="text-slate-300">Email: privacy@goatvault.io</p>
              <p className="text-slate-300 mt-2">Data Protection Officer: dpo@goatvault.io</p>
              <p className="text-slate-300 mt-2">Cookie Preference Center: Available in your account settings</p>
            </div>
            <p className="text-slate-300 mt-4 text-sm">
              <strong>Response Time</strong>: We aim to respond to privacy inquiries within 30 days.
            </p>
          </section>

          <section className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold text-cyan-300 mb-4">12. Additional Resources</h2>

            <h3 className="text-xl font-semibold text-cyan-400 mt-4 mb-3">Helpful Links</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>All About Cookies</strong>: ICO guide to cookies and online privacy</li>
              <li><strong>Your Online Choices</strong>: EU-wide opt-out tool for advertising cookies</li>
              <li><strong>Network Advertising Initiative</strong>: Opt-out of interest-based advertising</li>
              <li><strong>Digital Advertising Alliance</strong>: US opt-out tools for online advertising</li>
            </ul>

            <h3 className="text-xl font-semibold text-cyan-400 mt-6 mb-3">Browser Tools</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
              <li><strong>Chrome Extension</strong>: Cookie AutoDelete for automatic cookie management</li>
              <li><strong>Firefox Add-on</strong>: uBlock Origin for comprehensive cookie blocking</li>
              <li><strong>Safari Extension</strong>: Cookie for managing cookie preferences</li>
              <li><strong>Cross-browser</strong>: Privacy Badger for automatic tracker blocking</li>
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