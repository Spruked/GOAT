import React, { useState } from 'react';
import { ArrowLeft, Zap, Network } from 'lucide-react';
import GraphViewer from '../components/GraphViewer';

export default function GraphDemoPage() {
  const [graphURL, setGraphURL] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateGraph = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/graphs/html', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          concepts: {
            "Abby": ["Love", "Loss", "Courage"],
            "Butch": ["Legacy", "Strength"],
            "Angela": ["Trauma", "Conflict"],
            "Marcus": ["Hope", "Redemption"]
          },
          graph_type: "concepts",
          title: "GOAT Concept Graph Demo"
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setGraphURL(data.graph_url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const testGraph = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/graphs/test');

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setGraphURL(data.graph_url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0a', color: 'white' }}>
      {/* Header */}
      <div style={{
        padding: '1rem 2rem',
        borderBottom: '1px solid #333',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem'
      }}>
        <button
          onClick={() => window.history.back()}
          style={{
            background: 'none',
            border: 'none',
            color: '#888',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <ArrowLeft size={20} />
          Back to Dashboard
        </button>
      </div>

      {/* Main Content */}
      <div style={{ padding: '2rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Title */}
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h1 style={{
              fontSize: '2.5rem',
              fontWeight: 'bold',
              marginBottom: '1rem',
              background: 'linear-gradient(135deg, #00ff88, #0088ff)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              🧠 GOAT Knowledge Graphs
            </h1>
            <p style={{ color: '#888', fontSize: '1.2rem' }}>
              Interactive visualizations of concepts, characters, and story relationships
            </p>
          </div>

          {/* Controls */}
          <div style={{
            display: 'flex',
            gap: '1rem',
            justifyContent: 'center',
            marginBottom: '2rem',
            flexWrap: 'wrap'
          }}>
            <button
              onClick={generateGraph}
              disabled={loading}
              style={{
                background: loading ? '#333' : 'linear-gradient(135deg, #00ff88, #0088ff)',
                color: 'white',
                border: 'none',
                padding: '1rem 2rem',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.3s ease'
              }}
            >
              <Network size={20} />
              {loading ? 'Generating...' : 'Generate Concept Graph'}
            </button>

            <button
              onClick={testGraph}
              disabled={loading}
              style={{
                background: loading ? '#333' : '#ff6b6b',
                color: 'white',
                border: 'none',
                padding: '1rem 2rem',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.3s ease'
              }}
            >
              <Zap size={20} />
              {loading ? 'Testing...' : 'Test Graph'}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div style={{
              backgroundColor: '#ff3838',
              color: 'white',
              padding: '1rem',
              borderRadius: '8px',
              marginBottom: '2rem',
              textAlign: 'center'
            }}>
              ❌ Error: {error}
            </div>
          )}

          {/* Graph Viewer */}
          {graphURL && (
            <div style={{ marginTop: '2rem' }}>
              <GraphViewer url={graphURL} title="Interactive Knowledge Graph" />
            </div>
          )}

          {/* Info Section */}
          {!graphURL && !loading && (
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              backgroundColor: '#1a1a1a',
              borderRadius: '12px',
              border: '2px dashed #444'
            }}>
              <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>📊</div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>
                Generate Your First Knowledge Graph
              </h3>
              <p style={{ color: '#888', lineHeight: '1.6' }}>
                Click the buttons above to create interactive visualizations of concepts,
                character relationships, and story structures. Each graph is generated
                on-demand and saved for future reference.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}