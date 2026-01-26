
import React, { useState } from 'react';
import api from '../services/api';
import { Shield, AlertTriangle, CheckCircle, Zap, Server, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ThreatSimulator = () => {
  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState(null);

  const scenarios = [
    {
      id: 'normal',
      name: 'Routine User Activity',
      description: 'Standard file access and browsing during work hours.',
      icon: CheckCircle,
      color: 'text-green-500',
      data: {
        session_duration: 45.0,
        data_download_mb: 15.0,
        transaction_amount: 0,
        access_count: 12,
        login_frequency: 1,
        failed_logins: 0,
        role: 'Analyst',
        action_type: 'Report Generation'
      }
    },
    {
      id: 'exfiltration',
      name: 'Data Exfiltration Attack',
      description: 'Large volume download to external drive at odd hours.',
      icon: AlertTriangle,
      color: 'text-red-500',
      data: {
        session_duration: 10.0,
        data_download_mb: 4500.0,
        transaction_amount: 0,
        access_count: 200,
        login_frequency: 3,
        failed_logins: 1,
        role: 'Analyst',
        action_type: 'Bulk Export'
      }
    },
    {
      id: 'bruteforce',
      name: 'Brute Force Attempt',
      description: 'Multiple failed login attempts followed by access.',
      icon: Shield,
      color: 'text-orange-500',
      data: {
        session_duration: 2.0,
        data_download_mb: 0.0,
        transaction_amount: 0,
        access_count: 5,
        login_frequency: 20,
        failed_logins: 15,
        role: 'Unknown',
        action_type: 'Login Retry'
      }
    }
  ];

  const handleSimulate = async (scenario) => {
    setLoading(true);
    setSelectedScenario(scenario.id);
    setSimulationResult(null);

    try {
      // Simulate network delay for effect
      await new Promise(r => setTimeout(r, 800));

      const response = await api.post('/predict', scenario.data);
      setSimulationResult(response.data);
    } catch (error) {
      console.error("Simulation failed", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white mb-2">Threat Simulation Lab</h1>
        <p className="text-gray-400">Inject synthetic logs to test the Anomaly Detection Engine in real-time.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Scenarios Column */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-white mb-4">Select Scenario</h2>
          {scenarios.map((scenario) => {
            const Icon = scenario.icon;
            return (
              <button
                key={scenario.id}
                onClick={() => handleSimulate(scenario)}
                disabled={loading}
                className={`w-full text-left p-4 rounded-xl border transition-all ${selectedScenario === scenario.id
                    ? 'bg-accent-primary/10 border-accent-primary'
                    : 'bg-dark-card border-gray-800 hover:border-gray-600'
                  }`}
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg bg-dark-bg ${scenario.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-white font-medium">{scenario.name}</h3>
                    <p className="text-sm text-gray-500 mt-1">{scenario.description}</p>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Visualization Column */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-dark-card border border-gray-800 rounded-xl p-8 min-h-[400px] flex flex-col items-center justify-center relative overflow-hidden">
            {/* Background Grid */}
            <div className="absolute inset-0 opacity-5 bg-[linear-gradient(rgba(255,255,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.1)_1px,transparent_1px)] bg-[size:20px_20px]"></div>

            <AnimatePresence mode='wait'>
              {loading ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center z-10"
                >
                  <div className="w-16 h-16 border-4 border-accent-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-accent-primary font-mono animate-pulse">Analyzing Pattern...</p>
                </motion.div>
              ) : simulationResult ? (
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="w-full max-w-md z-10"
                >
                  <div className={`
                    text-center p-8 rounded-2xl border-2 mb-6
                    ${simulationResult.is_anomaly
                      ? 'bg-red-500/10 border-red-500'
                      : 'bg-green-500/10 border-green-500'}
                  `}>
                    {simulationResult.is_anomaly ? (
                      <ShieldAlert className="w-20 h-20 text-red-500 mx-auto mb-4" />
                    ) : (
                      <CheckCircle className="w-20 h-20 text-green-500 mx-auto mb-4" />
                    )}

                    <h3 className="text-2xl font-bold text-white mb-2">
                      {simulationResult.is_anomaly ? 'THREAT DETECTED' : 'NORMAL ACTIVITY'}
                    </h3>
                    <p className="text-gray-400">
                      The AI Engine has analyzed this session.
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-dark-bg p-4 rounded-lg border border-gray-700">
                      <div className="text-sm text-gray-500 mb-1">Risk Probability</div>
                      <div className={`text-2xl font-mono font-bold ${simulationResult.risk_score > 0.7 ? 'text-red-400' : 'text-green-400'
                        }`}>
                        {(simulationResult.risk_score * 100).toFixed(1)}%
                      </div>
                    </div>
                    <div className="bg-dark-bg p-4 rounded-lg border border-gray-700">
                      <div className="text-sm text-gray-500 mb-1">Raw Anomaly Score</div>
                      <div className="text-2xl font-mono font-bold text-white">
                        {simulationResult.raw_score.toFixed(3)}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="text-center text-gray-500 z-10">
                  <Server className="w-16 h-16 mx-auto mb-4 opacity-20" />
                  <p>Select a scenario to launch simulation</p>
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatSimulator;
