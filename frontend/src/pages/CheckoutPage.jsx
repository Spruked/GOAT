import React, { useState } from 'react';
import { Lock, CreditCard, Shield, Sparkles, ChevronRight } from 'lucide-react';

export default function CheckoutPage() {
  const [isProcessing, setIsProcessing] = useState(false);

  // Real cart from context or props — using same items as cart page
  const orderItems = [
    { id: 1, name: "Eternal Knowledge Artifact", price: 99.0, quantity: 1 },
    { id: 2, name: "Voice of the Ancestors", price: 79.0, quantity: 1 },
    { id: 3, name: "Lifetime Vault Guardian", price: 299.0, quantity: 1, badge: "Most Eternal" },
  ];

  const subtotal = orderItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const eternalBonus = orderItems.length >= 3 ? 50 : 0;
  const total = subtotal - eternalBonus;

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsProcessing(true);
    // Simulate payment processing
    setTimeout(() => {
      setTimeout(() => {
        alert("Payment successful! Your legacy is now eternal.");
        window.location.href = "/success";
      }, 3000);
    });
  };

  return (
    <div className="min-h-screen bg-black text-cyan-100">
      {/* Header */}
      <div className="bg-gradient-to-b from-cyan-950/30 via-black to-black pt-16 pb-10 border-b border-cyan-900/40">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <h1 className="text-6xl font-light tracking-wider mb-4 flex items-center justify-center gap-6">
            <Lock className="w-12 h-12 text-cyan-400" />
            Secure Eternal Checkout
            <Lock className="w-12 h-12 text-cyan-400" />
          </h1>
          <p className="text-2xl text-cyan-400 font-light">
            Your legacy is about to become immortal.
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-12 grid lg:grid-cols-3 gap-12">
        {/* Payment Form */}
        <div className="lg:col-span-2">
          <div className="bg-gradient-to-b from-cyan-950/20 to-black rounded-3xl border border-cyan-700/50 p-10 backdrop-blur-xl">
            <h2 className="text-4xl font-light mb-10 flex items-center gap-4">
              <CreditCard className="w-8 h-8 text-cyan-400" />
              Payment Details
            </h2>

            <form onSubmit={handleSubmit} className="space-y-8">
              <div>
                <label className="block text-cyan-300 text-lg mb-3">Name on Card</label>
                <input
                  type="text"
                  required
                  placeholder="John Doe"
                  className="w-full px-6 py-5 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 transition"
                />
              </div>

              <div>
                <label className="block text-cyan-300 text-lg mb-3">Card Number</label>
                <div className="relative">
                  <input
                    type="text"
                    required
                    placeholder="1234 5678 9012 3456"
                    maxLength="19"
                    className="w-full px-6 py-5 pl-16 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 transition"
                  />
                  <CreditCard className="absolute left-5 top-5 w-7 h-7 text-cyan-500" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-cyan-300 text-lg mb-3">Expiry Date</label>
                  <input
                    type="text"
                    required
                    placeholder="MM/YY"
                    className="w-full px-6 py-5 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 transition"
                  />
                </div>
                <div>
                  <label className="block text-cyan-300 text-lg mb-3">CVC</label>
                  <input
                    type="text"
                    required
                    placeholder="123"
                    maxLength="4"
                    className="w-full px-6 py-5 bg-cyan-950/40 border border-cyan-700/60 rounded-2xl text-xl text-cyan-100 placeholder-cyan-600 focus:outline-none focus:border-cyan-400 transition"
                  />
                </div>
              </div>

              <div className="pt-8 border-t border-cyan-800/50">
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="w-full py-7 bg-gradient-to-r from-cyan-600 via-cyan-500 to-amber-600 
                             rounded-3xl text-3xl font-light shadow-2xl shadow-cyan-600/40
                             hover:brightness-110 disabled:opacity-70 disabled:cursor-not-allowed
                             transition-all duration-500 flex items-center justify-center gap-5 group"
                >
                  {isProcessing ? (
                    <>
                      <div className="w-8 h-8 border-4 border-cyan-300 border-t-transparent rounded-full animate-spin" />
                      Securing Your Legacy...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-8 h-8 group-hover:animate-pulse" />
                      Complete Eternal Purchase
                      <ChevronRight className="w-8 h-8 group-hover:translate-x-2 transition" />
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Trust badges */}
          <div className="mt-10 flex flex-wrap justify-center gap-8 text-cyan-500">
            <div className="flex items-center gap-3">
              <Shield className="w-6 h-6" />
              <span>256-bit AES Encryption</span>
            </div>
            <div className="flex items-center gap-3">
              <Lock className="w-6 h-6" />
              <span>No Data Ever Stored</span>
            </div>
            <div className="flex items-center gap-3">
              <Sparkles className="w-6 h-6" />
              <span>30-Day Eternal Guarantee</span>
            </div>
          </div>
        </div>

        {/* Order Summary Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-8 bg-gradient-to-b from-cyan-950/40 to-black rounded-3xl border-2 border-cyan-600/60 p-10 backdrop-blur-xl">
            <h2 className="text-4xl font-light text-center mb-10 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-amber-400">
              Your Eternal Legacy
            </h2>

            <div className="space-y-6 mb-10">
              {orderItems.map(item => (
                <div key={item.id} className="flex justify-between items-start">
                  <div>
                    <div className="text-xl font-light">{item.name}</div>
                    {item.badge && (
                      <div className="text-amber-400 text-sm mt-1 font-medium">{item.badge}</div>
                    )}
                    <div className="text-cyan-500 text-sm">×{item.quantity}</div>
                  </div>
                  <div className="text-2xl font-light text-amber-400">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-cyan-700/50 pt-6 space-y-4">
              <div className="flex justify-between text-xl">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              {eternalBonus > 0 && (
                <div className="flex justify-between text-amber-400 text-xl font-medium">
                  <span>Eternal Bonus</span>
                  <span>-${eternalBonus.toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between text-3xl font-light pt-6 border-t border-cyan-600/50">
                <span>Total</span>
                <span className="text-amber-400 font-bold text-4xl">
                  ${total.toFixed(2)}
                </span>
              </div>
            </div>

            <p className="text-center text-cyan-400 italic mt-10 text-lg leading-relaxed">
              “One payment.  
              A thousand years of memory.”
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}