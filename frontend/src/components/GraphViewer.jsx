// components/GraphViewer.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const GraphViewer = ({ url, title = "Knowledge Graph", width = "100%", height = "650px" }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (url) {
      setLoading(true);
      setError(null);

      // Add a timeout to stop loading after a reasonable time
      const timer = setTimeout(() => {
        setLoading(false);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [url]);

  const handleLoad = () => {
    setLoading(false);
  };

  const handleError = () => {
    setLoading(false);
    setError("Failed to load graph visualization");
  };

  if (!url) {
    return (
      <div style={{
        width,
        height,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#1a1a1a',
        color: '#888',
        border: '2px dashed #444',
        borderRadius: '8px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📊</div>
          <div>No graph to display</div>
          <div style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
            Generate a graph to visualize relationships
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      width,
      position: 'relative',
      borderRadius: '8px',
      overflow: 'hidden',
      backgroundColor: '#1a1a1a'
    }}>
      {title && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#2a2a2a',
          color: '#fff',
          fontWeight: 'bold',
          borderBottom: '1px solid #444'
        }}>
          {title}
        </div>
      )}

      {loading && (
        <div style={{
          position: 'absolute',
          top: title ? '73px' : '0',
          left: '0',
          right: '0',
          bottom: '0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#1a1a1a',
          zIndex: 10
        }}>
          <div style={{ textAlign: 'center', color: '#888' }}>
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔄</div>
            <div>Loading graph visualization...</div>
          </div>
        </div>
      )}

      {error && (
        <div style={{
          position: 'absolute',
          top: title ? '73px' : '0',
          left: '0',
          right: '0',
          bottom: '0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#1a1a1a',
          color: '#ff6b6b',
          zIndex: 10
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>❌</div>
            <div>{error}</div>
          </div>
        </div>
      )}

      <iframe
        src={url}
        style={{
          width: '100%',
          height,
          border: 'none',
          display: loading || error ? 'none' : 'block'
        }}
        title={title}
        onLoad={handleLoad}
        onError={handleError}
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  );
};

GraphViewer.propTypes = {
  url: PropTypes.string,
  title: PropTypes.string,
  width: PropTypes.string,
  height: PropTypes.string
};

export default GraphViewer;