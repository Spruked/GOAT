import React, { useState, useRef, useEffect } from 'react';
import { useCaleonPresence } from './useCaleonPresence';
import './AssistantPanel.css';

export default function AssistantPanel({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [voiceMetrics, setVoiceMetrics] = useState({
    recognitionTime: 0,
    synthesisTime: 0,
    accuracy: 0,
    responseTime: 0
  });
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const synthesisRef = useRef(null);

  const statusMessage = useCaleonPresence();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onstart = () => {
        setIsListening(true);
        const startTime = Date.now();
        setVoiceMetrics(prev => ({ ...prev, recognitionTime: startTime }));
      };

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const endTime = Date.now();
        const recognitionDuration = endTime - voiceMetrics.recognitionTime;
        
        setVoiceMetrics(prev => ({
          ...prev,
          recognitionTime: recognitionDuration,
          accuracy: transcript.length > 0 ? 1 : 0 // Simple accuracy measure
        }));

        setInputValue(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      synthesisRef.current = window.speechSynthesis;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthesisRef.current) {
        synthesisRef.current.cancel();
      }
    };
  }, []);

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    // Add typing indicator
    const typingIndicator = {
      id: Date.now() + 1,
      type: 'caleon',
      content: ' Caleon is processing...',
      timestamp: new Date(),
      isTyping: true
    };
    setMessages(prev => [...prev, typingIndicator]);

    const requestStartTime = Date.now();

    try {
      // Call actual UCM API
      const response = await fetch('/api/caleon/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'goat_dev_key' // Use dev key for now
        },
        body: JSON.stringify({
          message: inputValue,
          user_id: 'user_demo',
          context: {
            activePanel: 'dashboard', // This should come from context
            activeBundle: null,
            selectedFile: null
          }
        })
      });

      if (!response.ok) {
        throw new Error(`API call failed: ${response.status}`);
      }

      const data = await response.json();
      const responseEndTime = Date.now();
      const responseDuration = responseEndTime - requestStartTime;

      setVoiceMetrics(prev => ({
        ...prev,
        responseTime: responseDuration
      }));

      // Remove typing indicator
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      // Add actual UCM response
      const caleonResponse = {
        id: Date.now() + 2,
        type: 'caleon',
        content: data.response,
        timestamp: new Date(),
        context: data.context,
        ucm_status: data.ucm_status
      };

      setMessages(prev => [...prev, caleonResponse]);

      // Auto-speak response if in voice test mode
      if (activeTab === 'voice' && synthesisRef.current) {
        speakText(data.response);
      }

    } catch (error) {
      console.error('Caleon API error:', error);

      // Remove typing indicator
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      // Add error response
      const errorResponse = {
        id: Date.now() + 2,
        type: 'caleon',
        content: 'I apologize, but I\'m having trouble connecting to the UCM right now. Please try again.',
        timestamp: new Date(),
        context: { error: error.message }
      };
      setMessages(prev => [...prev, errorResponse]);
    }
  };

  const handleVoiceInput = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start();
    }
  };

  const speakText = (text) => {
    if (synthesisRef.current) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      utterance.rate = 0.9;
      utterance.pitch = 1;

      utterance.onstart = () => {
        setIsSpeaking(true);
        const startTime = Date.now();
        setVoiceMetrics(prev => ({ ...prev, synthesisTime: startTime }));
      };

      utterance.onend = () => {
        const endTime = Date.now();
        const synthesisDuration = endTime - voiceMetrics.synthesisTime;
        setVoiceMetrics(prev => ({
          ...prev,
          synthesisTime: synthesisDuration
        }));
        setIsSpeaking(false);
      };

      synthesisRef.current.speak(utterance);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderChatTab = () => (
    <>
      <div className="assistant-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`assistant-message ${message.type === 'user' ? 'user' : 'caleon'}`}
          >
            <div className="message-content">
              {message.isTyping ? (
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <span className="typing-text">{message.content}</span>
                </div>
              ) : (
                message.content
              )}
            </div>
            {!message.isTyping && (
              <div className="message-time">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="assistant-input-wrapper">
        <input
          className="assistant-input"
          placeholder="Ask Caleon anything..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          className="assistant-send"
          onClick={handleSend}
          disabled={!inputValue.trim()}
        >
          Send
        </button>
      </div>
    </>
  );

  const renderVoiceTestTab = () => (
    <div className="voice-test-tab">
      <div className="voice-controls">
        <button
          className={`voice-button ${isListening ? 'listening' : ''}`}
          onClick={handleVoiceInput}
          disabled={isListening}
        >
          {isListening ? '🎤 Listening...' : '🎤 Start Voice Input'}
        </button>
        <button
          className={`voice-button ${isSpeaking ? 'speaking' : ''}`}
          onClick={() => speakText("Hello! I'm Caleon Prime, your AI assistant. How can I help you today?")}
          disabled={isSpeaking}
        >
          {isSpeaking ? '🔊 Speaking...' : '🔊 Test Speech'}
        </button>
      </div>

      <div className="voice-transcript">
        <h4>Voice Transcript:</h4>
        <div className="transcript-display">
          {inputValue || 'Click "Start Voice Input" to begin...'}
        </div>
      </div>

      <div className="voice-metrics">
        <h4>Voice Metrics:</h4>
        <div className="metrics-grid">
          <div className="metric-item">
            <span className="metric-label">Recognition Time:</span>
            <span className="metric-value">{voiceMetrics.recognitionTime}ms</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Synthesis Time:</span>
            <span className="metric-value">{voiceMetrics.synthesisTime}ms</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Accuracy:</span>
            <span className="metric-value">{(voiceMetrics.accuracy * 100).toFixed(1)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Response Time:</span>
            <span className="metric-value">{voiceMetrics.responseTime}ms</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderMetricsTab = () => (
    <div className="metrics-tab">
      <h4>Performance Metrics</h4>
      <div className="metrics-summary">
        <div className="metric-card">
          <h5>Voice Recognition</h5>
          <div className="metric-value-large">{voiceMetrics.recognitionTime}ms</div>
          <div className="metric-description">Average recognition time</div>
        </div>
        <div className="metric-card">
          <h5>Speech Synthesis</h5>
          <div className="metric-value-large">{voiceMetrics.synthesisTime}ms</div>
          <div className="metric-description">Average synthesis time</div>
        </div>
        <div className="metric-card">
          <h5>API Response</h5>
          <div className="metric-value-large">{voiceMetrics.responseTime}ms</div>
          <div className="metric-description">Average UCM response time</div>
        </div>
        <div className="metric-card">
          <h5>Accuracy</h5>
          <div className="metric-value-large">{(voiceMetrics.accuracy * 100).toFixed(1)}%</div>
          <div className="metric-description">Voice recognition accuracy</div>
        </div>
      </div>

      <div className="metrics-actions">
        <button 
          className="metrics-button"
          onClick={() => setVoiceMetrics({ recognitionTime: 0, synthesisTime: 0, accuracy: 0, responseTime: 0 })}
        >
          Reset Metrics
        </button>
        <button 
          className="metrics-button"
          onClick={() => console.log('Exporting metrics...', voiceMetrics)}
        >
          Export Data
        </button>
      </div>
    </div>
  );

  return (
    <div className={`assistant-panel ${isOpen ? 'open' : ''}`}>
      <div className="assistant-header">
        <div className="assistant-header-content">
          <div className="assistant-avatar-small">
            <span className="assistant-initial-small">C</span>
          </div>
          <div className="assistant-title">
            <h2>Caleon Prime</h2>
            <span className="assistant-status">● {statusMessage}</span>
          </div>
        </div>
        <button className="assistant-close" onClick={onClose}>×</button>
      </div>

      <div className="assistant-tabs">
        <button 
          className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button 
          className={`tab-button ${activeTab === 'voice' ? 'active' : ''}`}
          onClick={() => setActiveTab('voice')}
        >
          🎤 Voice Test
        </button>
        <button 
          className={`tab-button ${activeTab === 'metrics' ? 'active' : ''}`}
          onClick={() => setActiveTab('metrics')}
        >
          📊 Metrics
        </button>
      </div>

      <div className="assistant-body">
        <div className="assistant-bg-image" />
        {activeTab === 'chat' && renderChatTab()}
        {activeTab === 'voice' && renderVoiceTestTab()}
        {activeTab === 'metrics' && renderMetricsTab()}
      </div>
    </div>
  );
}