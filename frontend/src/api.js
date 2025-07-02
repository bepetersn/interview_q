// Axios instance for API requests
import axios from 'axios';
import { getCookie } from './utils.js';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'https://localhost:8000';
// To support access via IP (e.g., 100.115.92.194), you can set VITE_API_BASE_URL in your .env or .env.local file, e.g.:
// VITE_API_BASE_URL=https://100.115.92.194:8000
const api = axios.create({
    baseURL: baseURL + '/api/',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Ensure cookies (sessionid, csrftoken) are sent with every request
});


// Add CSRF token to unsafe requests
api.interceptors.request.use((config) => {
    const method = config.method?.toUpperCase();
    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
        const csrftoken = getCookie('csrftoken');
        if (csrftoken) {
            config.headers['X-CSRFToken'] = csrftoken;
        }
    }
    return config;
});

export default api;
