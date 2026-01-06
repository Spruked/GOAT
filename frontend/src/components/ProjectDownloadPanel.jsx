import React, { useRef } from 'react';
import './ProjectDownloadPanel.css';

export default function ProjectDownloadPanel({
  onDownload,
  onUpload,
  isResuming,
  resumeError
}) {
  const fileInputRef = useRef();

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="project-panel">
      <h2 className="project-panel-title">📦 Download Working Files</h2>
      <p className="project-panel-desc">
        Download a ZIP containing your original uploads, cleaned versions, OCR text, AI summaries, metadata, project.gproj, thumbnails, drafts, and everything needed to resume your project.
      </p>
      <button className="project-download-btn" onClick={onDownload}>
        Download Working Files
      </button>

      <div className="project-resume-section">
        <h3>🏁 Resume a GOAT Project</h3>
        <div
          className="project-dropzone"
          onClick={() => fileInputRef.current.click()}
        >
          <span>Drag & drop your GOAT Project ZIP here, or click to select.</span>
          <input
            type="file"
            accept=".zip"
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={handleFileChange}
          />
        </div>
        {isResuming && <div className="project-resume-status">Restoring your project...</div>}
        {resumeError && <div className="project-resume-error">{resumeError}</div>}
      </div>
    </div>
  );
}
