import { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'https://fraudar-api.onrender.com/api/v1';

interface AnalysisResult {
  source: string;
  content_preview: string;
  similar_known_scams: Array<{
    pattern: string;
    scam_type: string;
    source: string;
    similarity_score: number;
  }>;
  analysis: {
    scam_probability: number;
    scam_type: string;
    red_flags: string[];
    explanation: string;
    recommended_action: string;
  };
}

function getScoreColor(score: number): string {
  if (score >= 70) return '#ef4444';
  if (score >= 40) return '#f97316';
  return '#22c55e';
}

function getVerdictLabel(score: number): string {
  if (score >= 70) return '🚨 DANGEROUS';
  if (score >= 40) return '⚠️ SUSPICIOUS';
  return '✅ LIKELY SAFE';
}

function App() {
  const [inputText, setInputText] = useState('');
  const [inputUrl, setInputUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'text' | 'url'>('text');

  const pollJobResult = async (jobId: string): Promise<AnalysisResult> => {
    while (true) {
      const response = await axios.get(`${API_BASE}/jobs/${jobId}`);
      if (response.data.status === 'completed') return response.data.result;
      if (response.data.status === 'failed') throw new Error('Analysis failed');
      await new Promise(res => setTimeout(res, 2000));
    }
  };

  const handleAnalyze = async () => {
    if (!inputText && !inputUrl) {
      setError('Please enter text or a URL to analyze.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      let jobResponse;
      if (activeTab === 'text') {
        jobResponse = await axios.post(`${API_BASE}/jobs/analyze/text`, { text: inputText });
      } else {
        jobResponse = await axios.post(`${API_BASE}/jobs/analyze/url`, { url: inputUrl });
      }

      const analysisResult = await pollJobResult(jobResponse.data.job_id);
      setResult(analysisResult);
    } catch (err) {
      setError('Analysis failed. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🛡️ Fraudar</h1>
        <p>Real-time scam and fraud detection</p>
      </header>

      <main className="main">
        <div className="card">
          <div className="tabs">
            <button
              className={activeTab === 'text' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('text')}
            >
              Analyze Text / Email
            </button>
            <button
              className={activeTab === 'url' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('url')}
            >
              Analyze URL
            </button>
          </div>

          {activeTab === 'text' ? (
            <textarea
              className="input"
              placeholder="Paste suspicious email, job posting, or message here..."
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              rows={6}
            />
          ) : (
            <input
              className="input"
              type="text"
              placeholder="https://suspicious-site.com"
              value={inputUrl}
              onChange={e => setInputUrl(e.target.value)}
            />
          )}

          {error && <p className="error">{error}</p>}

          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? '🔍 Analyzing...' : '🔍 Analyze Now'}
          </button>
        </div>

        {result && (
          <div className="card results">
            <div className="score-section">
              <div
                className="score-circle"
                style={{ borderColor: getScoreColor(result.analysis.scam_probability) }}
              >
                <span
                  className="score-number"
                  style={{ color: getScoreColor(result.analysis.scam_probability) }}
                >
                  {result.analysis.scam_probability}
                </span>
                <span className="score-label">/ 100</span>
              </div>
              <div className="score-info">
                <h2 style={{ color: getScoreColor(result.analysis.scam_probability) }}>
                  {getVerdictLabel(result.analysis.scam_probability)}
                </h2>
                <p className="scam-type">Type: {result.analysis.scam_type.replace('_', ' ').toUpperCase()}</p>
                <p className="recommended-action">
                  Action: {result.analysis.recommended_action.replace('_', ' ').toUpperCase()}
                </p>
              </div>
            </div>

            <div className="section">
              <h3>🚩 Red Flags</h3>
              <ul className="red-flags">
                {result.analysis.red_flags.map((flag, i) => (
                  <li key={i}>{flag}</li>
                ))}
              </ul>
            </div>

            <div className="section">
              <h3>📋 Explanation</h3>
              <p>{result.analysis.explanation}</p>
            </div>

            {result.similar_known_scams && result.similar_known_scams.length > 0 && (
              <div className="section">
                <h3>🗄️ Similar Known Scams (from FTC & FBI IC3)</h3>
                {result.similar_known_scams.map((scam, i) => (
                  <div key={i} className="scam-match">
                    <span className="scam-match-type">{scam.scam_type.replace('_', ' ')}</span>
                    <span className="scam-match-source">{scam.source}</span>
                    <span className="scam-match-score">
                      {Math.round(scam.similarity_score * 100)}% match
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;