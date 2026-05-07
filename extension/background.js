const API_BASE = 'http://127.0.0.1:8000/api/v1';

// Listen for tab URL changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const url = tab.url;
    
    // Skip chrome:// and extension pages
    if (url.startsWith('chrome://') || url.startsWith('chrome-extension://')) {
      return;
    }
    
    analyzeUrl(tabId, url);
  }
});

async function analyzeUrl(tabId, url) {
  try {
    // Submit job to Fraudar backend
    const jobResponse = await fetch(`${API_BASE}/jobs/analyze/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    
    const jobData = await jobResponse.json();
    const jobId = jobData.job_id;
    
    // Poll for result
    const result = await pollResult(jobId);
    
    if (result) {
      const score = result.risk_score;
      
      // Store result for popup to display
      chrome.storage.local.set({
        [url]: {
          score,
          verdict: result.verdict,
          virustotal: result.virustotal,
          timestamp: Date.now()
        }
      });
      
      // Set badge color and text based on score
      let badgeColor = '#22c55e'; // green = safe
      if (score >= 70) badgeColor = '#ef4444'; // red = dangerous
      else if (score >= 40) badgeColor = '#f97316'; // orange = suspicious
      
      chrome.action.setBadgeText({ text: String(score), tabId });
      chrome.action.setBadgeBackgroundColor({ color: badgeColor, tabId });
    }
  } catch (error) {
    console.error('Fraudar analysis error:', error);
  }
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