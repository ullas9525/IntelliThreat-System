
import React from 'react';
import { Save, Lock, Sliders, Bell } from 'lucide-react';

const Settings = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">System Settings</h1>
        <p className="text-gray-400">Manage security configurations and ML sensitivity.</p>
      </div>

      {/* Security */}
      <div className="bg-dark-card border border-gray-800 rounded-xl p-6">
        <div className="flex items-center mb-6">
          <div className="p-2 bg-blue-500/10 rounded-lg mr-4">
            <Lock className="w-6 h-6 text-blue-500" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Security Preferences</h2>
            <p className="text-sm text-gray-500">Password and authentication settings</p>
          </div>
        </div>

        <div className="space-y-4 max-w-lg">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Current Password</label>
            <input type="password" placeholder="••••••••" className="w-full bg-dark-bg border border-gray-700 rounded-lg p-2 text-white" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">New Password</label>
              <input type="password" placeholder="••••••••" className="w-full bg-dark-bg border border-gray-700 rounded-lg p-2 text-white" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Confirm</label>
              <input type="password" placeholder="••••••••" className="w-full bg-dark-bg border border-gray-700 rounded-lg p-2 text-white" />
            </div>
          </div>
          <div className="flex items-center justify-between pt-4">
            <div>
              <div className="text-white font-medium">Two-Factor Authentication</div>
              <div className="text-xs text-gray-500">Secure your account with 2FA</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-primary"></div>
            </label>
          </div>
        </div>
      </div>

      {/* ML Config */}
      <div className="bg-dark-card border border-gray-800 rounded-xl p-6">
        <div className="flex items-center mb-6">
          <div className="p-2 bg-purple-500/10 rounded-lg mr-4">
            <Sliders className="w-6 h-6 text-purple-500" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">ML Model Sensitivity</h2>
            <p className="text-sm text-gray-500">Adjust the anomaly detection thresholds</p>
          </div>
        </div>

        <div className="space-y-6 max-w-lg">
          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium text-gray-300">Anomaly Threshold</label>
              <span className="text-sm font-mono text-purple-400">85%</span>
            </div>
            <input type="range" className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500" />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Conservative</span>
              <span>Aggressive</span>
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium text-gray-300">Observation Window</label>
              <span className="text-sm font-mono text-purple-400">24 Hours</span>
            </div>
            <input type="range" className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500" />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button className="bg-accent-primary hover:bg-blue-600 text-white px-6 py-2.5 rounded-lg flex items-center font-medium transition-colors">
          <Save className="w-4 h-4 mr-2" />
          Save Changes
        </button>
      </div>
    </div>
  );
};

export default Settings;
