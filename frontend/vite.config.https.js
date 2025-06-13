// This script reads dev.crt and dev.key from the project root and starts Vite with HTTPS enabled.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'

const cert = fs.readFileSync(path.resolve(__dirname, '../dev.crt'))
const key = fs.readFileSync(path.resolve(__dirname, '../dev.key'))

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
})
