import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [files, setFiles] = useState([null, null, null]);

  const handleFileChange = (index, event) => {
    const newFiles = [...files];
    newFiles[index] = event.target.files[0];
    setFiles(newFiles);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Banking Parser</h1>
        <div className='file-upload-container'>
          {[0, 1, 2].map(index => (
            <div key={index} className="file-input">
              <label
                htmlFor={`file-input-${index}`}
                className={`custom-file-upload ${files[index] ? 'file-selected' : '' // Apply conditional class for styling
                  }`}
              >
                Upload File {index + 1}:
              </label>
              <input
                type="file"
                id={`file-input-${index}`}
                onChange={(e) => handleFileChange(index, e)}
                className="file-input-hidden"
              />
              {/* {files[index] && <span className="file-name">{files[index].name}</span>} */}

            </div>

          ))}
        </div>
        <button className="upload-button">Upload Files</button>
      </header>
    </div>
  );
}

export default App;
