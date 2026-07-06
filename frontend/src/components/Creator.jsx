import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Send, Sparkles, Terminal, CheckCircle2, AlertTriangle, Play, RefreshCw, Eye } from 'lucide-react';
import axios from 'axios';

export default function Creator({ onBack, onSelectProposal }) {
  const [ideaText, setIdeaText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Active execution state
  const [activeProposalId, setActiveProposalId] = useState(null);
  const [proposalData, setProposalData] = useState(null);
  const [currentStep, setCurrentStep] = useState(0); // 0: Form, 1: Process Visualizer
  
  const terminalEndRef = useRef(null);

  const ideaLength = ideaText.trim().length;
  const isInputValid = ideaLength >= 10 && ideaLength <= 2000;

  // Poll proposal status while it is processing
  useEffect(() => {
    let intervalId;

    if (activeProposalId && currentStep === 1) {
      const fetchStatus = () => {
        axios.get(`http://127.0.0.1:8000/api/v1/proposals/${activeProposalId}`)
          .then(res => {
            setProposalData(res.data);
            
            // Check if workflow completed or failed
            if (res.data.status === 'completed' || res.data.status === 'failed') {
              clearInterval(intervalId);
              setLoading(false);
            }
          })
          .catch(err => {
            console.error('Error fetching proposal status:', err);
          });
      };

      // Poll every 1.5 seconds
      fetchStatus();
      intervalId = setInterval(fetchStatus, 1500);
    }

    return () => clearInterval(intervalId);
  }, [activeProposalId, currentStep]);

  // Autoscroll terminal logs
  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [proposalData]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isInputValid) return;

    setLoading(true);
    setError(null);
    setCurrentStep(1); // Go to visualizer screen

    axios.post('http://127.0.0.1:8000/api/v1/proposals', { idea_text: ideaText })
      .then(res => {
        setActiveProposalId(res.data.id);
        setProposalData(res.data);
      })
      .catch(err => {
        const detail = err.response?.data?.detail || 'An error occurred during safety check validation.';
        setError(detail);
        setLoading(false);
        setCurrentStep(0); // Go back to form to fix
      });
  };

  // Agent team list
  const agentTeam = [
    { name: 'Coordinator Agent', desc: 'Sets goals, compiles inputs, and routes delegation streams.' },
    { name: 'Inventor Agent', desc: 'Validates novelty, inspects patent classes, and defines innovation claims.' },
    { name: 'Engineer Agent', desc: 'Models system architecture, schemas, and REST endpoints.' },
    { name: 'Economist Agent', desc: 'Projects infrastructure budgets, development costing, and monetization models.' },
    { name: 'Critic Agent', desc: 'Performs SWOT analysis and scans security risk mitigation plans.' },
    { name: 'Pitch Generator Agent', desc: 'Compiles individual logs into executive marketing proposals.' },
  ];

  // Helper to check step status
  const getStepStatus = (agentName) => {
    if (!proposalData || !proposalData.logs) return 'pending';
    const logEntry = proposalData.logs.find(l => l.agent_name === agentName);
    return logEntry ? logEntry.status : 'pending';
  };

  // Render Form state
  if (currentStep === 0) {
    return (
      <div className="space-y-6 max-w-3xl mx-auto animate-fadeIn">
        <button
          onClick={onBack}
          className="flex items-center space-x-1 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </button>

        <div className="space-y-2">
          <h2 className="text-3xl font-extrabold tracking-tight">Launch Innovation Portal</h2>
          <p className="text-sm text-slate-400">
            Submit a concept. Our multi-agent team will coordinate offline to generate structural specifications and feasibility documentation.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="glass-panel p-6 rounded-xl space-y-4">
            <div className="space-y-2">
              <label htmlFor="idea" className="block text-xs font-bold uppercase tracking-wider text-slate-400">
                Innovation Idea Concept
              </label>
              <textarea
                id="idea"
                rows={6}
                value={ideaText}
                onChange={(e) => setIdeaText(e.target.value)}
                placeholder="Example: A smart solar-powered deadbolt lock for micro-cabins that utilizes NFC keys and logs device energy states offline..."
                className="w-full rounded-lg border border-slate-800 bg-slate-950 p-4 text-sm text-slate-200 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 placeholder-slate-600 transition"
              />
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-slate-500">
              <div className="flex items-center space-x-1">
                {ideaLength > 0 && ideaLength < 10 && (
                  <span className="text-amber-500 flex items-center space-x-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Too short (min 10 chars)</span>
                  </span>
                )}
                {ideaLength > 2000 && (
                  <span className="text-red-500 flex items-center space-x-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Exceeded maximum length</span>
                  </span>
                )}
                {ideaLength >= 10 && ideaLength <= 2000 && (
                  <span className="text-emerald-500 flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Ready for evaluation</span>
                  </span>
                )}
              </div>
              <span>{ideaLength}/2000 chars</span>
            </div>
            
            {error && (
              <div className="p-3 rounded-lg bg-red-950/40 border border-red-900/50 text-xs text-red-400 font-medium flex items-start space-x-2">
                <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!isInputValid}
              className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-bold text-sm shadow-md transition ${
                isInputValid
                  ? 'bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white cursor-pointer transform hover:-translate-y-0.5'
                  : 'bg-slate-800 text-slate-500 border border-slate-700/80 cursor-not-allowed'
              }`}
            >
              <Send className="w-4 h-4" />
              <span>Submit Concept</span>
            </button>
          </div>
        </form>
      </div>
    );
  }

  // Render Agent Pipeline Visualizer state
  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-fadeIn">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-extrabold tracking-tight">Orchestrating Innovation Team</h2>
          <p className="text-xs text-slate-400 font-mono">
            Orchestration Process ID: <span className="text-sky-400">{activeProposalId || 'spawning...'}</span>
          </p>
        </div>
        
        {proposalData?.status === 'completed' && (
          <button
            onClick={() => onSelectProposal(activeProposalId)}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-md transition"
          >
            <Eye className="w-4 h-4" />
            <span>View Full Report</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Agent pipeline tracking nodes */}
        <div className="md:col-span-1 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 font-mono">Workflow Status</h3>
          
          <div className="space-y-3 relative before:absolute before:left-4 before:top-2 before:bottom-2 before:w-[2px] before:bg-slate-800">
            {agentTeam.map((agent, index) => {
              const status = getStepStatus(agent.name);
              
              let stepStyle = 'border-slate-800 bg-slate-950 text-slate-500';
              let badgeStyle = 'bg-slate-900 border-slate-800 text-slate-500';
              
              if (status === 'running') {
                stepStyle = 'border-sky-500/50 bg-sky-950/20 text-slate-200';
                badgeStyle = 'bg-sky-950 border-sky-800 text-sky-400 animate-pulse';
              } else if (status === 'completed') {
                stepStyle = 'border-emerald-800/40 bg-emerald-950/10 text-slate-300';
                badgeStyle = 'bg-emerald-950 border-emerald-900 text-emerald-400';
              } else if (status === 'failed') {
                stepStyle = 'border-red-800/40 bg-red-950/10 text-red-400';
                badgeStyle = 'bg-red-950 border-red-900 text-red-400';
              }

              return (
                <div 
                  key={agent.name} 
                  className={`flex items-start space-x-3 p-3 rounded-lg border text-xs transition duration-300 ${stepStyle}`}
                >
                  <div className={`w-8 h-8 rounded-full border flex items-center justify-center font-mono font-bold text-xs shrink-0 relative z-10 ${badgeStyle}`}>
                    {status === 'completed' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : status === 'running' ? (
                      <RefreshCw className="w-4 h-4 text-sky-400 animate-spin" />
                    ) : (
                      index + 1
                    )}
                  </div>
                  <div>
                    <h4 className="font-bold">{agent.name}</h4>
                    <p className="text-[10px] text-slate-500 line-clamp-1">{agent.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Real-time Streaming stdout/thinking logs */}
        <div className="md:col-span-2 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 font-mono flex items-center justify-between">
            <span>Agent Execution Console</span>
            <span className="flex items-center space-x-1 text-slate-600 font-normal">
              <Terminal className="w-3.5 h-3.5" />
              <span>logs</span>
            </span>
          </h3>

          <div className="h-[430px] rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-[11px] leading-relaxed text-slate-300 overflow-y-auto shadow-inner space-y-2">
            <div>$ initializing secure agent execution framework...</div>
            <div>$ starting coordinating thread...</div>
            
            {proposalData?.logs && proposalData.logs.map((log, idx) => (
              <div key={idx} className="space-y-1">
                {/* Agent execution border banner */}
                <div className="text-slate-500 font-bold border-b border-slate-900 pb-1 mt-4">
                  &gt;&gt; RUNNING ACTIVE THREAD: {log.agent_name.toUpperCase()} (status: {log.status})
                </div>
                {/* Inner logs */}
                <div className="whitespace-pre-wrap text-slate-300">
                  {log.logs}
                </div>
                {log.output && (
                  <div className="p-2.5 rounded bg-slate-900/60 border border-slate-800 text-[10px] text-sky-300 max-h-32 overflow-y-auto font-sans mt-2">
                    <span className="font-bold font-mono text-[9px] block text-sky-500 uppercase tracking-widest mb-1">Generated Section Draft:</span>
                    {log.output.slice(0, 300)}...
                  </div>
                )}
              </div>
            ))}

            {proposalData?.status === 'processing' && (
              <div className="flex items-center space-x-2 text-sky-400 animate-pulse mt-4">
                <span className="w-2 h-2 bg-sky-400 rounded-full animate-ping"></span>
                <span>Agent in coordination thread is writing to telemetry...</span>
              </div>
            )}

            {proposalData?.status === 'completed' && (
              <div className="p-4 rounded-lg bg-emerald-950/20 border border-emerald-900/40 text-emerald-400 text-center font-bold text-xs space-y-2 mt-6 font-sans">
                <p>SUCCESS: Innovation Proposal Successfully Compiled and Sealed in SQLite database.</p>
                <button
                  onClick={() => onSelectProposal(activeProposalId)}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-[11px] font-bold shadow-md transition"
                >
                  Inspect Compiled Report
                </button>
              </div>
            )}

            {proposalData?.status === 'failed' && (
              <div className="p-4 rounded-lg bg-red-950/20 border border-red-900/40 text-red-400 text-center font-bold text-xs space-y-2 mt-6 font-sans">
                <p>ERROR: Execution terminated due to structural agent exception.</p>
                <button
                  onClick={() => {
                    setCurrentStep(0);
                    setActiveProposalId(null);
                    setProposalData(null);
                  }}
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-[11px] font-bold shadow-md transition"
                >
                  Retry Execution Flow
                </button>
              </div>
            )}

            <div ref={terminalEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}
