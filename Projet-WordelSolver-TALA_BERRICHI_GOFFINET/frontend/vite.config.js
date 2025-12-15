import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/wordle': {
        target: 'http://127.0.0.1:8000',  // Utilisez 127.0.0.1 au lieu de localhost
        changeOrigin: true,
        secure: false,
      },
      '/llm': {
        target: 'http://127.0.0.1:8000',  // Utilisez 127.0.0.1 au lieu de localhost
        changeOrigin: true,
        secure: false,
      },
    },
  },
})