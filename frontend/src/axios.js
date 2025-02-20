import axios from 'axios'

const axiosFetch = axios.create({
    baseURL: 'http://127.0.0.1:5000',
})
const authToken = localStorage.getItem('authToken');

// Add authentication header to all requests
axiosFetch.interceptors.request.use(config => {
    config.headers.Authorization = `Bearer ${authToken}`;
    return config;
}, error => {
    return Promise.reject(error);
});

export default axiosFetch