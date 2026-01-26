
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0f172a',    // Slate 900
          card: '#1e293b',  // Slate 800
          text: '#f8fafc',  // Slate 50
          muted: '#94a3b8'  // Slate 400
        },
        accent: {
          primary: '#3b82f6', // Blue 500
          danger: '#ef4444',  // Red 500
          success: '#10b981', // Emerald 500
          warning: '#f59e0b'  // Amber 500
        }
      }
    },
  },
  plugins: [],
}
