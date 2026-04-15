"use client";

import type { Question } from "@/lib/surveyQuestions";

interface SurveyStepProps {
    sectionLabel: string;
    sectionColor: string;
    questions: Question[];
    answers: Record<string, string | string[] | number>;
    onChange: (questionId: string, value: string | string[] | number) => void;
}

export default function SurveyStep({ sectionLabel, sectionColor, questions, answers, onChange }: SurveyStepProps) {
    return (
        <div className="flex flex-col gap-8">
            <p className={`text-xs font-semibold uppercase tracking-widest ${sectionColor}`}>
                {sectionLabel}
            </p>
            {questions.map((q) => (
                <QuestionBlock key={q.id} question={q} value={answers[q.id]} onChange={(v) => onChange(q.id, v)} />
            ))}
        </div>
    );
}

function QuestionBlock({
    question,
    value,
    onChange,
}: {
    question: Question;
    value: string | string[] | number | undefined;
    onChange: (v: string | string[] | number) => void;
}) {
    return (
        <div className="flex flex-col gap-3">
            <p className="text-sm font-medium text-foreground">{question.text}</p>
            {question.type === "single" && (
                <SingleSelect options={question.options!} value={value as string} onChange={onChange} />
            )}
            {question.type === "multi" && (
                <MultiSelect options={question.options!} value={(value as string[]) ?? []} onChange={onChange} />
            )}
            {question.type === "likert" && (
                <LikertScale value={value as number} onChange={onChange} />
            )}
            {question.type === "rank" && (
                <RankOrder options={question.options!} value={(value as string[]) ?? question.options!.map((o) => o.value)} onChange={onChange} />
            )}
        </div>
    );
}

function SingleSelect({
    options,
    value,
    onChange,
}: {
    options: { label: string; value: string }[];
    value: string | undefined;
    onChange: (v: string) => void;
}) {
    return (
        <div className="flex flex-col gap-2">
            {options.map((opt) => (
                <button
                    key={opt.value}
                    type="button"
                    onClick={() => onChange(opt.value)}
                    className={`rounded-lg border px-4 py-2.5 text-left text-sm transition ${
                        value === opt.value
                            ? "border-primary bg-primary/10 text-primary font-medium"
                            : "border-border bg-muted/30 text-foreground hover:border-primary/50 hover:bg-muted/60"
                    }`}
                >
                    {opt.label}
                </button>
            ))}
        </div>
    );
}

function MultiSelect({
    options,
    value,
    onChange,
}: {
    options: { label: string; value: string }[];
    value: string[];
    onChange: (v: string[]) => void;
}) {
    function toggle(opt: string) {
        const next = value.includes(opt) ? value.filter((v) => v !== opt) : [...value, opt];
        onChange(next);
    }
    return (
        <div className="flex flex-wrap gap-2">
            {options.map((opt) => {
                const selected = value.includes(opt.value);
                return (
                    <button
                        key={opt.value}
                        type="button"
                        onClick={() => toggle(opt.value)}
                        className={`rounded-full border px-4 py-1.5 text-sm transition ${
                            selected
                                ? "border-primary bg-primary/10 text-primary font-medium"
                                : "border-border bg-muted/30 text-muted-foreground hover:border-primary/50 hover:bg-muted/60"
                        }`}
                    >
                        {selected && <span className="mr-1">✓</span>}
                        {opt.label}
                    </button>
                );
            })}
        </div>
    );
}

function LikertScale({
    value,
    onChange,
}: {
    value: number | undefined;
    onChange: (v: number) => void;
}) {
    const labels = ["Not interested", "", "", "", "Very interested"];
    return (
        <div className="flex flex-col gap-2">
            <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((n) => (
                    <button
                        key={n}
                        type="button"
                        onClick={() => onChange(n)}
                        className={`flex h-11 flex-1 items-center justify-center rounded-lg border text-sm font-semibold transition ${
                            value === n
                                ? "border-primary bg-primary text-primary-foreground"
                                : "border-border bg-muted/30 text-foreground hover:border-primary/50 hover:bg-muted/60"
                        }`}
                    >
                        {n}
                    </button>
                ))}
            </div>
            <div className="flex justify-between text-xs text-muted-foreground">
                <span>{labels[0]}</span>
                <span>{labels[4]}</span>
            </div>
        </div>
    );
}

function RankOrder({
    options,
    value,
    onChange,
}: {
    options: { label: string; value: string }[];
    value: string[];
    onChange: (v: string[]) => void;
}) {
    const ordered = value.length === options.length
        ? value
        : options.map((o) => o.value);

    const labelMap = Object.fromEntries(options.map((o) => [o.value, o.label]));

    function move(index: number, dir: -1 | 1) {
        const next = [...ordered];
        const swap = index + dir;
        if (swap < 0 || swap >= next.length) return;
        [next[index], next[swap]] = [next[swap], next[index]];
        onChange(next);
    }

    return (
        <div className="flex flex-col gap-2">
            {ordered.map((val, i) => (
                <div key={val} className="flex items-center gap-3 rounded-lg border border-border bg-muted/30 px-4 py-2.5">
                    <span className="w-5 text-center text-xs font-bold text-primary">{i + 1}</span>
                    <span className="flex-1 text-sm text-foreground">{labelMap[val]}</span>
                    <div className="flex flex-col gap-0.5">
                        <button
                            type="button"
                            onClick={() => move(i, -1)}
                            disabled={i === 0}
                            className="text-muted-foreground hover:text-foreground disabled:opacity-20"
                        >
                            ▲
                        </button>
                        <button
                            type="button"
                            onClick={() => move(i, 1)}
                            disabled={i === ordered.length - 1}
                            className="text-muted-foreground hover:text-foreground disabled:opacity-20"
                        >
                            ▼
                        </button>
                    </div>
                </div>
            ))}
            <p className="text-xs text-muted-foreground">Use ▲ ▼ to reorder by priority</p>
        </div>
    );
}
