import React from 'react';
import ThreatSimulator from './ThreatSimulator';
import UserActivity from './UserActivity';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, UserCheck, Zap, Activity } from 'lucide-react';

const EmployeePortal = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-accent-primary/20 via-dark-card to-dark-card border border-accent-primary/30 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-accent-primary/20 flex items-center justify-center text-accent-primary font-bold text-xl">
            {user?.username?.charAt(0).toUpperCase() || 'E'}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl font-bold text-white">Welcome, {user?.username}</h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-500/20 text-green-300 border border-green-500/30 flex items-center">
                <ShieldCheck className="w-3.5 h-3.5 mr-1" /> Active Session
              </span>
            </div>
            <p className="text-sm text-gray-400 mt-1">
              Employee Portal — Role: <span className="text-accent-primary font-medium">{user?.role || 'Employee'}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3 bg-dark-bg/60 p-3 rounded-xl border border-gray-800 text-xs text-gray-300">
          <Zap className="w-4 h-4 text-amber-400 shrink-0" />
          <span>Simulated or logged attacks are automatically monitored & reported to Admin.</span>
        </div>
      </div>

      {/* Threat Simulator Section */}
      <div className="bg-dark-card border border-gray-800 rounded-2xl p-6">
        <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-gray-800">
          <div className="p-2 bg-red-500/20 text-red-400 rounded-lg">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Threat Simulation & Telemetry Lab</h2>
            <p className="text-xs text-gray-400">Test session scenarios to see real-time AI risk evaluation.</p>
          </div>
        </div>
        <ThreatSimulator />
      </div>

      {/* Personal Activity Section */}
      <div className="bg-dark-card border border-gray-800 rounded-2xl p-6">
        <UserActivity />
      </div>
    </div>
  );
};

export default EmployeePortal;
