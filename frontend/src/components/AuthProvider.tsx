"use client";

import React, { useCallback, useEffect, useState } from "react";
import api from "@/lib/api";
import { clearToken, getToken, saveToken } from "@/lib/auth";
import { AuthContext, type AuthContextValue } from "@/hooks/useAuth";
import type { User } from "@/types";

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const token = getToken();
        if (!token) {
            setIsLoading(false);
            return;
        }
        api.get<User>("/api/v1/users/me")
            .then((res) => setUser(res.data))
            .catch(() => clearToken())
            .finally(() => setIsLoading(false));
    }, []);

    const login = useCallback(async (username: string) => {
        setError(null);
        const res = await api.post<{ access_token: string }>("/api/v1/auth/login", {
            username,
        });
        saveToken(res.data.access_token);
        const me = await api.get<User>("/api/v1/users/me");
        setUser(me.data);
    }, []);

    const register = useCallback(
        async (username: string, firstName: string, lastName: string, gender: string) => {
            setError(null);
            await api.post("/api/v1/auth/register", {
                username,
                first_name: firstName,
                last_name: lastName,
                gender,
            });
            await login(username);
        },
        [login]
    );

    const logout = useCallback(() => {
        clearToken();
        setUser(null);
    }, []);

    const value: AuthContextValue = { user, isLoading, error, login, register, logout };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
