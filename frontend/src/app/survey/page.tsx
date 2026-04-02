"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { categorySections, generalQuestions } from "@/lib/surveyQuestions";
import SurveyProgress from "@/components/survey/SurveyProgress";
import SurveyStep from "@/components/survey/SurveyStep";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import type { AxiosError } from "axios";

const CATEGORIES = [
    { id: "tech",     label: "Tech",     icon: "💻" },
    { id: "politics", label: "Politics", icon: "🗳️" },
    { id: "sport",    label: "Sport",    icon: "⚽" },
];

type Answers = Record<string, string | string[] | number>;

export default function SurveyPage() {
    const router = useRouter();

    const [step, setStep] = useState(0);
    const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
    const [answers, setAnswers] = useState<Answers>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const categorySteps = categorySections.filter((s) => selectedCategories.includes(s.id));
    const totalSteps = 2 + categorySteps.length;
    const stepLabels = [
        "General",
        "Your Interests",
        ...categorySteps.map((s) => s.label),
    ];

    function toggleCategory(id: string) {
        setSelectedCategories((prev) =>
            prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
        );
    }

    function handleAnswer(questionId: string, value: string | string[] | number) {
        setAnswers((prev) => ({ ...prev, [questionId]: value }));
    }

    function handleBack() {
        if (step > 0) setStep((s) => s - 1);
    }

    function handleNext() {
        setStep((s) => s + 1);
    }

    async function handleSkip() {
        setIsSubmitting(true);
        try {
            await api.post("/api/v1/survey/skip");
            router.push("/dashboard");
        } catch {
            router.push("/dashboard");
        } finally {
            setIsSubmitting(false);
        }
    }

    async function handleSubmit() {
        setError(null);
        setIsSubmitting(true);
        try {
            await api.post("/api/v1/survey", {
                categories: selectedCategories,
                answers,
            });
            router.push("/dashboard");
        } catch (err) {
            const axiosErr = err as AxiosError<{ detail: string }>;
            setError(axiosErr.response?.data?.detail ?? "Failed to save survey. Please try again.");
        } finally {
            setIsSubmitting(false);
        }
    }

    const isLastStep = step === totalSteps - 1;
    const isCategoryStep = step === 1;
    const currentSection = step >= 2 ? categorySteps[step - 2] : null;

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-100 p-4">
            <Card className="w-full max-w-xl">
                <CardHeader>
                    <CardTitle className="text-2xl">Personalise your feed</CardTitle>
                    <CardDescription>Help us understand what matters to you</CardDescription>
                    <div className="pt-2">
                        <SurveyProgress
                            currentStep={step}
                            totalSteps={totalSteps}
                            stepLabels={stepLabels}
                        />
                    </div>
                </CardHeader>

                <CardContent className="flex flex-col gap-6">

                    {/* Step 0 — General questions */}
                    {step === 0 && (
                        <SurveyStep
                            sectionLabel="General & Onboarding"
                            sectionColor="text-muted-foreground"
                            questions={generalQuestions}
                            answers={answers}
                            onChange={handleAnswer}
                        />
                    )}

                    {/* Step 1 — Category selection */}
                    {isCategoryStep && (
                        <div className="flex flex-col gap-4">
                            <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                                Your Interests
                            </p>
                            <p className="text-sm font-medium text-foreground">
                                Which news categories are you interested in?
                            </p>
                            <p className="text-xs text-muted-foreground">Select one or more</p>
                            <div className="flex flex-col gap-3">
                                {CATEGORIES.map((cat) => {
                                    const selected = selectedCategories.includes(cat.id);
                                    return (
                                        <button
                                            key={cat.id}
                                            type="button"
                                            onClick={() => toggleCategory(cat.id)}
                                            className={`flex items-center gap-4 rounded-xl border px-5 py-4 text-left transition ${
                                                selected
                                                    ? "border-primary bg-primary/10 text-primary"
                                                    : "border-border bg-muted/30 hover:border-primary/50 hover:bg-muted/60"
                                            }`}
                                        >
                                            <span className="text-2xl">{cat.icon}</span>
                                            <span className={`text-base font-semibold ${selected ? "text-primary" : "text-foreground"}`}>
                                                {cat.label}
                                            </span>
                                            {selected && (
                                                <span className="ml-auto text-sm font-bold text-primary">✓</span>
                                            )}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    )}

                    {/* Steps 2+ — Category-specific questions */}
                    {currentSection && (
                        <SurveyStep
                            sectionLabel={currentSection.label}
                            sectionColor="text-primary"
                            questions={currentSection.questions}
                            answers={answers}
                            onChange={handleAnswer}
                        />
                    )}

                    {/* Error */}
                    {error && (
                        <p className="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                            {error}
                        </p>
                    )}

                    {/* Navigation */}
                    <div className="flex items-center justify-between gap-3 pt-2">
                        <div className="flex gap-2">
                            {step > 0 && (
                                <Button variant="ghost" onClick={handleBack}>
                                    ← Back
                                </Button>
                            )}
                            <Button variant="ghost" onClick={handleSkip} disabled={isSubmitting}>
                                Skip survey
                            </Button>
                        </div>

                        {isLastStep ? (
                            <Button onClick={handleSubmit} disabled={isSubmitting}>
                                {isSubmitting ? "Saving…" : "Finish →"}
                            </Button>
                        ) : (
                            <Button
                                onClick={handleNext}
                                disabled={isCategoryStep && selectedCategories.length === 0}
                            >
                                Next →
                            </Button>
                        )}
                    </div>

                </CardContent>
            </Card>
        </div>
    );
}
