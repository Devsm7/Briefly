// lib/api.ts — Axios instance pre-configured with base URL and auth interceptors

import axios, {
    type AxiosError,
    type AxiosResponse,
    type InternalAxiosRequestConfig,
} from "axios";
import { getToken } from "@/lib/auth";

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const token = getToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

api.interceptors.response.use(
    (res: AxiosResponse) => res,
    (err: AxiosError) => {
        if (err.response?.status === 401 && typeof window !== "undefined") {
            window.location.href = "/";
        }
        return Promise.reject(err);
    }
);

export default api;
