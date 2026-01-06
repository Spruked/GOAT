// frontend/src/components/VideoCreator.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

const VideoCreator = ({ apiKey }) => {
  const [clips, setClips] = useState([]);
  const [template, setTemplate] = useState('legacy');
  const [voiceStyle, setVoiceStyle] = useState('sean_connery');
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState('idle');

  const handleGenerate = async () => {
    setStatus('generating');

    const formData = new FormData();
    formData.append('clips', JSON.stringify(clips));
    formData.append('template', template);
    formData.append('voice_style', voiceStyle);

    try {
      const response = await axios.post(
        `${API_URL}/video/generate-memory`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setJobId(response.data.job_id);
      pollStatus(response.data.job_id);
    } catch (error) {
      console.error('Generation failed:', error);
      setStatus('error');
    }
  };

  const pollStatus = (jobId) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(
          `${API_URL}/video/job/${jobId}`,
          {
            headers: { 'Authorization': `Bearer ${apiKey}` }
          }
        );

        if (response.data.status === 'complete') {
          setStatus('complete');
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Status check failed:', error);
        clearInterval(interval);
      }
    }, 5000);
  };

  return (
    <div className="video-creator">
      <h2>Create Memory Video</h2>

      <div className="template-selector">
        <label>Template:</label>
        <select value={template} onChange={(e) => setTemplate(e.target.value)}>
          <option value="legacy">Timeless Legacy</option>
          <option value="modern">Clean Modern</option>
          <option value="nostalgic">Soft Nostalgia</option>
        </select>
      </div>

      <div className="voice-selector">
        <label>Voice Style:</label>
        <select value={voiceStyle} onChange={(e) => setVoiceStyle(e.target.value)}>
          <option value="sean_connery">Deep & Authoritative</option>
          <option value="warm_female">Warm & Comforting</option>
          <option value="wise_older">Wise & Experienced</option>
        </select>
      </div>

      <div className="clips-list">
        {clips.map((clip, index) => (
          <div key={index} className="clip-item">
            <span>{clip.caption || `Clip ${index + 1}`}</span>
          </div>
        ))}
      </div>

      <button
        onClick={handleGenerate}
        disabled={status === 'generating'}
        className="generate-btn"
      >
        {status === 'generating' ? 'Generating...' : 'Create Memory Video'}
      </button>

      {status === 'complete' && (
        <div className="success-message">
          ✅ Video ready! Download will start automatically.
        </div>
      )}
    </div>
  );
};

export default VideoCreator;