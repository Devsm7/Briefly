// lib/api.ts — Axios instance pre-configured with base URL and auth interceptors

// TODO: import axios from "axios"

// TODO: const api = axios.create({
//   baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
// });

// TODO: Request interceptor — attach Bearer token from storage if present:
// api.interceptors.request.use((config) => {
//   const token = getToken();  // from lib/auth
//   if (token) config.headers.Authorization = `Bearer ${token}`;
//   return config;
// });

// TODO: Response interceptor — handle 401 → redirect to /login:
// api.interceptors.response.use(
//   (res) => res,
//   (err) => {
//     if (err.response?.status === 401) window.location.href = "/login";
//     return Promise.reject(err);
//   }
// );

// TODO: export default api;

const api = {} as any; // TODO: replace with real axios instance
export default api;
