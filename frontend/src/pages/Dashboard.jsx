
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import { Users, ShieldAlert, Activity, ArrowUp, ArrowDown } from 'lucide-react';

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({
    totalIncidents: 0,
    highRiskCount: 0,
    avgRisk: 0,
    systemHealth: 100
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const response = await api.get('/logs');
      const data = response.data;
      processData(data);
      setLogs(data);
    } catch (error) {
      console.error("Failed to fetch logs", error);
    } finally {
      setLoading(false);
    }
  };

  const processData = (data) => {
    if (!data.length) return;

    const total = data.length;
    const highRisk = data.filter(l => l.is_anomaly).length;
    const avgRiskScore = data.reduce((acc, curr) => acc + (curr.risk_score || 0), 0) / total;

    setStats({
      totalIncidents: total,
      highRiskCount: highRisk,
      avgRisk: (avgRiskScore * 100).toFixed(1),
      systemHealth: Math.max(0, 100 - (highRisk * 5)) // Mock health metric
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
          <Icon className={`w-5 h-5 ${color.replace('text-', 'text-')}`} />
        </div>
        <div className="text-3xl font-bold text-white mb-1">{value}</div>
        <div className="text-xs text-gray-500 font-medium">{subtext}</div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Dashboard Overview</h1>
        <div className="flex items-center space-x-2 text-sm text-gray-400">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span>System Online</span>
        </div>
      </div>

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
          <h3 className="text-lg font-bold text-white mb-6">Live Risk Monitor</h3>
          <div className="h-[300px]">
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
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-dark-card border border-gray-800 rounded-xl p-6 flex flex-col">
          <h3 className="text-lg font-bold text-white mb-4">Recent Alerts</h3>
          <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
            {logs.filter(l => l.is_anomaly).slice(0, 5).map((log, idx) => (
              <div key={idx} className="bg-dark-bg/50 p-3 rounded-lg border border-red-500/20 flex items-start space-x-3">
                <ShieldAlert className="w-5 h-5 text-red-500 mt-0.5" />
                <div>
                  <div className="text-sm font-bold text-white">High Risk Activity Detected</div>
                  <div className="text-xs text-gray-400 mt-1">
                    Risk Score: <span className="text-red-400">{(log.risk_score * 100).toFixed(0)}</span>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {log.action_type || 'Unknown Action'} • {new Date(log.timestamp).toLocaleTimeString()}
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
