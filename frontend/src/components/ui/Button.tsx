// Reusable Button component

// TODO: Import clsx or cn utility for conditional class merging

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "primary" | "secondary" | "ghost" | "danger";
    size?: "sm" | "md" | "lg";
    isLoading?: boolean;
}

export default function Button({
    variant = "primary",
    size = "md",
    isLoading = false,
    children,
    ...props
}: ButtonProps) {
    // TODO: Map variant → Tailwind classes (e.g. primary → bg-indigo-600 hover:bg-indigo-700)
    // TODO: Map size → padding/text classes
    // TODO: Show Spinner if isLoading
    // TODO: Disable button while isLoading

    return (
        <button {...props}>
            {/* TODO: implement */}
            {children}
        </button>
    );
}
