// frontend/src/App.js (已修正)
import React, { useState } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState("尚未选择文件");
  const [targetLang, setTargetLang] = useState('中文');
  const [commentedCode, setCommentedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    // --- 这是关键的修改点 ---
    // event.target.files 是一个文件列表 (FileList)
    // 我们需要获取列表中的第一个文件，即 event.target.files[0]
    const file = event.target.files[0];

    if (file) {
      // 将单个文件对象存入 state，而不是整个列表
      setSelectedFile(file);
      // 现在 file.name 可以正确获取到文件名
      setFileName(file.name);
    }
  };

  const handleLanguageChange = (event) => {
    setTargetLang(event.target.value);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('请先选择一个代码文件！');
      return;
    }

    setIsLoading(true);
    setError('');
    setCommentedCode('');

    const formData = new FormData();
    // 现在 selectedFile 是一个正确的文件对象，可以被正确附加
    formData.append('file', selectedFile);
    formData.append('targetLang', targetLang);

    try {
      const response = await axios.post('http://localhost:5001/api/comment', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setCommentedCode(response.data.commentedCode);
    } catch (err) {
      const errorMessage = err.response?.data?.error || '生成注释时发生未知错误，请检查后端服务是否正常运行。';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!commentedCode || !selectedFile) return;
    const blob = new Blob([commentedCode], { type: 'text/plain;charset=utf-8' });
    saveAs(blob, `commented_${selectedFile.name}`);
  };

  return (
      <div className="App">
        <header className="App-header">
          <h1>智能代码注释生成器</h1>
          <p className="subtitle">上传您的代码文件，AI 将为您生成清晰的注释</p>
        </header>
        <main className="main-content">
          <div className="controls-card">
            <div className="file-upload-wrapper">
              <button className="btn-upload" onClick={() => document.getElementById('fileInput').click()}>选择文件</button>
              <span className="file-name">{fileName}</span>
              <input id="fileInput" type="file" hidden onChange={handleFileChange} />
            </div>

            <div className="language-selector-wrapper">
              <label htmlFor="language">注释语言：</label>
              <select id="language" value={targetLang} onChange={handleLanguageChange}>
                <option value="中文">中文</option>
                <option value="英文">English</option>
                <option value="日文">日本語</option>
              </select>
            </div>

            <button className="btn-submit" onClick={handleSubmit} disabled={isLoading}>
              {isLoading ? '正在生成中...' : '生成注释'}
            </button>
          </div>

          {error && <p className="error-message">{error}</p>}

          <div className="result-container">
            <h2>生成结果</h2>
            <textarea
                value={commentedCode}
                readOnly
                placeholder="生成的带注释的代码将显示在这里..."
            />
            {commentedCode && (
                <button className="btn-download" onClick={handleDownload}>下载已注释的文件</button>
            )}
          </div>
        </main>
      </div>
  );
}

export default App;