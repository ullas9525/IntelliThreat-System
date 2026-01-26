
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, Filter, Download, AlertTriangle, CheckCircle } from 'lucide-react';

const UserActivity = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all'); // all, normal, anomaly

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

  const filteredLogs = logs.filter(log => {
    const matchesSearch =
      log.action_type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
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
          <p className="text-gray-400 text-sm">Monitor and audit system access events.</p>
        </div>

        <div className="flex items-center space-x-3">
          <button className="bg-dark-card border border-gray-700 text-white px-4 py-2 rounded-lg flex items-center hover:bg-white/5 transition-colors">
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-dark-card border border-gray-800 rounded-xl p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-2.5 w-5 h-5 text-gray-500" />
          <input
            type="text"
            placeholder="Search by Action or IP..."
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
                <th className="px-6 py-4">User ID</th>
                <th className="px-6 py-4">Action</th>
                <th className="px-6 py-4">IP Address</th>
                <th className="px-6 py-4">Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800 text-sm">
              {loading ? (
                <tr>
                  <td colSpan="6" className="text-center py-8 text-gray-500">Loading logs...</td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-8 text-gray-500">No logs found matching criteria.</td>
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
                    <td className="px-6 py-4 text-gray-300">
                      User #{log.user_id}
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
