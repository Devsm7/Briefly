// TagButtons — "More like this" / "Less like this" fine-grained feedback

interface TagButtonsProps {
    onMoreLikeThis: () => void;
    onLessLikeThis: () => void;
}

export default function TagButtons({
    onMoreLikeThis,
    onLessLikeThis,
}: TagButtonsProps) {
    // TODO: Render two small text buttons or icon+label buttons
    //   "＋ More like this"  → calls onMoreLikeThis (action: "more_like_this")
    //   "－ Less like this"  → calls onLessLikeThis (action: "less_like_this")
    // TODO: Apply subtle ghost button style (outlined, small)
    // TODO: Show confirmation micro-animation on click

    return (
        <div>
            <button onClick={onMoreLikeThis}>＋ More like this</button>
            <button onClick={onLessLikeThis}>－ Less like this</button>
            {/* TODO: full styling */}
        </div>
    );
}
