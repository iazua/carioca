import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build',
    emptyOutDir: true,
    lib: {
      entry: 'src/index.tsx',
      formats: ['iife'],
      name: 'CariocaComponent'
    },
  },
});
