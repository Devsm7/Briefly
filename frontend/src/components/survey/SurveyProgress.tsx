interface SurveyProgressProps {
    currentStep: number;
    totalSteps: number;
    stepLabels: string[];
}

export default function SurveyProgress({ currentStep, totalSteps, stepLabels }: SurveyProgressProps) {
    return (
        <div className="w-full">
            <div className="mb-2 flex items-center justify-between text-xs text-muted-foreground">
                <span>{stepLabels[currentStep] ?? "Survey"}</span>
                <span>Step {currentStep + 1} of {totalSteps}</span>
            </div>
            <div className="flex gap-1">
                {Array.from({ length: totalSteps }).map((_, i) => (
                    <div
                        key={i}
                        className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                            i < currentStep
                                ? "bg-primary"
                                : i === currentStep
                                ? "bg-primary/60"
                                : "bg-muted"
                        }`}
                    />
                ))}
            </div>
        </div>
    );
}
