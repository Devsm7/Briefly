"use client";

import { createContext, useContext } from "react";
import type { User } from "@/types";

export interface AuthContextValue {
    user: User | null;
    isLoading: boolean;
    error: string | null;
    login: (username: string) => Promise<void>;
    register: (
        username: string,
        firstName: string,
        lastName: string,
        gender: string
    ) => Promise<void>;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within an <AuthProvider>");
    return ctx;
}
