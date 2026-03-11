// FeedFilters — horizontal category tab bar

// Displayed above the article feed on the dashboard

const CATEGORIES = [
    { label: "All", value: "all" },
    { label: "Tech", value: "tech" },
    { label: "Business", value: "business" },
    { label: "Politics", value: "politics" },
    { label: "Sports", value: "sports" },
];

interface FeedFiltersProps {
    activeCategory: string;
    onChange: (category: string) => void;
}

export default function FeedFilters({ activeCategory, onChange }: FeedFiltersProps) {
    // TODO: Render horizontal pill tabs from CATEGORIES
    // TODO: Active tab → primary color highlight + underline
    // TODO: Smooth color transition on tab switch
    // TODO: Scrollable on mobile

    return (
        <div role="tablist">
            {/* TODO: implement */}
        </div>
    );
}
