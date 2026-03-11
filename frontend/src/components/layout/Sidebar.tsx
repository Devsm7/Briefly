// Left sidebar — navigation links and category shortcuts

// TODO: Import Link from next/link
// TODO: Import active route detection (usePathname)

const NAV_ITEMS = [
    { label: "For You", href: "/dashboard", icon: "✦" },
    { label: "Trending", href: "/dashboard?mode=trending", icon: "🔥" },
    { label: "Library", href: "/library", icon: "🔖" },
    { label: "Daily Digest", href: "/digest", icon: "📰" },
    { label: "Settings", href: "/settings", icon: "⚙️" },
];

const CATEGORIES = [
    { label: "Technology", slug: "tech" },
    { label: "Business", slug: "business" },
    { label: "Politics", slug: "politics" },
    { label: "Sports", slug: "sports" },
];

export default function Sidebar() {
    // TODO: Highlight active link using usePathname()
    // TODO: Render NAV_ITEMS as vertical nav links
    // TODO: Render CATEGORIES as quick-filter links
    // TODO: Apply dark styling and hover states

    return (
        <aside>
            {/* TODO: implement */}
        </aside>
    );
}
