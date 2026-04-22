"""Shared CSS injected into every Streamlit page to match the React design."""

import streamlit as st

_CSS = """
<style>
/* ── Global ─────────────────────────────────────────────── */
[data-testid="stApp"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── Auth pages — gradient background ───────────────────── */
.auth-bg {
    background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}
.auth-bg-purple {
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
}
.auth-bg-pink {
    background: linear-gradient(135deg, #fdf4ff 0%, #fce7f3 100%);
}

/* ── Card ────────────────────────────────────────────────── */
.card {
    background: white;
    border-radius: 14px;
    padding: 2rem 2.5rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
    margin: 0 auto;
    max-width: 440px;
}
.card-wide { max-width: 560px; }
.card-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #111827;
    text-align: center;
    margin: 0 0 0.25rem;
}
.card-desc {
    font-size: 0.875rem;
    color: #6b7280;
    text-align: center;
    margin: 0 0 1.5rem;
}

/* ── Progress bar ───────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div {
    background-color: #4f46e5 !important;
}

/* ── Buttons ─────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    border-radius: 8px;
    font-weight: 500;
    transition: background 0.15s ease;
}

/* ── Top navbar ──────────────────────────────────────────── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid #e5e7eb;
}
.nav-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e1b4b;
    margin: 0;
}

/* ── Article card ─────────────────────────────────────────── */
.article-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s ease;
    height: 100%;
}
.article-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.article-card-body { padding: 1rem; }
.article-card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 0.4rem;
    line-height: 1.4;
}
.article-card-preview {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0 0 0.5rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.article-card-meta {
    font-size: 0.75rem;
    color: #9ca3af;
}

/* ── Category badge ──────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: #ede9fe;
    color: #4f46e5;
    margin-bottom: 0.5rem;
}

/* ── Survey category button ──────────────────────────────── */
.cat-btn {
    display: flex;
    align-items: center;
    gap: 1rem;
    width: 100%;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    border: 2px solid #e5e7eb;
    background: #f9fafb;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
    text-align: left;
    transition: all 0.15s ease;
    margin-bottom: 0.5rem;
}
.cat-btn.selected {
    border-color: #4f46e5;
    background: #ede9fe;
    color: #4f46e5;
}

/* ── Error box (matches React destructive style) ─────────── */
.err-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 0.625rem 1rem;
    font-size: 0.875rem;
    color: #dc2626;
    margin: 0.5rem 0;
}
</style>
"""


def inject():
    st.markdown(_CSS, unsafe_allow_html=True)
