"use client";

// Onboarding survey page — 5-7 step questionnaire on first login
// Steps:
//   1. Welcome screen
//   2. Select preferred categories (multi-select: Tech / Business / Politics / Sports)
//   3. Reading frequency preference (morning / evening / both / real-time)
//   4. Source preferences (optional)
//   5. Summary / confirmation

// TODO: Import SurveyStep, SurveyProgress components
// TODO: Import Button from UI components

export default function OnboardingPage() {
    // TODO: step state (1-based index)
    // TODO: surveyData state accumulating answers per step
    // TODO: handleNext(stepData) → merge into surveyData, advance step
    // TODO: handleSkip() → call POST /survey/skip → redirect to /dashboard
    // TODO: handleSubmit() → call POST /survey with surveyData → redirect to /dashboard

    return (
        <main>
            {/* TODO: Render SurveyProgress bar */}
            {/* TODO: Render current SurveyStep based on step index */}
            {/* TODO: Back / Next / Skip / Submit buttons */}
        </main>
    );
}
