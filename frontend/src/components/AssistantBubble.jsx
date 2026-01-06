import React, { useState, useEffect, useRef } from 'react';
import './AssistantBubble.css';

export default function AssistantBubble({ onToggle }) {
  const [isHovered, setIsHovered] = useState(false);
  const [pulse, setPulse] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);
  const speechSynthRef = useRef(null);

  useEffect(() => {
    // Voice recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Voice command:', transcript);

        if (
          transcript.toLowerCase().includes('caleon') ||
          transcript.toLowerCase().includes('assistant')
        ) {
          onToggle();
        }

        setIsListening(false);
      };

      recognitionRef.current.onend = () => setIsListening(false);
      recognitionRef.current.onerror = () => setIsListening(false);
    }

    // Speech synthesis
    if ('speechSynthesis' in window) {
      speechSynthRef.current = window.speechSynthesis;
    }

    // Idle pulse animation timer
    const interval = setInterval(() => {
      setPulse(true);
      setTimeout(() => setPulse(false), 2000);
    }, 8000);

    return () => {
      clearInterval(interval);
      if (recognitionRef.current) recognitionRef.current.stop();
      if (speechSynthRef.current) speechSynthRef.current.cancel();
    };
  }, [onToggle]);

  const startVoiceCommand = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const speak = (text) => {
    if (speechSynthRef.current) {
      setIsSpeaking(true);

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.volume = 0.8;

      utterance.onend = () => setIsSpeaking(false);

      speechSynthRef.current.speak(utterance);
    }
  };

  return (
    <div
      className={`assistant-bubble 
        ${isHovered ? 'hovered' : ''} 
        ${pulse ? 'pulse' : ''} 
        ${isListening ? 'listening' : ''} 
        ${isSpeaking ? 'speaking' : ''}
      `}
      onClick={onToggle}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >

      <div className="assistant-avatar">
        <div className="assistant-glow"></div>

        <div className="assistant-image">
          <div className="assistant-caleon">

            {/* ======== FIXED IMAGE PATH HERE ======== */}
            <img
              src="/caleonblue.jpg"
              alt="Caleon Prime"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'block';
              }}
            />

            {/* Fallback crest if image fails */}
            <div className="assistant-crest fallback">
              <div className="crest-inner"></div>
            </div>

          </div>
        </div>
      </div>

      {(isListening || isSpeaking) && (
        <div className="voice-indicator">
          <div className="voice-wave"></div>
          <div className="voice-wave"></div>
          <div className="voice-wave"></div>
        </div>
      )}

      {isHovered && (
        <div className="assistant-tooltip">
          <span>Click to talk to Caleon • Hold mic for voice</span>
        </div>
      )}

      {/* Microphone button */}
      <button
        className="voice-button"
        onClick={(e) => {
          e.stopPropagation();
          startVoiceCommand();
        }}
        title="Voice command"
      >
        🎤
      </button>
    </div>
  );
}
