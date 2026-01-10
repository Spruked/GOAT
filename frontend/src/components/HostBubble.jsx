
import React, { useState, useEffect, useRef } from 'react';
import { Brain, Zap, Target, TrendingUp } from 'lucide-react';
import { hostBubbleGreet, hostBubbleMessage } from '../utils/hostBubbleApi';


/**
 * @typedef {Object} HostBubbleProps
 * @property {any} user
 * @property {boolean} [isVisible]
 * @property {boolean} [onboardingMode]
 * @property {function} [onOnboardingComplete]
 */

/**
 * @typedef {Object} CognitiveSession
 * @property {string} session_id
 * @property {string} cognitive_state
 * @property {any} insights
 * @property {string} cali_response
 * @property {any} ucm_feedback
 */

/**
 * @param {HostBubbleProps} props
 */

export function HostBubble(props) {
  const { user, isVisible = true, onboardingMode = false, onOnboardingComplete } = props;
  const [persona, setPersona] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [onboardingState, setOnboardingState] = useState({
    step: 0,
    data: {},
    completed: false
  });
  const inputRef = useRef(null);

  // Greet on mount (or user change)
  useEffect(() => {
    if (user && user.id) {
      setIsLoading(true);

      if (onboardingMode) {
        // Start onboarding conversation
        setPersona({ name: 'Onboarding Assistant', tone_descriptor: 'helpful and guiding' });
        setConversation([{
          type: 'host',
          content: "Welcome to GOAT! I'm your personal assistant, here to help you get started. Let's begin by understanding what you'd like to create. What type of content are you interested in?\n\n1. 📚 A Book\n2. 🎓 A Course\n3. 🎤 A Masterclass\n4. 🤔 Something else\n\nJust tell me what interests you!",
          persona: { name: 'Onboarding Assistant' }
        }]);
        setOnboardingState({ step: 1, data: {}, completed: false });
        setIsLoading(false);
      } else {
        // Normal greeting
        hostBubbleGreet(user.id)
          .then((res) => {
            setPersona(res.persona);
            setConversation([{ type: 'host', content: res.greeting, persona: res.persona }]);
            setError(null);
          })
          .catch((e) => setError('Failed to greet: ' + e.message))
          .finally(() => setIsLoading(false));
      }
    }
  }, [user, onboardingMode]);

  // Send message to host bubble
  const sendMessage = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    const userMessage = input.trim();
    setConversation((prev) => [...prev, { type: 'user', content: userMessage }]);

    if (onboardingMode) {
      // Handle onboarding conversation
      const response = handleOnboardingMessage(userMessage);
      setTimeout(() => {
        setConversation((prev) => [...prev, {
          type: 'host',
          content: response.message,
          persona: { name: 'Onboarding Assistant' }
        }]);
        setIsLoading(false);

        if (response.completed) {
          setTimeout(() => {
            if (onOnboardingComplete) {
              onOnboardingComplete(onboardingState.data);
            }
          }, 2000);
        }
      }, 1000); // Simulate typing delay
    } else {
      // Normal host bubble message
      try {
        const res = await hostBubbleMessage(user.id, userMessage);
        setPersona(res.persona);
        setConversation((prev) => [...prev, { type: 'host', content: res.response, persona: res.persona }]);
        setError(null);
      } catch (e) {
        setError('Failed to send message: ' + e.message);
      } finally {
        setIsLoading(false);
      }
    }

    setInput('');
    inputRef.current?.focus();
  };

  // Handle onboarding conversation logic
  const handleOnboardingMessage = (message) => {
    const currentStep = onboardingState.step;
    const lowerMessage = message.toLowerCase();

    switch (currentStep) {
      case 1: // Goal selection
        if (lowerMessage.includes('book') || lowerMessage.includes('1') || lowerMessage.includes('📚')) {
          setOnboardingState(prev => ({
            ...prev,
            step: 2,
            data: { ...prev.data, goal: 'book' }
          }));
          return {
            message: "Great choice! 📚 Creating a book is perfect for sharing your knowledge in a structured, lasting format. Now, what type of content would you like your book to focus on?\n\n• Educational/Instructional\n• Memoir/Autobiography\n• Fiction/Storytelling\n• Professional/Business\n• Technical/How-to\n• Inspirational/Motivational\n\nOr tell me in your own words!"
          };
        } else if (lowerMessage.includes('course') || lowerMessage.includes('2') || lowerMessage.includes('🎓')) {
          setOnboardingState(prev => ({
            ...prev,
            step: 2,
            data: { ...prev.data, goal: 'course' }
          }));
          return {
            message: "Excellent! 🎓 Courses are fantastic for sharing knowledge and building communities. What subject would you like to create content about?\n\n• Business & Entrepreneurship\n• Technology & Programming\n• Health & Wellness\n• Creative Arts\n• Personal Development\n• Professional Skills\n\nWhat's your area of expertise?"
          };
        } else if (lowerMessage.includes('masterclass') || lowerMessage.includes('3') || lowerMessage.includes('🎤')) {
          setOnboardingState(prev => ({
            ...prev,
            step: 2,
            data: { ...prev.data, goal: 'masterclass' }
          }));
          return {
            message: "Perfect! 🎤 Masterclasses are ideal for deep dives into specialized topics. What unique skill or knowledge do you want to share?\n\n• Advanced Techniques\n• Industry Secrets\n• Creative Processes\n• Leadership & Strategy\n• Innovation & Trends\n\nWhat's your specialty?"
          };
        } else {
          // Handle custom responses
          setOnboardingState(prev => ({
            ...prev,
            step: 2,
            data: { ...prev.data, goal: 'custom', customGoal: message }
          }));
          return {
            message: `Interesting! "${message}" sounds like a unique project. Let's explore what type of content format would work best for this. Would you prefer:\n\n• 📖 A comprehensive book/guide\n• 🎥 A video course series\n• 🎙️ A podcast or audio program\n• 📱 An interactive online experience\n\nOr something else entirely?`
          };
        }

      case 2: // Content type or topic
        setOnboardingState(prev => ({
          ...prev,
          step: 3,
          data: { ...prev.data, contentType: message }
        }));
        return {
          message: "Awesome! Now, let's get specific. What's the main topic or theme you want to focus on? For example:\n\n• A specific skill you excel at\n• A problem you solve for others\n• A passion project you've been working on\n• An area where you have unique insights\n\nWhat's your topic?"
        };

      case 3: // Topic - final step
        setOnboardingState(prev => ({
          ...prev,
          step: 4,
          data: { ...prev.data, topic: message },
          completed: true
        }));
        return {
          message: `Perfect! 🎉 "${message}" is going to make an amazing ${onboardingState.data.goal}. \n\nI've got everything I need to set up your personalized GOAT experience. You're all set to start creating something incredible!\n\nRedirecting you to your dashboard now...`,
          completed: true
        };

      default:
        return {
          message: "Thanks for sharing that! I'm here to help you every step of the way. Let's get you started on your GOAT journey!"
        };
    }
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className={`${onboardingMode ? 'bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-200' : 'bg-white dark:bg-gray-800'} rounded-lg shadow-lg border ${onboardingMode ? 'border-indigo-200' : 'border-gray-200 dark:border-gray-700'} p-4 min-w-80 max-w-md`}>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-500" />
            <span className="font-semibold text-gray-900 dark:text-white">
              {onboardingMode ? 'Onboarding Assistant' : 'Host Assistant'}
            </span>
          </div>
          {onboardingMode && (
            <div className="flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-indigo-100 text-indigo-700">
              <Target className="w-4 h-4" />
              <span>Step {onboardingState.step}/3</span>
            </div>
          )}
          {persona && !onboardingMode && (
            <div className="flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-700">
              <Zap className="w-4 h-4" />
              <span className="capitalize">{persona.name || persona}</span>
            </div>
          )}
        </div>

        <div className="space-y-3">
          {/* Conversation */}
          <div className={`max-h-64 overflow-y-auto ${onboardingMode ? 'bg-indigo-50/50' : 'bg-gray-50 dark:bg-gray-700'} p-3 rounded text-sm`}>
            {conversation.map((msg, idx) => (
              <div key={idx} className={`mb-3 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block max-w-full p-2 rounded-lg ${
                  msg.type === 'user'
                    ? 'bg-indigo-500 text-white'
                    : onboardingMode
                      ? 'bg-white border border-indigo-200 text-gray-900'
                      : 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white'
                }`}>
                  {msg.type === 'user' ? (
                    <span className="font-medium">You: </span>
                  ) : (
                    <span className="font-medium text-indigo-600">
                      {onboardingMode ? 'Assistant: ' : (msg.persona?.name ? msg.persona.name + ': ' : 'Host: ')}
                    </span>
                  )}
                  <span className="whitespace-pre-line">{msg.content}</span>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="text-left">
                <div className={`inline-block p-2 rounded-lg ${onboardingMode ? 'bg-white border border-indigo-200' : 'bg-white dark:bg-gray-600'}`}>
                  <span className="font-medium text-indigo-600">Assistant: </span>
                  <span className="text-gray-400">typing...</span>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="flex gap-2 mt-2">
            <input
              ref={inputRef}
              type="text"
              className={`flex-1 px-3 py-2 rounded border ${
                onboardingMode
                  ? 'border-indigo-300 bg-white focus:border-indigo-500'
                  : 'border-gray-300 dark:bg-gray-900 dark:text-white'
              } focus:outline-none`}
              placeholder={
                onboardingMode
                  ? "Tell me about your project..."
                  : (persona ? `Message ${persona.name || persona}...` : 'Type a message...')
              }
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleInputKeyDown}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              className={`px-4 py-2 text-white text-sm rounded hover:opacity-90 disabled:opacity-50 ${
                onboardingMode ? 'bg-indigo-500 hover:bg-indigo-600' : 'bg-indigo-500 hover:bg-indigo-600'
              }`}
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? '...' : 'Send'}
            </button>
          </div>
          {error && <div className="text-xs text-red-500 mt-1">{error}</div>}
        </div>
      </div>
    </div>
  );
}