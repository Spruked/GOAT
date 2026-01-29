# CALI Scripts & Caleon Generative Frontend Integration

**Caleon Prime's unified voice across the entire GOAT platform.**

## Overview

This integration provides two complementary intelligence systems:

1. **CALI Scripts** - Consistent, non-LLM responses for UI consistency
2. **Caleon Generative** - Dynamic AI responses for the Bubble Assistant

## Architecture

```
Frontend (React)
├── hooks/
│   ├── useCaliScripts.js          # CALI Scripts hook
│   └── useCaleonGenerative.js     # Generative AI hook
├── components/
│   ├── CaliScriptedUI.jsx         # CALI integration demo
│   ├── EnhancedAssistantBubble.jsx # Dual-mode assistant
│   └── CaleonMessage.jsx          # Existing message component
└── Backend API
    ├── /api/cali-scripts/*        # Scripted responses
    └── /api/caleon/*              # Generative responses
```

## CALI Scripts Integration

### React Hook Usage

```javascript
import { useCaliScripts } from '../hooks/useCaliScripts';

function MyComponent() {
  const {
    greet,
    confirm,
    showError,
    draft,
    tooltip,
    isLoading,
    error
  } = useCaliScripts();

  const handleWelcome = async () => {
    const message = await greet('welcome_dashboard', { name: 'Bryan' });
    console.log(message); // "Welcome back, Bryan. Let's build something worth remembering."
  };

  const handleSave = async () => {
    const message = await confirm('saved');
    console.log(message); // "Saved. Nothing gets lost on my watch."
  };

  return (
    <div>
      <button onClick={handleWelcome}>Welcome User</button>
      <button onClick={handleSave}>Save</button>
    </div>
  );
}
```

### Available Categories

- **greetings** - Welcome messages, time-based greetings
- **onboarding** - User guidance, tutorials
- **navigation** - Menu transitions, page changes
- **goat_builder** - Project creation workflow
- **drafts** - Draft engine status messages
- **errors** - Error handling, recovery
- **confirmations** - Success messages, completion
- **tooltips** - Help text, UI guidance
- **pricing** - Package explanations
- **publishing** - Distribution advice

### API Endpoints

```javascript
// Get specific script
POST /api/cali-scripts/
{
  "category": "greetings",
  "entry": "welcome_dashboard",
  "variables": {"name": "Bryan"}
}

// Get available categories
GET /api/cali-scripts/categories

// Convenience endpoints
POST /api/cali-scripts/greet
POST /api/cali-scripts/error
POST /api/cali-scripts/confirm
POST /api/cali-scripts/draft
POST /api/cali-scripts/tooltip
```

## Caleon Generative Integration

### React Hook Usage

```javascript
import { useCaleonGenerative } from '../hooks/useCaleonGenerative';

function BubbleAssistant() {
  const { sendToCaleon, streamFromCaleon, isGenerating } = useCaleonGenerative();

  const handleQuery = async (userMessage) => {
    // Simple response
    const response = await sendToCaleon(userMessage, {
      interface: 'bubble_assistant'
    });

    // Streaming response
    await streamFromCaleon(
      userMessage,
      (chunk) => {
        setCurrentResponse(prev => prev + chunk);
      },
      { conversation_history: previousMessages }
    );
  };

  return (
    <div>
      {isGenerating && <div>Generating response...</div>}
      <button onClick={() => handleQuery("Help me create a book")}>
        Ask Caleon
      </button>
    </div>
  );
}
```

### API Endpoints

```javascript
// Generate response
POST /api/caleon/generate
{
  "message": "Help me create a book",
  "context": {"interface": "bubble_assistant"},
  "timestamp": "2025-11-25T12:00:00Z"
}

// Stream response (Server-Sent Events)
POST /api/caleon/stream
// Returns: data: {"chunk": "Here's how", "is_complete": false}
//         data: {"chunk": " to create", "is_complete": false}
//         data: {"chunk": " your book...", "is_complete": true}

// Health check
GET /api/caleon/health

// Update context
POST /api/caleon/bubble/context
{
  "conversation_history": [...],
  "user_preferences": {...}
}
```

## Enhanced Assistant Bubble

The `EnhancedAssistantBubble.jsx` component demonstrates dual-mode intelligence:

```javascript
// Uses CALI Scripts for:
- Greetings and confirmations
- Error messages
- Status updates
- Simple queries

// Uses Caleon Generative for:
- Complex questions
- Content creation help
- Analysis requests
- Dynamic conversations
```

### Voice Integration

```javascript
// Voice commands trigger appropriate responses
- "Hello Caleon" → CALI greeting
- "Help me write" → Caleon generative
- "Show status" → CALI status message
- "What's new" → Caleon generative
```

## Implementation Examples

### Dashboard Component

```javascript
function Dashboard({ user }) {
  const { greet, tooltip } = useCaliScripts();

  useEffect(() => {
    const loadWelcome = async () => {
      const welcomeMsg = await greet('welcome_dashboard', { name: user.name });
      setWelcomeMessage(welcomeMsg);
    };
    loadWelcome();
  }, [user, greet]);

  return (
    <div>
      <h1>{welcomeMessage}</h1>
      <HelpIcon title={tooltip('dashboard_overview')} />
    </div>
  );
}
```

### Error Boundary

```javascript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Use CALI Scripts for consistent error messaging
    this.setState({
      errorMessage: "Something unexpected happened. I'm on it — try again in a moment."
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorMessage message={this.state.errorMessage} />;
    }
    return this.props.children;
  }
}
```

### Form Validation

```javascript
function ProjectForm() {
  const { showError, confirm } = useCaliScripts();
  const [error, setError] = useState('');

  const handleSubmit = async (data) => {
    if (!data.title) {
      setError(await showError('missing_input'));
      return;
    }

    // Submit logic...
    const successMsg = await confirm('saved');
    showNotification(successMsg);
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      {/* form fields */}
    </form>
  );
}
```

## Testing

Run the API test suite:

```bash
python test_api_endpoints.py
```

This tests:
- CALI Scripts API endpoints
- Caleon Generative API endpoints
- Server health and connectivity

## Performance

- **CALI Scripts**: Sub-millisecond responses (cached)
- **Caleon Generative**: 1-3 seconds for generation
- **Streaming**: Real-time chunks for typing effect
- **Caching**: Frontend caches CALI responses

## Development

### Adding New Scripts

1. Add entries to `cali_scripts/scripts/*.json`
2. Use `{{{ variable }}}` for dynamic content
3. Test via API or React hooks

### Extending Generative Features

1. Add new context parameters
2. Implement conversation memory
3. Add response formatting options

## Platform Consistency

**CALI Scripts ensure:**
- Same greeting every time
- Consistent error messages
- Predictable confirmations
- Unified tooltips and help text

**Caleon Generative provides:**
- Dynamic help and guidance
- Creative content assistance
- Complex query responses
- Adaptive conversations

Together they create Caleon Prime's complete personality across GOAT.

---

**One voice. Infinite consistency. Pure Caleon.** 🧬✨

---

## 📄 Copyright

Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.