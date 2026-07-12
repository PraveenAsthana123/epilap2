import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Docs live one level up in ../docs, so allow serving files from the parent.
export default defineConfig({
  plugins: [react()],
  server: {
    fs: { allow: ['..'] },
    host: true,
    // Proxy /api to the FastAPI service so the viewer can call it in dev.
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true,
                rewrite: (p) => p.replace(/^\/api/, '') },
    },
  },
  // Vitest: jsdom so React component/button tests can render + click.
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.js'],
  },
})
