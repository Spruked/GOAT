import { useState, useEffect, useRef, useContext, createContext } from 'react'
import { MessageCircle, X, Send, Bot, User, Mic, MicOff, Volume2, VolumeX, Eye, FileText, HelpCircle, Zap, Settings, Activity } from 'lucide-react'

// Create Caleon Context for sharing state across the app
export const CaleonContext = createContext()

export function CaleonProvider({ children }) {
  const [activePanel, setActivePanel] = useState('dashboard')
  const [activeBundle, setActiveBundle] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [recentActions, setRecentActions] = useState([])
  const [currentUser, setCurrentUser] = useState('user_demo')

  const addAction = (action) => {
    setRecentActions(prev => [action, ...prev.slice(0, 9)]) // Keep last 10 actions
  }

  return (
    <CaleonContext.Provider value={{
      activePanel,
      setActivePanel,
      activeBundle,
      setActiveBundle,
      selectedFile,
      setSelectedFile,
      recentActions,
      addAction,
      currentUser,
      setCurrentUser
    }}>
      {children}
    </CaleonContext.Provider>
  )
}

export function CaleonOverlay() {
  const [isOpen, setIsOpen] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'caleon',
      content: 'HOST online. How can I assist you today?',
      timestamp: new Date(),
      context: null
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  const messagesEndRef = useRef(null)
  const recognitionRef = useRef(null)
  const speechSynthRef = useRef(null)

  const caleonContext = useContext(CaleonContext)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize speech recognition and synthesis
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        setInputMessage(transcript)
        setIsListening(false)
        // Auto-send voice input
        setTimeout(() => handleSendMessage(transcript), 500)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }

      recognitionRef.current.onerror = () => {
        setIsListening(false)
      }
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      speechSynthRef.current = window.speechSynthesis
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
      if (speechSynthRef.current) {
        speechSynthRef.current.cancel()
      }
    }
  }, [])

  // Auto-messages based on context changes
  useEffect(() => {
    if (caleonContext?.activePanel && caleonContext.activePanel !== 'dashboard') {
      const contextMessage = {
        id: Date.now(),
        type: 'system',
        content: `👁️ I see you're in the ${caleonContext.activePanel} panel. I can help you with that!`,
        timestamp: new Date(),
        context: caleonContext.activePanel
      }
      setMessages(prev => [...prev, contextMessage])
      setUnreadCount(prev => prev + 1)
    }
  }, [caleonContext?.activePanel])

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true)
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      setIsListening(false)
      recognitionRef.current.stop()
    }
  }

  const speak = (text) => {
    if (speechSynthRef.current) {
      setIsSpeaking(true)
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 0.8

      utterance.onend = () => {
        setIsSpeaking(false)
      }

      speechSynthRef.current.speak(utterance)
    }
  }

  const handleSendMessage = async (message = inputMessage) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date(),
      context: caleonContext?.activePanel || 'general'
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)
    setUnreadCount(0)

    // Add to recent actions
    caleonContext?.addAction({
      type: 'caleon_query',
      content: message,
      panel: caleonContext?.activePanel,
      timestamp: new Date()
    })

    try {
      // Generate context-aware Caleon response
      const response = await generateCaleonResponse(message, caleonContext)
      const caleonResponse = {
        id: Date.now() + 1,
        type: 'caleon',
        content: response.text,
        timestamp: new Date(),
        context: response.context,
        actions: response.actions
      }

      setMessages(prev => [...prev, caleonResponse])

      // Speak response if voice is enabled
      if (isSpeaking) {
        speak(response.text)
      }

    } catch (error) {
      const errorResponse = {
        id: Date.now() + 1,
        type: 'caleon',
        content: 'I apologize, but I\'m having trouble connecting to the UCM right now. Please try again.',
        timestamp: new Date(),
        context: 'error'
      }
      setMessages(prev => [...prev, errorResponse])
    }

    setIsTyping(false)
  }

  const generateCaleonResponse = async (query, context) => {
    // Context-aware response generation
    const lowerQuery = query.toLowerCase()

    // Panel-specific responses
    if (context?.activePanel === 'vault' && lowerQuery.includes('vault')) {
      return {
        text: 'The Vault is your immutable knowledge storage system. Each glyph is cryptographically signed and stored with full provenance. Would you like me to help you create a new vault package or analyze existing ones?',
        context: 'vault_help',
        actions: ['create_vault', 'analyze_glyphs']
      }
    }

    if (context?.activePanel === 'learn' && (lowerQuery.includes('learn') || lowerQuery.includes('quiz'))) {
      return {
        text: 'I see you\'re in the content panel. The UCM has analyzed your progress and suggests focusing on foundational skills first. Would you like me to generate personalized content or recommend your next creation?',
        context: 'content_help',
        actions: ['generate_quiz', 'recommend_lesson']
      }
    }

    if (lowerQuery.includes('help') || lowerQuery.includes('wtf') || lowerQuery.includes('what')) {
      return {
        text: `You're currently in the ${context?.activePanel || 'dashboard'} panel. This is where you ${getPanelDescription(context?.activePanel)}. I can guide you through any workflow or answer questions about the GOAT system.`,
        context: 'help',
        actions: ['guide_workflow', 'explain_panel']
      }
    }

    if (lowerQuery.includes('file') || lowerQuery.includes('bundle')) {
      const bundleInfo = context?.activeBundle ? `You're working with the "${context.activeBundle}" bundle. ` : ''
      return {
        text: `${bundleInfo}I can help you analyze files, create bundles, or manage your knowledge assets. What would you like to do with your files?`,
        context: 'file_help',
        actions: ['analyze_file', 'create_bundle', 'upload_vault']
      }
    }

    // General responses
    const responses = [
      'I\'m here to help you navigate the GOAT system. The UCM is analyzing your request...',
      'Based on your current context, I recommend checking the knowledge graph for connections.',
      'The vault system ensures your content achievements are permanently stored and verifiable.',
      'I can guide you through any workflow in the GOAT system. What would you like to accomplish?',
      'The UCM cognition engine is processing your query with full context awareness.',
      'I\'m monitoring your progress across all panels. You\'re doing great work!',
      'Would you like me to summarize what you\'re currently looking at, or help with a specific task?'
    ]

    return {
      text: responses[Math.floor(Math.random() * responses.length)],
      context: 'general',
      actions: ['summarize', 'guide', 'analyze']
    }
  }

  const getPanelDescription = (panel) => {
    const descriptions = {
      'dashboard': 'main GOAT dashboard - your central hub for all activities',
      'collect': 'collect and ingest NFTs from various sources like IPFS and blockchain',
      'learn': 'engage with adaptive content creation powered by UCM cognition',
      'vault': 'manage your immutable knowledge vault with cryptographic proofs',
      'vault-forge': 'create multi-tier vault packages for permanent storage',
      'profile': 'view your content progress and achievements'
    }
    return descriptions[panel] || 'this section of the GOAT system'
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded)
    setIsOpen(true)
  }

  return (
    <>
      {/* Floating Caleon Crest */}
      <div className="fixed bottom-6 right-6 z-50">
        <div className="relative">
          <button
            onClick={toggleExpanded}
            className="bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 hover:from-purple-700 hover:via-blue-700 hover:to-cyan-700 text-white p-4 rounded-full shadow-2xl transition-all duration-300 hover:scale-110 border-2 border-cyan-400/30"
          >
            <div className="relative">
              <Bot size={24} className="animate-pulse" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
            </div>
          </button>

          {/* Notification Badge */}
          {unreadCount > 0 && (
            <div className="absolute -top-3 -right-3 bg-red-500 text-white text-xs rounded-full w-7 h-7 flex items-center justify-center animate-bounce font-bold border-2 border-slate-900">
              {unreadCount > 9 ? '9+' : unreadCount}
            </div>
          )}

          {/* Status Indicator */}
          <div className="absolute -bottom-1 -left-1 w-4 h-4 bg-green-400 rounded-full border-2 border-slate-900 animate-pulse"></div>
        </div>

        {/* Quick Actions Menu */}
        {isExpanded && !isOpen && (
          <div className="absolute bottom-16 right-0 bg-slate-800 rounded-lg shadow-2xl border border-slate-700 p-3 min-w-[200px]">
            <div className="text-xs text-slate-400 mb-2 font-semibold">QUICK ACTIONS</div>
            <div className="space-y-2">
              <button
                onClick={() => {
                  setIsOpen(true)
                  setInputMessage('Help me understand what I\'m looking at')
                }}
                className="w-full text-left p-2 rounded hover:bg-slate-700 transition-colors flex items-center gap-2 text-sm"
              >
                <Eye size={16} />
                Explain Current Panel
              </button>
              <button
                onClick={() => {
                  setIsOpen(true)
                  setInputMessage('Guide me through this workflow')
                }}
                className="w-full text-left p-2 rounded hover:bg-slate-700 transition-colors flex items-center gap-2 text-sm"
              >
                <HelpCircle size={16} />
                Step-by-Step Guide
              </button>
              <button
                onClick={() => {
                  setIsOpen(true)
                  setInputMessage('Analyze my recent files')
                }}
                className="w-full text-left p-2 rounded hover:bg-slate-700 transition-colors flex items-center gap-2 text-sm"
              >
                <FileText size={16} />
                Analyze Files
              </button>
              <button
                onClick={startListening}
                className={`w-full text-left p-2 rounded transition-colors flex items-center gap-2 text-sm ${
                  isListening ? 'bg-red-600 text-white' : 'hover:bg-slate-700'
                }`}
              >
                <Mic size={16} />
                Voice Command
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Caleon Panel */}
      {isOpen && (
        <div className={`fixed bottom-24 right-6 bg-slate-800 rounded-lg shadow-2xl border border-slate-700 z-40 transition-all duration-300 ${
          isExpanded ? 'w-[500px] h-[600px]' : 'w-96 h-[500px]'
        } flex flex-col`}>
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 p-4 rounded-t-lg border-b border-cyan-500/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Bot size={24} className="text-white" />
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                </div>
                <div>
                  <h3 className="text-white font-bold text-lg">Caleon</h3>
                  <p className="text-cyan-100 text-sm">AI Guardian • UCM Connected</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsSpeaking(!isSpeaking)}
                  className={`p-2 rounded transition-colors ${
                    isSpeaking ? 'bg-cyan-600 text-white' : 'hover:bg-slate-700 text-slate-300'
                  }`}
                  title={isSpeaking ? 'Voice responses enabled' : 'Enable voice responses'}
                >
                  {isSpeaking ? <Volume2 size={16} /> : <VolumeX size={16} />}
                </button>
                <button
                  onClick={toggleExpanded}
                  className="p-2 rounded hover:bg-slate-700 text-slate-300 transition-colors"
                  title={isExpanded ? 'Collapse panel' : 'Expand panel'}
                >
                  <Zap size={16} />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 rounded hover:bg-slate-700 text-slate-300 transition-colors"
                >
                  <X size={16} />
                </button>
              </div>
            </div>

            {/* Context Display */}
            <div className="mt-3 bg-slate-900/50 rounded p-2">
              <div className="text-xs text-slate-400 mb-1">CURRENT CONTEXT</div>
              <div className="text-sm text-cyan-100">
                Panel: <span className="font-semibold">{caleonContext?.activePanel || 'Dashboard'}</span>
                {caleonContext?.activeBundle && (
                  <> • Bundle: <span className="font-semibold">{caleonContext.activeBundle}</span></>
                )}
                {caleonContext?.selectedFile && (
                  <> • File: <span className="font-semibold">{caleonContext.selectedFile}</span></>
                )}
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.type !== 'user' && (
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    {message.type === 'caleon' ? <Bot size={16} className="text-white" /> :
                     message.type === 'ucm' ? <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div> :
                     <div className="w-3 h-3 bg-blue-400 rounded-full"></div>}
                  </div>
                )}

                <div
                  className={`max-w-[80%] p-3 rounded-lg shadow-sm ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : message.type === 'ucm'
                      ? 'bg-green-900/50 border border-green-500/30 text-green-100'
                      : message.type === 'caleon'
                      ? 'bg-gradient-to-r from-purple-900/50 to-cyan-900/50 border border-cyan-500/30 text-cyan-100'
                      : 'bg-slate-700 text-slate-100'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                  <div className="flex items-center justify-between mt-2">
                    <p className="text-xs opacity-70">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                    {message.context && (
                      <span className="text-xs bg-slate-800/50 px-2 py-1 rounded">
                        {message.context}
                      </span>
                    )}
                  </div>
                  {message.actions && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {message.actions.map((action, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSendMessage(action.replace('_', ' '))}
                          className="text-xs bg-cyan-600/30 hover:bg-cyan-600/50 px-2 py-1 rounded transition-colors"
                        >
                          {action.replace('_', ' ')}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {message.type === 'user' && (
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <User size={16} className="text-white" />
                  </div>
                )}
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-full flex items-center justify-center">
                  <Bot size={16} className="text-white" />
                </div>
                <div className="bg-slate-700 p-3 rounded-lg">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-slate-700">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask Caleon anything..."
                className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors"
                disabled={isTyping}
              />
              <button
                onClick={isListening ? stopListening : startListening}
                className={`p-2 rounded-lg transition-colors ${
                  isListening ? 'bg-red-600 text-white animate-pulse' : 'bg-slate-600 hover:bg-slate-500 text-slate-300'
                }`}
                title={isListening ? 'Stop listening' : 'Start voice input'}
              >
                {isListening ? <MicOff size={20} /> : <Mic size={20} />}
              </button>
              <button
                onClick={() => handleSendMessage()}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 disabled:from-slate-600 disabled:to-slate-600 text-white p-2 rounded-lg transition-colors"
              >
                <Send size={20} />
              </button>
            </div>
            <div className="flex items-center justify-between mt-2 text-xs text-slate-400">
              <span>UCM Status: <span className="text-green-400">Connected</span></span>
              <span>Voice: <span className={isSpeaking ? 'text-green-400' : 'text-slate-500'}>
                {isSpeaking ? 'Enabled' : 'Disabled'}
              </span></span>
            </div>
          </div>
        </div>
      )}
    </>
  )
}