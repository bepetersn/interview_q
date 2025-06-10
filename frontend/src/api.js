// Axios instance for API requests
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Adjust if your Django API runs elsewhere
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
