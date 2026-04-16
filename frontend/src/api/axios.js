import axios from 'axios';

// Use production API URL if in production, otherwise use env var or localhost
const getBaseURL = () => {
    // Check if we're in production (Vercel deployment)
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return 'https://forecastiq-backend.onrender.com/api';
    }
    // Use environment variable or default to localhost
    return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
};

const api = axios.create({
    baseURL: getBaseURL(),
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;
