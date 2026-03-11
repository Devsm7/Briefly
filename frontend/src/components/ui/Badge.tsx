// Category / tag badge — color-coded by category

type Category = "tech" | "business" | "politics" | "sports" | string;

interface BadgeProps {
    label: string;
    category?: Category;
}

export default function Badge({ label, category }: BadgeProps) {
    // TODO: Map category → color class:
    //   tech       → indigo
    //   business   → emerald
    //   politics   → amber
    //   sports     → rose
    //   default    → slate
    // TODO: Apply pill styling (rounded-full, small padding, uppercase, font-semibold)

    return <span>{label}</span>; // TODO: implement
}
