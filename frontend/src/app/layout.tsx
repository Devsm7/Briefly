// TODO: Implement the root layout
// - Import Inter / Outfit font from next/font/google
// - Set <html lang="en">
// - Wrap children in a Providers component (auth context, etc.)
// - Apply global className for dark theme base

import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Briefly — Your Personalized News Digest",
    description:
        "AI-powered personalized news platform that learns your interests and delivers smart briefings.",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    // TODO: implement
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
