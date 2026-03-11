// SurveyStep — renders the content for a single survey question step
// Each step has a title, optional subtitle, and one or more answer options

export interface SurveyOption {
    label: string;
    value: string;
    icon?: string;
}

interface SurveyStepProps {
    stepNumber: number;
    title: string;
    subtitle?: string;
    options: SurveyOption[];
    selectedValues: string[];
    multiSelect?: boolean;
    onSelect: (value: string) => void;
}

export default function SurveyStep({
    stepNumber,
    title,
    subtitle,
    options,
    selectedValues,
    multiSelect = false,
    onSelect,
}: SurveyStepProps) {
    // TODO: Render step number indicator
    // TODO: Render title and optional subtitle
    // TODO: Render answer options as clickable cards/buttons
    // TODO: If multiSelect=true → allow multiple selections (checkbox style)
    // TODO: If multiSelect=false → single selection (radio style)
    // TODO: Animate selected state with border highlight or checkmark

    return (
        <div>
            <h2>{title}</h2>
            {/* TODO: full step UI */}
        </div>
    );
}
