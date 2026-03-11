// useInteractions — log user behavior events against articles

// TODO: Import api from @/lib/api
// TODO: Import InteractionAction type

export type InteractionAction =
    | "view"
    | "like"
    | "dislike"
    | "save"
    | "unsave"
    | "more_like_this"
    | "less_like_this";

export function useInteractions() {
    // TODO: logInteraction(articleId, action, extras?) →
    //       POST /api/v1/interactions with { article_id, action, read_time?, scroll_depth? }
    // TODO: Return { logInteraction }

    return {
        logInteraction: (
            _articleId: number,
            _action: InteractionAction,
            _extras?: { read_time?: number; scroll_depth?: number }
        ) => {
            // TODO: implement
            throw new Error("logInteraction not implemented");
        },
    };
}
