// SurveyProgress — horizontal step progress bar for the onboarding survey

interface SurveyProgressProps {
    currentStep: number; // 1-based
    totalSteps: number;
}

export default function SurveyProgress({
    currentStep,
    totalSteps,
}: SurveyProgressProps) {
    // TODO: Render a segmented progress bar or numbered steps row
    // TODO: Completed steps → filled primary color
    // TODO: Current step → active highlight
    // TODO: Future steps → muted/gray
    // TODO: Show "Step N of M" label

    return (
        <div>
            {/* TODO: implement */}
            <span>{currentStep} / {totalSteps}</span>
        </div>
    );
}
