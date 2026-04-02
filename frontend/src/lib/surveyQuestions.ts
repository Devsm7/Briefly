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

// ── General & Onboarding ─────────────────────────────────────────────────────

export const generalQuestions: Question[] = [
    {
        id: "Q01",
        text: "How often do you read news or articles online?",
        type: "single",
        options: [
            { label: "Multiple times a day", value: "multiple_daily" },
            { label: "Once a day", value: "once_daily" },
            { label: "A few times a week", value: "few_weekly" },
            { label: "Once a week", value: "once_weekly" },
            { label: "Rarely", value: "rarely" },
        ],
    },
    {
        id: "Q02",
        text: "What is your preferred content format?",
        type: "multi",
        options: [
            { label: "Short articles", value: "short_articles" },
            { label: "Long reads", value: "long_reads" },
            { label: "Videos", value: "videos" },
            { label: "Podcasts", value: "podcasts" },
            { label: "Newsletters", value: "newsletters" },
            { label: "Social media posts", value: "social_media" },
        ],
    },
    {
        id: "Q03",
        text: "What time of day do you usually consume news?",
        type: "multi",
        options: [
            { label: "Morning (6am–12pm)", value: "morning" },
            { label: "Afternoon (12pm–6pm)", value: "afternoon" },
            { label: "Evening (6pm–10pm)", value: "evening" },
            { label: "Late night (10pm+)", value: "late_night" },
        ],
    },
];

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
            {
                id: "Q06",
                text: "What best describes your relationship with technology?",
                type: "single",
                options: [
                    { label: "Tech professional / developer", value: "professional" },
                    { label: "Tech enthusiast / early adopter", value: "enthusiast" },
                    { label: "Casual user", value: "casual" },
                    { label: "Skeptic / minimal user", value: "skeptic" },
                ],
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
            {
                id: "Q09",
                text: "Which geographic scope of political news matters most to you?",
                type: "rank",
                options: [
                    { label: "Local", value: "local" },
                    { label: "National", value: "national" },
                    { label: "Regional", value: "regional" },
                    { label: "Global", value: "global" },
                ],
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
            {
                id: "Q15",
                text: "What type of sports content do you prefer?",
                type: "multi",
                options: [
                    { label: "Match results & scores", value: "results" },
                    { label: "Transfer news", value: "transfers" },
                    { label: "Analysis & tactics", value: "analysis" },
                    { label: "Player interviews", value: "interviews" },
                    { label: "Statistics & data", value: "statistics" },
                ],
            },
        ],
    },
];
