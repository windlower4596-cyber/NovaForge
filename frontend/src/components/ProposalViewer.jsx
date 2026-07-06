import React, { useState, useEffect } from 'react';
import { ArrowLeft, FileText, Cpu, Coins, ShieldCheck, Terminal, Trash2, Calendar, FileDown } from 'lucide-react';
import axios from 'axios';

// A simple custom Markdown formatter to render headers, lists, code blocks, and tables beautifully.
function SimpleMarkdown({ content }) {
  if (!content) return <p className="text-slate-500 italic">No section content generated.</p>;

  const lines = content.split('\n');
  let inCodeBlock = false;
  let codeContent = [];
  let inTable = false;
  let tableRows = [];

  const elements = [];

  lines.forEach((line, index) => {
    // Code block check
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        inCodeBlock = false;
        elements.push(
          <pre key={`code-${index}`} className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs text-sky-400 font-mono overflow-x-auto my-3 whitespace-pre-wrap">
            <code>{codeContent.join('\n')}</code>
          </pre>
        );
        codeContent = [];
      } else {
        inCodeBlock = true;
      }
      return;
    }

    if (inCodeBlock) {
      codeContent.push(line);
      return;
    }

    // Table check
    if (line.trim().startsWith('|')) {
      inTable = true;
      tableRows.push(line);
      return;
    } else if (inTable) {
      // Process table when table ends
      inTable = false;
      const rows = [...tableRows];
      tableRows = [];
      elements.push(renderTable(rows, index));
    }

    // Headers
    if (line.startsWith('# ')) {
      elements.push(<h1 key={index} className="text-2xl font-extrabold tracking-tight mt-6 mb-3 text-slate-100 border-b border-slate-800 pb-2">{line.substring(2)}</h1>);
    } else if (line.startsWith('## ')) {
      elements.push(<h2 key={index} className="text-xl font-bold tracking-tight mt-6 mb-3 text-slate-200 border-b border-slate-850 pb-1">{line.substring(3)}</h2>);
    } else if (line.startsWith('### ')) {
      elements.push(<h3 key={index} className="text-lg font-bold tracking-tight mt-5 mb-2 text-sky-400">{line.substring(4)}</h3>);
    } else if (line.startsWith('#### ')) {
      elements.push(<h4 key={index} className="text-sm font-bold uppercase tracking-wider text-slate-400 mt-4 mb-1">{line.substring(5)}</h4>);
    }
    // Lists
    else if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
      const cleanLine = line.trim().substring(2);
      // Basic bold extraction
      const parts = cleanLine.split('**');
      const formattedParts = parts.map((part, i) => i % 2 === 1 ? <strong key={i} className="text-slate-100 font-bold">{part}</strong> : part);
      elements.push(
        <ul key={index} className="list-disc list-inside ml-4 text-xs text-slate-300 space-y-1.5 my-1">
          <li>{formattedParts}</li>
        </ul>
      );
    }
    // Empty line
    else if (line.trim() === '') {
      elements.push(<div key={index} className="h-2" />);
    }
    // Paragraph
    else {
      const parts = line.split('**');
      const formattedParts = parts.map((part, i) => i % 2 === 1 ? <strong key={i} className="text-slate-100 font-bold">{part}</strong> : part);
      elements.push(<p key={index} className="text-xs text-slate-350 leading-relaxed my-2">{formattedParts}</p>);
    }
  });

  // Final check if table was open at EOF
  if (inTable && tableRows.length > 0) {
    elements.push(renderTable(tableRows, lines.length));
  }

  return <div className="space-y-1">{elements}</div>;
}

// Render markdown tables into JSX
function renderTable(rows, keyIndex) {
  const parsedRows = rows.map(r => r.split('|').map(cell => cell.trim()).filter((_, i) => i > 0 && i < r.split('|').length - 1));
  if (parsedRows.length < 2) return null;

  // Filter separator row (e.g. |---|---|)
  const header = parsedRows[0];
  const bodyRows = parsedRows.slice(1).filter(row => !row.every(cell => cell.startsWith('---')));

  return (
    <div key={`table-${keyIndex}`} className="overflow-x-auto my-4 rounded-lg border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800 text-xs">
        <thead className="bg-slate-900/60 font-semibold font-mono text-[10px] text-slate-400 uppercase tracking-wider">
          <tr>
            {header.map((col, idx) => (
              <th key={idx} className="px-4 py-2.5 text-left border-r border-slate-800/50 last:border-0">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/80 bg-slate-950/20 text-slate-300">
          {bodyRows.map((row, rIdx) => (
            <tr key={rIdx} className="hover:bg-slate-900/30">
              {row.map((cell, cIdx) => (
                <td key={cIdx} className="px-4 py-2 border-r border-slate-800/50 last:border-0" dangerouslySetInnerHTML={{ __html: cell }} />
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function ProposalViewer({ proposal, onBack, onDelete }) {
  const [activeTab, setActiveTab] = useState('pitch');
  const [proposalDetails, setProposalDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(true);

  useEffect(() => {
    if (!proposal?.id) return;

    let intervalId;
    let isMounted = true;

    const fetchDetails = () => {
      axios.get(`http://127.0.0.1:8000/api/v1/proposals/${proposal.id}`)
        .then(res => {
          if (!isMounted) return;
          setProposalDetails(res.data);
          setLoadingDetails(false);
          
          if (res.data.status !== 'processing' && intervalId) {
            clearInterval(intervalId);
          }
        })
        .catch(err => {
          console.error('Error fetching proposal details:', err);
          if (isMounted) {
            setLoadingDetails(false);
          }
        });
    };

    fetchDetails();

    if (proposal.status === 'processing') {
      intervalId = setInterval(fetchDetails, 1500);
    }

    return () => {
      isMounted = false;
      if (intervalId) clearInterval(intervalId);
    };
  }, [proposal?.id, proposal?.status]);

  const currentProposal = proposalDetails || proposal;

  const downloadMarkdown = () => {
    if (!currentProposal || !currentProposal.final_proposal) return;
    const final_md = currentProposal.final_proposal.pitch || '';
    const blob = new Blob([final_md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${currentProposal.title.toLowerCase().replace(/[^a-z0-9]+/g, '_')}_proposal.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const tabs = [
    { id: 'pitch', label: 'Executive Pitch', icon: FileDown },
    { id: 'tech', label: 'Technical Spec', icon: FileText },
    { id: 'finance', label: 'Financial Plan', icon: Coins },
    { id: 'security', label: 'Security & SWOT', icon: ShieldCheck },
    { id: 'logs', label: 'Agent Run Logs', icon: Terminal },
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Upper header action area */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-5">
        <div className="space-y-1.5">
          <button
            onClick={onBack}
            className="flex items-center space-x-1 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </button>
          <h2 className="text-2xl font-extrabold tracking-tight text-slate-100">
            {currentProposal.title || 'Loading proposal details...'}
          </h2>
          <div className="flex items-center space-x-4 text-[10px] text-slate-500 font-mono">
            {currentProposal.created_at && (
              <span className="flex items-center space-x-1">
                <Calendar className="w-3.5 h-3.5" />
                <span>{new Date(currentProposal.created_at).toLocaleString()}</span>
              </span>
            )}
            <span>ID: {currentProposal.id}</span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => onDelete(currentProposal.id)}
            className="flex items-center space-x-1.5 px-3 py-2 rounded-lg border border-red-900/40 bg-red-950/20 text-red-400 text-xs font-semibold hover:bg-red-950/40 hover:border-red-900/60 transition"
          >
            <Trash2 className="w-4 h-4" />
            <span>Delete</span>
          </button>
          
          {currentProposal.status === 'completed' && (
            <button
              onClick={downloadMarkdown}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold shadow-md shadow-sky-500/10 transition"
            >
              <FileDown className="w-4 h-4" />
              <span>Export Markdown</span>
            </button>
          )}
        </div>
      </div>

      {/* Tabs navigation */}
      <div className="flex border-b border-slate-800 space-x-1 p-1 bg-slate-900/30 rounded-lg max-w-2xl">
        {tabs.map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-medium transition shrink-0 ${
                isActive
                  ? 'bg-slate-800 text-sky-400 border-b-2 border-sky-500 rounded-b-none'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab content area */}
      <div className="glass-panel p-6 rounded-xl min-h-[400px]">
        {loadingDetails ? (
          <div className="flex flex-col items-center justify-center h-96 space-y-4">
            <div className="w-8 h-8 border-2 border-t-sky-500 border-r-sky-500 border-slate-800 rounded-full animate-spin"></div>
            <p className="text-xs text-slate-400 font-mono">Retrieving agent sections...</p>
          </div>
        ) : currentProposal.status !== 'completed' ? (
          <div className="flex flex-col items-center justify-center h-96 space-y-4">
            <div className="w-8 h-8 border-2 border-t-sky-500 border-r-sky-500 border-slate-800 rounded-full animate-spin"></div>
            <p className="text-xs text-slate-400 font-mono">Agent team is analyzing logs. Current status: {currentProposal.status}...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Tab: Compiled Pitch */}
            {activeTab === 'pitch' && (
              <div className="prose prose-invert max-w-none">
                <SimpleMarkdown content={currentProposal.final_proposal?.pitch} />
              </div>
            )}

            {/* Tab: Technical Spec */}
            {activeTab === 'tech' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5 mb-3">Inventor Findings</h3>
                  <SimpleMarkdown content={currentProposal.final_proposal?.inventor} />
                </div>
                <div className="pt-6 border-t border-slate-900">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5 mb-3">Architectural Engineering</h3>
                  <SimpleMarkdown content={currentProposal.final_proposal?.engineer} />
                </div>
              </div>
            )}

            {/* Tab: Financial Plan */}
            {activeTab === 'finance' && (
              <div>
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5 mb-3">Economist Projections</h3>
                <SimpleMarkdown content={currentProposal.final_proposal?.economist} />
              </div>
            )}

            {/* Tab: Security & SWOT */}
            {activeTab === 'security' && (
              <div>
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5 mb-3">Critic Audit & Vulnerabilities</h3>
                <SimpleMarkdown content={currentProposal.final_proposal?.critic} />
              </div>
            )}

            {/* Tab: Agent Run Logs */}
            {activeTab === 'logs' && (
              <div className="space-y-4">
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5">Orchestration Event Logs</h3>
                
                <div className="space-y-3">
                  {currentProposal.logs && currentProposal.logs.map((log) => (
                    <div key={log.id} className="p-4 bg-slate-950 rounded-lg border border-slate-850/80 font-mono text-xs space-y-2">
                      <div className="flex items-center justify-between border-b border-slate-900 pb-1.5 text-[10px] text-slate-500">
                        <span className="font-bold text-slate-350">{log.agent_name.toUpperCase()}</span>
                        <span>{new Date(log.created_at).toLocaleTimeString()}</span>
                      </div>
                      <div className="whitespace-pre-wrap text-slate-400 text-[11px] leading-relaxed">
                        {log.logs}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
