import React, { useState, useRef } from 'react';
import { Upload, FileAudio, FileVideo, CheckCircle, AlertCircle, BookOpen, GraduationCap, Archive, FileText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function UploadPage() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = [
      'audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-m4a',
      'video/mp4', 'video/quicktime', 'video/x-msvideo'
    ];

    if (!allowedTypes.includes(file.type)) {
      alert('Please select an audio or video file');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/upload/file', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      setUploadResult(result);

      // Start polling for processing status
      pollProcessingStatus(result.upload_id);

    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
      setUploadProgress(100);
    }
  };

  const pollProcessingStatus = async (uploadId) => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`/upload/status/${uploadId}`);
        const status = await response.json();
        setProcessingStatus(status);

        if (status.status === 'completed') {
          // Processing complete
        } else if (status.status === 'failed') {
          alert('Processing failed');
        } else {
          // Continue polling
          setTimeout(checkStatus, 2000);
        }
      } catch (error) {
        console.error('Status check error:', error);
        setTimeout(checkStatus, 2000);
      }
    };

    checkStatus();
  };

  const getFileIcon = (type) => {
    if (type?.startsWith('audio/')) return <FileAudio className="w-8 h-8" />;
    if (type?.startsWith('video/')) return <FileVideo className="w-8 h-8" />;
    return <Upload className="w-8 h-8" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-4">
            Upload Content
          </h1>
          <p className="text-slate-300">
            Drop your audio or video files for AI-powered processing
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 mb-6">
          <div
            className="border-2 border-dashed border-slate-600 rounded-xl p-12 text-center cursor-pointer hover:border-cyan-400 transition-colors"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*,video/*"
              onChange={handleFileSelect}
              className="hidden"
            />

            {isUploading ? (
              <div className="space-y-4">
                <div className="w-16 h-16 mx-auto bg-cyan-500 rounded-full flex items-center justify-center">
                  <Upload className="w-8 h-8 text-white animate-pulse" />
                </div>
                <div className="space-y-2">
                  <div className="text-lg font-semibold">Uploading...</div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div
                      className="bg-cyan-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <div className="text-sm text-slate-400">{uploadProgress}%</div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="w-16 h-16 mx-auto bg-slate-600 rounded-full flex items-center justify-center">
                  <Upload className="w-8 h-8 text-slate-400" />
                </div>
                <div>
                  <div className="text-lg font-semibold mb-2">Drop files here or click to browse</div>
                  <div className="text-slate-400">
                    Supports MP3, WAV, MP4, MOV, AVI files up to 2GB
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {uploadResult && (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <CheckCircle className="w-6 h-6 text-green-400" />
              <h3 className="text-lg font-semibold text-green-400">Upload Complete</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-slate-400">Filename:</span>
                <span className="ml-2 text-white">{uploadResult.filename}</span>
              </div>
              <div>
                <span className="text-slate-400">Size:</span>
                <span className="ml-2 text-white">{(uploadResult.file_size / 1024 / 1024).toFixed(2)} MB</span>
              </div>
              <div>
                <span className="text-slate-400">Type:</span>
                <span className="ml-2 text-white">{uploadResult.content_type}</span>
              </div>
              <div>
                <span className="text-slate-400">Upload ID:</span>
                <span className="ml-2 text-cyan-400 font-mono">{uploadResult.upload_id}</span>
              </div>
            </div>
          </div>
        )}

        {processingStatus && (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              {processingStatus.status === 'completed' ? (
                <CheckCircle className="w-6 h-6 text-green-400" />
              ) : processingStatus.status === 'failed' ? (
                <AlertCircle className="w-6 h-6 text-red-400" />
              ) : (
                <div className="w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
              )}
              <h3 className="text-lg font-semibold">
                {processingStatus.status === 'completed' ? 'Processing Complete' :
                 processingStatus.status === 'failed' ? 'Processing Failed' :
                 'Processing Content...'}
              </h3>
            </div>

            {processingStatus.status === 'completed' && (
              <div className="space-y-4">
                {processingStatus.transcript && (
                  <div>
                    <h4 className="font-semibold text-cyan-400 mb-2">Transcript Preview</h4>
                    <p className="text-slate-300 text-sm bg-slate-700/50 rounded p-3 max-h-32 overflow-y-auto">
                      {processingStatus.transcript.substring(0, 300)}...
                    </p>
                  </div>
                )}

                {processingStatus.summary && (
                  <div>
                    <h4 className="font-semibold text-purple-400 mb-2">AI Summary</h4>
                    <p className="text-slate-300 text-sm bg-slate-700/50 rounded p-3">
                      {processingStatus.summary}
                    </p>
                  </div>
                )}

                {processingStatus.chapters && (
                  <div>
                    <h4 className="font-semibold text-green-400 mb-2">Detected Chapters</h4>
                    <div className="space-y-2">
                      {processingStatus.chapters.map((chapter, index) => (
                        <div key={index} className="flex justify-between text-sm bg-slate-700/50 rounded p-2">
                          <span>{chapter.title}</span>
                          <span className="text-slate-400">
                            {Math.floor(chapter.start / 60)}:{(chapter.start % 60).toString().padStart(2, '0')} - 
                            {Math.floor(chapter.end / 60)}:{(chapter.end % 60).toString().padStart(2, '0')}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex flex-wrap gap-3 pt-4">
                  <button 
                    onClick={() => navigate('/book-builder')}
                    className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                  >
                    <BookOpen className="w-4 h-4 mr-2" />
                    Create Book
                  </button>
                  <button 
                    onClick={() => navigate('/podcast-engine')}
                    className="bg-purple-500 hover:bg-purple-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                  >
                    <GraduationCap className="w-4 h-4 mr-2" />
                    Masterclass
                  </button>
                  <button 
                    onClick={() => navigate('/vault')}
                    className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                  >
                    <Archive className="w-4 h-4 mr-2" />
                    Legacy Archive
                  </button>
                  <button 
                    onClick={() => navigate('/vault')}
                    className="bg-orange-500 hover:bg-orange-600 px-4 py-2 rounded-lg text-white font-semibold transition-colors flex items-center text-sm"
                  >
                    <FileText className="w-4 h-4 mr-2" />
                    View in Vault
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}