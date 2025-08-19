import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [generatedCode, setGeneratedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPreview, setShowPreview] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError('');
      setGeneratedCode('');
      setShowPreview(false);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError('');
      setGeneratedCode('');
      setShowPreview(false);
    }
  };

  const generateUI = async () => {
    if (!selectedFile) {
      setError('Please select an image file first');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('/generate-ui', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setGeneratedCode(response.data.html_code);
        setShowPreview(true); // Show preview by default
      } else {
        setError(response.data.error || 'Failed to generate UI');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while generating UI');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadCode = () => {
    const blob = new Blob([generatedCode], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated-ui.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GenUI</h1>
      </header>

      <main className="App-main">
        {/* Error Display */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Top Section - Upload and Image Preview */}
        <div className={`top-section ${selectedFile ? 'has-preview' : 'upload-only'}`}>
          {/* Left Column - Upload */}
          <div className="upload-column">
            <div className="upload-section">
              <h2>Upload Image</h2>
              <div
                className="upload-area"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="file-input"
                  id="file-input"
                />
                <label htmlFor="file-input" className="upload-label">
                  {selectedFile ? (
                    <div className="file-selected">
                      <span>{selectedFile.name}</span>
                    </div>
                  ) : (
                    <div className="upload-placeholder">
                      <p>Click to upload or drag & drop your wireframe image</p>
                      <small>Supports PNG, JPG, JPEG, GIF, BMP</small>
                    </div>
                  )}
                </label>
              </div>

              <button
                onClick={generateUI}
                disabled={!selectedFile || isLoading}
                className="generate-btn"
              >
                {isLoading ? 'Generating...' : 'Generate UI Code'}
              </button>
            </div>
          </div>

          {/* Right Column - Image Preview (only when image is uploaded) */}
          {selectedFile && (
            <div className="preview-column">
              <div className="preview-container">
                <h2>Image Preview</h2>
                <img
                  src={URL.createObjectURL(selectedFile)}
                  alt="Preview"
                  className="image-preview"
                />
              </div>
            </div>
          )}
        </div>

        {/* Bottom Section - Generated UI Output (only show when code is generated) */}
        {generatedCode && (
          <div className="bottom-section">
            <div className="results-section">
              <div className="results-header">
                <h2>Generated UI</h2>
                <div className="action-buttons">
                  <button onClick={downloadCode} className="download-btn">
                    Download Code
                  </button>
                  <button
                    onClick={() => setShowPreview(!showPreview)}
                    className="preview-btn"
                  >
                    {showPreview ? 'Show Code' : 'Show Preview'}
                  </button>
                </div>
              </div>

              {showPreview ? (
                <div className="preview-section">
                  <iframe
                    srcDoc={generatedCode}
                    title="Generated UI Preview"
                    className="preview-iframe"
                    sandbox="allow-same-origin"
                  />
                </div>
              ) : (
                <div className="code-section">
                  <pre className="code-block">
                    <code>{generatedCode}</code>
                  </pre>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
