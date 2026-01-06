// frontend/src/components/EnhancedAssistantBubble.jsx
import React, { useState, useEffect, useRef } from 'react';
import { useCaliScripts, useCaleonGenerative } from '../hooks/useCaliScripts';
import './AssistantBubble.css';

export default function EnhancedAssistantBubble({ onToggle }) {
  const [isHovered, setIsHovered] = useState(false);
  const [pulse, setPulse] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const recognitionRef = useRef(null);
  const speechSynthRef = useRef(null);

  // CALI Scripts for consistent responses
  const {
    greet,
    confirm,
    showError,
    tooltip,
    isLoading: caliLoading
  } = useCaliScripts();

  // Caleon generative for dynamic AI responses
  const {
    sendToCaleon,
    streamFromCaleon,
    isGenerating
  } = useCaleonGenerative();

  useEffect(() => {
    // Voice recognition setup
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Voice command:', transcript);
        setIsListening(false);

        // Process voice command
        await handleUserMessage(transcript, 'voice');
      };

      recognitionRef.current.onend = () => setIsListening(false);
      recognitionRef.current.onerror = () => setIsListening(false);
    }

    // Speech synthesis setup
    if ('speechSynthesis' in window) {
      speechSynthRef.current = window.speechSynthesis;
    }

    // Idle pulse animation
    const interval = setInterval(() => {
      setPulse(true);
      setTimeout(() => setPulse(false), 2000);
    }, 8000);

    return () => clearInterval(interval);
  }, []);

  // Handle user messages (text or voice)
  const handleUserMessage = async (message, source = 'text') => {
    // Add user message to conversation
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date(),
      source
    };
    setConversation(prev => [...prev, userMessage]);

    setIsTyping(true);
    setCurrentMessage('');

    try {
      // Determine if this needs AI response or scripted response
      const needsAI = shouldUseAI(message);

      if (needsAI) {
        // Use Caleon generative for complex queries
        await handleGenerativeResponse(message);
      } else {
        // Use CALI Scripts for consistent responses
        await handleScriptedResponse(message);
      }
    } catch (error) {
      console.error('Response error:', error);
      // Fallback to error script
      const errorResponse = await showError('unknown_error');
      addCaleonMessage(errorResponse);
    } finally {
      setIsTyping(false);
    }
  };

  // Determine if message needs AI or can use scripts
  const shouldUseAI = (message) => {
    const aiTriggers = [
      'help', 'how', 'what', 'why', 'explain', 'create', 'build',
      'draft', 'write', 'generate', 'analyze', 'review', 'suggest'
    ];

    const lowerMessage = message.toLowerCase();
    return aiTriggers.some(trigger => lowerMessage.includes(trigger));
  };

  // Handle scripted responses using CALI Scripts
  const handleScriptedResponse = async (message) => {
    const lowerMessage = message.toLowerCase();

    let response;
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      response = await greet('first_time');
    } else if (lowerMessage.includes('save') || lowerMessage.includes('done')) {
      response = await confirm('saved');
    } else if (lowerMessage.includes('error') || lowerMessage.includes('problem')) {
      response = await showError('unknown_error');
    } else if (lowerMessage.includes('help')) {
      response = await tooltip('help_button');
    } else {
      // Default greeting
      response = await greet('welcome_back');
    }

    addCaleonMessage(response);
  };

  // Handle generative responses using Caleon UCM
  const handleGenerativeResponse = async (message) => {
    // Use streaming for real-time feel
    await streamFromCaleon(
      message,
      (chunk) => {
        setCurrentMessage(prev => prev + chunk);
      },
      {
        conversation_history: conversation.slice(-5), // Last 5 messages
        interface: 'bubble_assistant'
      }
    );

    // Add completed message to conversation
    addCaleonMessage(currentMessage);
    setCurrentMessage('');
  };

  // Add Caleon message to conversation
  const addCaleonMessage = (content) => {
    const caleonMessage = {
      id: Date.now() + 1,
      type: 'caleon',
      content,
      timestamp: new Date(),
      isScripted: !isGenerating // True if from CALI Scripts, false if generative
    };
    setConversation(prev => [...prev, caleonMessage]);
  };

  // Voice activation
  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  // Text input handler
  const handleTextSubmit = async (text) => {
    if (text.trim()) {
      await handleUserMessage(text, 'text');
    }
  };

  // Speak response (optional)
  const speakResponse = (text) => {
    if (speechSynthRef.current && isSpeaking) {
      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthRef.current.speak(utterance);
    }
  };

  return (
    <div className="assistant-bubble-container">
      {/* Main Bubble */}
      <div
        className={`assistant-bubble ${isHovered ? 'hovered' : ''} ${pulse ? 'pulse' : ''}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={onToggle}
      >
        {/* Caleon Avatar */}
        <div className="caleon-avatar">
          <img src="/caleonblue.jpg" alt="Caleon" />
          {isTyping && <div className="typing-indicator">...</div>}
        </div>

        {/* Status Indicators */}
        <div className="status-indicators">
          {isListening && <div className="status listening">🎤</div>}
          {isGenerating && <div className="status generating">⚡</div>}
          {caliLoading && <div className="status scripted">📝</div>}
        </div>

        {/* Voice Activation Button */}
        <button
          className={`voice-button ${isListening ? 'active' : ''}`}
          onClick={(e) => {
            e.stopPropagation();
            startListening();
          }}
          disabled={isListening}
        >
          🎤
        </button>
      </div>

      {/* Conversation Preview (when expanded) */}
      {conversation.length > 0 && (
        <div className="conversation-preview">
          <div className="last-message">
            {conversation[conversation.length - 1]?.content?.slice(0, 50)}...
          </div>
          {currentMessage && (
            <div className="current-typing">{currentMessage}</div>
          )}
        </div>
      )}

      {/* Quick Actions */}
      <div className="quick-actions">
        <button onClick={() => handleTextSubmit("Help me get started")}>
          🚀 Quick Start
        </button>
        <button onClick={() => handleTextSubmit("What's new?")}>
          ✨ What's New
        </button>
        <button onClick={() => handleTextSubmit("Show me drafts")}>
          📝 Draft Status
        </button>
      </div>
    </div>
  );
}