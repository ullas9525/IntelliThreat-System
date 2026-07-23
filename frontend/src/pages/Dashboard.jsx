import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { Users, ShieldAlert, Activity, RefreshCw, Trash2, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({
    totalIncidents: 0,
    highRiskCount: 0,
    avgRisk: 0,
    systemHealth: 100
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [actionMsg, setActionMsg] = useState('');

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setRefreshing(true);
      const response = await api.get('/logs');
      const data = response.data;
      processData(data);
      setLogs(data);
    } catch (error) {
      console.error("Failed to fetch logs", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleClearTelemetry = async () => {
    if (!window.confirm("Are you sure you want to clear all telemetry logs from the database? This cannot be undone.")) {
      return;
    }

    try {
      await api.delete('/logs');
      setActionMsg('All telemetry logs purged successfully!');
      fetchData();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (error) {
      console.error("Failed to clear logs", error);
      alert(error.response?.data?.msg || "Failed to clear logs");
    }
  };

  const processData = (data) => {
    if (!data.length) {
      setStats({
        totalIncidents: 0,
        highRiskCount: 0,
        avgRisk: '0.0',
        systemHealth: 100
      });
      return;
    }

    const total = data.length;
    const highRisk = data.filter(l => l.is_anomaly).length;
    const avgRiskScore = data.reduce((acc, curr) => acc + (curr.risk_score || 0), 0) / total;

    setStats({
      totalIncidents: total,
      highRiskCount: highRisk,
      avgRisk: (avgRiskScore * 100).toFixed(1),
      systemHealth: Math.max(0, 100 - (highRisk * 5))
    });
  };

  // Prepare chart data (Time series of risk scores)
  const chartData = logs.slice(0, 20).reverse().map(log => ({
    time: new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    risk: (log.risk_score * 100).toFixed(0),
    threshold: 85
  }));

  const StatCard = ({ title, value, subtext, icon: Icon, color }) => (
    <div className="bg-dark-card border border-gray-800 p-6 rounded-xl relative overflow-hidden group hover:border-gray-700 transition-all">
      <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${color}`}>
        <Icon className="w-16 h-16" />
      </div>
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider">{title}</h3>
          <Icon className={`w-5 h-5 ${color}`} />
        </div>
        <div className="text-3xl font-bold text-white mb-1">{value}</div>
        <div className="text-xs text-gray-500 font-medium">{subtext}</div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Admin Security Console</h1>
          <p className="text-xs text-gray-400 mt-1">Real-Time Insider Threat Telemetry & AI Anomaly Detection</p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={fetchData}
            disabled={refreshing}
            className="flex items-center space-x-2 px-3.5 py-2 bg-dark-card border border-gray-700 hover:bg-white/5 text-gray-300 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin' : ''}`} />
            <span>Refresh Data</span>
          </button>

          <button
            onClick={handleClearTelemetry}
            className="flex items-center space-x-2 px-3.5 py-2 bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 text-red-400 rounded-lg text-xs font-medium transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Telemetry</span>
          </button>

          <div className="hidden md:flex items-center space-x-2 text-xs text-gray-400 border-l border-gray-800 pl-3">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span>Live Stream</span>
          </div>
        </div>
      </div>

      {actionMsg && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-3 bg-green-500/20 border border-green-500/40 text-green-300 rounded-xl text-xs flex items-center space-x-2"
        >
          <CheckCircle2 className="w-4 h-4 text-green-400 shrink-0" />
          <span>{actionMsg}</span>
        </motion.div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Incidents"
          value={stats.totalIncidents}
          subtext="Last 24 Hours"
          icon={Activity}
          color="text-blue-500"
        />
        <StatCard
          title="High Risk Alerts"
          value={stats.highRiskCount}
          subtext="Requires Review"
          icon={ShieldAlert}
          color="text-red-500"
        />
        <StatCard
          title="Avg Risk Score"
          value={stats.avgRisk}
          subtext="0-100 Scale"
          icon={Users}
          color="text-yellow-500"
        />
        <StatCard
          title="System Health"
          value={`${stats.systemHealth}%`}
          subtext="Optimized"
          icon={Activity}
          color="text-green-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="lg:col-span-2 bg-dark-card border border-gray-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-white">Live Risk Monitor</h3>
            <span className="text-xs text-gray-500">Real-time Isolation Score Boundary</span>
          </div>
          <div className="h-[300px]">
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                  <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
                    itemStyle={{ color: '#f8fafc' }}
                  />
                  <Area
                    type="monotone"
                    dataKey="risk"
                    stroke="#ef4444"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorRisk)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500 text-sm">
                No telemetry logs recorded. System ready.
              </div>
            )}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-dark-card border border-gray-800 rounded-xl p-6 flex flex-col">
          <h3 className="text-lg font-bold text-white mb-4">Recent Alerts</h3>
          <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
            {logs.filter(l => l.is_anomaly).slice(0, 5).map((log, idx) => (
              <div key={idx} className="bg-dark-bg/50 p-3 rounded-lg border border-red-500/20 flex items-start space-x-3">
                <ShieldAlert className="w-5 h-5 text-red-500 mt-0.5 shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-bold text-white truncate flex items-center justify-between">
                    <span>{log.username || `User #${log.user_id}`}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/20 text-red-300 rounded-full font-mono font-normal">
                      {(log.risk_score * 100).toFixed(0)}% Risk
                    </span>
                  </div>
                  <div className="text-xs text-gray-400 mt-1 truncate">
                    Action: <span className="text-gray-200">{log.action_type || 'Unknown Action'}</span>
                  </div>
                  <div className="text-xs text-gray-500 mt-1 truncate">
                    IP: {log.ip_address || 'N/A'} • {new Date(log.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            {logs.filter(l => l.is_anomaly).length === 0 && (
              <div className="text-center text-gray-500 py-8">
                No active alerts. System secure.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
