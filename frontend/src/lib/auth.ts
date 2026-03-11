// lib/auth.ts — token persistence helpers (localStorage)

const TOKEN_KEY = "briefly_token";

export function saveToken(token: string): void {
    // TODO: localStorage.setItem(TOKEN_KEY, token)
    throw new Error("Not implemented");
}

export function getToken(): string | null {
    // TODO: return localStorage.getItem(TOKEN_KEY)
    throw new Error("Not implemented");
}

export function clearToken(): void {
    // TODO: localStorage.removeItem(TOKEN_KEY)
    throw new Error("Not implemented");
}

export function isAuthenticated(): boolean {
    // TODO: return !!getToken()
    throw new Error("Not implemented");
}
