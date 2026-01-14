/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    './src/components/**/*.{vue,js,ts}',
    './src/pages/**/*.{vue,js,ts}',
    './src/views/**/*.{vue,js,ts}'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0055FF',
        dark: {
          bg: '#0F1319',
          card: '#1a1f2e',
          input: '#0F1319'
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif']
      },
      spacing: {
        'safe-bottom': 'env(safe-area-inset-bottom)'
      }
    }
  },
  plugins: [],
  safelist: [
    'bg-green-900',
    'text-green-300',
    'bg-blue-900',
    'text-blue-300',
    'text-yellow-400',
    'border-blue-900'
  ]
}
