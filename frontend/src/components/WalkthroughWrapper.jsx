import React from 'react';
import { ProductWalkthrough } from './ProductWalkthrough';
import { useProductWalkthrough } from '../hooks/useProductWalkthrough';

/**
 * WalkthroughWrapper - Easy-to-use wrapper for adding product walkthroughs
 *
 * Usage:
 * <WalkthroughWrapper productId="podcast" productName="Podcast Engine">
 *   <YourProductComponent />
 * </WalkthroughWrapper>
 */
export function WalkthroughWrapper({ productId, productName, children }) {
  const {
    showWalkthrough,
    completeWalkthrough,
    skipWalkthrough
  } = useProductWalkthrough(productId);

  return (
    <>
      {children}
      <ProductWalkthrough
        productId={productId}
        productName={productName}
        isVisible={showWalkthrough}
        onComplete={completeWalkthrough}
        onSkip={skipWalkthrough}
      />
    </>
  );
}