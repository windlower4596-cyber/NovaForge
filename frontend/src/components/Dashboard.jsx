import React from 'react';
import { Plus, Award, ShieldAlert, Cpu, Sparkles, FolderKanban, Trash2, Calendar } from 'lucide-react';

export default function Dashboard({ proposals, onSelectProposal, onDeleteProposal, onStartNew }) {
  const totalProposals = proposals.length;
  const completedProposals = proposals.filter(p => p.status === 'completed').length;
  const processingProposals = proposals.filter(p => p.status === 'processing').length;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Upper banner section */}
      <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/40 p-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 max-w-xl text-center md:text-left">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-950/50 border border-sky-900/60 text-sky-400 text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            <span>AI Multi-Agent Innovation Synthesizer</span>
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight">Forge Ideas into Enterprise Proposals</h2>
          <p className="text-sm text-slate-400">
            NovaForge AI orchestrates specialized offline agents (Inventor, Engineer, Economist, Critic) 
            to generate patentable claims, software specs, budgets, and security audits—instantly and privately.
          </p>
        </div>
        <button
          onClick={onStartNew}
          className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-sky-500/20 hover:shadow-sky-500/30 transition transform hover:-translate-y-0.5 active:translate-y-0"
        >
          <Plus className="w-4 h-4" />
          <span>New Proposal</span>
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Card 1: Total */}
        <div className="glass-card p-5 rounded-xl flex items-center space-x-4">
          <div className="w-12 h-12 rounded-lg bg-sky-950/60 border border-sky-900/40 flex items-center justify-center text-sky-400">
            <FolderKanban className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Total Proposals</p>
            <h3 className="text-2xl font-bold font-mono text-slate-100">{totalProposals}</h3>
          </div>
        </div>

        {/* Card 2: Completed */}
        <div className="glass-card p-5 rounded-xl flex items-center space-x-4">
          <div className="w-12 h-12 rounded-lg bg-emerald-950/60 border border-emerald-900/40 flex items-center justify-center text-emerald-400">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Completed</p>
            <h3 className="text-2xl font-bold font-mono text-slate-100">{completedProposals}</h3>
          </div>
        </div>

        {/* Card 3: Processing */}
        <div className="glass-card p-5 rounded-xl flex items-center space-x-4">
          <div className="w-12 h-12 rounded-lg bg-amber-950/60 border border-amber-900/40 flex items-center justify-center text-amber-400">
            <Cpu className="w-6 h-6 animate-spin-slow" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Processing</p>
            <h3 className="text-2xl font-bold font-mono text-slate-100">{processingProposals}</h3>
          </div>
        </div>

        {/* Card 4: Agent Core */}
        <div className="glass-card p-5 rounded-xl flex items-center space-x-4">
          <div className="w-12 h-12 rounded-lg bg-indigo-950/60 border border-indigo-900/40 flex items-center justify-center text-indigo-400">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Active Agents</p>
            <h3 className="text-2xl font-bold font-mono text-slate-100">6 Specialized</h3>
          </div>
        </div>
      </div>

      {/* Historical Proposals Listing */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold tracking-wide">Historical Proposals</h3>

        {proposals.length === 0 ? (
          <div className="glass-panel rounded-xl p-12 text-center flex flex-col items-center justify-center space-y-4">
            <FolderKanban className="w-12 h-12 text-slate-600" />
            <div className="space-y-1">
              <p className="text-slate-400 font-semibold text-sm">No proposals generated yet</p>
              <p className="text-xs text-slate-500 max-w-sm">
                Enter an innovation idea to coordinate your specialized agent team and compile a business proposal.
              </p>
            </div>
            <button
              onClick={onStartNew}
              className="px-4 py-2 bg-slate-800 border border-slate-700 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-200 transition"
            >
              Start Forging
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {proposals.map(proposal => (
              <div 
                key={proposal.id} 
                className="glass-card p-6 rounded-xl relative group flex flex-col justify-between h-52 border border-slate-800"
              >
                {/* Upper info */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] text-slate-500 font-mono tracking-widest uppercase">ID: {proposal.id.slice(0, 8)}</span>
                    
                    {/* Status badge */}
                    {proposal.status === 'completed' && (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md bg-emerald-950/40 border border-emerald-900/50 text-[10px] font-semibold text-emerald-400">
                        <span className="w-1 h-1 bg-emerald-400 rounded-full"></span>
                        <span>Completed</span>
                      </span>
                    )}
                    {proposal.status === 'processing' && (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md bg-amber-950/40 border border-amber-900/50 text-[10px] font-semibold text-amber-400">
                        <span className="w-1 h-1 bg-amber-400 rounded-full animate-ping"></span>
                        <span>Processing</span>
                      </span>
                    )}
                    {proposal.status === 'failed' && (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md bg-red-950/40 border border-red-900/50 text-[10px] font-semibold text-red-400">
                        <span className="w-1 h-1 bg-red-400 rounded-full"></span>
                        <span>Failed</span>
                      </span>
                    )}
                  </div>
                  
                  <h4 
                    onClick={() => onSelectProposal(proposal.id)}
                    className="text-base font-bold text-slate-100 hover:text-sky-400 transition cursor-pointer line-clamp-1"
                  >
                    {proposal.title === 'Processing...' ? 'Agent Analysis in Progress...' : proposal.title}
                  </h4>
                  <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                    {proposal.idea_text}
                  </p>
                </div>

                {/* Footer links */}
                <div className="flex items-center justify-between border-t border-slate-800/80 pt-3 mt-4">
                  <span className="flex items-center space-x-1 text-[10px] text-slate-500 font-mono">
                    <Calendar className="w-3.5 h-3.5" />
                    <span>{new Date(proposal.created_at).toLocaleDateString()}</span>
                  </span>
                  
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => onDeleteProposal(proposal.id)}
                      className="p-1.5 rounded-md text-slate-500 hover:text-red-400 hover:bg-red-950/20 transition"
                      title="Delete Proposal"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onSelectProposal(proposal.id)}
                      className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-200 border border-slate-700 hover:border-slate-600 transition"
                    >
                      View Report
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
