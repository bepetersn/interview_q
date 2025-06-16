import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'

// Always read cert/key from project root
const cert = fs.readFileSync(path.resolve(__dirname, '../example.com+5.pem'))
const key = fs.readFileSync(path.resolve(__dirname, '../example.com+5-key.pem'))

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key,
      cert,
    },
    host: '127.0.0.1',
    port: 5173,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './jest.setup.js', // If you have global setup, otherwise remove this line
    coverage: {
      reporter: ['text', 'json', 'html'],
    },
  },
})
