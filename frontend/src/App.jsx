import React, { useState, useEffect, useRef } from 'react';
import { 
  Rocket, Sparkles, Search, Compass, DollarSign, 
  ClipboardList, CheckCircle2, AlertCircle, Key, 
  RefreshCw, Copy, Download, LayoutDashboard, Cpu, Target, 
  TrendingUp, ShieldCheck, Layers, Globe, Printer, Zap, Activity, Briefcase
} from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, BarChart, Bar
} from 'recharts';

export default function App() {
  // Input fields
  const [idea, setIdea] = useState('');
  const [industry, setIndustry] = useState('AI');
  const [targetAudience, setTargetAudience] = useState('');
  const [monetization, setMonetization] = useState('SaaS Subscription');
  const [customKey, setCustomKey] = useState('');
  const [appToken, setAppToken] = useState('');

  // Execution states
  const [sessionId, setSessionId] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, generating, completed, failed
  const [currentStep, setCurrentStep] = useState('');
  const [progressPercent, setProgressPercent] = useState(0);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  // Result data
  const [results, setResults] = useState({
    idea_analysis: null,
    competitor_research: null,
    feature_plan: null,
    business_plan: null,
    final_report: null
  });

  // Detailed agent state indicators
  const [agentStatuses, setAgentStatuses] = useState(null);

  // UI state
  const [activeTab, setActiveTab] = useState('concept');
  const [copied, setCopied] = useState(false);
  const pollInterval = useRef(null);

  // History state
  const [historyList, setHistoryList] = useState([]);

  // Fetch history list from backend
  const fetchHistory = async () => {
    try {
      const response = await fetch('/api/history');
      if (response.ok) {
        const data = await response.json();
        setHistoryList(data);
      }
    } catch (e) {
      console.error("Failed to load history list:", e);
    }
  };

  // Load a past session details
  const loadPastSession = async (pastSessionId) => {
    setError(null);
    setStatus('idle');
    setSessionId(pastSessionId);
    try {
      const response = await fetch(`/api/plan-status/${pastSessionId}`);
      if (response.ok) {
        const data = await response.json();
        setResults({
          idea_analysis: parseJsonSafely(data.idea_analysis),
          competitor_research: parseJsonSafely(data.competitor_research),
          feature_plan: parseJsonSafely(data.feature_plan),
          business_plan: parseJsonSafely(data.business_plan),
          final_report: data.final_report
        });
        setAgentStatuses(data.agent_statuses || {
          planner: "completed",
          idea_analyzer: "completed",
          competitor_researcher: "completed",
          feature_planner: "completed",
          business_planner: "completed",
          synthesizer: "completed"
        });
        setStatus(data.status);
        setProgressPercent(data.progress_percent);
        setCurrentStep(data.current_step || 'Loaded Past Session');
        if (data.status === 'failed' || data.status === 'paused') {
          setError(data.error || 'The loaded session was not completed successfully.');
        } else {
          showSuccessNotification("Successfully restored past session details.");
        }
        setActiveTab('concept');
      } else {
        throw new Error("Could not retrieve past analysis session.");
      }
    } catch (err) {
      setError(err.message);
      setStatus('failed');
    }
  };

  // Poll status from backend
  const checkStatus = async (id) => {
    try {
      const response = await fetch(`/api/plan-status/${id}`);
      if (!response.ok) {
        throw new Error('Failed to retrieve generation status.');
      }
      
      const data = await response.json();
      
      // Update intermediate state variables
      setStatus(data.status);
      setCurrentStep(data.current_step);
      setProgressPercent(data.progress_percent);
      setAgentStatuses(data.agent_statuses || null);
      
      // Update result payloads
      setResults({
        idea_analysis: parseJsonSafely(data.idea_analysis),
        competitor_research: parseJsonSafely(data.competitor_research),
        feature_plan: parseJsonSafely(data.feature_plan),
        business_plan: parseJsonSafely(data.business_plan),
        final_report: data.final_report
      });

      if (data.status === 'completed') {
        clearInterval(pollInterval.current);
        showSuccessNotification("Market strategy & business blueprint successfully synthesized!");
        fetchHistory();
      } else if (data.status === 'failed') {
        setError(data.error || 'The orchestration agents encountered an error.');
        clearInterval(pollInterval.current);
        fetchHistory();
      } else if (data.status === 'paused') {
        setError(data.error || 'The orchestration agents are paused.');
        clearInterval(pollInterval.current);
        fetchHistory();
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
      setStatus('failed');
      clearInterval(pollInterval.current);
    }
  };

  // Safe JSON parsing helper
  const parseJsonSafely = (raw) => {
    if (!raw) return null;
    if (typeof raw === 'object') return raw;
    try {
      let clean = raw.trim();
      if (clean.startsWith('```json')) {
        clean = clean.substring(7);
      }
      if (clean.startsWith('```')) {
        clean = clean.substring(3);
      }
      if (clean.endsWith('```')) {
        clean = clean.substring(0, clean.length - 3);
      }
      return JSON.parse(clean.trim());
    } catch (e) {
      console.warn('Failed to parse agent output JSON:', e);
      return { raw_content: raw };
    }
  };

  // Handle Form Submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setStatus('generating');
    setProgressPercent(10);
    setCurrentStep('Contacting FastAPI Backend...');
    setAgentStatuses(null);
    setResults({
      idea_analysis: null,
      competitor_research: null,
      feature_plan: null,
      business_plan: null,
      final_report: null
    });

    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (appToken) {
        headers['X-Startup-Studio-Token'] = appToken;
      }

      const payload = {
        idea,
        industry,
        target_audience: targetAudience || 'General Public',
        monetization,
        custom_gemini_key: customKey || null
      };

      const response = await fetch('/api/generate-plan', {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });

      if (response.status === 429) {
        throw new Error('Rate limit exceeded. You can only generate 5 business plans per minute.');
      }

      if (!response.ok) {
        const errData = await response.json();
        let errorMessage = 'Failed to submit startup idea to agents.';
        if (errData.detail) {
          if (typeof errData.detail === 'string') {
            errorMessage = errData.detail;
          } else if (Array.isArray(errData.detail)) {
            errorMessage = errData.detail
              .map((err) => {
                const field = err.loc ? err.loc[err.loc.length - 1] : 'field';
                return `${field}: ${err.msg}`;
              })
              .join('; ');
          } else if (typeof errData.detail === 'object') {
            errorMessage = JSON.stringify(errData.detail);
          }
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setSessionId(data.session_id);
      
      // Start polling
      pollInterval.current = setInterval(() => checkStatus(data.session_id), 2000);
    } catch (err) {
      setError(err.message);
      setStatus('failed');
    }
  };

  // Show a success notification
  const showSuccessNotification = (msg) => {
    setNotification(msg);
    setTimeout(() => {
      setNotification(null);
    }, 4500);
  };

  // Load history list on mount and cleanup polling on unmount
  useEffect(() => {
    fetchHistory();
    return () => {
      if (pollInterval.current) clearInterval(pollInterval.current);
    };
  }, []);

  // Utility to copy report to clipboard
  const copyToClipboard = () => {
    if (!results.final_report) return;
    navigator.clipboard.writeText(results.final_report);
    setCopied(true);
    showSuccessNotification("Markdown business report copied to clipboard!");
    setTimeout(() => setCopied(false), 2000);
  };

  // Utility to download report as markdown file
  const downloadMarkdown = () => {
    if (!results.final_report) return;
    const element = document.createElement("a");
    const file = new Blob([results.final_report], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = `${industry.toLowerCase()}-business-plan.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showSuccessNotification("Downloading business blueprint markdown file.");
  };

  // Select a preset sample card
  const selectSample = (ind, aud, mon, desc) => {
    setIdea(desc);
    setIndustry(ind);
    setTargetAudience(aud);
    setMonetization(mon);
    setCustomKey('mock');
    showSuccessNotification(`Preset loaded: ${ind} category.`);
  };

  // Roadmap helper classes
  const getStepClass = (agentKey, fallbackRunning) => {
    const s = agentStatuses?.[agentKey];
    if (s === 'completed') return 'completed';
    if (s === 'running') return 'active';
    if (s === 'pending') return '';
    if (status === 'generating' && fallbackRunning) return 'active';
    if (status === 'completed' || results.final_report) return 'completed';
    return '';
  };

  const getStepBadgeClass = (agentKey, fallbackRunning) => {
    const s = agentStatuses?.[agentKey];
    if (s === 'completed') return 'badge-completed';
    if (s === 'running') return 'badge-running';
    if (s === 'pending') return 'badge-pending';
    if (status === 'generating' && fallbackRunning) return 'badge-running';
    if (status === 'completed') return 'badge-completed';
    return 'badge-pending';
  };

  const getStepBadgeLabel = (agentKey, fallbackRunning) => {
    const s = agentStatuses?.[agentKey];
    if (s === 'completed') return '✓ Done';
    if (s === 'running') return '● Running';
    if (s === 'pending') return 'Pending';
    if (status === 'generating' && fallbackRunning) return '● Running';
    if (status === 'completed') return '✓ Done';
    return 'Pending';
  };

  // Chart Helper Calculations
  const getSwotRadarData = () => {
    if (results.idea_analysis?.swot_radar_data) {
      return results.idea_analysis.swot_radar_data;
    }
    return [
      { subject: 'Market Opportunity', value: 85 },
      { subject: 'Execution Feasibility', value: 70 },
      { subject: 'Technology Advantage', value: 75 },
      { subject: 'Financial Viability', value: 80 },
      { subject: 'Defensibility', value: 65 }
    ];
  };

  const getMarketGrowthProjection = () => {
    if (results.competitor_research?.market_growth_projection) {
      return results.competitor_research.market_growth_projection;
    }
    const cagr = results.competitor_research?.market_stats?.cagr_percent || 15;
    const base = results.competitor_research?.market_stats?.market_size_billions || 100;
    const data = [];
    let size = base;
    for (let i = 0; i < 5; i++) {
      const year = 2026 + i;
      data.push({ year: String(year), market_size: parseFloat(size.toFixed(1)) });
      size = size * (1 + cagr / 100);
    }
    return data;
  };

  const getCompetitorComparisonScores = () => {
    if (results.competitor_research?.competitor_comparison_scores) {
      return results.competitor_research.competitor_comparison_scores;
    }
    const comps = results.competitor_research?.competitors || [];
    const data = [{ name: 'Us (Target)', market_share: 5, pricing_score: 85, feature_score: 90 }];
    comps.forEach((c, idx) => {
      data.push({
        name: c.name.length > 12 ? c.name.substring(0, 10) + '..' : c.name,
        market_share: idx === 0 ? 45 : 25,
        pricing_score: idx === 0 ? 60 : 50,
        feature_score: idx === 0 ? 70 : 65
      });
    });
    return data;
  };

  const getRoadmapTimeline = () => {
    if (results.feature_plan?.roadmap_timeline) {
      return results.feature_plan.roadmap_timeline;
    }
    const roadmap = results.feature_plan?.roadmap || [];
    if (roadmap.length > 0) {
      return roadmap.map((r, idx) => ({
        name: r.phase ? r.phase.split(':')[0] : `Phase ${idx+1}`,
        start: idx * 3,
        duration: 3
      }));
    }
    return [
      {"name": "Phase 1: Foundation", "start": 0, "duration": 3},
      {"name": "Phase 2: MVP Launch", "start": 3, "duration": 3},
      {"name": "Phase 3: Scale & Expand", "start": 6, "duration": 4}
    ];
  };

  const getFinancialForecast = () => {
    if (results.business_plan?.financial_forecast) {
      return results.business_plan.financial_forecast;
    }
    return [
      { year: 'Year 1', revenue: 100000, costs: 120000 },
      { year: 'Year 2', revenue: 350000, costs: 220000 },
      { year: 'Year 3', revenue: 900000, costs: 500000 },
      { year: 'Year 4', revenue: 2100000, costs: 1000000 },
      { year: 'Year 5', revenue: 4500000, costs: 1800000 }
    ];
  };

  // Custom Inline Markdown Formatter
  const parseInlineFormatting = (text) => {
    if (!text) return '';
    const parts = text.split('**');
    return parts.map((part, i) => {
      if (i % 2 === 1) return <strong key={i} style={{ color: 'var(--text-bright)', fontWeight: '700' }}>{part}</strong>;
      return part;
    });
  };

  // Custom Report Markdown Parser
  const renderMarkdown = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    let inList = false;
    let listItems = [];
    let inTable = false;
    let tableRows = [];
    const rendered = [];

    const flushList = (key) => {
      if (listItems.length > 0) {
        rendered.push(<ul key={`list-${key}`} className="report-ul">{listItems}</ul>);
        listItems = [];
      }
      inList = false;
    };

    const flushTable = (key) => {
      if (tableRows.length > 0) {
        const headers = tableRows[0];
        const dataRows = tableRows.slice(1).filter(r => !r.every(cell => cell.trim().startsWith('---') || cell.trim() === ''));
        rendered.push(
          <div key={`table-wrapper-${key}`} className="report-table-wrapper">
            <table className="report-table">
              <thead>
                <tr>
                  {headers.map((h, i) => <th key={i}>{h.trim()}</th>)}
                </tr>
              </thead>
              <tbody>
                {dataRows.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex}>{parseInlineFormatting(cell.trim())}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        tableRows = [];
      }
      inTable = false;
    };

    lines.forEach((line, index) => {
      const trimmed = line.trim();
      
      // List parsing
      if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
        if (inTable) flushTable(index);
        inList = true;
        const content = trimmed.substring(2);
        listItems.push(<li key={index} className="report-li">{parseInlineFormatting(content)}</li>);
        return;
      } else if (inList && trimmed !== '') {
        // Continue list if line is not empty and not heading/divider/table
        if (!trimmed.startsWith('|') && !trimmed.startsWith('#') && trimmed !== '---') {
          listItems.push(<span key={index} className="report-list-span"> {parseInlineFormatting(trimmed)}</span>);
          return;
        } else {
          flushList(index);
        }
      } else if (inList) {
        flushList(index);
      }

      // Table parsing
      if (trimmed.startsWith('|')) {
        if (inList) flushList(index);
        inTable = true;
        const parts = line.split('|').slice(1, -1);
        tableRows.push(parts);
        return;
      } else if (inTable) {
        flushTable(index);
      }

      // Headings and other blocks
      if (trimmed.startsWith('### ')) {
        rendered.push(<h3 key={index} className="report-h3">{trimmed.substring(4)}</h3>);
      } else if (trimmed.startsWith('## ')) {
        rendered.push(<h2 key={index} className="report-h2">{trimmed.substring(3)}</h2>);
      } else if (trimmed.startsWith('# ')) {
        rendered.push(<h1 key={index} className="report-h1">{trimmed.substring(2)}</h1>);
      } else if (trimmed === '---') {
        rendered.push(<hr key={index} className="report-hr" />);
      } else if (trimmed !== '') {
        rendered.push(<p key={index} className="report-p">{parseInlineFormatting(trimmed)}</p>);
      }
    });

    if (inList) flushList(lines.length);
    if (inTable) flushTable(lines.length);

    return rendered;
  };

  return (
    <div className="app-container">
      {/* Success Notification Alert */}
      {notification && (
        <div className="success-toast" role="alert" aria-live="polite">
          <CheckCircle2 style={{ width: '16px', height: '16px', color: 'var(--accent-emerald)' }} />
          <span>{notification}</span>
        </div>
      )}

      {/* Top Header */}
      <header className="app-header">
        <div className="logo" tabIndex={0} aria-label="Startup Studio AI Logo">
          <div className="logo-icon">
            <Rocket style={{ width: '18px', height: '18px' }} />
          </div>
          <span className="logo-text">Startup Studio AI</span>
        </div>
        <div className="header-badge" tabIndex={0} aria-label="Kaggle Agent Engine Active">
          <span className="badge-dot" aria-hidden="true"></span>
          Kaggle Agent Engine Active
        </div>
      </header>

      {/* Main Layout Grid */}
      <main className="dashboard-grid">
        {/* Sidebar Inputs */}
        <section className="glass-container sidebar-panel" aria-label="Startup Configuration Form">
          <div className="sidebar-header">
            <Cpu className="logo-icon" style={{ width: '20px', height: '20px', margin: 0, boxShadow: 'none', background: 'transparent', color: 'var(--accent-indigo)' }} />
            <h2 className="sidebar-title">Startup Config</h2>
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div className="form-group">
              <label htmlFor="elevator-idea" className="form-label">
                <ClipboardList style={{ width: '13px' }} /> Elevator Description
              </label>
              <textarea 
                id="elevator-idea"
                className="form-textarea" 
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="Explain what your startup does, the core problem it solves, and how it works..."
                required
                disabled={status === 'generating'}
                aria-required="true"
                aria-describedby="idea-helper-text"
              />
              <span id="idea-helper-text" className="form-helper">Minimum 10 characters. Detail your vision to yield higher fidelity output.</span>
            </div>

            <div className="form-group">
              <label htmlFor="industry-select" className="form-label">
                <Globe style={{ width: '13px' }} /> Industry Category
              </label>
              <select 
                id="industry-select"
                className="form-select"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                disabled={status === 'generating'}
              >
                <option value="AI">Artificial Intelligence & LLMs</option>
                <option value="Healthcare">Healthcare & Biotech</option>
                <option value="E-commerce">E-Commerce & Retail</option>
                <option value="Fintech">Financial Technology</option>
                <option value="General">Other / General SaaS</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="audience-input" className="form-label">
                <Target style={{ width: '13px' }} /> Target Customer base
              </label>
              <input 
                id="audience-input"
                type="text" 
                className="form-input"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                placeholder="e.g. Small business owners, freelancers"
                disabled={status === 'generating'}
              />
            </div>

            <div className="form-group">
              <label htmlFor="monetization-select" className="form-label">
                <DollarSign style={{ width: '13px' }} /> Monetization Model
              </label>
              <select 
                id="monetization-select"
                className="form-select"
                value={monetization}
                onChange={(e) => setMonetization(e.target.value)}
                disabled={status === 'generating'}
              >
                <option value="SaaS Subscription">Monthly Subscription (SaaS)</option>
                <option value="Transactional">Transaction / Payment Cut</option>
                <option value="Freemium">Freemium Model</option>
                <option value="Ad-supported">Advertising / Data monetization</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="api-key-input" className="form-label">
                <Key style={{ width: '13px' }} /> Gemini API Key (Optional)
              </label>
              <input 
                id="api-key-input"
                type="password" 
                className="form-input"
                value={customKey}
                onChange={(e) => setCustomKey(e.target.value)}
                placeholder="AI key fallback bypass (AI.google.dev)"
                disabled={status === 'generating'}
                autoComplete="new-password"
                aria-describedby="api-key-helper"
              />
              <span id="api-key-helper" className="form-helper">Input your Gemini API key, or type <b>mock</b> to run the demo simulation instantly.</span>
            </div>

            <div className="form-group">
              <label htmlFor="app-token-input" className="form-label">
                <ShieldCheck style={{ width: '13px' }} /> App Token Access (Optional)
              </label>
              <input 
                id="app-token-input"
                type="password" 
                className="form-input"
                value={appToken}
                onChange={(e) => setAppToken(e.target.value)}
                placeholder="X-Startup-Studio-Token"
                disabled={status === 'generating'}
                autoComplete="new-password"
              />
            </div>

            <button 
              type="submit" 
              className="btn-primary"
              disabled={status === 'generating' || idea.length < 10}
              aria-label={status === 'generating' ? "Running Agents..." : "Synthesize Business Plan"}
            >
              {status === 'generating' ? (
                <>
                  <div className="spinner-container" style={{ width: '16px', height: '16px' }} aria-hidden="true">
                    <div className="double-spinner-outer" style={{ borderWidth: '2px' }}></div>
                    <div className="double-spinner-inner" style={{ borderWidth: '2px' }}></div>
                  </div>
                  Running Agents...
                </>
              ) : (
                <>
                  <Rocket style={{ width: '16px', height: '16px' }} aria-hidden="true" />
                  Synthesize Plan
                </>
              )}
            </button>
          </form>

          {/* History Navigation List */}
          {historyList.length > 0 && (
            <div className="history-section">
              <h3 className="history-section-title">
                <Activity style={{ width: '13px', height: '13px', color: 'var(--accent-indigo)' }} /> Past Analyses
              </h3>
              <div className="history-list" role="navigation" aria-label="Past synthesized sessions">
                {historyList.map((item) => (
                  <button 
                    type="button" 
                    key={item.session_id} 
                    className={`history-item ${sessionId === item.session_id ? 'active' : ''}`}
                    onClick={() => loadPastSession(item.session_id)}
                    aria-label={`Restore session from ${item.timestamp} for ${item.raw_idea_preview}`}
                  >
                    <div className="history-item-title">{item.raw_idea_preview}</div>
                    <div className="history-item-meta">
                      <span>{item.industry}</span>
                      <span>{item.timestamp?.split(' ')[0]}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Content Viewer Panel */}
        <section className="content-panel" aria-label="Startup Planning Dashboard Workspace">
          {/* Real-time Status Banner */}
          {status === 'generating' && (
            <div className="status-banner" role="status" aria-live="assertive">
              <div className="status-info">
                <div className="spinner-container" aria-hidden="true">
                  <div className="double-spinner-outer"></div>
                  <div className="double-spinner-inner"></div>
                </div>
                <div>
                  <h4 className="status-text-title">Orchestration: {currentStep}</h4>
                  <p className="status-text-desc">Workflow graph executing sequential agent reasoning nodes</p>
                </div>
              </div>
              <span className="progress-number">{progressPercent}%</span>
            </div>
          )}

          {(status === 'failed' || status === 'paused') && (
            <div className="status-banner" style={{ borderColor: status === 'paused' ? 'var(--accent-purple)' : 'var(--accent-rose)', background: status === 'paused' ? 'rgba(139, 92, 246, 0.1)' : 'rgba(244, 63, 94, 0.1)' }} role="alert">
              <div className="status-info">
                <AlertCircle style={{ color: status === 'paused' ? 'var(--accent-purple)' : 'var(--accent-rose)', width: '28px', height: '28px' }} />
                <div>
                  <h4 className="status-text-title">{status === 'paused' ? 'Agent Pipeline Paused (Quota Limit)' : 'Agent Pipeline Terminated'}</h4>
                  <p className="status-text-desc">{error}</p>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Tip: Enter 'mock' in the Gemini API Key input field to run in mock demo mode.</p>
                </div>
              </div>
            </div>
          )}

          {/* Glowing Roadmap Node indicators */}
          {status !== 'idle' && (
            <div className="glass-container roadmap-container" aria-label="Agent pipeline progress">
              <div className={`roadmap-step ${getStepClass('planner', progressPercent <= 15)}`}>
                <div className="step-node">1</div>
                <div className="step-label">Coordinator</div>
                <span className={`step-badge ${getStepBadgeClass('planner', progressPercent <= 15)}`}>
                  {getStepBadgeLabel('planner', progressPercent <= 15)}
                </span>
              </div>
              <div className={`roadmap-step ${getStepClass('idea_analyzer', progressPercent > 15 && progressPercent <= 30)}`}>
                <div className="step-node">2</div>
                <div className="step-label">Idea Analyzer</div>
                <span className={`step-badge ${getStepBadgeClass('idea_analyzer', progressPercent > 15 && progressPercent <= 30)}`}>
                  {getStepBadgeLabel('idea_analyzer', progressPercent > 15 && progressPercent <= 30)}
                </span>
              </div>
              <div className={`roadmap-step ${getStepClass('competitor_researcher', progressPercent > 30 && progressPercent <= 50)}`}>
                <div className="step-node">3</div>
                <div className="step-label">Researcher</div>
                <span className={`step-badge ${getStepBadgeClass('competitor_researcher', progressPercent > 30 && progressPercent <= 50)}`}>
                  {getStepBadgeLabel('competitor_researcher', progressPercent > 30 && progressPercent <= 50)}
                </span>
              </div>
              <div className={`roadmap-step ${getStepClass('feature_planner', progressPercent > 50 && progressPercent <= 70)}`}>
                <div className="step-node">4</div>
                <div className="step-label">Feature Planner</div>
                <span className={`step-badge ${getStepBadgeClass('feature_planner', progressPercent > 50 && progressPercent <= 70)}`}>
                  {getStepBadgeLabel('feature_planner', progressPercent > 50 && progressPercent <= 70)}
                </span>
              </div>
              <div className={`roadmap-step ${getStepClass('business_planner', progressPercent > 70 && progressPercent <= 85)}`}>
                <div className="step-node">5</div>
                <div className="step-label">Biz Planner</div>
                <span className={`step-badge ${getStepBadgeClass('business_planner', progressPercent > 70 && progressPercent <= 85)}`}>
                  {getStepBadgeLabel('business_planner', progressPercent > 70 && progressPercent <= 85)}
                </span>
              </div>
              <div className={`roadmap-step ${getStepClass('synthesizer', progressPercent > 85)}`}>
                <div className="step-node">6</div>
                <div className="step-label">Synthesizer</div>
                <span className={`step-badge ${getStepBadgeClass('synthesizer', progressPercent > 85)}`}>
                  {getStepBadgeLabel('synthesizer', progressPercent > 85)}
                </span>
              </div>
            </div>
          )}

          {/* Main Plan Viewer Tab panel */}
          <div className="glass-container workspace-card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            {status === 'idle' ? (
              <div className="empty-state">
                <div className="empty-icon"><LayoutDashboard style={{ width: '32px', height: '32px' }} /></div>
                <h2>Prepare Your Startup Blueprint</h2>
                <p style={{ maxWidth: '520px', fontSize: '14px', lineHeight: '1.6', color: 'var(--text-secondary)' }}>
                  Enter your raw business idea in the sidebar and trigger the planning suite. Six autonomous AI agents will query market intelligence and build your launch plan.
                </p>

                {/* Predefined Clickable Ideas */}
                <h3 className="sample-ideas-title">
                  Select a Sample Startup Idea to Try
                </h3>
                <div className="sample-ideas-grid">
                  <div 
                    className="sample-card" 
                    onClick={() => selectSample("Healthcare", "Remote office workers", "SaaS Subscription", "An AI-powered mobile app connecting users with live physical therapy feedback and real-time computer vision posture tracking to prevent chronic back pain.")}
                    tabIndex={0}
                    onKeyDown={(e) => e.key === 'Enter' && selectSample("Healthcare", "Remote office workers", "SaaS Subscription", "An AI-powered mobile app connecting users with live physical therapy feedback and real-time computer vision posture tracking to prevent chronic back pain.")}
                    aria-label="Load Healthcare sample HealthPT AI"
                  >
                    <h4>🏥 HealthPT AI</h4>
                    <p>Computer vision posture coach and live therapy feedback.</p>
                  </div>
                  <div 
                    className="sample-card" 
                    onClick={() => selectSample("Fintech", "Gig economy freelancers", "Transactional", "An autonomous accounting agent that automatically reconciles banking transactions with local tax codes, flagging suspicious deductions and auto-filing quarterly taxes.")}
                    tabIndex={0}
                    onKeyDown={(e) => e.key === 'Enter' && selectSample("Fintech", "Gig economy freelancers", "Transactional", "An autonomous accounting agent that automatically reconciles banking transactions with local tax codes, flagging suspicious deductions and auto-filing quarterly taxes.")}
                    aria-label="Load Fintech sample Ledger AI"
                  >
                    <h4>💳 Ledger AI</h4>
                    <p>Autonomous freelancer transaction auditor and quarterly filer.</p>
                  </div>
                  <div 
                    className="sample-card" 
                    onClick={() => selectSample("E-commerce", "Independent merchant storefronts", "Freemium", "An interactive storefront widget that acts as an expert sales advisor, using lightweight multi-agent reasoning to recommend products based on intent instead of simple cookie histories.")}
                    tabIndex={0}
                    onKeyDown={(e) => e.key === 'Enter' && selectSample("E-commerce", "Independent merchant storefronts", "Freemium", "An interactive storefront widget that acts as an expert sales advisor, using lightweight multi-agent reasoning to recommend products based on intent instead of simple cookie histories.")}
                    aria-label="Load E-Commerce sample ShopGenie"
                  >
                    <h4>🛒 ShopGenie</h4>
                    <p>Storefront buyer advisor using intent product matching.</p>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {/* Navigation Bar */}
                <div className="tabs-nav" role="tablist" aria-label="Startup Plan Workspace Tabs">
                  <button 
                    role="tab" 
                    aria-selected={activeTab === 'concept'} 
                    aria-controls="tab-concept-panel"
                    className={`tab-btn ${activeTab === 'concept' ? 'active' : ''}`} 
                    onClick={() => setActiveTab('concept')}
                    onKeyDown={(e) => e.key === 'Enter' && setActiveTab('concept')}
                  >
                    <Compass style={{ width: '15px' }} /> Concept & SWOT
                  </button>
                  <button 
                    role="tab" 
                    aria-selected={activeTab === 'competitors'} 
                    aria-controls="tab-competitors-panel"
                    className={`tab-btn ${activeTab === 'competitors' ? 'active' : ''}`} 
                    onClick={() => setActiveTab('competitors')}
                    onKeyDown={(e) => e.key === 'Enter' && setActiveTab('competitors')}
                  >
                    <Search style={{ width: '15px' }} /> Competitors
                  </button>
                  <button 
                    role="tab" 
                    aria-selected={activeTab === 'roadmap'} 
                    aria-controls="tab-roadmap-panel"
                    className={`tab-btn ${activeTab === 'roadmap' ? 'active' : ''}`} 
                    onClick={() => setActiveTab('roadmap')}
                    onKeyDown={(e) => e.key === 'Enter' && setActiveTab('roadmap')}
                  >
                    <Cpu style={{ width: '15px' }} /> Product Roadmap
                  </button>
                  <button 
                    role="tab" 
                    aria-selected={activeTab === 'business'} 
                    aria-controls="tab-business-panel"
                    className={`tab-btn ${activeTab === 'business' ? 'active' : ''}`} 
                    onClick={() => setActiveTab('business')}
                    onKeyDown={(e) => e.key === 'Enter' && setActiveTab('business')}
                  >
                    <DollarSign style={{ width: '15px' }} /> Business Model
                  </button>
                  <button 
                    role="tab" 
                    aria-selected={activeTab === 'summary'} 
                    aria-controls="tab-summary-panel"
                    className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`} 
                    onClick={() => setActiveTab('summary')}
                    onKeyDown={(e) => e.key === 'Enter' && setActiveTab('summary')}
                  >
                    <ClipboardList style={{ width: '15px' }} /> Executive Summary
                  </button>
                </div>

                {/* Tab Render Area */}
                <div className="viewer-panel">
                  {activeTab === 'concept' && (
                    <div id="tab-concept-panel" role="tabpanel" className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                      {!results.idea_analysis ? (
                        <div className="skeleton-loading-container" aria-label="Loading idea analysis data">
                          <div className="skeleton-line header-skeleton"></div>
                          <div className="skeleton-line text-skeleton"></div>
                          <div className="skeleton-line text-skeleton-short"></div>
                          <div className="skeleton-grid">
                            <div className="skeleton-card"></div>
                            <div className="skeleton-card"></div>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="concept-showcase-grid">
                            <div className="concept-text-side">
                              <h3 className="section-headline"><Compass style={{ width: '18px', color: 'var(--accent-indigo)' }} /> Refined Concept</h3>
                              <p className="concept-refined-para">
                                {results.idea_analysis.refined_concept || results.idea_analysis.raw_content}
                              </p>
                              
                              <div className="info-grid" style={{ marginTop: '24px' }}>
                                <div className="info-card">
                                  <h3><Target style={{ color: 'var(--accent-indigo)', width: '16px' }} /> Target Demographics</h3>
                                  <p>{results.idea_analysis.target_audience || 'Parsing...'}</p>
                                </div>
                                <div className="info-card">
                                  <h3><Sparkles style={{ color: 'var(--accent-cyan)', width: '16px' }} /> Unique Value Prop</h3>
                                  <p>{results.idea_analysis.value_proposition || 'Parsing...'}</p>
                                </div>
                              </div>
                            </div>
                            
                            <div className="concept-chart-side">
                              <h3 className="section-headline"><TrendingUp style={{ width: '18px', color: 'var(--accent-purple)' }} /> Viability Metrics Radar</h3>
                              <div className="chart-wrapper">
                                <ResponsiveContainer width="100%" height={260}>
                                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={getSwotRadarData()}>
                                    <PolarGrid stroke="var(--border-glass)" />
                                    <PolarAngleAxis dataKey="subject" stroke="var(--text-secondary)" tick={{ fontSize: 10, fontWeight: '500' }} />
                                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="var(--border-glass)" tick={{ fontSize: 8 }} />
                                    <Radar name="Startup Viability" dataKey="value" stroke="var(--accent-indigo)" fill="var(--accent-indigo)" fillOpacity={0.25} />
                                    <Tooltip contentStyle={{ backgroundColor: 'rgba(10, 14, 26, 0.95)', borderColor: 'var(--border-glass)', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                                  </RadarChart>
                                </ResponsiveContainer>
                              </div>
                            </div>
                          </div>

                          {results.idea_analysis.swot_summary && (
                            <div style={{ marginTop: '10px' }}>
                              <h3 className="section-headline"><Layers style={{ width: '18px', color: 'var(--accent-purple)' }} /> SWOT Quadrants Analysis</h3>
                              <div className="swot-grid" style={{ marginTop: '12px' }}>
                                <div className="swot-quad-card strengths">
                                  <h4 className="swot-title-s">Strengths</h4>
                                  <p>{results.idea_analysis.swot_summary.strengths || 'Parsing...'}</p>
                                </div>
                                <div className="swot-quad-card weaknesses">
                                  <h4 className="swot-title-w">Weaknesses</h4>
                                  <p>{results.idea_analysis.swot_summary.weaknesses || 'Parsing...'}</p>
                                </div>
                                <div className="swot-quad-card opportunities">
                                  <h4 className="swot-title-o">Opportunities</h4>
                                  <p>{results.idea_analysis.swot_summary.opportunities || 'Scalable integration with emerging automation workflows, and high expansion potential into adjacent market verticals.'}</p>
                                </div>
                                <div className="swot-quad-card threats">
                                  <h4 className="swot-title-t">Threats</h4>
                                  <p>{results.idea_analysis.swot_summary.threats || 'Shifting regulatory restrictions (e.g. HIPAA or GDPR) and rapid technological entry by large legacy incumbents.'}</p>
                                </div>
                              </div>
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  )}

                  {activeTab === 'competitors' && (
                    <div id="tab-competitors-panel" role="tabpanel" className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                      {!results.competitor_research ? (
                        <div className="skeleton-loading-container" aria-label="Loading competitor intelligence data">
                          <div className="skeleton-line header-skeleton"></div>
                          <div className="skeleton-grid">
                            <div className="skeleton-card" style={{ height: '220px' }}></div>
                            <div className="skeleton-card" style={{ height: '220px' }}></div>
                          </div>
                        </div>
                      ) : (
                        <>
                          {results.competitor_research.market_stats && (
                            <div className="market-stats-banner">
                              <h3 className="section-headline" style={{ color: 'var(--accent-cyan)' }}><TrendingUp style={{ width: '18px', color: 'var(--accent-cyan)' }} /> FastMCP Market Data Summary</h3>
                              <div className="market-stats-grid">
                                <div className="market-stat-item">
                                  <span className="market-stat-label">Market Size Estimate</span>
                                  <span className="market-stat-value">${results.competitor_research.market_stats.market_size_billions}B</span>
                                </div>
                                <div className="market-stat-item">
                                  <span className="market-stat-label">Sector CAGR Rate</span>
                                  <span className="market-stat-value" style={{ color: 'var(--accent-emerald)' }}>{results.competitor_research.market_stats.cagr_percent}%</span>
                                </div>
                                <div className="market-stat-item">
                                  <span className="market-stat-label">Industry Sector</span>
                                  <span className="market-stat-value" style={{ color: 'var(--accent-indigo)' }}>{industry}</span>
                                </div>
                              </div>
                              <div className="market-trends-section">
                                <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Top Trends Observed:</span>
                                <div className="trend-badge-list">
                                  {results.competitor_research.market_stats.trends?.map((t, i) => (
                                    <span key={i} className="trend-badge">{t}</span>
                                  ))}
                                </div>
                              </div>
                            </div>
                          )}

                          <div className="competitors-charts-grid">
                            <div className="chart-card">
                              <h4>Market Valuation Forecast (USD Billions)</h4>
                              <div className="chart-container" style={{ marginTop: '16px' }}>
                                <ResponsiveContainer width="100%" height={230}>
                                  <AreaChart data={getMarketGrowthProjection()}>
                                    <defs>
                                      <linearGradient id="colorGrowth" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-cyan)" stopOpacity={0.25}/>
                                        <stop offset="95%" stopColor="var(--accent-cyan)" stopOpacity={0}/>
                                      </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-glass)" vertical={false} />
                                    <XAxis dataKey="year" stroke="var(--text-secondary)" tick={{ fontSize: 10 }} />
                                    <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 10 }} />
                                    <Tooltip contentStyle={{ backgroundColor: 'rgba(10, 14, 26, 0.95)', borderColor: 'var(--border-glass)', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                                    <Area type="monotone" dataKey="market_size" name="Market Value ($B)" stroke="var(--accent-cyan)" fillOpacity={1} fill="url(#colorGrowth)" />
                                  </AreaChart>
                                </ResponsiveContainer>
                              </div>
                            </div>

                            <div className="chart-card">
                              <h4>Competitor Positioning Metrics</h4>
                              <div className="chart-container" style={{ marginTop: '16px' }}>
                                <ResponsiveContainer width="100%" height={230}>
                                  <BarChart data={getCompetitorComparisonScores()}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-glass)" vertical={false} />
                                    <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{ fontSize: 10 }} />
                                    <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 10 }} />
                                    <Tooltip contentStyle={{ backgroundColor: 'rgba(10, 14, 26, 0.95)', borderColor: 'var(--border-glass)', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                                    <Legend verticalAlign="top" height={24} iconSize={8} wrapperStyle={{ fontSize: 10 }} />
                                    <Bar dataKey="feature_score" name="Features" fill="var(--accent-indigo)" radius={[3, 3, 0, 0]} />
                                    <Bar dataKey="pricing_score" name="Pricing" fill="var(--accent-purple)" radius={[3, 3, 0, 0]} />
                                    <Bar dataKey="market_share" name="Share %" fill="var(--accent-cyan)" radius={[3, 3, 0, 0]} />
                                  </BarChart>
                                </ResponsiveContainer>
                              </div>
                            </div>
                          </div>

                          <div>
                            <h3 className="section-headline"><Search style={{ width: '18px', color: 'var(--accent-indigo)' }} /> Competitor Landscape Matrix Differentiator</h3>
                            <div className="competitor-table-wrapper" style={{ marginTop: '12px' }}>
                              <table className="competitor-table">
                                <thead>
                                  <tr>
                                    <th>Competitor Name</th>
                                    <th>Core Description</th>
                                    <th>Strategic Advantages & Weaknesses</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {results.competitor_research.competitors?.map((comp, idx) => (
                                    <tr key={idx}>
                                      <td style={{ fontWeight: '700', color: 'var(--text-bright)', whiteSpace: 'nowrap' }}>{comp.name}</td>
                                      <td style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{comp.description}</td>
                                      <td>
                                        <div className="competitor-pro-con">
                                          <span className="pro-badge"><strong>Pros:</strong> {comp.strengths}</span>
                                          <span className="con-badge"><strong>Cons:</strong> {comp.weaknesses}</span>
                                        </div>
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>

                          <div>
                            <h3 className="section-headline"><Zap style={{ width: '18px', color: 'var(--accent-amber)' }} /> Competitive Differentiator</h3>
                            <p className="concept-refined-para" style={{ padding: '18px 22px' }}>
                              {results.competitor_research.differentiator}
                            </p>
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {activeTab === 'roadmap' && (
                    <div id="tab-roadmap-panel" role="tabpanel" className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                      {!results.feature_plan ? (
                        <div className="skeleton-loading-container" aria-label="Loading product architecture planning">
                          <div className="skeleton-line header-skeleton"></div>
                          <div className="skeleton-line text-skeleton"></div>
                          <div className="skeleton-card" style={{ height: '180px' }}></div>
                        </div>
                      ) : (
                        <>
                          {results.feature_plan.tech_stack && (
                            <div>
                              <h3 className="section-headline"><Layers style={{ width: '18px', color: 'var(--accent-purple)' }} /> Google Dev Canonical Stack</h3>
                              <div className="tech-grid" style={{ marginTop: '10px' }}>
                                <div className="tech-card">
                                  <span className="tech-card-label">Frontend View</span>
                                  <span className="tech-card-val">{results.feature_plan.tech_stack.frontend}</span>
                                </div>
                                <div className="tech-card">
                                  <span className="tech-card-label">Backend API</span>
                                  <span className="tech-card-val">{results.feature_plan.tech_stack.backend}</span>
                                </div>
                                <div className="tech-card">
                                  <span className="tech-card-label">Database Storage</span>
                                  <span className="tech-card-val">{results.feature_plan.tech_stack.database}</span>
                                </div>
                                <div className="tech-card">
                                  <span className="tech-card-label">Cloud Deployment</span>
                                  <span className="tech-card-val">{results.feature_plan.tech_stack.cloud_services}</span>
                                </div>
                              </div>
                            </div>
                          )}

                          <div>
                            <h3 className="section-headline"><Activity style={{ width: '18px', color: 'var(--accent-cyan)' }} /> Strategic Development Timeline</h3>
                            <div className="chart-card" style={{ padding: '24px 20px', marginTop: '10px' }}>
                              <ResponsiveContainer width="100%" height={160}>
                                <BarChart data={getRoadmapTimeline()} layout="vertical" stackOffset="none">
                                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-glass)" horizontal={false} />
                                  <XAxis type="number" stroke="var(--text-secondary)" tick={{ fontSize: 10 }} label={{ value: 'Timeline Month Offset', position: 'insideBottom', offset: -5, fill: 'var(--text-secondary)', style: { fontSize: 10 } }} />
                                  <YAxis type="category" dataKey="name" stroke="var(--text-secondary)" tick={{ fontSize: 10 }} width={110} />
                                  <Tooltip contentStyle={{ backgroundColor: 'rgba(10, 14, 26, 0.95)', borderColor: 'var(--border-glass)', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                                  <Bar dataKey="start" stackId="a" fill="transparent" />
                                  <Bar dataKey="duration" name="Duration (Months)" stackId="a" fill="var(--accent-indigo)" radius={[0, 4, 4, 0]} />
                                </BarChart>
                              </ResponsiveContainer>
                            </div>
                          </div>

                          <div>
                            <h3 className="section-headline"><Sparkles style={{ width: '18px', color: 'var(--accent-indigo)' }} /> MVP Core Feature Scope</h3>
                            <div className="info-grid" style={{ marginTop: '10px' }}>
                              {results.feature_plan.mvp_features?.map((f, idx) => (
                                <div className="info-card" key={idx} style={{ position: 'relative' }}>
                                  <span className={`step-badge ${f.priority === 'High' ? 'feature-badge-high' : 'feature-badge-med'}`} style={{ position: 'absolute', top: '16px', right: '16px' }}>{f.priority} Priority</span>
                                  <h4 style={{ color: 'var(--text-bright)', fontSize: '14px', marginBottom: '8px', paddingRight: '70px' }}>{f.feature_name}</h4>
                                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>{f.description}</p>
                                </div>
                              ))}
                            </div>
                          </div>

                          <div>
                            <h3 className="section-headline"><Activity style={{ width: '18px', color: 'var(--accent-cyan)' }} /> Detailed System Milestones</h3>
                            <div className="vertical-timeline" style={{ marginTop: '12px' }}>
                              {results.feature_plan.roadmap?.map((r, idx) => (
                                <div key={idx} className="timeline-node-item">
                                  <div className="timeline-node-circle">{idx+1}</div>
                                  <div className="timeline-node-content">
                                    <h4 className="timeline-node-title">{r.phase}</h4>
                                    <ul className="timeline-bullet-list">
                                      {r.milestones?.map((m, mIdx) => (
                                        <li key={mIdx}>{m}</li>
                                      ))}
                                    </ul>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {activeTab === 'business' && (
                    <div id="tab-business-panel" role="tabpanel" className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                      {!results.business_plan ? (
                        <div className="skeleton-loading-container" aria-label="Loading financial business model">
                          <div className="skeleton-line header-skeleton"></div>
                          <div className="skeleton-grid">
                            <div className="skeleton-card" style={{ height: '240px' }}></div>
                            <div className="skeleton-card" style={{ height: '240px' }}></div>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="concept-showcase-grid">
                            <div className="concept-text-side">
                              <h3 className="section-headline"><Briefcase style={{ width: '18px', color: 'var(--accent-indigo)' }} /> Monetization Strategy</h3>
                              <p className="concept-refined-para">
                                {results.business_plan.monetization_strategy}
                              </p>
                              
                              <div className="info-grid" style={{ marginTop: '24px' }}>
                                <div className="info-card">
                                  <h3><Compass style={{ color: 'var(--accent-indigo)', width: '16px' }} /> Go-to-Market Action Plan</h3>
                                  <p style={{ fontSize: '13px', lineHeight: '1.5' }}>{results.business_plan.gtm_strategy}</p>
                                </div>
                                <div className="info-card">
                                  <h3><TrendingUp style={{ color: 'var(--accent-cyan)', width: '16px' }} /> Target Key Metrics</h3>
                                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '6px', fontSize: '13px' }}>
                                    <span style={{ color: 'var(--text-secondary)' }}><strong>Break-even target:</strong> <span style={{ color: 'var(--text-bright)' }}>{results.business_plan.financial_metrics?.breakeven_timeframe}</span></span>
                                    <span style={{ color: 'var(--text-secondary)' }}><strong>Costs Structure:</strong> <span style={{ color: 'var(--text-bright)' }}>{results.business_plan.financial_metrics?.estimated_cost_structure}</span></span>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <div className="concept-chart-side">
                              <h3 className="section-headline"><DollarSign style={{ width: '18px', color: 'var(--accent-emerald)' }} /> 5-Year Financial Projection</h3>
                              <div className="chart-card" style={{ padding: '20px 16px' }}>
                                <ResponsiveContainer width="100%" height={220}>
                                  <AreaChart data={getFinancialForecast()}>
                                    <defs>
                                      <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-emerald)" stopOpacity={0.25}/>
                                        <stop offset="95%" stopColor="var(--accent-emerald)" stopOpacity={0}/>
                                      </linearGradient>
                                      <linearGradient id="colorCost" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-rose)" stopOpacity={0.15}/>
                                        <stop offset="95%" stopColor="var(--accent-rose)" stopOpacity={0}/>
                                      </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-glass)" vertical={false} />
                                    <XAxis dataKey="year" stroke="var(--text-secondary)" tick={{ fontSize: 9 }} />
                                    <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 9 }} />
                                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ backgroundColor: 'rgba(10, 14, 26, 0.95)', borderColor: 'var(--border-glass)', borderRadius: '8px', color: '#fff', fontSize: '11px' }} />
                                    <Legend verticalAlign="top" height={24} iconSize={8} wrapperStyle={{ fontSize: 9 }} />
                                    <Area type="monotone" dataKey="revenue" name="Revenue ($)" stroke="var(--accent-emerald)" fillOpacity={1} fill="url(#colorRev)" />
                                    <Area type="monotone" dataKey="costs" name="Opex ($)" stroke="var(--accent-rose)" fillOpacity={1} fill="url(#colorCost)" />
                                  </AreaChart>
                                </ResponsiveContainer>
                              </div>
                            </div>
                          </div>

                          <div>
                            <h3 className="section-headline"><DollarSign style={{ width: '18px', color: 'var(--accent-emerald)' }} /> Pricing Architecture Plan</h3>
                            <div className="pricing-card-grid" style={{ marginTop: '12px' }}>
                              {results.business_plan.pricing_model?.map((tier, idx) => (
                                <div className={`pricing-card ${idx === 1 ? 'featured' : ''}`} key={idx}>
                                  {idx === 1 && <span className="featured-tag">Recommended</span>}
                                  <span className="pricing-tier-name">{tier.tier_name}</span>
                                  <h2 className="pricing-price-val">
                                    {tier.price} <span>/ month</span>
                                  </h2>
                                  <ul className="pricing-features-list">
                                    {tier.features?.map((f, fIdx) => (
                                      <li key={fIdx}>
                                        <CheckCircle2 style={{ width: '14px', color: 'var(--accent-emerald)', marginTop: '2px', flexShrink: 0 }} /> <span>{f}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {activeTab === 'summary' && (
                    <div id="tab-summary-panel" role="tabpanel" className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                      {!results.final_report ? (
                        <div className="skeleton-loading-container" aria-label="Compiling executive blueprint report">
                          <div className="skeleton-line header-skeleton" style={{ width: '60%' }}></div>
                          <div className="skeleton-line text-skeleton"></div>
                          <div className="skeleton-line text-skeleton"></div>
                          <div className="skeleton-line text-skeleton-short"></div>
                          <div className="skeleton-card" style={{ height: '140px', marginTop: '16px' }}></div>
                        </div>
                      ) : (
                        <>
                          <div className="doc-action-bar">
                            <button className="btn-secondary" onClick={copyToClipboard} aria-label="Copy entire markdown report text">
                              <Copy style={{ width: '14px' }} />
                              {copied ? 'Copied!' : 'Copy Report'}
                            </button>
                            <button className="btn-secondary" style={{ borderColor: 'var(--accent-indigo)' }} onClick={downloadMarkdown} aria-label="Download report markdown file">
                              <Download style={{ width: '14px', color: 'var(--accent-indigo)' }} />
                              Download Markdown
                            </button>
                            <button className="btn-primary" style={{ padding: '10px 18px', fontSize: '13px', boxShadow: 'none' }} onClick={() => window.print()} aria-label="Print report or export to PDF">
                              <Printer style={{ width: '14px' }} />
                              Print / Export PDF
                            </button>
                          </div>
                          
                          <div className="markdown-container">
                            <article className="markdown-body">
                              {renderMarkdown(results.final_report)}
                            </article>
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
