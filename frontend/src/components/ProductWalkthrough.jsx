import React, { useState, useEffect, useRef } from 'react';
import { Brain, X, ChevronRight, ChevronLeft, CheckCircle, SkipForward } from 'lucide-react';

/**
 * ProductWalkthrough Component
 * Provides guided first-time user experience for each GOAT product
 *
 * @param {Object} props
 * @param {string} props.productId - The product identifier (e.g., 'podcast', 'book', 'audiobook')
 * @param {string} props.productName - Display name of the product
 * @param {boolean} props.isVisible - Whether to show the walkthrough
 * @param {function} props.onComplete - Callback when walkthrough is completed
 * @param {function} props.onSkip - Callback when walkthrough is skipped
 */
export function ProductWalkthrough({ productId, productName, isVisible, onComplete, onSkip }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isSkipped, setIsSkipped] = useState(false);
  const walkthroughRef = useRef(null);

  // Check if user has already completed this walkthrough
  useEffect(() => {
    if (productId) {
      const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
      if (completedWalkthroughs[productId]) {
        setIsCompleted(true);
        if (onComplete) onComplete();
        return;
      }

      const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');
      if (skippedWalkthroughs[productId]) {
        setIsSkipped(true);
        if (onSkip) onSkip();
        return;
      }
    }
  }, [productId, onComplete, onSkip]);

  // Don't render if already completed or skipped
  if (isCompleted || isSkipped || !isVisible) {
    return null;
  }

  // Get walkthrough steps for this product
  const walkthroughSteps = getWalkthroughSteps(productId, productName);

  const nextStep = () => {
    if (currentStep < walkthroughSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      completeWalkthrough();
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const completeWalkthrough = () => {
    const completedWalkthroughs = JSON.parse(localStorage.getItem('completedWalkthroughs') || '{}');
    completedWalkthroughs[productId] = true;
    localStorage.setItem('completedWalkthroughs', JSON.stringify(completedWalkthroughs));
    setIsCompleted(true);
    if (onComplete) onComplete();
  };

  const skipWalkthrough = () => {
    const skippedWalkthroughs = JSON.parse(localStorage.getItem('skippedWalkthroughs') || '{}');
    skippedWalkthroughs[productId] = true;
    localStorage.setItem('skippedWalkthroughs', JSON.stringify(skippedWalkthroughs));
    setIsSkipped(true);
    if (onSkip) onSkip();
  };

  const currentStepData = walkthroughSteps[currentStep];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div
        ref={walkthroughRef}
        className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="w-8 h-8" />
              <div>
                <h2 className="text-xl font-bold">{productName} Walkthrough</h2>
                <p className="text-blue-100 text-sm">Step {currentStep + 1} of {walkthroughSteps.length}</p>
              </div>
            </div>
            <button
              onClick={skipWalkthrough}
              className="text-blue-200 hover:text-white transition-colors p-1"
              title="Skip walkthrough"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Progress Bar */}
          <div className="mt-4 bg-blue-500 bg-opacity-30 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / walkthroughSteps.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <div className="flex items-start gap-6">
            {/* Icon */}
            <div className="flex-shrink-0">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center">
                {currentStepData.icon}
              </div>
            </div>

            {/* Text Content */}
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-gray-900 mb-3">
                {currentStepData.title}
              </h3>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                {currentStepData.description}
              </p>

              {/* Additional content if provided */}
              {currentStepData.content && (
                <div className="bg-gray-50 rounded-lg p-4 mb-6">
                  {currentStepData.content}
                </div>
              )}

              {/* Tips */}
              {currentStepData.tips && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">💡 Pro Tips:</h4>
                  <ul className="text-blue-800 space-y-1">
                    {currentStepData.tips.map((tip, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="text-blue-600 mt-1">•</span>
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-8 py-4 flex items-center justify-between">
          <button
            onClick={skipWalkthrough}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <SkipForward className="w-4 h-4" />
            Skip for now
          </button>

          <div className="flex items-center gap-3">
            <button
              onClick={prevStep}
              disabled={currentStep === 0}
              className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
              Previous
            </button>

            <button
              onClick={nextStep}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {currentStep === walkthroughSteps.length - 1 ? (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Get Started
                </>
              ) : (
                <>
                  Next
                  <ChevronRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Walkthrough content for each product
function getWalkthroughSteps(productId, productName) {
  const walkthroughs = {
    podcast: [
      {
        title: "Welcome to Podcast Engine",
        description: "Create professional podcasts with multiple voices, sound effects, and intelligent editing. Let's get you set up for your first episode!",
        icon: <div className="text-3xl">🎤</div>,
        tips: [
          "Prepare your script or key points before recording",
          "Use a quiet environment for best audio quality",
          "Multiple voice synthesis creates natural conversations"
        ]
      },
      {
        title: "Choose Your Format",
        description: "Select how you want to create your podcast. You can start with a script, record live, or use our AI to help structure your content.",
        icon: <div className="text-3xl">📝</div>,
        content: (
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-white rounded border">
              <span className="text-2xl">📄</span>
              <div>
                <div className="font-medium">Script-based</div>
                <div className="text-sm text-gray-600">Write your script first, then generate audio</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white rounded border">
              <span className="text-2xl">🎙️</span>
              <div>
                <div className="font-medium">Live Recording</div>
                <div className="text-sm text-gray-600">Record directly with voice synthesis</div>
              </div>
            </div>
          </div>
        ),
        tips: [
          "Script-based podcasts give you more control over timing",
          "Live recording feels more natural and spontaneous"
        ]
      },
      {
        title: "Add Multiple Voices",
        description: "Make your podcast engaging with different voice personalities. Each voice can have its own tone, style, and characteristics.",
        icon: <div className="text-3xl">👥</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">Available voice options include:</p>
            <ul className="space-y-1 ml-4">
              <li>• Professional Narrator - Clear, authoritative tone</li>
              <li>• Conversational Host - Friendly, engaging style</li>
              <li>• Expert Guest - Knowledgeable, insightful delivery</li>
              <li>• Enthusiastic Co-host - Energetic, passionate voice</li>
            </ul>
          </div>
        ),
        tips: [
          "Use different voices for different speakers in interviews",
          "Test voice combinations to find the best fit",
          "Voice consistency helps build listener familiarity"
        ]
      }
    ],
    book: [
      {
        title: "Welcome to Book Builder",
        description: "Transform your knowledge into a structured, professional book. Our AI helps you organize your thoughts and create compelling content.",
        icon: <div className="text-3xl">📚</div>,
        tips: [
          "Start with your main message or key insight",
          "Break complex topics into digestible chapters",
          "Include real examples and stories"
        ]
      },
      {
        title: "Structure Your Book",
        description: "Good books have a clear structure that guides readers through your content. We'll help you create chapters, sections, and flow.",
        icon: <div className="text-3xl">📋</div>,
        content: (
          <div className="space-y-2 text-sm">
            <div className="font-medium">Typical Book Structure:</div>
            <div className="grid grid-cols-2 gap-2">
              <div>• Introduction</div>
              <div>• Chapter 1-3</div>
              <div>• Main Content</div>
              <div>• Chapter 4-6</div>
              <div>• Advanced Topics</div>
              <div>• Conclusion</div>
              <div>• Case Studies</div>
              <div>• Resources</div>
            </div>
          </div>
        ),
        tips: [
          "Each chapter should have a clear purpose",
          "Use transitions to connect ideas smoothly",
          "Include practical exercises or takeaways"
        ]
      },
      {
        title: "AI-Powered Writing",
        description: "Our AI assistant helps you write, edit, and refine your content. Get suggestions for better wording, structure, and clarity.",
        icon: <div className="text-3xl">✍️</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">AI features include:</p>
            <ul className="space-y-1 ml-4">
              <li>• Content expansion from key points</li>
              <li>• Style and tone suggestions</li>
              <li>• Grammar and clarity improvements</li>
              <li>• Chapter outline generation</li>
            </ul>
          </div>
        ),
        tips: [
          "Write your first draft without worrying about perfection",
          "Use AI suggestions as a starting point, not final answers",
          "Review and personalize AI-generated content"
        ]
      }
    ],
    audiobook: [
      {
        title: "Welcome to Audiobook Creator",
        description: "Turn your written content into engaging audio experiences. Professional voice synthesis brings your words to life.",
        icon: <div className="text-3xl">🎧</div>,
        tips: [
          "Choose content that's well-suited for audio",
          "Consider pacing and natural breaks",
          "Audio engages different senses than reading"
        ]
      },
      {
        title: "Voice Selection",
        description: "Select the perfect voice for your content. Different voices work better for different types of material.",
        icon: <div className="text-3xl">🗣️</div>,
        content: (
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-white rounded border">
              <span className="text-2xl">📖</span>
              <div>
                <div className="font-medium">Narrator Voice</div>
                <div className="text-sm text-gray-600">Clear, professional storytelling</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white rounded border">
              <span className="text-2xl">🎭</span>
              <div>
                <div className="font-medium">Character Voices</div>
                <div className="text-sm text-gray-600">For fiction with multiple characters</div>
              </div>
            </div>
          </div>
        ),
        tips: [
          "Test different voices with your content",
          "Consider the emotional tone of your material",
          "Natural pacing is more important than speed"
        ]
      },
      {
        title: "Audio Enhancement",
        description: "Add music, sound effects, and adjust timing to create a professional listening experience.",
        icon: <div className="text-3xl">🎵</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">Enhancement options:</p>
            <ul className="space-y-1 ml-4">
              <li>• Background music and intro/outro</li>
              <li>• Chapter breaks and transitions</li>
              <li>• Sound effects for emphasis</li>
              <li>• Volume leveling and noise reduction</li>
            </ul>
          </div>
        ),
        tips: [
          "Keep background music subtle and non-distracting",
          "Use sound effects sparingly for impact",
          "Test your audiobook on different devices"
        ]
      }
    ],
    course: [
      {
        title: "Welcome to Course Builder",
        description: "Create comprehensive content experiences with modules, videos, and interactive elements. Help others discover your expertise.",
        icon: <div className="text-3xl">🎓</div>,
        tips: [
          "Focus on practical, actionable content outcomes",
          "Break complex topics into manageable modules",
          "Include quizzes and exercises for engagement"
        ]
      },
      {
        title: "Course Structure",
        description: "Organize your course into logical modules that build on each other. Each module should have a clear content objective.",
        icon: <div className="text-3xl">📚</div>,
        content: (
          <div className="space-y-2 text-sm">
            <div className="font-medium">Effective Course Structure:</div>
            <div className="space-y-1">
              <div><strong>Module 1:</strong> Foundation & Basics</div>
              <div><strong>Module 2:</strong> Core Concepts</div>
              <div><strong>Module 3:</strong> Practical Application</div>
              <div><strong>Module 4:</strong> Advanced Techniques</div>
              <div><strong>Module 5:</strong> Projects & Implementation</div>
            </div>
          </div>
        ),
        tips: [
          "Start with why students should care about the topic",
          "Each module should take 1-2 hours to complete",
          "Include downloadable resources and checklists"
        ]
      },
      {
        title: "Interactive Elements",
        description: "Make your course engaging with multimedia, assignments, and community features. Content is more effective when interactive.",
        icon: <div className="text-3xl">🎯</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">Interactive features:</p>
            <ul className="space-y-1 ml-4">
              <li>• Knowledge checks and quizzes</li>
              <li>• Practical exercises and assignments</li>
              <li>• Discussion forums and Q&A</li>
              <li>• Progress tracking and certificates</li>
            </ul>
          </div>
        ),
        tips: [
          "Use quizzes to reinforce key concepts",
          "Provide feedback on assignments promptly",
          "Create a supportive content community"
        ]
      }
    ],
    masterclass: [
      {
        title: "Welcome to Masterclass Creator",
        description: "Share your deepest expertise and unique insights. Masterclasses are for those with specialized knowledge to teach.",
        icon: <div className="text-3xl">👑</div>,
        tips: [
          "Focus on what only you can teach uniquely",
          "Be authentic and share real experiences",
          "Create value that justifies premium pricing"
        ]
      },
      {
        title: "Expert Positioning",
        description: "Position yourself as the authority in your niche. Share your journey, credentials, and unique perspective.",
        icon: <div className="text-3xl">⭐</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">Build credibility through:</p>
            <ul className="space-y-1 ml-4">
              <li>• Your unique experiences and breakthroughs</li>
              <li>• Case studies and success stories</li>
              <li>• Industry recognition and achievements</li>
              <li>• The problems you solve that others can't</li>
            </ul>
          </div>
        ),
        tips: [
          "Be specific about what makes you different",
          "Share both successes and lessons learned",
          "Focus on transformation, not just information"
        ]
      },
      {
        title: "Premium Content",
        description: "Create high-value content that goes deep into your specialty. Include advanced techniques and insider knowledge.",
        icon: <div className="text-3xl">💎</div>,
        content: (
          <div className="text-sm text-gray-700">
            <p className="mb-2">Premium elements include:</p>
            <ul className="space-y-1 ml-4">
              <li>• Advanced strategies and techniques</li>
              <li>• Private community access</li>
              <li>• One-on-one coaching sessions</li>
              <li>• Exclusive tools and templates</li>
            </ul>
          </div>
        ),
        tips: [
          "Deliver more value than expected",
          "Include implementation support",
          "Create ongoing engagement opportunities"
        ]
      }
    ]
  };

  return walkthroughs[productId] || [
    {
      title: `Welcome to ${productName}`,
      description: `Let's get you started with ${productName}. This walkthrough will help you understand the key features and how to make the most of this tool.`,
      icon: <div className="text-3xl">🚀</div>,
      tips: [
        "Explore the features at your own pace",
        "Don't hesitate to experiment and try different approaches",
        "Use the help resources if you need assistance"
      ]
    }
  ];
}