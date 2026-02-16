/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        surface: 'var(--surface)',
        surface2: 'var(--surface2)',
        border: 'var(--border)',
        accent: 'var(--accent)',
        accent2: 'var(--accent2)',
        accent3: 'var(--accent3)',
        warn: 'var(--warn)',
        danger: 'var(--danger)',
        text: 'var(--text)',
        muted: 'var(--muted)',
        bronze: 'var(--bronze)',
        silver: 'var(--silver)',
        gold: 'var(--gold)',
        platinum: 'var(--platinum)',
      },
      fontFamily: {
        syne: ['Syne', 'sans-serif'],
        sans: ['DM Sans', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
      animation: {
        'pulse-green': 'pulse-green 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        'slide-up': 'slide-up 0.4s ease-out',
        'gradient-shift': 'gradient-shift 15s ease infinite',
      },
      transitionDuration: {
        '250': '250ms',
      },
    },
  },
  plugins: [],
}
