// SpaceField3D.jsx - React/Three.js version
// Faithful to the Python/SketchUp logic, but for React Three Fiber
import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function generateVertices(center, radius, sides) {
  const vertices = [];
  const angle = (2 * Math.PI) / sides;
  for (let side = 0; side < sides; side++) {
    let theta = sides % 2 === 0
      ? angle * side
      : angle * side - angle / 2;
    const x = center[0] + radius * Math.sin(theta);
    const y = center[1] + radius * Math.cos(theta);
    vertices.push([x, y, center[2]]);
  }
  return vertices;
}

function SpaceField3D({ sides = 6, levels = 3, radius = 2, emergent = true, rotationSpeed = 0.02 }) {
  const group = useRef();
  // Memoize geometry for performance
  const polygons = useMemo(() => {
    let polys = [];
    let currentCenter = [0, 0, 0];
    let currentRadius = radius;
    for (let level = 1; level <= levels; level++) {
      const verts = generateVertices(currentCenter, currentRadius, sides);
      polys.push(verts);
      // Next level origin: even sides use first vertex, odd use midpoint of first edge
      if (sides % 2 === 1) {
        const v0 = verts[0], v1 = verts[1];
        currentCenter = [
          (v0[0] + v1[0]) / 2,
          (v0[1] + v1[1]) / 2,
          (v0[2] + v1[2]) / 2
        ];
      } else {
        currentCenter = verts[0];
      }
      currentRadius *= sides % 2 === 0 ? 2 : 1.5;
    }
    return polys;
  }, [sides, levels, radius]);

  useFrame((_, delta) => {
    if (group.current) {
      group.current.rotation.z += rotationSpeed * delta;
    }
  });

  return (
    <group ref={group}>
      {polygons.map((verts, idx) => (
        <line key={idx}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={verts.length + 1}
              array={new Float32Array([...verts.flat(), ...verts[0]])}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial color={`hsl(${(idx * 60) % 360},100%,60%)`} linewidth={2} />
        </line>
      ))}
    </group>
  );
}

export default SpaceField3D;
