"""
UI Styles for Knowledge Assistant
Contains custom CSS for cards, header, untruncated studio buttons, and a normal bottom footer.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #E5E3DC;
}

/* Hide default Streamlit chrome */
header[data-testid="stHeader"] {
    display: none !important;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Page container */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* Rounded border cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 16px !important;
    border: 1px solid #ECEAE4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

/* Top bar buttons */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid #E4E1D8 !important;
    background: #FFFFFF;
    color: #1F2937;
    font-weight: 500;
    padding: 0.45rem 1rem;
    transition: all 0.15s ease-in-out;
}

div.stButton > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    background: #F5F8FF !important;
}

/* ---------- STUDIO BUTTONS: PREVENT TEXT TRUNCATION ---------- */
/* Force studio column buttons to accommodate 2 lines and larger icons */
div[data-testid="stColumn"] div[data-testid="stButton"] button {
    min-height: 60px !important;
    height: auto !important;
    padding: 6px 4px !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FAFAFA !important;
}

/* Eliminate ellipsis and force wrap across all descendant nodes */
div[data-testid="stColumn"] div[data-testid="stButton"] button,
div[data-testid="stColumn"] div[data-testid="stButton"] button *,
div[data-testid="stColumn"] div[data-testid="stButton"] button p,
div[data-testid="stColumn"] div[data-testid="stButton"] button span {
    white-space: normal !important;
    text-overflow: clip !important;
    overflow: visible !important;
    word-break: break-word !important;
    text-align: center !important;
    font-size: 0.82rem !important;
    line-height: 1.25 !important;
}

/* Hover state */
div[data-testid="stColumn"] div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    box-shadow: 0 2px 5px rgba(37,99,235,0.08) !important;
}

/* Chat bubble styling */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #ECEAE4;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.6rem;
}

.history-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem 0.3rem;
    border-radius: 8px;
    font-size: 0.84rem;
    color: #374151;
}

.history-item:hover {
    background: #F3F2EC;
}

/* ---------- NATURAL FOOTER (APPEARS ONLY AT BOTTOM OF PAGE) ---------- */
.app-footer {
    position: relative !important;
    display: block !important;
    width: 100%;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    padding-bottom: 0.8rem;
    border-top: 1px solid #E5E7EB;
    text-align: center;
    font-size: 0.76rem;
    color: #6B7280;
    letter-spacing: 0.01em;
}
</style>
"""
