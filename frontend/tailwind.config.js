/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        safi: {
          bg: '#0B0E14',
          surface: '#161B22',
          border: '#30363D',
          accentBlue: '#00A3FF',
          accentMint: '#70FFB8',
        },
      },
    },
  },
  plugins: [],
}