import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Personalise your feed — Briefly", layout="centered")
styles.inject()

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("pages/log_in_page.py")

# ── Survey data (mirrors surveyQuestions.ts) ──────────────────────────────────
CATEGORIES = [
    {"id": "tech",     "label": "Tech",     "icon": "💻"},
    {"id": "politics", "label": "Politics", "icon": "🗳️"},
    {"id": "sport",    "label": "Sport",    "icon": "⚽"},
]

CATEGORY_QUESTIONS = {
    "tech": [
        {
            "id": "Q04",
            "text": "Which technology topics interest you most?",
            "type": "multi",
            "options": [
                ("Artificial Intelligence", "ai"),
                ("Cybersecurity", "cybersecurity"),
                ("Startups", "startups"),
                ("Consumer Electronics", "electronics"),
                ("Software & Apps", "software"),
                ("Science & Space", "science"),
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
                ("Domestic policy", "domestic"),
                ("International relations", "international"),
                ("Elections & democracy", "elections"),
                ("Economic policy", "economic"),
                ("Social issues", "social"),
                ("Environmental policy", "environment"),
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
                ("Football / Soccer", "football"),
                ("Basketball", "basketball"),
                ("Tennis", "tennis"),
                ("Cricket", "cricket"),
                ("Formula 1", "f1"),
                ("Athletics", "athletics"),
                ("Rugby", "rugby"),
                ("Baseball", "baseball"),
            ],
        },
        {
            "id": "Q14",
            "text": "How would you rate your interest in sports news overall?",
            "type": "likert",
        },
    ],
}

LIKERT_LABELS = ["1 — Not at all", "2", "3 — Neutral", "4", "5 — Very much"]

# ── Session state initialisation ──────────────────────────────────────────────
if "survey_step" not in st.session_state:
    st.session_state["survey_step"] = 0
if "survey_categories" not in st.session_state:
    st.session_state["survey_categories"] = []
if "survey_answers" not in st.session_state:
    st.session_state["survey_answers"] = {}

step = st.session_state["survey_step"]
selected_cats = st.session_state["survey_categories"]
category_steps = [c for c in CATEGORIES if c["id"] in selected_cats]
total_steps = 1 + len(category_steps)
step_labels = ["Your Interests"] + [c["label"] for c in category_steps]

# ── Progress bar ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="card card-wide">
    <p class="card-title" style="text-align:left;font-size:1.4rem;">Personalise your feed</p>
    <p class="card-desc" style="text-align:left;">Help us understand what matters to you</p>
</div>
""", unsafe_allow_html=True)

progress_pct = step / max(total_steps - 1, 1)
st.progress(progress_pct)

label_cols = st.columns(len(step_labels))
for i, lbl in enumerate(step_labels):
    with label_cols[i]:
        colour = "#4f46e5" if i == step else ("#9ca3af" if i > step else "#6b7280")
        st.markdown(
            f'<p style="font-size:0.7rem;text-align:center;color:{colour};font-weight:{"700" if i==step else "400"}">{lbl}</p>',
            unsafe_allow_html=True,
        )

st.divider()

# ── Step 0 — Category selection ───────────────────────────────────────────────
if step == 0:
    st.markdown("**Which news categories are you interested in?**")
    st.caption("Select one or more")

    for cat in CATEGORIES:
        is_selected = cat["id"] in selected_cats
        label = f"{'✓  ' if is_selected else '      '}{cat['icon']}  {cat['label']}"
        if st.button(label, key=f"cat_{cat['id']}", use_container_width=True):
            if is_selected:
                st.session_state["survey_categories"].remove(cat["id"])
            else:
                st.session_state["survey_categories"].append(cat["id"])
            st.rerun()

# ── Steps 1+ — Category questions ─────────────────────────────────────────────
else:
    current_cat = category_steps[step - 1]
    questions = CATEGORY_QUESTIONS[current_cat["id"]]

    st.markdown(f"#### {current_cat['icon']}  {current_cat['label']}")

    for q in questions:
        st.markdown(f"**{q['text']}**")

        if q["type"] == "multi":
            current_vals = st.session_state["survey_answers"].get(q["id"], [])
            new_vals = []
            for label, value in q["options"]:
                checked = st.checkbox(label, value=value in current_vals, key=f"{q['id']}_{value}")
                if checked:
                    new_vals.append(value)
            st.session_state["survey_answers"][q["id"]] = new_vals

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

        st.write("")

# ── Navigation ─────────────────────────────────────────────────────────────────
st.divider()
nav_left, nav_right = st.columns([1, 1])

with nav_left:
    col_back, col_skip = st.columns(2)
    with col_back:
        if step > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state["survey_step"] -= 1
                st.rerun()
    with col_skip:
        if st.button("Skip survey", use_container_width=True):
            with st.spinner("Skipping…"):
                try:
                    api_client.skip_survey()
                except Exception:
                    pass
            st.switch_page("pages/ForYou.py")

with nav_right:
    is_last = step == total_steps - 1

    if is_last:
        if st.button("Finish →", use_container_width=True, type="primary"):
            with st.spinner("Saving preferences…"):
                try:
                    api_client.submit_survey(
                        categories=st.session_state["survey_categories"],
                        answers=st.session_state["survey_answers"],
                    )
                    # Clear survey state
                    for k in ["survey_step", "survey_categories", "survey_answers"]:
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
