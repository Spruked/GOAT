import { useState, useEffect } from 'react';

/**
 * Custom hook to manage product walkthrough state
 * @param {string} productId - The product identifier
 * @returns {Object} Walkthrough state and controls
 */
export function useProductWalkthrough(productId) {
  const [showWalkthrough, setShowWalkthrough] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isSkipped, setIsSkipped] = useState(false);

  useEffect(() => {
    if (!productId) return;

    // Check if user has completed this walkthrough
    const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
    if (completedWalkthroughs[productId]) {
      setIsCompleted(true);
      return;
    }

    // Check if user has skipped this walkthrough
    const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');
    if (skippedWalkthroughs[productId]) {
      setIsSkipped(true);
      return;
    }

    // Show walkthrough for first-time users
    setShowWalkthrough(true);
  }, [productId]);

  const completeWalkthrough = () => {
    setShowWalkthrough(false);
    setIsCompleted(true);
    const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
    completedWalkthroughs[productId] = true;
    localStorage.setItem('completedWalkthroughs', JSON.stringify(completedWalkthroughs));
  };

  const skipWalkthrough = () => {
    setShowWalkthrough(false);
    setIsSkipped(true);
    const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');
    skippedWalkthroughs[productId] = true;
    localStorage.setItem('skippedWalkthroughs', JSON.stringify(skippedWalkthroughs));
  };

  const resetWalkthrough = () => {
    setShowWalkthrough(true);
    setIsCompleted(false);
    setIsSkipped(false);
    const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
    delete completedWalkthroughs[productId];
    localStorage.setItem('completedWalkthroughs', JSON.stringify(completedWalkthroughs));

    const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');
    delete skippedWalkthroughs[productId];
    localStorage.setItem('skippedWalkthroughs', JSON.stringify(skippedWalkthroughs));
  };

  return {
    showWalkthrough,
    isCompleted,
    isSkipped,
    completeWalkthrough,
    skipWalkthrough,
    resetWalkthrough
  };
}

/**
 * Utility function to check walkthrough status for a product
 * @param {string} productId - The product identifier
 * @returns {Object} Status information
 */
export function getWalkthroughStatus(productId) {
  const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
  const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');

  return {
    isCompleted: !!completedWalkthroughs[productId],
    isSkipped: !!skippedWalkthroughs[productId],
    hasSeen: !!(completedWalkthroughs[productId] || skippedWalkthroughs[productId])
  };
}

/**
 * Utility function to reset all walkthroughs (useful for testing)
 */
export function resetAllWalkthroughs() {
  localStorage.removeItem('completedWalkthroughs');
  localStorage.removeItem('skippedWalkthroughs');
}