
import React from 'react';
import { Outlet } from 'react-router-dom';
import { motion } from 'framer-motion';

const AuthLayout = () => {
  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-accent-primary/20 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent-primary/10 rounded-full blur-[100px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md z-10"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-dark-text tracking-tight">IntelliThreat</h1>
          <p className="text-dark-muted mt-2">Identify Insider Threats Before They Strike</p>
        </div>

        <Outlet />

        <div className="text-center mt-8 text-sm text-dark-muted">
          &copy; {new Date().getFullYear()} IntelliThreat Systems. Secure Access Only.
        </div>
      </motion.div>
    </div>
  );
};

export default AuthLayout;
