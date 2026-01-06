import React from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Shield,
  Zap,
  Users,
  Database,
  GraduationCap,
  FileText,
  Cpu,
  Globe,
  Lock,
  CheckCircle,
  ArrowRight,
  Mic,
  FolderOpen
} from 'lucide-react';

export default function MenuPage() {
  const offerings = [
    {
      icon: <Mic className="w-8 h-8" />,
      title: "Podcast Engine",
      description: "Transform your knowledge into legacies using the original podcast generator architecture. COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE.",
      features: [
        "AI-powered content structuring",
        "VisiData integration for data analysis",
        "Caleon-guided creation process",
        "Multiple output formats (books, courses, masterclasses)",
        "Automatic vault archiving",
        "Minting partner integration"
      ],
      featured: true,
      route: "/podcast"
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: "Book Creation Studio",
      description: "Transform your expertise and life story into comprehensive, publishable books with AI-guided structuring and enhancement.",
      features: [
        "AI-powered content organization",
        "Chapter and section structuring",
        "Narrative flow optimization",
        "Multi-format export (PDF, EPUB, etc.)",
        "Professional formatting and layout"
      ],
      route: "/book-builder"
    },
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: "Masterclass Builder",
      description: "Create immersive masterclass experiences that capture your unique methodology and teaching style.",
      features: [
        "Video and audio integration",
        "Interactive exercises and worksheets",
        "Q&A session structuring",
        "Progress tracking for students",
        "Monetization-ready packaging"
      ]
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: "Course Development Platform",
      description: "Build structured online courses with modules, assessments, and certification pathways.",
      features: [
        "Modular course design",
        "Automated assessment generation",
        "Progress certificates",
        "Multi-media content support",
        "Learning analytics and insights"
      ]
    },
    {
      icon: <Database className="w-8 h-8" />,
      title: "Knowledge Archives",
      description: "Preserve your complete body of work in organized, searchable archives with advanced metadata.",
      features: [
        "Comprehensive content indexing",
        "Cross-referenced knowledge linking",
        "Version history and evolution tracking",
        "Advanced search and discovery",
        "Export to multiple formats"
      ]
    },
    {
      icon: <FolderOpen className="w-8 h-8" />,
      title: "File Organizer",
      description: "Automatically organize and classify your files into structured folders with ZIP download for easy project management.",
      features: [
        "Automatic file classification by type",
        "Custom folder structure creation",
        "ZIP archive generation",
        "Bulk file upload and processing",
        "Organized download packages",
        "Project-ready file structures"
      ],
      route: "/organizer"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Framework Engineering",
      description: "Develop and document your unique frameworks, methodologies, and philosophical systems.",
      features: [
        "Visual framework mapping",
        "Step-by-step implementation guides",
        "Case study integration",
        "Framework validation tools",
        "Publication-ready documentation"
      ]
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Booklet & Guide Creator",
      description: "Craft focused booklets, guides, and quick-reference materials for specific topics or audiences.",
      features: [
        "Rapid content prototyping",
        "Target audience customization",
        "Quick publication cycles",
        "A/B testing capabilities",
        "Distribution optimization"
      ]
    },
    {
      icon: <Lock className="w-8 h-8" />,
      title: "Authorship NFTs",
      description: "Mint permanent proof of your authorship and ownership through CertSig and TrueMark minting engines.",
      features: [
        "Blockchain-verified authorship",
        "Timestamped creation records",
        "Immutable ownership proof",
        "Royalty and licensing tracking",
        "Decentralized preservation"
      ]
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: "Vault Artifacts",
      description: "Create and store vault artifacts - digital artifacts that represent milestones in your creative journey.",
      features: [
        "Artifact versioning and evolution",
        "Milestone documentation",
        "Creative process archiving",
        "Artifact networking and linking",
        "Permanent vault storage"
      ]
    },
    {
      icon: <Cpu className="w-8 h-8" />,
      title: "Caleon-Guided Creation",
      description: "Work with Caleon, your AI creation companion, to structure, enhance, and perfect your masterpiece.",
      features: [
        "Step-by-step guidance",
        "Content analysis and suggestions",
        "Style and voice refinement",
        "Creative block resolution",
        "Quality assurance checks"
      ]
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Publishing & Monetization",
      description: "Tools and integrations for publishing, selling, and licensing your created works worldwide.",
      features: [
        "Multi-platform publishing",
        "Licensing agreement generation",
        "Royalty tracking and payments",
        "Audience building tools",
        "Marketing and promotion support"
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <div className="relative overflow-hidden bg-gradient-to-r from-cyan-500/10 to-purple-500/10">
        <div className="max-w-7xl mx-auto px-4 py-16">
          <div className="text-center space-y-6">
            <div className="w-24 h-24 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full flex items-center justify-center shadow-2xl">
              <BookOpen className="w-12 h-12 text-white" />
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
              GOAT Offerings
            </h1>
            <p className="text-2xl text-slate-300 max-w-3xl mx-auto">
              Everything you need to create, preserve, and share knowledge in the decentralized education revolution.
            </p>
          </div>
        </div>
      </div>

      {/* Offerings Grid */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {offerings.map((offering, index) => (
            <div
              key={index}
              className={`bg-slate-800/50 backdrop-blur-sm border rounded-xl p-6 hover:bg-slate-800/70 hover:border-slate-600/50 transition-all duration-300 group cursor-pointer ${
                offering.featured ? 'border-purple-500/50 bg-gradient-to-r from-purple-900/20 to-cyan-900/20' : 'border-slate-700/50'
              }`}
              onClick={() => offering.route && (window.location.href = offering.route)}
            >
              <div className="flex items-center space-x-4 mb-4">
                <div className={`p-3 rounded-lg text-white group-hover:scale-110 transition-transform ${
                  offering.featured ? 'bg-gradient-to-r from-purple-500 to-cyan-500' : 'bg-gradient-to-r from-cyan-500 to-purple-500'
                }`}>
                  {offering.icon}
                </div>
                <div className="flex-1">
                  <h3 className={`text-xl font-bold group-hover:text-cyan-200 transition-colors ${
                    offering.featured ? 'text-purple-300' : 'text-cyan-300'
                  }`}>
                    {offering.title}
                    {offering.featured && <span className="ml-2 text-xs bg-purple-600 px-2 py-1 rounded-full">FEATURED</span>}
                  </h3>
                </div>
              </div>

              <p className="text-slate-400 mb-4 leading-relaxed">
                {offering.description}
              </p>

              <ul className="space-y-2 mb-4">
                {offering.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start space-x-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                    <span className="text-slate-300">{feature}</span>
                  </li>
                ))}
              </ul>

              {offering.route && (
                <div className="flex items-center justify-end text-cyan-400 group-hover:text-cyan-300 transition-colors">
                  <span className="text-sm font-medium">Get Started</span>
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action */}
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold text-white mb-6">
          Ready to Transform Education?
        </h2>
        <p className="text-xl text-slate-400 mb-8">
          Join the decentralized knowledge revolution and start building your eternal legacy of learning.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-8 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <span>Get Started</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/data"
            className="border border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200"
          >
            Data Explorer
          </Link>
        </div>
      </div>
    </div>
  );
}