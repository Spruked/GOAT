// frontend/src/hooks/useCaliScripts.js
import { useState, useEffect, useCallback } from 'react';

/**
 * React hook for Caleon Scripted Response System (CALI Scripts)
 * Provides consistent, non-LLM responses across the GOAT frontend
 */
export function useCaliScripts() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Cache for script responses to avoid repeated API calls
  const [cache, setCache] = useState(new Map());

  /**
   * Get a scripted response from CALI Scripts
   * @param {string} category - Script category (e.g., 'greetings')
   * @param {string} entry - Specific entry key (e.g., 'welcome_dashboard')
   * @param {object} variables - Variables for substitution (e.g., {name: 'Bryan'})
   * @returns {Promise<string>} The scripted response
   */
  const getScript = useCallback(async (category, entry, variables = {}) => {
    const cacheKey = `${category}.${entry}.${JSON.stringify(variables)}`;

    // Check cache first
    if (cache.has(cacheKey)) {
      return cache.get(cacheKey);
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/cali-scripts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          category,
          entry,
          variables
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const script = data.script;

      // Cache the result
      setCache(prev => new Map(prev).set(cacheKey, script));

      return script;
    } catch (err) {
      const errorMessage = `Failed to load script: ${err.message}`;
      setError(errorMessage);
      console.error('CALI Scripts error:', err);
      return `[Script Error: ${category}.${entry}]`;
    } finally {
      setIsLoading(false);
    }
  }, [cache]);

  /**
   * Convenience methods for common categories
   */
  const greet = useCallback((entry, variables) =>
    getScript('greetings', entry, variables), [getScript]);

  const onboard = useCallback((entry, variables) =>
    getScript('onboarding', entry, variables), [getScript]);

  const navigate = useCallback((entry, variables) =>
    getScript('navigation', entry, variables), [getScript]);

  const showError = useCallback((entry, variables) =>
    getScript('errors', entry, variables), [getScript]);

  const confirm = useCallback((entry, variables) =>
    getScript('confirmations', entry, variables), [getScript]);

  const draft = useCallback((entry, variables) =>
    getScript('drafts', entry, variables), [getScript]);

  const tooltip = useCallback((entry, variables) =>
    getScript('tooltips', entry, variables), [getScript]);

  /**
   * Clear the cache (useful for development)
   */
  const clearCache = useCallback(() => {
    setCache(new Map());
  }, []);

  /**
   * Get available categories (for debugging)
   */
  const getCategories = useCallback(async () => {
    try {
      const response = await fetch('/api/cali-scripts/categories');
      if (!response.ok) throw new Error('Failed to fetch categories');
      const data = await response.json();
      return data.categories;
    } catch (err) {
      console.error('Failed to get categories:', err);
      return [];
    }
  }, []);

  return {
    // Core functionality
    getScript,
    isLoading,
    error,

    // Convenience methods
    greet,
    onboard,
    navigate,
    showError,
    confirm,
    draft,
    tooltip,

    // Utilities
    clearCache,
    getCategories
  };
}

/**
 * Hook for Caleon generative responses (UCM pipeline)
 * For dynamic AI responses, not scripted ones
 */
export function useCaleonGenerative() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Send a message to Caleon via UCM pipeline
   * @param {string} message - User message
   * @param {object} context - Additional context
   * @returns {Promise<string>} Caleon's response
   */
  const sendToCaleon = useCallback(async (message, context = {}) => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('/api/caleon/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          context,
          timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data.response;
    } catch (err) {
      const errorMessage = `Caleon generation failed: ${err.message}`;
      setError(errorMessage);
      console.error('Caleon generative error:', err);
      return 'I apologize, but I am currently unable to respond. Please try again in a moment.';
    } finally {
      setIsGenerating(false);
    }
  }, []);

  /**
   * Stream Caleon's response (for real-time UI updates)
   * @param {string} message - User message
   * @param {function} onChunk - Callback for each chunk received
   * @param {object} context - Additional context
   */
  const streamFromCaleon = useCallback(async (message, onChunk, context = {}) => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('/api/caleon/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          context,
          timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              onChunk(data.chunk);
            } catch (e) {
              // Ignore malformed chunks
            }
          }
        }
      }
    } catch (err) {
      const errorMessage = `Caleon streaming failed: ${err.message}`;
      setError(errorMessage);
      console.error('Caleon streaming error:', err);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return {
    sendToCaleon,
    streamFromCaleon,
    isGenerating,
    error
  };
}