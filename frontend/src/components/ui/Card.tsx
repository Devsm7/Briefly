// Reusable Card container with optional glassmorphism style

interface CardProps {
    children: React.ReactNode;
    className?: string;
    glass?: boolean; // apply glassmorphism styling
}

export default function Card({ children, className, glass }: CardProps) {
    // TODO: Apply base card styles (dark bg, rounded-xl, shadow)
    // TODO: If glass=true, apply backdrop-blur + semi-transparent bg
    // TODO: Merge with className via cn()

    return (
        <div className={className}>
            {/* TODO: implement */}
            {children}
        </div>
    );
}
