import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Personalise your feed — Briefly", layout="centered")
styles.inject()

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("pages/log_in_page.py")

# ── Survey categories & questions ──────────────────────────────────────────────
CATEGORIES = [
    {"id": "tech",     "label": "Tech",     "icon": "💻", "color": "#6366f1"},
    {"id": "politics", "label": "Politics", "icon": "🗳️",  "color": "#ef4444"},
    {"id": "sport",    "label": "Sport",   "icon": "⚽",  "color": "#22c55e"},
    {"id": "business", "label": "Business", "icon": "💼",  "color": "#f59e0b"},
    {"id": "health",   "label": "Health",   "icon": "🏥",  "color": "#ec4899"},
    {"id": "science",  "label": "Science",  "icon": "🔬",  "color": "#14b8a6"},
]

CATEGORY_QUESTIONS = {
    "tech": [
        {
            "id": "Q04",
            "text": "Which technology topics interest you most?",
            "type": "multi",
            "options": [
                ("Artificial Intelligence", "artificial_intelligence"),
                ("Cybersecurity", "cybersecurity"),
                ("Cloud Computing", "cloud_computing"),
                ("Data Management", "data_management"),
                ("Technology Infrastructure", "technology_infrastructure"),
            ],
        },
        {
            "id": "Q05",
            "text": "How would you rate your interest in technology news overall?",
            "type": "likert",
        },
    ],
    "politics": [
        {
            "id": "Q07",
            "text": "Which political topics are you most interested in?",
            "type": "multi",
            "options": [
                ("Election Politics", "election_politics"),
                ("Executive Policy", "executive_policy"),
                ("Maritime Security", "maritime_security"),
                ("Disability Rights", "disability_rights"),
            ],
        },
        {
            "id": "Q08",
            "text": "How would you rate your interest in political news overall?",
            "type": "likert",
        },
    ],
    "sport": [
        {
            "id": "Q13",
            "text": "Which sports do you follow?",
            "type": "multi",
            "options": [
                ("American Football", "american_football"),
                ("Basketball", "basketball"),
                ("Baseball", "baseball"),
                ("Soccer", "soccer"),
                ("Combat Sports", "combat_sports"),
            ],
        },
        {
            "id": "Q14",
            "text": "How would you rate your interest in sports news overall?",
            "type": "likert",
        },
    ],
    "business": [
        {
            "id": "Q15",
            "text": "Which business topics interest you most?",
            "type": "multi",
            "options": [
                ("Earnings Reports", "earnings_reports"),
                ("Financial Markets", "financial_markets"),
                ("Company Performance", "company_performance"),
                ("Investment Strategies", "investment_strategies"),
                ("Industry Trends", "industry_trends"),
            ],
        },
        {
            "id": "Q18",
            "text": "How would you rate your interest in business news overall?",
            "type": "likert",
        },
    ],
    "health": [
        {
            "id": "Q19",
            "text": "Which health topics interest you most?",
            "type": "multi",
            "options": [
                ("Mental health & wellness", "mental_health"),
                ("Nutrition & diet", "nutrition"),
                ("Fitness & exercise", "fitness"),
                ("Medical research", "medical_research"),
                ("Public health & policy", "public_health"),
                ("Aging & longevity", "longevity"),
            ],
        },
        {
            "id": "Q21",
            "text": "How would you rate your interest in health news overall?",
            "type": "likert",
        },
    ],
    "science": [
        {
            "id": "Q22",
            "text": "Which science topics interest you most?",
            "type": "multi",
            "options": [
                ("Space & astronomy", "space"),
                ("Physics & chemistry", "physics"),
                ("Biology & life sciences", "biology"),
                ("Climate & environment", "climate"),
                ("Technology & engineering", "tech_science"),
                ("Archaeology & history", "archaeology"),
            ],
        },
        {
            "id": "Q24",
            "text": "How would you rate your interest in science news overall?",
            "type": "likert",
        },
    ],
}

LIKERT_LABELS = ["1 — Not at all", "2", "3 — Neutral", "4", "5 — Very much"]

# ── Session state initialisation ──────────────────────────────────────────────
for key, default in [
    ("survey_step", 0),
    ("survey_categories", []),
    ("survey_answers", {}),
]:
    if key not in st.session_state:
        st.session_state[key] = default

step = st.session_state["survey_step"]
selected_cats = st.session_state["survey_categories"]
category_steps = [c for c in CATEGORIES if c["id"] in selected_cats]
total_steps = 1 + len(category_steps)
step_labels = ["Interests"] + [c["label"] for c in category_steps]

# ── Page styles ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .survey-header { text-align: center; margin-bottom: 1.5rem; }
    .survey-header h2 { font-size: 1.8rem; font-weight: 800; color: #1e1b4b; margin: 0 0 0.25rem; }
    .survey-header p { font-size: 0.9rem; color: #6b7280; margin: 0; }

    [data-testid="stProgressBar"] > div > div { background-color: #6366f1 !important; }

    .cat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        max-width: 520px;
        margin: 0 auto;
    }
    @media (max-width: 480px) { .cat-grid { grid-template-columns: 1fr; } }

    .cat-btn {
        display: flex; align-items: center; gap: 0.75rem;
        padding: 0.9rem 1rem; border-radius: 14px;
        border: 2px solid #e5e7eb; background: #f9fafb;
        cursor: pointer; font-size: 0.95rem; font-weight: 600;
        color: #374151; text-align: left; width: 100%;
        transition: all 0.15s ease;
    }
    .cat-btn:hover { border-color: #c7d2fe; background: #eef2ff; }
    .cat-btn.selected { border-color: var(--cat-color, #6366f1); background: var(--cat-bg, #eef2ff); color: var(--cat-color, #6366f1); }
    .cat-icon { font-size: 1.4rem; flex-shrink: 0; }
    .cat-check { margin-left: auto; font-size: 1rem; }

    .q-block { max-width: 520px; margin: 0 auto 1.25rem; }
    .q-text { font-size: 0.9rem; font-weight: 700; color: #374151; margin-bottom: 0.65rem; }

    .opt-row { display: flex; flex-direction: column; gap: 0.35rem; }
    .opt-item { display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.75rem; border-radius: 10px; background: #f3f4f6; transition: all 0.15s; }
    .opt-item.checked { background: #eef2ff; border: 1.5px solid #6366f1; }
    .opt-label { font-size: 0.875rem; color: #374151; cursor: pointer; width: 100%; }
    .opt-item.checked .opt-label { color: #4338ca; font-weight: 500; }

    .likert-labels { display: flex; justify-content: space-between; font-size: 0.7rem; color: #9ca3af; margin-top: 0.3rem; }

    .cat-header { text-align: center; margin-bottom: 1.25rem; }
    .cat-header .cat-icon-big { font-size: 2.2rem; }
    .cat-header .cat-name { font-size: 1.2rem; font-weight: 800; margin-top: 0.25rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="survey-header">'
    '<h2>Personalise your feed ✨</h2>'
    '<p>Pick categories and topics you care about — takes under a minute</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Progress ────────────────────────────────────────────────────────────────────
if total_steps > 1:
    st.progress(step / max(total_steps - 1, 1))
    cols = st.columns(len(step_labels))
    for i, lbl in enumerate(step_labels):
        col = cols[i]
        color = "#6366f1" if i == step else ("#a5b4fc" if i < step else "#d1d5db")
        fw = "700" if i == step else "400"
        col.markdown(
            f'<p style="font-size:0.65rem;text-align:center;color:{color};font-weight:{fw};margin-top:0.3rem;text-transform:uppercase;letter-spacing:0.05em">{lbl}</p>',
            unsafe_allow_html=True,
        )

st.divider()

# ── Step 0 — Category selection ───────────────────────────────────────────────
if step == 0:
    st.markdown('<p style="text-align:center;font-weight:600;color:#374151;margin-bottom:1rem">What topics interest you?</p>', unsafe_allow_html=True)

    for i in range(0, len(CATEGORIES), 2):
        row = CATEGORIES[i : i + 2]
        cols = st.columns(2)
        for ci, cat in enumerate(row):
            with cols[ci]:
                is_sel = cat["id"] in selected_cats
                # Inline style via st.markdown div triggered by session_state
                border = cat["color"] if is_sel else "#e5e7eb"
                bg = "#eef2ff" if is_sel else "#f9fafb"
                color = cat["color"] if is_sel else "#374151"
                check = "✓" if is_sel else ""
                if st.button(
                    f"⚙ {cat['icon']}  {cat['label']}  {check}",
                    key=f"cat_{cat['id']}",
                    use_container_width=True,
                ):
                    if is_sel:
                        st.session_state["survey_categories"].remove(cat["id"])
                    else:
                        st.session_state["survey_categories"].append(cat["id"])
                    st.rerun()

# ── Steps 1+ — Category questions ─────────────────────────────────────────────
else:
    current_cat = category_steps[step - 1]
    questions = CATEGORY_QUESTIONS.get(current_cat["id"], [])

    st.markdown(
        f'<div class="cat-header">'
        f'<div class="cat-icon-big">{current_cat["icon"]}</div>'
        f'<div class="cat-name" style="color:{current_cat["color"]}">{current_cat["label"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    for q in questions:
        st.markdown(f'<div class="q-block"><p class="q-text">{q["text"]}</p>', unsafe_allow_html=True)

        if q["type"] == "multi":
            opts = q["options"]

            # Two-column checkbox layout
            for i in range(0, len(opts), 2):
                row_opts = opts[i : i + 2]
                opt_cols = st.columns(2)
                for oc, (label, value) in enumerate(row_opts):
                    # Re-read on every iteration so changes from earlier checkboxes are visible
                    current_vals = st.session_state["survey_answers"].get(q["id"], [])
                    checked = value in current_vals
                    with opt_cols[oc]:
                        if st.checkbox(f"  {label}", value=checked, key=f"cb_{q['id']}_{value}"):
                            if value not in current_vals:
                                st.session_state["survey_answers"][q["id"]] = current_vals + [value]
                        else:
                            st.session_state["survey_answers"][q["id"]] = [v for v in current_vals if v != value]

        elif q["type"] == "likert":
            current_val = st.session_state["survey_answers"].get(q["id"], 3)
            chosen = st.select_slider(
                "",
                options=[1, 2, 3, 4, 5],
                value=current_val,
                format_func=lambda x: LIKERT_LABELS[x - 1],
                key=f"likert_{q['id']}",
            )
            st.session_state["survey_answers"][q["id"]] = chosen
            st.markdown('<div class="likert-labels"><span>Not at all</span><span>Neutral</span><span>Very much</span></div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ── Navigation ─────────────────────────────────────────────────────────────────
st.divider()
lcol, rcol = st.columns([1, 1], vertical_alignment="center")

with lcol:
    back_col, skip_col = st.columns(2)
    with back_col:
        if step > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state["survey_step"] -= 1
                st.rerun()
    with skip_col:
        if st.button("Skip", use_container_width=True):
            for k in ["survey_step", "survey_categories", "survey_answers", "recommendations_cache"]:
                st.session_state.pop(k, None)
            st.switch_page("pages/ForYou.py")

with rcol:
    is_last = step == total_steps - 1
    if is_last:
        if st.button("Finish →", use_container_width=True, type="primary"):
            with st.spinner("Saving preferences…"):
                try:
                    api_client.submit_survey(
                        categories=st.session_state["survey_categories"],
                        answers=st.session_state["survey_answers"],
                    )
                    for k in ["survey_step", "survey_categories", "survey_answers", "recommendations_cache"]:
                        st.session_state.pop(k, None)
                    st.switch_page("pages/ForYou.py")
                except RuntimeError as e:
                    st.markdown(f'<div class="err-box">{e}</div>', unsafe_allow_html=True)
                except Exception:
                    st.markdown('<div class="err-box">Failed to save survey. Please try again.</div>', unsafe_allow_html=True)
    else:
        disabled = step == 0 and len(st.session_state["survey_categories"]) == 0
        if st.button("Next →", use_container_width=True, type="primary", disabled=disabled):
            st.session_state["survey_step"] += 1
            st.rerun()