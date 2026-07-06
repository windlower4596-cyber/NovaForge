import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import Creator from './components/Creator';
import ProposalViewer from './components/ProposalViewer';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard'); // dashboard, creator, viewer
  const [selectedProposalId, setSelectedProposalId] = useState(null);
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch proposals from API
  const fetchProposals = () => {
    setLoading(true);
    axios.get('http://127.0.0.1:8000/api/v1/proposals')
      .then(res => {
        setProposals(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching proposals:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProposals();
  }, []);

  const handleSelectProposal = (id) => {
    setSelectedProposalId(id);
    setActivePage('viewer');
  };

  const handleDeleteProposal = (id) => {
    if (window.confirm('Are you sure you want to delete this innovation proposal?')) {
      axios.delete(`http://127.0.0.1:8000/api/v1/proposals/${id}`)
        .then(() => {
          fetchProposals();
          if (selectedProposalId === id) {
            setActivePage('dashboard');
          }
        })
        .catch(err => {
          console.error('Error deleting proposal:', err);
        });
    }
  };

  // Find the selected proposal object
  const selectedProposal = proposals.find(p => p.id === selectedProposalId);

  return (
    <div className="min-h-screen flex flex-col pb-16">
      {/* Sleek brand Navigation */}
      <Navigation />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 pt-8">
        {activePage === 'dashboard' && (
          <div>
            {loading && proposals.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-[400px] space-y-3">
                <div className="w-8 h-8 border-2 border-t-sky-500 border-r-sky-500 border-slate-800 rounded-full animate-spin"></div>
                <p className="text-xs text-slate-500 font-mono">Synchronizing database indices...</p>
              </div>
            ) : (
              <Dashboard
                proposals={proposals}
                onSelectProposal={handleSelectProposal}
                onDeleteProposal={handleDeleteProposal}
                onStartNew={() => setActivePage('creator')}
              />
            )}
          </div>
        )}

        {activePage === 'creator' && (
          <Creator
            onBack={() => {
              setActivePage('dashboard');
              fetchProposals();
            }}
            onSelectProposal={handleSelectProposal}
          />
        )}

        {activePage === 'viewer' && (selectedProposal || selectedProposalId) && (
          <ProposalViewer
            proposal={selectedProposal || { id: selectedProposalId }}
            onBack={() => {
              setActivePage('dashboard');
              fetchProposals();
            }}
            onDelete={handleDeleteProposal}
          />
        )}
      </main>
    </div>
  );
}
