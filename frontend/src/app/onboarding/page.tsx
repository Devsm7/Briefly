"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { categorySections, generalQuestions } from "@/lib/surveyQuestions";
import SurveyProgress from "@/components/survey/SurveyProgress";
import SurveyStep from "@/components/survey/SurveyStep";
import { Button } from "@/components/ui/button";
import type { AxiosError } from "axios";

const CATEGORIES = [
    { id: "tech",     label: "Tech",     color: "text-indigo-400", bg: "bg-indigo-600/20 border-indigo-500", icon: "💻" },
    { id: "politics", label: "Politics", color: "text-amber-400",  bg: "bg-amber-600/20 border-amber-500",  icon: "🗳️" },
    { id: "sport",    label: "Sport",    color: "text-red-400",    bg: "bg-red-600/20 border-red-500",      icon: "⚽" },
];

type Answers = Record<string, string | string[] | number>;

export default function OnboardingPage() {
    const router = useRouter();

    const [step, setStep] = useState(0);
    const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
    const [answers, setAnswers] = useState<Answers>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Build the ordered list of steps dynamically based on selected categories
    const categorySteps = categorySections.filter((s) => selectedCategories.includes(s.id));
    // step 0 = general, step 1 = category selection, step 2+ = per-category questions
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

    // Current category section (steps 2+)
    const currentSection = step >= 2 ? categorySteps[step - 2] : null;

    return (
        <main className="flex min-h-screen flex-col items-center bg-gray-950 px-4 py-10">
            <div className="w-full max-w-xl">

                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-2xl font-bold text-white">Personalise your feed</h1>
                    <p className="mt-1 text-sm text-gray-400">
                        Help us understand what matters to you
                    </p>
                </div>

                {/* Progress */}
                <div className="mb-8">
                    <SurveyProgress
                        currentStep={step}
                        totalSteps={totalSteps}
                        stepLabels={stepLabels}
                    />
                </div>

                {/* Step content */}
                <div className="mb-8">

                    {/* Step 0 — General questions */}
                    {step === 0 && (
                        <SurveyStep
                            sectionLabel="General & Onboarding"
                            sectionColor="text-gray-400"
                            questions={generalQuestions}
                            answers={answers}
                            onChange={handleAnswer}
                        />
                    )}

                    {/* Step 1 — Category selection */}
                    {isCategoryStep && (
                        <div className="flex flex-col gap-4">
                            <p className="text-xs font-semibold uppercase tracking-widest text-gray-400">
                                Your Interests
                            </p>
                            <p className="text-sm font-medium text-gray-200">
                                Which news categories are you interested in?
                            </p>
                            <p className="text-xs text-gray-500">Select one or more</p>
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
                                                    ? cat.bg
                                                    : "border-gray-700 bg-gray-800/50 hover:border-gray-600"
                                            }`}
                                        >
                                            <span className="text-2xl">{cat.icon}</span>
                                            <span className={`text-base font-semibold ${selected ? cat.color : "text-gray-300"}`}>
                                                {cat.label}
                                            </span>
                                            {selected && (
                                                <span className={`ml-auto text-sm font-bold ${cat.color}`}>✓</span>
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
                            sectionColor={currentSection.color}
                            questions={currentSection.questions}
                            answers={answers}
                            onChange={handleAnswer}
                        />
                    )}
                </div>

                {/* Error */}
                {error && (
                    <p className="mb-4 rounded-lg border border-red-800 bg-red-900/40 px-4 py-2.5 text-sm text-red-300">
                        {error}
                    </p>
                )}

                {/* Navigation */}
                <div className="flex items-center justify-between gap-3">
                    <div className="flex gap-2">
                        {step > 0 && (
                            <Button variant="ghost" onClick={handleBack}>
                                ← Back
                            </Button>
                        )}
                        <Button variant="ghost" onClick={handleSkip} isLoading={isSubmitting}>
                            Skip survey
                        </Button>
                    </div>

                    {isLastStep ? (
                        <Button onClick={handleSubmit} isLoading={isSubmitting}>
                            Finish →
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

            </div>
        </main>
    );
}
