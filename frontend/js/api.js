// api.js

// Create Axios Instance
const api = axios.create({
    baseURL: 'http://54.205.186.130:5000/api', // To be replaced in prod with actual API URL
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add Authorization Interceptor
api.interceptors.request.use(config => {
    const token = localStorage.getItem('auth_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Global Error Handler
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Unauthorized
            console.error('Session expired or unauthorized.');
            Auth.logout();
        }
        return Promise.reject(error);
    }
);
