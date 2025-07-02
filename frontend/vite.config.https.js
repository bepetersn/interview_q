// This script reads example.com+5.pem and example.com+5-key.pem from the project root and starts Vite with HTTPS enabled.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'

// Always read cert/key from project root
const cert = fs.readFileSync(path.resolve(__dirname, '../localhost.pem'))
const key = fs.readFileSync(path.resolve(__dirname, '../localhost-key.pem'))

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key,
      cert,
    },
    host: '0.0.0.0',
    port: 5173,
  },
})
