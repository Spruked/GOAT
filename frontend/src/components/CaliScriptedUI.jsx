// frontend/src/components/CaliScriptedUI.jsx
import React, { useState, useEffect } from 'react';
import { useCaliScripts } from '../hooks/useCaliScripts';

/**
 * Example component showing how to use CALI Scripts throughout the UI
 * for consistent Caleon messaging across all components
 */
export default function CaliScriptedUI() {
  const {
    greet,
    onboard,
    navigate,
    showError,
    confirm,
    draft,
    tooltip,
    isLoading
  } = useCaliScripts();

  const [messages, setMessages] = useState({});
  const [userName, setUserName] = useState('Bryan');

  // Load all scripted messages on component mount
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const [
          welcomeMsg,
          onboardingMsg,
          navMsg,
          errorMsg,
          confirmMsg,
          draftMsg,
          tooltipMsg
        ] = await Promise.all([
          greet('welcome_dashboard', { name: userName }),
          onboard('start', { name: userName }),
          navigate('to_builder'),
          showError('network_error'),
          confirm('saved'),
          draft('done'),
          tooltip('dashboard_overview')
        ]);

        setMessages({
          welcome: welcomeMsg,
          onboarding: onboardingMsg,
          navigation: navMsg,
          error: errorMsg,
          confirmation: confirmMsg,
          draft: draftMsg,
          tooltip: tooltipMsg
        });
      } catch (error) {
        console.error('Failed to load CALI messages:', error);
      }
    };

    loadMessages();
  }, [userName, greet, onboard, navigate, showError, confirm, draft, tooltip]);

  return (
    <div className="cali-scripted-ui">
      <h1>CALI Scripts Integration Demo</h1>

      {/* Welcome Section */}
      <section className="welcome-section">
        <h2>Dashboard Welcome</h2>
        <div className="message-box welcome">
          {isLoading ? 'Loading...' : messages.welcome}
        </div>
        <input
          type="text"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          placeholder="Enter your name"
        />
      </section>

      {/* Onboarding Flow */}
      <section className="onboarding-section">
        <h2>Onboarding Messages</h2>
        <div className="message-box onboarding">
          {isLoading ? 'Loading...' : messages.onboarding}
        </div>
      </section>

      {/* Navigation */}
      <section className="navigation-section">
        <h2>Navigation Messages</h2>
        <div className="message-box navigation">
          {isLoading ? 'Loading...' : messages.navigation}
        </div>
      </section>

      {/* Error Handling */}
      <section className="error-section">
        <h2>Error Messages</h2>
        <div className="message-box error">
          {isLoading ? 'Loading...' : messages.error}
        </div>
      </section>

      {/* Confirmations */}
      <section className="confirmation-section">
        <h2>Confirmation Messages</h2>
        <div className="message-box confirmation">
          {isLoading ? 'Loading...' : messages.confirmation}
        </div>
      </section>

      {/* Draft Engine */}
      <section className="draft-section">
        <h2>Draft Engine Messages</h2>
        <div className="message-box draft">
          {isLoading ? 'Loading...' : messages.draft}
        </div>
      </section>

      {/* Tooltips */}
      <section className="tooltip-section">
        <h2>Tooltip Messages</h2>
        <div className="message-box tooltip">
          {isLoading ? 'Loading...' : messages.tooltip}
        </div>
      </section>

      {/* Interactive Demo */}
      <section className="interactive-demo">
        <h2>Interactive Demo</h2>
        <p>Try these actions to see CALI Scripts in action:</p>

        <div className="action-buttons">
          <button onClick={() => alert(messages.welcome)}>
            Show Welcome
          </button>
          <button onClick={() => alert(messages.error)}>
            Show Error
          </button>
          <button onClick={() => alert(messages.confirmation)}>
            Show Confirmation
          </button>
          <button onClick={() => alert(messages.draft)}>
            Show Draft Status
          </button>
        </div>
      </section>

      <style jsx>{`
        .cali-scripted-ui {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        section {
          margin-bottom: 30px;
          padding: 20px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
        }

        h2 {
          margin-top: 0;
          color: #2c3e50;
          border-bottom: 2px solid #3498db;
          padding-bottom: 10px;
        }

        .message-box {
          padding: 15px;
          margin: 10px 0;
          border-radius: 6px;
          font-style: italic;
          line-height: 1.5;
        }

        .welcome { background: #e8f4fd; border-left: 4px solid #3498db; }
        .onboarding { background: #f0f9e8; border-left: 4px solid #27ae60; }
        .navigation { background: #fdf2e9; border-left: 4px solid #e67e22; }
        .error { background: #fdeaea; border-left: 4px solid #e74c3c; }
        .confirmation { background: #e8f8f5; border-left: 4px solid #16a085; }
        .draft { background: #f4ecf7; border-left: 4px solid #9b59b6; }
        .tooltip { background: #fef5e7; border-left: 4px solid #f39c12; }

        input {
          padding: 8px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          margin-top: 10px;
        }

        .action-buttons {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
          margin-top: 15px;
        }

        button {
          padding: 10px 15px;
          background: #3498db;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: background 0.3s;
        }

        button:hover {
          background: #2980b9;
        }
      `}</style>
    </div>
  );
}