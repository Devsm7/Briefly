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
    username?: string;
    firstName?: string;
    lastName?: string;
}

export default function RegisterPage() {
    const { register } = useAuth();
    const router = useRouter();

    const [username, setUsername] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [gender, setGender] = useState<"male" | "female">("male");
    const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
    const [apiError, setApiError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    function validate(): boolean {
        const errors: FieldErrors = {};
        if (!username.trim()) {
            errors.username = "Username is required";
        } else if (username.length < 3) {
            errors.username = "Username must be at least 3 characters";
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            errors.username = "Letters, numbers, and underscores only";
        }
        if (!firstName.trim()) {
            errors.firstName = "First name is required";
        }
        if (!lastName.trim()) {
            errors.lastName = "Last name is required";
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
            await register(username.trim(), firstName.trim(), lastName.trim(), gender);
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
                            <Label htmlFor="first_name">First Name</Label>
                            <Input
                                id="first_name"
                                type="text"
                                placeholder="Jane"
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                autoComplete="given-name"
                                aria-invalid={!!fieldErrors.firstName}
                            />
                            {fieldErrors.firstName && (
                                <p className="text-xs text-destructive">{fieldErrors.firstName}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="last_name">Last Name</Label>
                            <Input
                                id="last_name"
                                type="text"
                                placeholder="Doe"
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                autoComplete="family-name"
                                aria-invalid={!!fieldErrors.lastName}
                            />
                            {fieldErrors.lastName && (
                                <p className="text-xs text-destructive">{fieldErrors.lastName}</p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label>Gender</Label>
                            <div className="flex gap-6">
                                <label className="flex items-center gap-2 cursor-pointer">
                                    <input
                                        type="radio"
                                        name="gender"
                                        value="male"
                                        checked={gender === "male"}
                                        onChange={() => setGender("male")}
                                        className="accent-primary h-4 w-4"
                                    />
                                    <span className="text-sm">Male</span>
                                </label>
                                <label className="flex items-center gap-2 cursor-pointer">
                                    <input
                                        type="radio"
                                        name="gender"
                                        value="female"
                                        checked={gender === "female"}
                                        onChange={() => setGender("female")}
                                        className="accent-primary h-4 w-4"
                                    />
                                    <span className="text-sm">Female</span>
                                </label>
                            </div>
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
