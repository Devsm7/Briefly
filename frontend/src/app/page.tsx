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

export default function LoginPage() {
    const { login } = useAuth();
    const router = useRouter();

    const [username, setUsername] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setError(null);
        if (!username.trim()) {
            setError("Please enter your username.");
            return;
        }
        setIsLoading(true);
        try {
            await login(username.trim());
            router.push("/dashboard");
        } catch (err) {
            const axiosErr = err as AxiosError<{ detail: string }>;
            setError(axiosErr.response?.data?.detail ?? "Login failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
            <Card className="w-full max-w-md">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-3xl text-center">Welcome back</CardTitle>
                    <CardDescription className="text-center">
                        Sign in to your Briefly account
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} noValidate className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="username">Username</Label>
                            <Input
                                id="username"
                                type="text"
                                placeholder="Enter your username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                autoComplete="username"
                            />
                        </div>

                        {error && (
                            <p className="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                                {error}
                            </p>
                        )}

                        <Button type="submit" disabled={isLoading} className="w-full">
                            {isLoading ? "Signing in…" : "Sign in"}
                        </Button>
                    </form>

                    <p className="mt-6 text-center text-sm text-muted-foreground">
                        Don&apos;t have an account?{" "}
                        <Link href="/register" className="font-medium text-primary hover:underline">
                            Create one
                        </Link>
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
