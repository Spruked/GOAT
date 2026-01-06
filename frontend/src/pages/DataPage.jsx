import React, { useState } from 'react';
import { BarChart3, Table, Upload, Play, Download } from 'lucide-react';
import axios from 'axios';

export function DataPage() {
  const [data, setData] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [legacyForm, setLegacyForm] = useState({
    productType: 'book',
    title: '',
    author: '',
    description: ''
  });
  const [buildingLegacy, setBuildingLegacy] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setFile(file);
    
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      try {
        if (file.name.endsWith('.json')) {
          const jsonData = JSON.parse(text);
          setData(Array.isArray(jsonData) ? jsonData : [jsonData]);
        } else if (file.name.endsWith('.csv')) {
          // Simple CSV parser
          const lines = text.split('\n');
          const headers = lines[0].split(',');
          const rows = lines.slice(1).map(line => {
            const values = line.split(',');
            const obj = {};
            headers.forEach((header, i) => {
              obj[header.trim()] = values[i]?.trim() || '';
            });
            return obj;
          });
          setData(rows);
        }
      } catch (error) {
        alert('Error parsing file: ' + error.message);
      }
    };
    reader.readAsText(file);
  };

  const exploreData = async () => {
    if (!data.length) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/data/explore', {
        data: data,
        format: 'json'
      }, {
        headers: { 'Authorization': 'Bearer goat_api_key' }
      });
      setAnalysis(response.data);
    } catch (error) {
      alert('Exploration failed: ' + error.response?.data?.detail || error.message);
    }
    setLoading(false);
  };

  const analyzeData = async () => {
    if (!data.length) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/data/analyze', {
        data: data,
        format: 'json'
      }, {
        headers: { 'Authorization': 'Bearer goat_api_key' }
      });
      setAnalysis(response.data);
    } catch (error) {
      alert('Analysis failed: ' + error.response?.data?.detail || error.message);
    }
    setLoading(false);
  };

  const buildLegacy = async () => {
    if (!legacyForm.title || !legacyForm.author) {
      alert('Please fill in title and author');
      return;
    }

    setBuildingLegacy(true);
    try {
      const response = await axios.post('/api/legacy/build', {
        user_id: legacyForm.author.toLowerCase().replace(/\s+/g, '_'),
        author: legacyForm.author,
        title: legacyForm.title,
        product_type: legacyForm.productType,
        data_files: file ? [file.name] : [], // In real implementation, upload files first
        description: legacyForm.description
      }, {
        headers: { 'Authorization': 'Bearer goat_api_key' }
      });

      // Redirect to minting page
      window.location.href = `/mint?legacyId=${response.data.legacy.user_id}_${response.data.legacy.product_type}`;
    } catch (error) {
      alert('Legacy building failed: ' + error.response?.data?.detail || error.message);
    }
    setBuildingLegacy(false);
  };

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <div className="w-16 h-16 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full flex items-center justify-center">
          <BarChart3 className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
          Data Explorer
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Powered by VisiData - Explore, analyze, and visualize your data with advanced terminal-based tools
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h2 className="text-xl font-semibold mb-4 text-cyan-300">Upload Data</h2>
        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg cursor-pointer transition">
            <Upload className="w-5 h-5" />
            <span>Choose File</span>
            <input
              type="file"
              accept=".json,.csv"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
          {file && <span className="text-slate-300">{file.name}</span>}
        </div>
        <p className="text-sm text-slate-500 mt-2">Supports JSON and CSV files</p>
      </div>

      {/* Data Preview */}
      {data.length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl font-semibold mb-4 text-cyan-300">Data Preview</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-600">
                  {Object.keys(data[0]).map(key => (
                    <th key={key} className="text-left p-2 text-cyan-300">{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.slice(0, 5).map((row, i) => (
                  <tr key={i} className="border-b border-slate-700">
                    {Object.values(row).map((value, j) => (
                      <td key={j} className="p-2 text-slate-300">{String(value)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-sm text-slate-500 mt-2">
            Showing {Math.min(5, data.length)} of {data.length} rows
          </p>
        </div>
      )}

      {/* Action Buttons */}
      {data.length > 0 && (
        <div className="flex flex-wrap gap-4">
          <button
            onClick={exploreData}
            disabled={loading}
            className="bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 flex items-center space-x-2 disabled:opacity-50"
          >
            <Table className="w-5 h-5" />
            <span>Explore with VisiData</span>
          </button>
          <button
            onClick={analyzeData}
            disabled={loading}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 flex items-center space-x-2 disabled:opacity-50"
          >
            <BarChart3 className="w-5 h-5" />
            <span>Advanced Analysis</span>
          </button>
        </div>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl font-semibold mb-4 text-cyan-300">Analysis Results</h2>
          
          {analysis.stats && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Basic Statistics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-slate-700 p-3 rounded">
                  <div className="text-2xl font-bold text-cyan-400">{analysis.stats.nRows}</div>
                  <div className="text-sm text-slate-400">Rows</div>
                </div>
                <div className="bg-slate-700 p-3 rounded">
                  <div className="text-2xl font-bold text-cyan-400">{analysis.stats.nCols}</div>
                  <div className="text-sm text-slate-400">Columns</div>
                </div>
                <div className="bg-slate-700 p-3 rounded">
                  <div className="text-2xl font-bold text-cyan-400">{analysis.stats.columns?.length || 0}</div>
                  <div className="text-sm text-slate-400">Fields</div>
                </div>
                <div className="bg-slate-700 p-3 rounded">
                  <div className="text-2xl font-bold text-cyan-400">{analysis.visidata_ready ? 'Yes' : 'No'}</div>
                  <div className="text-sm text-slate-400">VisiData Ready</div>
                </div>
              </div>
            </div>
          )}

          {analysis.analysis && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Detailed Analysis</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-purple-300">Data Shape</h4>
                  <p className="text-slate-300">{analysis.analysis.shape[0]} rows × {analysis.analysis.shape[1]} columns</p>
                </div>
                
                <div>
                  <h4 className="font-semibold text-purple-300">Column Types</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {Object.entries(analysis.analysis.dtypes).map(([col, type]) => (
                      <div key={col} className="text-sm">
                        <span className="text-cyan-300">{col}:</span> {String(type)}
                      </div>
                    ))}
                  </div>
                </div>

                {analysis.analysis.frequency_first_col && (
                  <div>
                    <h4 className="font-semibold text-purple-300">Top Values ({Object.keys(analysis.analysis.frequency_first_col)[0]})</h4>
                    <div className="space-y-1">
                      {Object.entries(analysis.analysis.frequency_first_col).slice(0, 5).map(([value, count]) => (
                        <div key={value} className="flex justify-between text-sm">
                          <span className="text-slate-300">{value}</span>
                          <span className="text-cyan-400">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Legacy Building Section */}
      <div className="bg-gradient-to-r from-purple-900/20 to-cyan-900/20 p-6 rounded-lg border border-purple-600/30">
        <h2 className="text-xl font-semibold mb-4 text-purple-300">Build Your Legacy</h2>
        <p className="text-slate-400 mb-4">
          Transform your analyzed data into a masterpiece. GOAT uses VisiData insights to structure books, courses, and masterclasses that become your permanent legacy.
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Product Type</label>
              <select
                value={legacyForm.productType}
                onChange={(e) => setLegacyForm({...legacyForm, productType: e.target.value})}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
              >
                <option value="book">Book</option>
                <option value="course">Course</option>
                <option value="masterclass">Masterclass</option>
                <option value="framework">Framework</option>
                <option value="archive">Knowledge Archive</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Title</label>
              <input
                type="text"
                placeholder="Your Greatest Work Title"
                value={legacyForm.title}
                onChange={(e) => setLegacyForm({...legacyForm, title: e.target.value})}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white placeholder-slate-400"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Author</label>
              <input
                type="text"
                placeholder="Your Name"
                value={legacyForm.author}
                onChange={(e) => setLegacyForm({...legacyForm, author: e.target.value})}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white placeholder-slate-400"
              />
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Description</label>
              <textarea
                placeholder="Describe your masterpiece..."
                rows={4}
                value={legacyForm.description}
                onChange={(e) => setLegacyForm({...legacyForm, description: e.target.value})}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white placeholder-slate-400"
              />
            </div>

            <button
              onClick={buildLegacy}
              disabled={buildingLegacy}
              className="w-full bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 disabled:opacity-50 px-6 py-3 rounded-lg font-semibold transition"
            >
              {buildingLegacy ? 'Building Your Legacy...' : 'Build My Legacy'}
            </button>
          </div>
        </div>

        <div className="mt-6 p-4 bg-slate-800/50 rounded-lg">
          <h3 className="font-semibold text-cyan-300 mb-2">What Happens Next?</h3>
          <ol className="list-decimal list-inside space-y-1 text-slate-300 text-sm">
            <li>GOAT analyzes your data with VisiData to extract insights</li>
            <li>Caleon guides you through structuring your masterpiece</li>
            <li>Your work is exported as a complete, publishable product</li>
            <li>Mint permanent authorship NFTs via CertSig or TrueMark</li>
            <li>Your legacy lives forever on the blockchain</li>
          </ol>
        </div>
      </div>

      {/* VisiData Info */}
      <div className="bg-gradient-to-r from-slate-800/50 to-slate-900/50 p-6 rounded-lg border border-slate-700">
        <h2 className="text-xl font-semibold mb-4 text-cyan-300">About VisiData Integration</h2>
        <p className="text-slate-400 mb-4">
          VisiData is a powerful terminal-based tool for exploring and manipulating tabular data.
          This integration brings VisiData's capabilities to the web interface, allowing you to:
        </p>
        <ul className="list-disc list-inside space-y-2 text-slate-300">
          <li>Load and explore data from various formats (CSV, JSON, SQL, etc.)</li>
          <li>Perform complex data transformations and analysis</li>
          <li>Create visualizations and frequency tables</li>
          <li>Filter, sort, and pivot data with ease</li>
          <li>Export results in multiple formats</li>
        </ul>
        <p className="text-slate-400 mt-4">
          For full VisiData functionality, you can also run it directly in your terminal with:
          <code className="bg-slate-700 px-2 py-1 rounded text-sm ml-2">vd your_data_file</code>
        </p>
      </div>
    </div>
  );
}