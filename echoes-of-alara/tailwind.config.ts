import type { Config } from 'tailwindcss';
import typography from '@tailwindcss/typography';
import animate from 'tailwindcss-animate';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      animation: { 'spin-slow': 'spin 6s linear infinite' },
    },
  },
  plugins: [typography, animate],
};
export default config;
