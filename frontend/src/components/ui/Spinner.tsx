// Animated loading spinner

interface SpinnerProps {
    size?: "sm" | "md" | "lg";
}

export default function Spinner({ size = "md" }: SpinnerProps) {
    // TODO: Render an SVG or CSS spinner
    // TODO: Map size → dimension classes
    // TODO: Use primary brand color for the spinning arc

    return <div aria-label="Loading" />; // TODO: implement
}
