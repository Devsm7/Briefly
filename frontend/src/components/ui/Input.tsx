// Styled text input with label and error message support

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

export default function Input({ label, error, ...props }: InputProps) {
    // TODO: Render label above input if provided
    // TODO: Style input: dark bg, border (red if error), rounded-lg, focus ring
    // TODO: Render error message below input if provided

    return (
        <div>
            {label && <label>{label}</label>}
            <input {...props} />
            {error && <p>{error}</p>}
            {/* TODO: apply full styling */}
        </div>
    );
}
