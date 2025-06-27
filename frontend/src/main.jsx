import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import * as Sentry from '@sentry/react'
import { BrowserTracing } from '@sentry/react'
import './index.css'
import App from './App.jsx'

Sentry.init({
  dsn: import.meta.env.VITE_FRONTEND_SENTRY_DSN,
  integrations: [new BrowserTracing()],
  tracesSampleRate: 1.0,
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
