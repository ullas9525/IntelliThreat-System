import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Cpu, Lock, Activity, Users, ArrowRight, CheckCircle2, Zap, Eye, Terminal } from 'lucide-react';
import { motion } from 'framer-motion';

const Landing = () => {
  return (
    <div className="min-h-screen bg-dark-bg text-dark-text overflow-x-hidden">
      {/* Background Glow Overlay */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-gradient-to-b from-accent-primary/15 via-blue-600/5 to-transparent blur-3xl pointer-events-none z-0" />

      {/* Navbar */}
      <nav className="relative z-20 max-w-7xl mx-auto px-6 h-20 flex items-center justify-between border-b border-gray-800/60">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-accent-primary/20 border border-accent-primary/40 flex items-center justify-center text-accent-primary shadow-lg shadow-accent-primary/10">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white bg-gradient-to-r from-white via-gray-100 to-gray-400 bg-clip-text text-transparent">
            IntelliThreat System
          </span>
        </div>

        <div className="hidden md:flex items-center space-x-8 text-sm text-gray-400 font-medium">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#ai-engine" className="hover:text-white transition-colors">AI Engine</a>
          <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
        </div>

        <Link
          to="/login"
          className="px-5 py-2.5 bg-accent-primary hover:bg-blue-600 text-white text-sm font-semibold rounded-xl transition-all shadow-lg shadow-accent-primary/25 hover:shadow-accent-primary/40 flex items-center space-x-2"
        >
          <span>Sign In</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-accent-primary/10 border border-accent-primary/30 text-xs font-semibold text-accent-primary mb-8 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-accent-primary animate-pulse" />
            <span>AI-Powered Insider & Vendor Threat Intelligence</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight leading-tight mb-6">
            Detect Zero-Day Insider Attacks <br />
            <span className="bg-gradient-to-r from-accent-primary via-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Before Data Leaves Your Network
            </span>
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            IntelliThreat uses Unsupervised Isolation Forest Ensembles to identify data exfiltration, credential abuse, and anomalous employee telemetry in real time without historical labels.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/login"
              className="w-full sm:w-auto px-8 py-4 bg-accent-primary hover:bg-blue-600 text-white font-bold rounded-xl transition-all shadow-xl shadow-accent-primary/30 flex items-center justify-center space-x-3 text-base"
            >
              <span>Access Console & Sign In</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <a
              href="#features"
              className="w-full sm:w-auto px-8 py-4 bg-dark-card border border-gray-800 hover:border-gray-700 text-gray-300 font-semibold rounded-xl transition-all text-base"
            >
              Explore AI Engine
            </a>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 pt-12 border-t border-gray-800/60">
          <div className="p-4 rounded-xl bg-dark-card/50 border border-gray-800/60">
            <h3 className="text-3xl font-extrabold text-white">99.4%</h3>
            <p className="text-xs text-gray-400 mt-1">Anomaly Precision</p>
          </div>
          <div className="p-4 rounded-xl bg-dark-card/50 border border-gray-800/60">
            <h3 className="text-3xl font-extrabold text-accent-primary">&lt; 50ms</h3>
            <p className="text-xs text-gray-400 mt-1">Inference Latency</p>
          </div>
          <div className="p-4 rounded-xl bg-dark-card/50 border border-gray-800/60">
            <h3 className="text-3xl font-extrabold text-green-400">100%</h3>
            <p className="text-xs text-gray-400 mt-1">Unsupervised Learning</p>
          </div>
          <div className="p-4 rounded-xl bg-dark-card/50 border border-gray-800/60">
            <h3 className="text-3xl font-extrabold text-cyan-400">24 / 7</h3>
            <p className="text-xs text-gray-400 mt-1">Real-Time Monitoring</p>
          </div>
        </div>
      </section>

      {/* Feature Section */}
      <section id="features" className="relative z-10 max-w-6xl mx-auto px-6 py-20 border-t border-gray-800/60">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Enterprise Threat Capabilities</h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-sm">
            Designed specifically for FinTech and high-security enterprise environments to protect sensitive financial records and proprietary data.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-dark-card border border-gray-800 hover:border-accent-primary/50 p-6 rounded-2xl transition-all group">
            <div className="w-12 h-12 rounded-xl bg-accent-primary/10 text-accent-primary flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Isolation Forest Ensemble</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Multi-model ensemble trained on high-dimensional employee telemetry to isolate rare statistical outliers without supervised attack data.
            </p>
          </div>

          <div className="bg-dark-card border border-gray-800 hover:border-accent-primary/50 p-6 rounded-2xl transition-all group">
            <div className="w-12 h-12 rounded-xl bg-red-500/10 text-red-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Real-Time Risk Scoring</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Calculates continuous risk probability scores (0–100%) for every employee session, scaling decision boundaries dynamically.
            </p>
          </div>

          <div className="bg-dark-card border border-gray-800 hover:border-accent-primary/50 p-6 rounded-2xl transition-all group">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Users className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Role-Based Security Console</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Provides dedicated IT Admin threat monitoring views alongside Employee portals featuring interactive Threat Simulation Labs.
            </p>
          </div>
        </div>
      </section>

      {/* AI Engine & Workflow Section */}
      <section id="ai-engine" className="relative z-10 max-w-6xl mx-auto px-6 py-20 border-t border-gray-800/60">
        <div className="bg-gradient-to-b from-dark-card to-dark-bg border border-gray-800 rounded-3xl p-8 md:p-12 relative overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-md bg-blue-500/10 text-blue-400 text-xs font-mono mb-4">
                <Terminal className="w-4 h-4" />
                <span>HOW IT WORKS</span>
              </div>
              <h2 className="text-3xl font-extrabold text-white mb-6">
                Automated 4-Step Threat Prevention Pipeline
              </h2>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-white">1. Telemetry Ingestion</h4>
                    <p className="text-xs text-gray-400">Captures session duration, download volume (MB), login frequency, failed login counts, and IP address.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-white">2. Feature Engineering & Scaling</h4>
                    <p className="text-xs text-gray-400">Extracts time features, intensity ratios, and encodes roles via MinMaxScaler & LabelEncoder.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-white">3. Machine Learning Inference</h4>
                    <p className="text-xs text-gray-400">Ensemble decision function calculates raw anomaly score and normalizes to a 0–100% risk probability.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-white">4. Admin Dashboard Alerting</h4>
                    <p className="text-xs text-gray-400">Flags high-risk employee sessions and immediately displays attacker details on the Admin Console.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="glass p-6 rounded-2xl border border-gray-700/60 font-mono text-xs text-gray-300 space-y-3">
              <div className="flex items-center justify-between pb-3 border-b border-gray-700 text-gray-400">
                <span>INTEL_THREAT_AI.log</span>
                <span className="text-green-400">● LIVE</span>
              </div>
              <div className="text-green-400">&gt; Loading optimized_ensemble_model.pkl ... OK</div>
              <div className="text-gray-400">&gt; Evaluating session: emp_john (Analyst)</div>
              <div>[DATA] Downloads: 4,800 MB | Failed Logins: 15 | Hour: 02:00 AM</div>
              <div className="text-yellow-400">&gt; Decision function score: -0.2346 (Anomaly Outlier)</div>
              <div className="p-3 bg-red-500/20 border border-red-500/40 rounded-lg text-red-300 font-bold">
                ⚠️ ALERT: MASS DATA EXFILTRATION DETECTED!
                <br />
                Risk Score: 97.8% | User: emp_john | Action: Flagged to Admin
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Footer Banner */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-20 text-center">
        <div className="bg-gradient-to-r from-accent-primary/20 via-blue-600/20 to-accent-primary/20 border border-accent-primary/30 rounded-3xl p-10 md:p-14">
          <h2 className="text-3xl font-extrabold text-white mb-4">Ready to Access the Security Console?</h2>
          <p className="text-gray-300 max-w-xl mx-auto mb-8 text-sm">
            Log in with your administrator or employee credentials to monitor real-time threat telemetry or test session scenarios.
          </p>
          <Link
            to="/login"
            className="inline-flex items-center space-x-2 px-8 py-4 bg-accent-primary hover:bg-blue-600 text-white font-bold rounded-xl transition-all shadow-xl shadow-accent-primary/30 text-base"
          >
            <span>Proceed to Sign In Page</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-800/60 py-8 text-center text-xs text-gray-500">
        <p>© 2026 IntelliThreat System — Advanced Insider & Vendor Threat Detection Solution.</p>
      </footer>
    </div>
  );
};

export default Landing;
