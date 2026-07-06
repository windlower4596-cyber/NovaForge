import React, { useEffect, useState } from 'react';
import { Cpu, Server, Layers, HelpCircle, HardDrive } from 'lucide-react';
import axios from 'axios';

export default function Navigation() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [mcpOnline, setMcpOnline] = useState(false);

  useEffect(() => {
    // Check Backend Server
    const checkBackend = () => {
      axios.get('http://127.0.0.1:8000/')
        .then(() => setBackendOnline(true))
        .catch(() => setBackendOnline(false));
    };

    // Check MCP Server
    const checkMCP = () => {
      axios.get('http://127.0.0.1:8001/')
        .then(() => setMcpOnline(true))
        .catch(() => setMcpOnline(false));
    };

    checkBackend();
    checkMCP();

    const interval = setInterval(() => {
      checkBackend();
      checkMCP();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/85 backdrop-blur-md px-6 py-4 flex items-center justify-between">
      {/* Brand logo & title */}
      <div className="flex items-center space-x-3">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 text-white shadow-lg shadow-sky-500/25">
          <Cpu className="w-5.5 h-5.5 animate-pulse" />
          <div className="absolute -inset-0.5 bg-gradient-to-tr from-sky-500 to-indigo-500 rounded-xl blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-tilt"></div>
        </div>
        <div>
          <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-sky-400 bg-clip-text text-transparent">
            NovaForge <span className="font-light text-sky-400">AI</span>
          </h1>
          <p className="text-[10px] text-slate-500 font-mono tracking-widest uppercase">Multi-Agent Engine</p>
        </div>
      </div>

      {/* Center navigation links */}
      <div className="hidden md:flex items-center space-x-1 bg-slate-900/60 p-1 rounded-lg border border-slate-800/80">
        <button className="flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-slate-100 hover:bg-slate-800/50 transition">
          <Layers className="w-3.5 h-3.5" />
          <span>Architecture</span>
        </button>
        <button className="flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-slate-100 hover:bg-slate-800/50 transition">
          <HelpCircle className="w-3.5 h-3.5" />
          <span>Documentation</span>
        </button>
      </div>

      {/* Services status */}
      <div className="flex items-center space-x-3 text-xs font-mono">
        {/* Local mode */}
        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 text-[11px] font-sans">
          <HardDrive className="w-3 h-3" />
          <span>Offline Mode</span>
        </div>

        {/* Backend status */}
        <div className="flex items-center space-x-2 bg-slate-900/70 border border-slate-800 px-3 py-1.5 rounded-lg">
          <Server className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400 hidden sm:inline">Backend:</span>
          {backendOnline ? (
            <span className="flex items-center space-x-1 text-emerald-400">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping"></span>
              <span>Online</span>
            </span>
          ) : (
            <span className="flex items-center space-x-1 text-red-400">
              <span className="w-1.5 h-1.5 bg-red-400 rounded-full"></span>
              <span>Offline</span>
            </span>
          )}
        </div>

        {/* MCP Status */}
        <div className="flex items-center space-x-2 bg-slate-900/70 border border-slate-800 px-3 py-1.5 rounded-lg">
          <Cpu className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400 hidden sm:inline">MCP:</span>
          {mcpOnline ? (
            <span className="flex items-center space-x-1 text-sky-400">
              <span className="w-1.5 h-1.5 bg-sky-400 rounded-full animate-ping"></span>
              <span>Active</span>
            </span>
          ) : (
            <span className="flex items-center space-x-1 text-red-400">
              <span className="w-1.5 h-1.5 bg-red-400 rounded-full"></span>
              <span>Offline</span>
            </span>
          )}
        </div>
      </div>
    </header>
  );
}
