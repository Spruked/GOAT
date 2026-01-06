import React, { useState } from 'react';
import ProjectDownloadPanel from '../components/ProjectDownloadPanel';
import { downloadProjectZip, uploadProjectZip } from '../utils/api';

export default function ProjectPanelPage() {
  const [isResuming, setIsResuming] = useState(false);
  const [resumeError, setResumeError] = useState(null);
  const [projectId, setProjectId] = useState('demo_project');

  const handleDownload = async () => {
    try {
      const res = await downloadProjectZip(projectId);
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `GOAT_Project_${projectId}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download project ZIP: ' + err.message);
    }
  };

  const handleUpload = async (file) => {
    setIsResuming(true);
    setResumeError(null);
    try {
      const result = await uploadProjectZip(file);
      setIsResuming(false);
      alert('Project resumed!\n' + JSON.stringify(result.project, null, 2));
    } catch (err) {
      setIsResuming(false);
      setResumeError('Failed to resume project: ' + err.message);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-12">
      <div className="mb-4">
        <label className="block text-slate-300 mb-1">Project ID for export:</label>
        <input
          className="border rounded px-2 py-1 text-black"
          value={projectId}
          onChange={e => setProjectId(e.target.value)}
        />
      </div>
      <ProjectDownloadPanel
        onDownload={handleDownload}
        onUpload={handleUpload}
        isResuming={isResuming}
        resumeError={resumeError}
      />
    </div>
  );
}
