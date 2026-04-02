"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { AxiosError } from "axios";

interface FieldErrors {
    email?: string;
    username?: string;
    password?: string;
}

export default function RegisterPage() {
    const { register } = useAuth();
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [fullName, setFullName] = useState("");
    const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
    const [apiError, setApiError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    function validate(): boolean {
        const errors: FieldErrors = {};
        if (!email.trim()) {
            errors.email = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            errors.email = "Enter a valid email address";
        }
        if (!username.trim()) {
            errors.username = "Username is required";
        } else if (username.length < 3) {
            errors.username = "Username must be at least 3 characters";
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            errors.username = "Letters, numbers, and underscores only";
        }
        if (!password) {
            errors.password = "Password is required";
        } else if (password.length < 8) {
            errors.password = "Password must be at least 8 characters";
        }
        setFieldErrors(errors);
        return Object.keys(errors).length === 0;
    }

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setApiError(null);
        if (!validate()) return;
        setIsLoading(true);
        try {
            await register(email.trim(), username.trim(), password, fullName.trim() || undefined);
            router.push("/survey");
        } catch (err) {
            const axiosErr = err as AxiosError<{ detail: string }>;
            setApiError(axiosErr.response?.data?.detail ?? "Registration failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-indigo-100 p-4">
            <Card className="w-full max-w-md">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-3xl text-center">Create an account</CardTitle>
                    <CardDescription className="text-center">
                        Join Briefly and get personalised news
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} noValidate className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="full_name">Full Name <span className="text-muted-foreground font-normal">(optional)</span></Label>
                            <Input
                                id="full_name"
                                type="text"
                                placeholder="Jane Doe"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                autoComplete="name"
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                autoComplete="email"
                                aria-invalid={!!fieldErrors.email}
                            />
                            {fieldErrors.email && (
                                <p className="text-xs text-destructive">{fieldErrors.email}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="username">Username</Label>
                            <Input
                                id="username"
                                type="text"
                                placeholder="janedoe"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                autoComplete="username"
                                aria-invalid={!!fieldErrors.username}
                            />
                            {fieldErrors.username && (
                                <p className="text-xs text-destructive">{fieldErrors.username}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                placeholder="Min. 8 characters"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                autoComplete="new-password"
                                aria-invalid={!!fieldErrors.password}
                            />
                            {fieldErrors.password && (
                                <p className="text-xs text-destructive">{fieldErrors.password}</p>
                            )}
                        </div>

                        {apiError && (
                            <p className="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                                {apiError}
                            </p>
                        )}

                        <Button type="submit" disabled={isLoading} className="w-full">
                            {isLoading ? "Creating account…" : "Create account"}
                        </Button>
                    </form>

                    <p className="mt-6 text-center text-sm text-muted-foreground">
                        Already have an account?{" "}
                        <Link href="/" className="font-medium text-primary hover:underline">
                            Sign in
                        </Link>
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
