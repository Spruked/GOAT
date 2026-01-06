import { useState, useEffect } from 'react';

function KayGeeOrbWidget({ position = 'bottom-right' }) {
  const [speaking, setSpeaking] = useState(false);

  return (
    <div style={{
      position: 'fixed',
      [position.includes('bottom') ? 'bottom' : 'top']: '20px',
      [position.includes('right') ? 'right' : 'left']: '20px',
      zIndex: 9999,
      pointerEvents: 'none'
    }}>
      <iframe
        src="http://localhost:3000/orb-only"
        style={{
          width: '300px',
          height: '300px',
          border: 'none',
          borderRadius: '50%',
          boxShadow: speaking ? '0 0 60px cyan' : '0 0 30px rgba(0,255,255,0.6)',
          transition: 'all 0.3s',
          pointerEvents: 'auto'
        }}
        title="KayGee Orb"
        onMouseEnter={() => setSpeaking(true)}
        onMouseLeave={() => setSpeaking(false)}
      />
    </div>
  );
}

export default KayGeeOrbWidget;
