import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen, Headphones, Plus, Check, X, DollarSign,
  FileText, Type, Shield, Clock, Archive, Zap,
  Calculator, Star, ArrowRight
} from 'lucide-react';

export default function PricingPage() {
  const [selectedPackage, setSelectedPackage] = useState('print');
  const [pageCount, setPageCount] = useState(200);
  const [selectedAddons, setSelectedAddons] = useState([]);

  const toggleAddon = (addonId) => {
    setSelectedAddons(prev =>
      prev.includes(addonId)
        ? prev.filter(id => id !== addonId)
        : [...prev, addonId]
    );
  };

  const calculateTotal = () => {
    let total = 0;

    // Base package
    if (selectedPackage === 'print') {
      total += 74;
      if (pageCount > 200) {
        total += (pageCount - 200) * 0.30;
      }
    } else if (selectedPackage === 'bundle') {
      total += 199.99;
    }

    // Add-ons
    const addonPrices = {
      structural: 49.88,
      typography: 55,
      validation: 65,
      complex: 39,
      priority: 49,
      archival: 29
    };

    selectedAddons.forEach(addon => {
      total += addonPrices[addon] || 0;
    });

    return total;
  };

  const packages = {
    print: {
      name: "Print-Type Book Preparation",
      subtitle: "Professional preparation for physical books",
      price: 74,
      icon: BookOpen,
      description: "Focused on structure, layout, typography, and print-safe output for novels, memoirs, keepsakes, proof copies, or archival editions.",
      includes: [
        "Manuscript intake & normalization",
        "Chapter and section structuring",
        "Professional interior layout",
        "Print-safe margins, trim, and spacing",
        "Font hierarchy and readability optimization",
        "Export-ready print PDF",
        "Compatible with POD or local printers"
      ],
      overage: {
        rate: 0.30,
        unit: "page",
        base: 200
      }
    },
    bundle: {
      name: "Book + Audiobook Bundle",
      subtitle: "Complete print and audio preparation",
      price: 199.99,
      icon: Headphones,
      description: "Includes complete base audiobook preparation alongside professional print formatting.",
      includes: [
        "Full manuscript audio prep",
        "Chapter segmentation for audio",
        "Narration-ready script formatting",
        "Audio structure aligned to print",
        "Base audiobook build",
        "All print package features",
        "Audiobook add-ons available separately"
      ]
    }
  };

  const addons = [
    {
      id: 'structural',
      name: 'Structural Review',
      price: 49.88,
      icon: FileText,
      description: 'Chapter flow review, section consistency check, structural clarity notes (non-editorial), and prep guidance for future revisions.',
      category: 'content'
    },
    {
      id: 'typography',
      name: 'Typography Enhancement',
      price: 55,
      icon: Type,
      description: 'Refined font pairing, improved spacing and hierarchy, and enhanced long-form readability optimization.',
      category: 'design'
    },
    {
      id: 'validation',
      name: 'Final Print Validation',
      price: 65,
      icon: Shield,
      description: 'Printer compatibility check, POD compliance verification, and final export integrity review.',
      category: 'quality'
    },
    {
      id: 'complex',
      name: 'Complex Manuscript Handling',
      price: 39,
      icon: Calculator,
      description: 'Applied only when needed for tables, charts, footnotes, poetry, academic, or technical formatting.',
      category: 'specialized',
      note: 'Only applied when needed'
    },
    {
      id: 'priority',
      name: 'Priority Queue (Rush Handling)',
      price: 49,
      icon: Clock,
      description: 'Front-of-line processing, faster turnaround, and priority support with no scope changes.',
      category: 'service'
    },
    {
      id: 'archival',
      name: 'Archival & Reuse Package',
      price: 29,
      icon: Archive,
      description: 'Organized final file set, reusable formats, and long-term archival clarity for future projects.',
      category: 'organization'
    }
  ];

  const notIncluded = [
    "Developmental editing",
    "Copyediting or proofreading",
    "Cover design",
    "ISBN registration",
    "Publishing or marketing"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <DollarSign className="w-12 h-12 text-cyan-400 mr-4" />
            <h1 className="text-4xl font-bold text-cyan-400">GOAT Product Catalog</h1>
          </div>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Professional content preparation services designed for creators who value quality,
            precision, and long-term value.
          </p>
          <div className="mt-6 bg-gradient-to-r from-cyan-600/20 to-purple-600/20 border border-cyan-500/30 rounded-lg p-4 inline-block">
            <p className="text-cyan-300 font-semibold">
              🚀 <strong>Bottom-line impact:</strong> $117–$156 of optional, high-margin revenue per motivated customer
            </p>
          </div>
        </div>

        {/* Package Selection */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {Object.entries(packages).map(([key, pkg]) => (
            <div
              key={key}
              onClick={() => setSelectedPackage(key)}
              className={`bg-slate-800/50 rounded-lg p-6 border-2 cursor-pointer transition-all ${
                selectedPackage === key
                  ? 'border-cyan-400 bg-slate-800/70'
                  : 'border-slate-700 hover:border-slate-600'
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <pkg.icon className="w-8 h-8 text-cyan-400 mr-3" />
                  <div>
                    <h3 className="text-xl font-bold text-cyan-300">{pkg.name}</h3>
                    <p className="text-slate-400 text-sm">{pkg.subtitle}</p>
                  </div>
                </div>
                {selectedPackage === key && (
                  <Check className="w-6 h-6 text-cyan-400" />
                )}
              </div>

              <p className="text-slate-300 mb-4">{pkg.description}</p>

              <div className="mb-4">
                <span className="text-3xl font-bold text-cyan-400">${pkg.price}</span>
                {pkg.overage && (
                  <span className="text-slate-400 text-sm ml-2">
                    (includes {pkg.overage.base} pages)
                  </span>
                )}
              </div>

              <ul className="space-y-2 text-sm text-slate-300">
                {pkg.includes.map((item, idx) => (
                  <li key={idx} className="flex items-start">
                    <Check className="w-4 h-4 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Page Calculator (for Print Package) */}
        {selectedPackage === 'print' && (
          <div className="bg-slate-800/50 rounded-lg p-6 mb-8 border border-slate-700">
            <h3 className="text-xl font-bold text-cyan-300 mb-4 flex items-center">
              <Calculator className="w-6 h-6 mr-2" />
              Page Count Calculator
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-slate-300 mb-2">Total Pages</label>
                <input
                  type="number"
                  value={pageCount}
                  onChange={(e) => setPageCount(Math.max(1, parseInt(e.target.value) || 200))}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white"
                  min="1"
                />
              </div>
              <div className="flex items-end">
                <div className="text-slate-300">
                  <p className="text-sm">Base: 200 pages included</p>
                  {pageCount > 200 && (
                    <p className="text-cyan-400 font-semibold">
                      Overage: +${((pageCount - 200) * 0.30).toFixed(2)} ({pageCount - 200} pages × $0.30)
                    </p>
                  )}
                  <p className="text-lg font-bold text-cyan-400 mt-2">
                    Total: ${(74 + Math.max(0, (pageCount - 200) * 0.30)).toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Add-Ons */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-center mb-8 text-cyan-300">Optional Add-Ons</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {addons.map((addon) => (
              <div
                key={addon.id}
                onClick={() => toggleAddon(addon.id)}
                className={`bg-slate-800/50 rounded-lg p-6 border-2 cursor-pointer transition-all ${
                  selectedAddons.includes(addon.id)
                    ? 'border-purple-400 bg-slate-800/70'
                    : 'border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <addon.icon className="w-6 h-6 text-purple-400 mr-3 flex-shrink-0" />
                  {selectedAddons.includes(addon.id) && (
                    <Check className="w-5 h-5 text-purple-400 flex-shrink-0" />
                  )}
                </div>

                <h4 className="font-bold text-purple-300 mb-2">{addon.name}</h4>
                <p className="text-slate-300 text-sm mb-3">{addon.description}</p>

                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-purple-400">${addon.price}</span>
                  {addon.note && (
                    <span className="text-xs text-slate-500">{addon.note}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Price Summary */}
        <div className="bg-gradient-to-r from-cyan-900/20 to-purple-900/20 rounded-lg p-8 mb-8 border border-cyan-500/30">
          <h2 className="text-2xl font-bold text-center mb-6 text-cyan-300">Price Summary</h2>

          <div className="max-w-2xl mx-auto">
            <div className="space-y-3 mb-6">
              <div className="flex justify-between items-center">
                <span className="text-slate-300">
                  {packages[selectedPackage].name}
                  {selectedPackage === 'print' && pageCount > 200 && ` (${pageCount} pages)`}
                </span>
                <span className="text-cyan-400 font-semibold">
                  ${selectedPackage === 'print'
                    ? (74 + Math.max(0, (pageCount - 200) * 0.30)).toFixed(2)
                    : packages[selectedPackage].price
                  }
                </span>
              </div>

              {selectedAddons.map(addonId => {
                const addon = addons.find(a => a.id === addonId);
                return (
                  <div key={addonId} className="flex justify-between items-center">
                    <span className="text-slate-300">{addon.name}</span>
                    <span className="text-purple-400 font-semibold">${addon.price}</span>
                  </div>
                );
              })}
            </div>

            <div className="border-t border-slate-600 pt-4">
              <div className="flex justify-between items-center text-xl font-bold">
                <span className="text-white">Total</span>
                <span className="text-cyan-400">${calculateTotal().toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* What's Not Included */}
        <div className="bg-slate-800/50 rounded-lg p-6 mb-8 border border-slate-700">
          <h3 className="text-xl font-bold text-red-300 mb-4 flex items-center">
            <X className="w-6 h-6 mr-2" />
            Not Included
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {notIncluded.map((item, idx) => (
              <div key={idx} className="flex items-center text-slate-300">
                <X className="w-4 h-4 text-red-400 mr-2 flex-shrink-0" />
                {item}
              </div>
            ))}
          </div>
          <p className="text-slate-400 text-sm mt-4">
            These services are available through our trusted partner network if needed.
          </p>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <Link
            to="/book-builder"
            className="inline-flex items-center bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-lg transition-all duration-200 text-lg"
          >
            Start Your Project
            <ArrowRight className="w-5 h-5 ml-2" />
          </Link>
          <p className="text-slate-400 mt-4">
            Ready to create something amazing? Let's prepare your content for success.
          </p>
        </div>

        {/* Footer Note */}
        <div className="mt-12 text-center text-slate-400 text-sm">
          <p>
            All prices are in USD and subject to our Terms of Service.
            Professional preparation services only - we do not provide publishing or distribution.
          </p>
        </div>
      </div>
    </div>
  );
}