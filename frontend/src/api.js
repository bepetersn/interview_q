// Axios instance for API requests
import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/', // removed trailing 'api/'
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Ensure cookies (sessionid, csrftoken) are sent with every request
});

export default api;
