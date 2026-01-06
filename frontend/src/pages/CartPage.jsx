import React, { useState } from 'react';
import { Trash2, Plus, Minus, Lock, Sparkles } from 'lucide-react';

export default function CartPage() {
  const [items, setItems] = useState([
    {
      id: 1,
      name: "Eternal Knowledge Artifact",
      description: "Your memories forged into a permanent book + audiobook + NFT",
      price: 99.0,
      quantity: 1,
    },
    {
      id: 2,
      name: "Voice of the Ancestors",
      description: "30-second voice clone → full narrated legacy in their voice",
      price: 79.0,
      quantity: 1,
    },
    {
      id: 3,
      name: "Lifetime Vault Guardian",
      description: "Unlimited projects • offline • encrypted forever",
      price: 299.0,
      quantity: 1,
      badge: "Most Eternal",
    },
  ]);

  const updateQuantity = (id, delta) => {
    setItems(prev =>
      prev
        .map(item =>
          item.id === id
            ? { ...item, quantity: Math.max(1, item.quantity + delta) }
            : item
        )
        .filter(item => item.quantity > 0)
    );
  };

  const removeItem = (id) => {
    setItems(prev => prev.filter(item => item.id !== id));
  };

  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const eternalBonus = items.length >= 3 ? 50 : 0;
  const total = subtotal - eternalBonus;

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center px-6">
        <div className="text-center">
          <div className="text-cyan-800 text-9xl mb-8 opacity-20 font-light">Vault Empty</div>
          <p className="text-cyan-400 text-3xl font-light mb-12">
            Your cart is waiting for something eternal.
          </p>
          <a href="/" className="inline-block px-12 py-6 bg-cyan-600/20 border border-cyan-500 rounded-2xl text-cyan-100 text-xl hover:bg-cyan-600/30 transition">
            Return to Vault
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-cyan-100">
      {/* Header */}
      <div className="bg-gradient-to-b from-cyan-950/20 via-black to-black pt-20 pb-12 border-b border-cyan-900/30">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <h1 className="text-6xl font-light tracking-wider mb-4">Your Eternal Order</h1>
          <p className="text-2xl text-cyan-400 font-light">
            These artifacts will outlive empires.
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-12 grid lg:grid-cols-3 gap-12">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-8">
          {items.map(item => (
            <div
              key={item.id}
              className="relative bg-gradient-to-r from-cyan-950/20 via-black to-cyan-950/10 rounded-2xl border border-cyan-800/40 p-8 backdrop-blur-xl hover:border-cyan-500/60 transition-all duration-500"
            >
              {item.badge && (
                <div className="absolute -top-4 left-8 px-4 py-1 bg-gradient-to-r from-amber-600 to-yellow-600 rounded-full text-sm font-bold uppercase tracking-wider">
                  {item.badge}
                </div>
              )}

              <div className="flex gap-8 items-start">
                <div className="w-32 h-32 bg-gradient-to-br from-cyan-900/40 to-black rounded-xl border border-cyan-700/50 flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-12 h-12 text-cyan-400" />
                </div>

                <div className="flex-1">
                  <h3 className="text-2xl font-light mb-3">{item.name}</h3>
                  <p className="text-cyan-400 text-lg leading-relaxed opacity-90">
                    {item.description}
                  </p>

                  <div className="flex items-center gap-6 mt-8">
                    <div className="flex items-center gap-4 bg-cyan-950/40 rounded-xl px-5 py-3">
                      <button onClick={() => updateQuantity(item.id, -1)} className="text-cyan-400 hover:text-white transition">
                        <Minus className="w-5 h-5" />
                      </button>
                      <span className="text-xl w-12 text-center font-mono">{item.quantity}</span>
                      <button onClick={() => updateQuantity(item.id, 1)} className="text-cyan-400 hover:text-white transition">
                        <Plus className="w-5 h-5" />
                      </button>
                    </div>

                    <button onClick={() => removeItem(item.id)} className="text-red-400/70 hover:text-red-400 transition">
                      <Trash2 className="w-6 h-6" />
                    </button>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-3xl font-light text-amber-400">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                  {item.quantity > 1 && (
                    <div className="text-cyan-500 text-sm mt-1">
                      ${item.price.toFixed(2)} each
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="lg:col-span-1">
          <div className="sticky top-8 bg-gradient-to-b from-cyan-950/30 to-black rounded-2xl border border-cyan-700/50 p-8 backdrop-blur-xl">
            <h2 className="text-3xl font-light text-center mb-8">Order Summary</h2>

            <div className="space-y-4 mb-8">
              <div className="flex justify-between text-lg">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              {eternalBonus > 0 && (
                <div className="flex justify-between text-amber-400 font-medium">
                  <span>Eternal Bundle Bonus</span>
                  <span>-${eternalBonus.toFixed(2)}</span>
                </div>
              )}
              <div className="border-t border-cyan-800/50 pt-6">
                <div className="flex justify-between text-3xl font-light">
                  <span>Total</span>
                  <span className="text-amber-400 font-bold">${total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            <button className="w-full py-6 bg-gradient-to-r from-cyan-600 via-cyan-500 to-amber-600 rounded-2xl text-2xl font-light hover:brightness-110 transition-all duration-500 shadow-2xl shadow-cyan-500/30 flex items-center justify-center gap-4 group">
              <Lock className="w-7 h-7 group-hover:animate-pulse" />
              Secure Checkout
            </button>

            <p className="text-center text-cyan-500 text-sm mt-6 opacity-80">
              256-bit encrypted • Nothing ever leaves your vault
            </p>

            <p className="text-center text-cyan-400 italic mt-10 text-lg">
              “I paid once. My great-grandchildren will listen forever.”
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}+999