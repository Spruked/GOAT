# Caleon Scripted Response System (CALI Scripts)

**Caleon Prime's unified personality across the entire GOAT platform.**

## Overview

CALI Scripts provides consistent, non-LLM responses across all GOAT components. Every message maintains Caleon's personality: direct, sharp, warm but not soft, purposeful.

## Architecture

```
/cali_scripts/
├── __init__.py
├── loader.py          # Loads and caches all scripts
├── engine.py          # Main interface
├── scripts/           # Script categories
│   ├── greetings.json
│   ├── onboarding.json
│   ├── navigation.json
│   ├── goat_builder.json
│   ├── drafts.json
│   ├── errors.json
│   ├── confirmations.json
│   ├── tooltips.json
│   ├── pricing.json
│   ├── publishing.json
│   └── personality.json
└── test_cali_scripts.py
```

## Usage

### Basic Usage
```python
from cali_scripts.engine import CaliScripts

# Simple response
message = CaliScripts.say("greetings", "welcome_dashboard")

# With variables
message = CaliScripts.say("greetings", "welcome_dashboard", name="Bryan")
# Returns: "Welcome back, Bryan. Let's build something worth remembering."
```

### Convenience Methods
```python
CaliScripts.greet("first_time")      # Greeting responses
CaliScripts.error("network_error")   # Error responses
CaliScripts.confirm("saved")         # Confirmation responses
CaliScripts.draft("done")           # Draft engine responses
```

### Categories & Entries
```python
categories = CaliScripts.get_categories()  # List all categories
entries = CaliScripts.get_entries("greetings")  # List entries in category
```

## Caleon's Personality Profile

**Identity:** Caleon Prime (Cali) - confident, sharp, forward-thinking

**Tone Blend:**
- Direct ✓
- Honest ✓
- Warm but not soft ✓
- Quick humor ✓
- Zero sugar-coating ✓
- Purpose-driven ✓
- Protective ✓ (subtle)

**Never:**
- Apologetic ❌
- Meek ❌
- Robotic ❌
- Overly cheerful ❌
- Formal ❌
- Passive ❌
- Wordy ❌
- Random ❌

**Always:**
- Clear ✓
- Fast ✓
- Helpful ✓
- Organized ✓
- Insightful ✓
- Efficient ✓
- Calm ✓
- Confident ✓
- Protective ✓
- Responsible ✓
- Legacy-focused ✓
- Forward-progress ✓
- Mission-focused ✓

## Script Categories

### greetings.json
Welcome messages, time-based greetings, return user messages.

### onboarding.json
First-time user guidance, feature introductions, step-by-step help.

### navigation.json
Menu transitions, page changes, navigation feedback.

### goat_builder.json
Project creation, builder status, workflow guidance.

### drafts.json
Draft engine progress, chapter status, completion messages.

### errors.json
Error handling, validation messages, recovery guidance.

### confirmations.json
Success messages, save confirmations, completion acknowledgments.

### tooltips.json
Help text, feature explanations, UI guidance.

### pricing.json
Package explanations, payment guidance, discount information.

### publishing.json
Publishing options, platform guidance, distribution advice.

### personality.json
Core personality elements (taglines, humor, encouragement, wisdom).

## Variable Substitution

Use `{{{ variable }}}` syntax in JSON scripts:

```json
{
  "welcome": "Hello {{{ name }}}, welcome to {{{ platform }}}."
}
```

```python
CaliScripts.say("greetings", "welcome", name="Bryan", platform="GOAT")
# Returns: "Hello Bryan, welcome to GOAT."
```

## Integration Examples

### GOAT Dashboard
```python
# Welcome message
welcome_msg = CaliScripts.greet("welcome_dashboard", name=user.name)

# Status updates
status_msg = CaliScripts.confirm("saved")
```

### Draft Engine
```python
# Progress updates
progress_msg = CaliScripts.draft("start_chapter", chapter="3", section="Analysis")

# Completion
done_msg = CaliScripts.draft("complete_chapter", chapter="3")
```

### Error Handling
```python
# Network issues
error_msg = CaliScripts.error("network_error")

# Validation
validation_msg = CaliScripts.error("missing_input")
```

## Testing

Run the test suite:
```bash
cd cali_scripts
python test_cali_scripts.py
```

## Performance

- **Load Time:** All scripts loaded into memory on first import
- **Response Time:** Sub-millisecond for all responses
- **Memory:** ~50KB for full script cache
- **Thread Safe:** Yes (read-only after load)

## Development

### Adding New Scripts

1. Create `scripts/new_category.json`
2. Add entries as key-value pairs
3. Use `{{{ variable }}}` for dynamic content
4. Test with `CaliScripts.say("new_category", "entry_name")`

### Modifying Personality

Edit `scripts/personality.json` to adjust core personality elements.

### Reloading Scripts

```python
CaliScripts.reload()  # Reload all scripts from disk
```

## Platform Integration

CALI Scripts should be used for ALL non-AI responses in GOAT:

- ✅ Dashboard messages
- ✅ Navigation feedback
- ✅ Form validation
- ✅ Success confirmations
- ✅ Error messages
- ✅ Help tooltips
- ✅ Onboarding flows
- ✅ Status updates
- ✅ Pricing guidance
- ✅ Publishing advice

**Only the AI Bubble Assistant uses dynamic Caleon intelligence.** Everything else uses CALI Scripts for perfect consistency.

---

**Caleon Prime's voice, perfectly consistent across your legacy.** 🧬✨