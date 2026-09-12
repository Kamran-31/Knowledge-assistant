"""
Injected CSS that reshapes Streamlit's default widgets into the
rounded-card, pill-button, soft-shadow aesthetic from the UI mockup.
Streamlit doesn't allow arbitrary custom components without extra
packages, so this styles native elements (containers, buttons, inputs,
chat bubbles) as closely as possible to the target design.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Overall background */
.stApp {
    background-color: #F7F6F3;
}

/* Hide default Streamlit chrome for a cleaner "product" feel */
#MainMenu, footer {visibility: hidden;}

/* ---------- Header bar ---------- */
.notebook-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1rem;
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #ECEAE4;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.notebook-header .brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 600;
    font-size: 1.05rem;
    color: #1F2937;
}
.notebook-header .brand .logo-dot {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F8FFF, #7AD1FF);
    display: inline-block;
}
.pro-badge {
    background: #EAF1FF;
    color: #3B6FE0;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 999px;
    margin-left: 6px;
    letter-spacing: 0.03em;
}

/* ---------- Cards ---------- */
.card {
    background: #FFFFFF;
    border: 1px solid #ECEAE4;
    border-radius: 18px;
    padding: 1.1rem 1.1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.card h4 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #1F2937;
}
.card-subtle {
    color: #8A8578;
    font-size: 0.8rem;
}

/* ---------- Pill buttons ---------- */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid #E4E1D8 !important;
    background: #FFFFFF;
    color: #1F2937;
    font-weight: 500;
    padding: 0.45rem 1.1rem;
    transition: all 0.15s ease;
}
div.stButton > button:hover {
    border-color: #4F8FFF !important;
    color: #3B6FE0;
    background: #F5F8FF;
}

/* Primary / dark pill button variant */
.pill-primary button {
    background: #111827 !important;
    color: #FFFFFF !important;
    border: none !important;
}
.pill-primary button:hover {
    background: #1F2937 !important;
    color: #FFFFFF !important;
}

/* ---------- Quick prompt chips ---------- */
.chip-row { display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; }
.chip {
    background: #EEF3FF;
    color: #3B6FE0;
    border-radius: 999px;
    padding: 0.5rem 1.1rem;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
}

/* ---------- Empty state (welcome) ---------- */
.welcome-wrap {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
}
.welcome-wrap .emoji { font-size: 2.4rem; }
.welcome-wrap h2 {
    font-weight: 600;
    color: #1F2937;
    margin: 0.4rem 0 0.3rem 0;
}
.welcome-wrap p {
    color: #8A8578;
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
}

/* ---------- Source count tag ---------- */
.source-tag {
    background: #F1F0EB;
    color: #6B6858;
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
    display: inline-block;
}

/* ---------- Studio tiles ---------- */
.studio-tile {
    background: linear-gradient(135deg, #F5F0FF 0%, #EAF3FF 100%);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
    border: 1px solid #ECEAE4;
    font-weight: 500;
    color: #1F2937;
    font-size: 0.85rem;
}
.studio-placeholder {
    text-align: center;
    color: #A6A296;
    font-size: 0.82rem;
    padding: 2rem 0.5rem;
    border: 1px dashed #E4E1D8;
    border-radius: 16px;
}

/* ---------- History list ---------- */
.history-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0.3rem;
    border-radius: 10px;
    font-size: 0.83rem;
    color: #3A3730;
}
.history-item:hover { background: #F5F4EF; }
.history-time { color: #A6A296; font-size: 0.75rem; margin-left: auto; }

/* Chat message bubbles */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #ECEAE4;
    padding: 0.4rem 0.2rem;
}
</style>
"""
