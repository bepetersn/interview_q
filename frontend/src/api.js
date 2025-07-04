/**
 * Axios instance for API requests with CSRF token handling
 * @fileoverview API client configuration with automatic CSRF token injection
 */
import axios from 'axios';
import { getCookie } from './utils.js';

/** @type {string} Base URL for API requests */
const baseURL = import.meta.env.VITE_API_BASE_URL || 'https://localhost:8000';

/** @type {string[]} HTTP methods that require CSRF token */
const UNSAFE_METHODS = ["POST", "PUT", "PATCH", "DELETE"];

/**
 * Configured axios instance with interceptors
 * @type {import('axios').AxiosInstance}
 */
const api = axios.create({
    baseURL: baseURL + '/api/',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Ensure cookies (sessionid, csrftoken) are sent with every request
});

/**
 * Add CSRF token to unsafe requests
 * @param {import('axios').AxiosRequestConfig} config - Request configuration
 * @returns {import('axios').AxiosRequestConfig} Modified config with CSRF token
 */
api.interceptors.request.use((config) => {
    const method = config.method?.toUpperCase();
    if (UNSAFE_METHODS.includes(method)) {
        const csrftoken = getCookie('csrftoken');
        if (csrftoken) {
            config.headers['X-CSRFToken'] = csrftoken;
        } else {
            console.warn('CSRF token not found for unsafe request');
        }
    }
    return config;
});

/**
 * Add response interceptor for consistent error handling
 */
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Log errors for debugging
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export default api;
