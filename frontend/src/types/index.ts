// Shared TypeScript type definitions for the Briefly frontend

// ── User ─────────────────────────────────────────────────────────────────────

export interface User {
    id: number;
    email: string;
    full_name?: string;
    is_active: boolean;
    created_at: string;
}

// ── Article ───────────────────────────────────────────────────────────────────

export type Category = "tech" | "business" | "politics" | "sports";

export interface Article {
    id: number;
    title: string;
    description?: string;
    url: string;
    source?: string;
    category: Category | string;
    published_at?: string;
    summary?: string;   // LLM bullet-point summary
    created_at: string;
}

export interface ArticleFeed {
    articles: Article[];
    total: number;
    page: number;
    per_page: number;
}

// ── Survey ────────────────────────────────────────────────────────────────────

export interface SurveyPreference {
    id: number;
    user_id: number;
    categories: string[];
    frequency?: string;
    preferred_sources?: string[];
    interest_vector?: Record<string, number>;
    survey_completed: number;
    created_at: string;
}

// ── Interaction ───────────────────────────────────────────────────────────────

export type InteractionAction =
    | "view"
    | "like"
    | "dislike"
    | "save"
    | "unsave"
    | "more_like_this"
    | "less_like_this";

export interface Interaction {
    id: number;
    user_id: number;
    article_id: number;
    action: InteractionAction;
    read_time?: number;
    scroll_depth?: number;
    created_at: string;
}

// ── Auth ──────────────────────────────────────────────────────────────────────

export interface TokenResponse {
    access_token: string;
    token_type: string;
}
