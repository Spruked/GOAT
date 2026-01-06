// frontend/src/components/LegacyManager.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

const LegacyManager = ({ apiKey }) => {
  const [archives, setArchives] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArchives();
  }, []);

  const loadArchives = async () => {
    try {
      // This would load user's archives
      setArchives([]);
    } catch (error) {
      console.error('Failed to load archives:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="legacy-manager">
      <h2>Manage Your Legacy Archives</h2>

      {loading ? (
        <div>Loading archives...</div>
      ) : (
        <div className="archives-grid">
          {archives.length === 0 ? (
            <div className="empty-state">
              <p>No archives yet. Create your first memory video!</p>
            </div>
          ) : (
            archives.map(archive => (
              <div key={archive.id} className="archive-card">
                <h3>{archive.title}</h3>
                <p>{archive.description}</p>
                <div className="archive-actions">
                  <button>View</button>
                  <button>Download</button>
                  <button>Share</button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default LegacyManager;