// LikeDislikeButtons — 👍 / 👎 action buttons on each article card

interface LikeDislikeButtonsProps {
    articleId: number;
    userAction?: "like" | "dislike" | null; // current state from user_interactions
    onLike: () => void;
    onDislike: () => void;
}

export default function LikeDislikeButtons({
    articleId,
    userAction,
    onLike,
    onDislike,
}: LikeDislikeButtonsProps) {
    // TODO: Render 👍 and 👎 icon buttons
    // TODO: If userAction === "like" → highlight 👍 (active color)
    // TODO: If userAction === "dislike" → highlight 👎 (active color)
    // TODO: Clicking an already-active button should toggle it off
    //       (send a neutral / remove action or do nothing)
    // TODO: Animate button press (scale down briefly)

    return (
        <div>
            <button onClick={onLike} aria-label="Like">👍</button>
            <button onClick={onDislike} aria-label="Dislike">👎</button>
            {/* TODO: full styling */}
        </div>
    );
}
