import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import SpaceField3D from './components/SpaceField3D';
import { useState, useEffect } from 'react';

function OrbOnly() {
  const [resonance, setResonance] = useState({ phaseCoherence: 0.5 });

  // Connect to backend WebSocket for UCM resonance data
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:5000/ws/orb');
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'resonance_update') {
        setResonance(data.data);
      }
    };
    
    ws.onerror = (error) => {
      console.error('Orb WebSocket error:', error);
    };
    
    return () => ws.close();
  }, []);

  const sides = 4 + Math.floor(resonance.phaseCoherence * 8);
  const levels = 2 + Math.floor(resonance.phaseCoherence * 6);

  return (
    <div style={{ width: '100%', height: '100%', background: 'transparent' }}>
      <Canvas camera={{ position: [0, 0, 8], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[0, 0, 0]} intensity={1 + resonance.phaseCoherence * 2} color="#00ffff" />
        <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade />
        <SpaceField3D 
          sides={sides}
          levels={levels}
          radius={2}
          emergent={true}
          rotationSpeed={0.01 + resonance.phaseCoherence * 0.02}
        />
      </Canvas>
    </div>
  );
}

export default OrbOnly;
