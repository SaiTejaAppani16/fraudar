const API_BASE = 'http://127.0.0.1:8000/api/v1';

function getScoreColor(score) {
  if (score >= 70) return '#ef4444';
  if (score >= 40) return '#f97316';
  return '#22c55e';
}

function getVerdictLabel(score) {
  if (score >= 70) return '🚨 DANGEROUS';
  if (score >= 40) return '⚠️ SUSPICIOUS';
  return '✅ SAFE';
}

function showState(stateId) {
  ['loading', 'result', 'error'].forEach(id => {
    document.getElementById(id).classList.add('hidden');
  });
  document.getElementById(stateId).classList.remove('hidden');
}

async function analyzeCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  if (url.startsWith('chrome://') || url.startsWith('chrome-extension://')) {
    showState('error');
    return;
  }

  // Check if we already have a cached result
  chrome.storage.local.get([url], async (cached) => {
    if (cached[url]) {
      displayUrlResult(cached[url], url);
      return;
    }

    // No cache — submit new job
    showState('loading');
    try {
      const jobResponse = await fetch(`${API_BASE}/jobs/analyze/url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      const jobData = await jobResponse.json();
      const result = await pollResult(jobData.job_id);

      if (result) {
        chrome.storage.local.set({ [url]: { ...result, timestamp: Date.now() } });
        displayUrlResult(result, url);
      } else {
        showState('error');
      }
    } catch (err) {
      showState('error');
    }
  });
}

async function pollResult(jobId, maxAttempts = 15) {
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(res => setTimeout(res, 2000));
    const response = await fetch(`${API_BASE}/jobs/${jobId}`);
    const data = await response.json();
    if (data.status === 'completed') return data.result;
    if (data.status === 'failed') return null;
  }
  return null;
}

function displayUrlResult(result, url) {
  const score = result.risk_score || result.score || 0;
  const color = getScoreColor(score);

  const scoreCircle = document.getElementById('score-circle');
  scoreCircle.style.borderColor = color;
  document.getElementById('score-value').textContent = score;
  document.getElementById('score-value').style.color = color;

  const verdict = document.getElementById('verdict');
  verdict.textContent = getVerdictLabel(score);
  verdict.style.color = color;

  // VirusTotal results
  if (result.virustotal) {
    const vt = result.virustotal;
    document.getElementById('vt-results').innerHTML = `
      <div class="vt-stat danger">🔴 ${vt.malicious} malicious</div>
      <div class="vt-stat warning">🟡 ${vt.suspicious} suspicious</div>
      <div class="vt-stat safe">🟢 ${vt.harmless} harmless</div>
    `;
  }

  // Google Safe Browsing result
  const gsb = result.google_safe_browsing;
  if (gsb) {
    const gsbEl = document.getElementById('gsb-result');
    if (gsb.is_threat) {
      gsbEl.innerHTML = `<span class="threat">⚠️ Threat detected: ${gsb.threats.join(', ')}</span>`;
    } else {
      gsbEl.innerHTML = `<span class="safe-text">✅ No threats detected</span>`;
    }
  }

  // URL display
  const shortUrl = url.length > 40 ? url.substring(0, 40) + '...' : url;
  document.getElementById('url-display').textContent = shortUrl;

  showState('result');
}

// Run on popup open
analyzeCurrentTab();