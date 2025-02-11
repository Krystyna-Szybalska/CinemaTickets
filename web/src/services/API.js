import axios from 'axios';

const ApiInstance = axios.create({
  baseURL: 'https://127.0.0.1:8000',
  timeout: 10000,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': true,
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default ApiInstance;
