# Product Walkthrough System

The GOAT platform includes a comprehensive first-time user walkthrough system that guides users through each product's key features and best practices.

## Overview

Each product in GOAT has a dedicated walkthrough that appears automatically the first time a user visits that product. The walkthrough:

- Introduces the product's main features
- Provides step-by-step guidance
- Offers pro tips and best practices
- Can be completed or skipped
- Won't show again once completed/skipped

## Components

### ProductWalkthrough
The main walkthrough component that displays modal overlays with step-by-step guidance.

### useProductWalkthrough Hook
Manages walkthrough state and persistence using localStorage.

### WalkthroughWrapper
A convenience wrapper that makes it easy to add walkthroughs to any product page.

## Usage

### Method 1: Using the Hook (Recommended for complex products)

```jsx
import { useProductWalkthrough } from '../hooks/useProductWalkthrough';
import { ProductWalkthrough } from '../components/ProductWalkthrough';

function MyProductPage() {
  const {
    showWalkthrough,
    completeWalkthrough,
    skipWalkthrough
  } = useProductWalkthrough('myproduct');

  return (
    <div>
      {/* Your product content */}
      <ProductWalkthrough
        productId="myproduct"
        productName="My Product"
        isVisible={showWalkthrough}
        onComplete={completeWalkthrough}
        onSkip={skipWalkthrough}
      />
    </div>
  );
}
```

### Method 2: Using the Wrapper (Recommended for simple products)

```jsx
import { WalkthroughWrapper } from '../components/WalkthroughWrapper';

function MyProductPage() {
  return (
    <WalkthroughWrapper productId="myproduct" productName="My Product">
      {/* Your product content */}
    </WalkthroughWrapper>
  );
}
```

## Adding Walkthrough Content

Walkthrough content is defined in `ProductWalkthrough.jsx` in the `getWalkthroughSteps` function. Each product has an array of steps with:

- `title`: Step headline
- `description`: Main explanation
- `icon`: Visual element (emoji or component)
- `content`: Optional additional JSX content
- `tips`: Array of pro tips

### Example Walkthrough Definition

```javascript
podcast: [
  {
    title: "Welcome to Podcast Engine",
    description: "Create professional podcasts with multiple voices...",
    icon: <div className="text-3xl">🎤</div>,
    tips: [
      "Prepare your script or key points before recording",
      "Use a quiet environment for best audio quality"
    ]
  },
  // More steps...
]
```

## Supported Products

Currently implemented walkthroughs:
- `podcast` - Podcast Engine
- `book` - Book Builder
- `audiobook` - Audiobook Creator
- `course` - Course Builder
- `masterclass` - Masterclass Creator

## State Management

Walkthrough completion is stored in localStorage:
- `completedWalkthroughs`: Object tracking completed walkthroughs
- `skippedWalkthroughs`: Object tracking skipped walkthroughs

## Utility Functions

### getWalkthroughStatus(productId)
Returns status information for a product:
```javascript
const status = getWalkthroughStatus('podcast');
// { isCompleted: true, isSkipped: false, hasSeen: true }
```

### resetAllWalkthroughs()
Clears all walkthrough data (useful for testing):
```javascript
import { resetAllWalkthroughs } from '../hooks/useProductWalkthrough';
resetAllWalkthroughs();
```

## Best Practices

1. **Keep it Short**: 2-4 steps maximum per product
2. **Focus on Value**: Highlight what makes the product unique
3. **Actionable Tips**: Provide specific, practical advice
4. **Progressive Disclosure**: Start simple, get more advanced
5. **Skippable**: Always allow users to skip if they prefer

## Adding New Products

1. Add walkthrough content to `getWalkthroughSteps` in `ProductWalkthrough.jsx`
2. Use the hook or wrapper in your product page
3. Test the walkthrough flow
4. Update this documentation

## Customization

The walkthrough system is fully customizable:
- Modal styling can be adjusted in `ProductWalkthrough.jsx`
- Step content can include any React components
- Icons and colors can be customized per product
- Timing and animations can be modified

## Accessibility

The walkthrough includes:
- Keyboard navigation support
- Screen reader friendly content
- High contrast colors
- Clear focus indicators
- Skip options for all users</content>
<parameter name="filePath">c:\dev\GOAT\frontend\src\components\ProductWalkthrough_README.md