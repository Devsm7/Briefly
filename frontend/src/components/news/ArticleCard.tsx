// ArticleCard — main news feed card component

// TODO: Import Badge, LikeDislikeButtons, TagButtons components
// TODO: Import Article type from @/types

interface ArticleCardProps {
    article: {
        id: number;
        title: string;
        description?: string;
        url: string;
        source?: string;
        category: string;
        published_at?: string;
        summary?: string;
    };
    onLike: () => void;
    onDislike: () => void;
    onSave: () => void;
}

export default function ArticleCard({
    article,
    onLike,
    onDislike,
    onSave,
}: ArticleCardProps) {
    // TODO: Track view event on mount (Intersection Observer or useEffect)
    // TODO: Display:
    //   - Category Badge (top-left)
    //   - Source name + publication date (top-right)
    //   - Headline (h2, font-bold)
    //   - TL;DR summary (3-5 bullets if available, else description)
    //   - Read Full Article link (opens in new tab)
    //   - LikeDislikeButtons + Save button (bottom row)
    // TODO: Hover → subtle scale / border-glow animation

    return (
        <article>
            {/* TODO: full card UI */}
            <h2>{article.title}</h2>
        </article>
    );
}
