// Survey question definitions — single source of truth for all survey steps

export type QuestionType = "single" | "multi" | "likert" | "rank";

export interface Question {
    id: string;
    text: string;
    type: QuestionType;
    options?: { label: string; value: string }[];
}

export interface SurveySection {
    id: string;
    label: string;
    color: string; // Tailwind text color class
    questions: Question[];
}

// ── Category Sections ─────────────────────────────────────────────────────────

export const categorySections: SurveySection[] = [
    {
        id: "tech",
        label: "Tech",
        color: "text-indigo-400",
        questions: [
            {
                id: "Q04",
                text: "Which technology topics interest you most?",
                type: "multi",
                options: [
                    { label: "Artificial Intelligence", value: "ai" },
                    { label: "Cybersecurity", value: "cybersecurity" },
                    { label: "Startups", value: "startups" },
                    { label: "Consumer Electronics", value: "electronics" },
                    { label: "Software & Apps", value: "software" },
                    { label: "Science & Space", value: "science" },
                ],
            },
            {
                id: "Q05",
                text: "How would you rate your interest in technology news overall?",
                type: "likert",
            },
        ],
    },
    {
        id: "politics",
        label: "Politics",
        color: "text-amber-400",
        questions: [
            {
                id: "Q07",
                text: "Which political topics are you most interested in?",
                type: "multi",
                options: [
                    { label: "Domestic policy", value: "domestic" },
                    { label: "International relations", value: "international" },
                    { label: "Elections & democracy", value: "elections" },
                    { label: "Economic policy", value: "economic" },
                    { label: "Social issues", value: "social" },
                    { label: "Environmental policy", value: "environment" },
                ],
            },
            {
                id: "Q08",
                text: "How would you rate your interest in political news overall?",
                type: "likert",
            },
        ],
    },
    {
        id: "sport",
        label: "Sport",
        color: "text-red-400",
        questions: [
            {
                id: "Q13",
                text: "Which sports do you follow?",
                type: "multi",
                options: [
                    { label: "Football / Soccer", value: "football" },
                    { label: "Basketball", value: "basketball" },
                    { label: "Tennis", value: "tennis" },
                    { label: "Cricket", value: "cricket" },
                    { label: "Formula 1", value: "f1" },
                    { label: "Athletics", value: "athletics" },
                    { label: "Rugby", value: "rugby" },
                    { label: "Baseball", value: "baseball" },
                ],
            },
            {
                id: "Q14",
                text: "How would you rate your interest in sports news overall?",
                type: "likert",
            },
        ],
    },
];
