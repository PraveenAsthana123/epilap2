import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Docs live one level up in ../docs, so allow serving files from the parent.
export default defineConfig({
  plugins: [react()],
  server: {
    fs: { allow: ['..'] },
    host: true,
  },
})
