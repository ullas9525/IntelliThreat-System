import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, Filter, AlertTriangle, CheckCircle, Trash2, CheckCircle2, User } from 'lucide-react';
import { motion } from 'framer-motion';

const UserActivity = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all'); // all, normal, anomaly
  const [actionMsg, setActionMsg] = useState('');

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const response = await api.get('/logs');
      setLogs(response.data);
    } catch (error) {
      console.error("Failed to fetch logs", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSingleLog = async (logId) => {
    if (!window.confirm(`Are you sure you want to delete Log ID #${logId}?`)) {
      return;
    }

    try {
      await api.delete(`/logs/${logId}`);
      setActionMsg(`Log #${logId} deleted successfully.`);
      fetchLogs();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (error) {
      console.error("Failed to delete log", error);
      alert(error.response?.data?.msg || "Failed to delete log");
    }
  };

  const handleClearAllLogs = async () => {
    if (!window.confirm("Are you sure you want to clear ALL activity logs from the database? This action cannot be undone.")) {
      return;
    }

    try {
      await api.delete('/logs');
      setActionMsg('All activity logs purged successfully.');
      fetchLogs();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (error) {
      console.error("Failed to clear logs", error);
      alert(error.response?.data?.msg || "Failed to clear logs");
    }
  };

  const filteredLogs = logs.filter(log => {
    const matchesSearch =
      log.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.action_type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.role?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.ip_address?.includes(searchTerm);

    const matchesFilter =
      filter === 'all' ? true :
        filter === 'anomaly' ? log.is_anomaly :
          !log.is_anomaly;

    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">User Activity Logs</h1>
          <p className="text-gray-400 text-sm">Monitor, audit, and manage employee access events.</p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleClearAllLogs}
            className="bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 text-red-400 px-4 py-2 rounded-lg text-xs font-semibold flex items-center transition-colors"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Clear All Logs
          </button>
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

      {/* Filters */}
      <div className="bg-dark-card border border-gray-800 rounded-xl p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-2.5 w-5 h-5 text-gray-500" />
          <input
            type="text"
            placeholder="Search by Username, Action, or IP..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-dark-bg border border-gray-700 rounded-lg py-2 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
          />
        </div>

        <div className="flex items-center space-x-2 w-full md:w-auto">
          <Filter className="w-5 h-5 text-gray-500" />
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-dark-bg border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent-primary"
          >
            <option value="all">All Events</option>
            <option value="normal">Normal Activity</option>
            <option value="anomaly">Anomalies Only</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-dark-card border border-gray-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-dark-bg border-b border-gray-800 text-gray-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Timestamp</th>
                <th className="px-6 py-4">Employee / Username</th>
                <th className="px-6 py-4">Action</th>
                <th className="px-6 py-4">IP Address</th>
                <th className="px-6 py-4">Risk Score</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800 text-sm">
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-8 text-gray-500">Loading logs...</td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-8 text-gray-500">No logs found matching criteria.</td>
                </tr>
              ) : (
                filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-white/5 transition-colors">
                    <td className="px-6 py-4">
                      {log.is_anomaly ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-500/10 text-red-500 border border-red-500/20">
                          <AlertTriangle className="w-3 h-3 mr-1" /> Anomaly
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/10 text-green-500 border border-green-500/20">
                          <CheckCircle className="w-3 h-3 mr-1" /> Normal
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-gray-300">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-7 h-7 rounded-full bg-accent-primary/20 flex items-center justify-center text-accent-primary font-bold text-xs">
                          {log.username?.charAt(0).toUpperCase() || 'U'}
                        </div>
                        <div>
                          <span className="text-white font-semibold block">{log.username || `User #${log.user_id}`}</span>
                          <span className="text-xs text-gray-400 block">{log.role || 'Employee'}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white font-medium">
                      {log.action_type || 'Unknown'}
                    </td>
                    <td className="px-6 py-4 text-gray-400 font-mono">
                      {log.ip_address || 'N/A'}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="w-16 h-1.5 bg-gray-700 rounded-full mr-2 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${log.risk_score > 0.7 ? 'bg-red-500' : 'bg-green-500'}`}
                            style={{ width: `${log.risk_score * 100}%` }}
                          />
                        </div>
                        <span className={`font-mono font-bold ${log.risk_score > 0.7 ? 'text-red-400' : 'text-green-400'}`}>
                          {(log.risk_score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => handleDeleteSingleLog(log.id)}
                        className="p-1.5 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                        title="Delete Log"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UserActivity;
