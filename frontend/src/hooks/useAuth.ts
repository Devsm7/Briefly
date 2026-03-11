"use client";

// useAuth — authentication state and actions (login, register, logout)

// TODO: Import createContext, useContext, useState from react
// TODO: Import api client from @/lib/api
// TODO: Import auth helpers from @/lib/auth (save/clear token)

export interface AuthUser {
    id: number;
    email: string;
    full_name?: string;
}

export interface AuthContextValue {
    user: AuthUser | null;
    isLoading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string, fullName?: string) => Promise<void>;
    logout: () => void;
}

// TODO: export const AuthContext = createContext<AuthContextValue>(...)
// TODO: export function AuthProvider({ children }: ...) { ... }

export function useAuth(): AuthContextValue {
    // TODO: return useContext(AuthContext)
    throw new Error("useAuth must be used within an <AuthProvider>");
}
