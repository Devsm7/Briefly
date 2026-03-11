import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            // TODO: Add Briefly brand tokens
            colors: {
                // primary: indigo/purple palette
                // surface: dark card backgrounds
                // accent: highlight color
            },
            fontFamily: {
                // TODO: Add Inter or Outfit from Google Fonts
            },
        },
    },
    plugins: [],
};

export default config;
