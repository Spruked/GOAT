import React, { useState, useCallback } from 'react';

const OrganizerPage = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleUpload = async () => {
    if (files.length === 0) return;

    setUploading(true);
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    formData.append('save_to_vault', saveToVault.toString());

    try {
      const response = await fetch('/organizer/organize/', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Upload failed');
      const result = await response.json();
      setResult(result);
    } catch (error) {
      console.error('Upload failed:', error);
      setResult({ error: 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  const [saveToVault, setSaveToVault] = useState(false);

  const handlePreview = async () => {
    if (files.length === 0) return;

    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch('/organizer/organize/preview', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Preview failed');
      const result = await response.json();
      setPreview(result);
    } catch (error) {
      console.error('Preview failed:', error);
      setPreview({ error: 'Preview failed' });
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-2xl font-bold mb-6 text-center">File Organizer</h1>
      
      <div 
        className={`border-2 border-dashed rounded-lg p-8 mb-4 text-center transition-colors ${
          dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div className="mb-4">
          <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <p className="text-lg mb-2">Drop files here or click to select</p>
        <p className="text-sm text-gray-500 mb-4">Files will be automatically organized by type</p>
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="hidden"
          id="file-input"
        />
        <label htmlFor="file-input" className="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Select Files
        </label>
      </div>

      {files.length > 0 && (
        <div className="mb-4">
          <h3 className="text-lg font-semibold mb-2">Selected Files ({files.length})</h3>
          <ul className="list-disc list-inside text-sm text-gray-600 max-h-32 overflow-y-auto">
            {files.map((file, index) => (
              <li key={index}>{file.name} ({(file.size / 1024).toFixed(1)} KB)</li>
            ))}
          </ul>
        </div>
      )}

      <div className="flex gap-4 mb-4">
        <button
          onClick={handlePreview}
          disabled={files.length === 0}
          className="flex-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Preview Organization
        </button>
        <button
          onClick={handleUpload}
          disabled={uploading || files.length === 0}
          className="flex-1 bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploading ? 'Organizing Files...' : 'Organize & Download'}
        </button>
      </div>

      <div className="mb-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={saveToVault}
            onChange={(e) => setSaveToVault(e.target.checked)}
            className="mr-2"
          />
          Save organized files to GOAT Vault for permanent storage
        </label>
      </div>

      {preview && (
        <div className="mt-6 p-4 border rounded-lg bg-gray-50">
          {preview.error ? (
            <div className="text-red-600">
              <h3 className="font-semibold">Preview Error</h3>
              <p>{preview.error}</p>
            </div>
          ) : (
            <div>
              <h3 className="font-semibold mb-4">Organization Preview</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(preview.preview).map(([category, files]) => (
                  <div key={category} className="bg-white p-3 rounded border">
                    <h4 className="font-medium text-blue-600 mb-2">{category} ({files.length} files)</h4>
                    <ul className="text-sm text-gray-600 list-disc list-inside max-h-32 overflow-y-auto">
                      {files.slice(0, 5).map((file, idx) => (
                        <li key={idx}>{file}</li>
                      ))}
                      {files.length > 5 && <li>... and {files.length - 5} more</li>}
                    </ul>
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Total: {preview.total_files} files across {preview.categories.length} categories
              </p>
            </div>
          )}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 border rounded-lg">
          {result.error ? (
            <div className="text-red-600">
              <h3 className="font-semibold">Error</h3>
              <p>{result.error}</p>
            </div>
          ) : (
            <div className="text-green-600">
              <h3 className="font-semibold mb-2">Files Organized Successfully!</h3>
              <p className="mb-4">Your files have been organized and packaged into a ZIP file.</p>
              <div className="space-y-2">
                <button
                  onClick={handleDownload}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                >
                  Download Organized Files
                </button>
                {result.saved_to_vault && result.vault_url && (
                  <a
                    href={result.vault_url}
                    className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded inline-block"
                  >
                    View in Vault
                  </a>
                )}
              </div>
              {result.saved_to_vault && (
                <p className="text-sm text-purple-600 mt-2">
                  ✓ Files also saved to your GOAT Vault for permanent storage
                </p>
              )}
              {result.glyph_trace && (
                <p className="text-sm text-blue-600 mt-1">
                  🔗 Glyph Trace: {result.glyph_trace}
                </p>
              )}
              {result.manifest && (
                <div className="mt-4 p-3 bg-gray-100 rounded text-sm">
                  <p className="font-medium">Manifest Summary:</p>
                  <p>{result.manifest.total_files} files, {(result.manifest.total_size / 1024).toFixed(1)} KB total</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default OrganizerPage;