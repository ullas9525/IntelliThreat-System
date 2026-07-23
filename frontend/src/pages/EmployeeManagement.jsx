import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { UserPlus, Users, CheckCircle, AlertCircle, Shield, Key, Mail, User, Trash2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

const EmployeeManagement = () => {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createLoading, setCreateLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'Analyst'
  });

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await api.get('/auth/users');
      setUsers(res.data);
    } catch (err) {
      console.error("Failed to fetch users", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCreateEmployee = async (e) => {
    e.preventDefault();
    setCreateLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await api.post('/auth/register', formData);
      setMessage({ type: 'success', text: `Successfully created employee account for ${formData.username}!` });
      setFormData({ username: '', email: '', password: '', role: 'Analyst' });
      fetchUsers();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.msg || 'Failed to create employee account' });
    } finally {
      setCreateLoading(false);
    }
  };

  const handleDeleteUser = async (targetUser) => {
    if (targetUser.id === currentUser?.id) {
      alert("You cannot delete your own logged-in admin account!");
      return;
    }

    if (!window.confirm(`Are you sure you want to remove employee account "${targetUser.username}"?`)) {
      return;
    }

    try {
      await api.delete(`/auth/users/${targetUser.id}`);
      setMessage({ type: 'success', text: `Employee account "${targetUser.username}" removed.` });
      fetchUsers();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.msg || 'Failed to delete user' });
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">Employee Account Provisioning</h1>
        <p className="text-gray-400 text-sm">IT Admin Console for creating, auditing, and managing employee access credentials.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Creation Form */}
        <div className="bg-dark-card border border-gray-800 rounded-xl p-6 h-fit">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2.5 bg-accent-primary/20 text-accent-primary rounded-lg">
              <UserPlus className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-semibold text-white">Create Employee Login</h2>
          </div>

          {message.text && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-3 rounded-lg text-sm mb-4 flex items-center space-x-2 ${
                message.type === 'success'
                  ? 'bg-green-500/20 border border-green-500 text-green-300'
                  : 'bg-red-500/20 border border-red-500 text-red-300'
              }`}
            >
              {message.type === 'success' ? <CheckCircle className="w-4 h-4 shrink-0" /> : <AlertCircle className="w-4 h-4 shrink-0" />}
              <span>{message.text}</span>
            </motion.div>
          )}

          <form onSubmit={handleCreateEmployee} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="e.g. emp_john"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john@fintech.com"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Initial Password</label>
              <div className="relative">
                <Key className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Role / Privilege</label>
              <div className="relative">
                <Shield className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
                <select
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-accent-primary"
                >
                  <option value="Analyst">Analyst</option>
                  <option value="Employee">Employee</option>
                  <option value="Vendor">Vendor</option>
                  <option value="Manager">Manager</option>
                  <option value="IT Admin">IT Admin</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={createLoading}
              className="w-full bg-accent-primary hover:bg-blue-600 text-white font-medium py-2.5 rounded-lg text-sm transition-colors flex items-center justify-center disabled:opacity-50 mt-4"
            >
              {createLoading ? 'Provisioning...' : 'Create Employee Account'}
            </button>
          </form>
        </div>

        {/* Employee Roster Table */}
        <div className="lg:col-span-2 bg-dark-card border border-gray-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-blue-500/20 text-blue-400 rounded-lg">
                <Users className="w-5 h-5" />
              </div>
              <h2 className="text-lg font-semibold text-white">Active Employee Roster</h2>
            </div>
            <span className="text-xs px-2.5 py-1 bg-gray-800 text-gray-300 rounded-full font-mono">
              Total: {users.length}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-800 text-xs text-gray-400 uppercase tracking-wider">
                  <th className="pb-3 px-4">User ID</th>
                  <th className="pb-3 px-4">Username</th>
                  <th className="pb-3 px-4">Email</th>
                  <th className="pb-3 px-4">Role</th>
                  <th className="pb-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50 text-sm">
                {users.length > 0 ? (
                  users.map((u) => (
                    <tr key={u.id} className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-mono text-gray-400">#{u.id}</td>
                      <td className="py-3 px-4 text-white font-medium">{u.username}</td>
                      <td className="py-3 px-4 text-gray-400">{u.email}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          u.role === 'IT Admin' || u.role === 'Admin'
                            ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                            : u.role === 'Vendor'
                            ? 'bg-orange-500/20 text-orange-300 border border-orange-500/30'
                            : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                        }`}>
                          {u.role}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        {u.id !== currentUser?.id ? (
                          <button
                            onClick={() => handleDeleteUser(u)}
                            className="p-1.5 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                            title="Remove Employee"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        ) : (
                          <span className="text-xs text-gray-500 italic">(You)</span>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="py-8 text-center text-gray-500">
                      No accounts provisioned yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmployeeManagement;
