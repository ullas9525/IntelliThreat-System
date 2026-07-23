import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Lock, User, Loader2, ShieldCheck, Info } from 'lucide-react';
import { motion } from 'framer-motion';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);

    if (result.success) {
      const storedUser = localStorage.getItem('user');
      const parsedUser = storedUser ? JSON.parse(storedUser) : null;
      const isAdmin = parsedUser?.role === 'IT Admin' || parsedUser?.role === 'Admin';
      window.location.href = isAdmin ? '/dashboard' : '/portal';
    } else {
      setError(result.message);
    }
    setLoading(false);
  };

  return (
    <div className="glass p-8 rounded-2xl border border-gray-700 w-full max-w-sm mx-auto shadow-2xl">
      <div className="text-center mb-6">
        <div className="w-12 h-12 bg-accent-primary/20 rounded-xl flex items-center justify-center mx-auto mb-3 text-accent-primary">
          <ShieldCheck className="w-7 h-7" />
        </div>
        <h2 className="text-2xl font-bold text-white">Employee Sign In</h2>
        <p className="text-xs text-gray-400 mt-1">Access IntelliThreat Security Console</p>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="bg-accent-danger/20 border border-accent-danger text-red-200 text-sm p-3 rounded-lg mb-4"
        >
          {error}
        </motion.div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1 uppercase tracking-wider">Username</label>
          <div className="relative">
            <User className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-dark-bg/50 border border-gray-700 rounded-lg py-2.5 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-all"
              placeholder="Enter username"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1 uppercase tracking-wider">Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-dark-bg/50 border border-gray-700 rounded-lg py-2.5 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-all"
              placeholder="••••••••"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent-primary hover:bg-blue-600 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed mt-6"
        >
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Sign In'}
        </button>
      </form>

      <div className="mt-6 p-3 rounded-lg bg-blue-500/10 border border-blue-500/30 text-xs text-blue-300 flex items-start space-x-2">
        <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
        <span>
          Employee accounts are created by IT Admin. Please contact your administrator for login credentials.
        </span>
      </div>
    </div>
  );
};

export default Login;
