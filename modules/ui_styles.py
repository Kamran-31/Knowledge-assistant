"""
UI Styles for Knowledge Assistant
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F7F6F3;
}

/* Hide native Streamlit chrome */
header[data-testid="stHeader"] {
    display: none !important;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Container page padding */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 4.5rem !important;
    max-width: 100% !important;
}

/* Professional card containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 16px !important;
    border: 1px solid #ECEAE4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

/* Top bar standard buttons */
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

/* ---------- STUDIO BUTTON FIXES ---------- */
/* Container button box */
.studio-card div[data-testid="stButton"] button {
    min-height: 72px !important;
    height: auto !important;
    padding: 8px 4px !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FAFAFA !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease-in-out !important;
}

.studio-card div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(37,99,235,0.08) !important;
}

/* Remove Streamlit's default truncation on all child text nodes */
.studio-card div[data-testid="stButton"] button * {
    white-space: pre-line !important;
    text-overflow: unset !important;
    overflow: visible !important;
    word-break: normal !important;
    text-align: center !important;
    line-height: 1.25 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #1F2937 !important;
    margin: 0 !important;
}

/* First line (Emoji) enlargement */
.studio-card div[data-testid="stButton"] button *:first-line {
    font-size: 1.25rem !important;
    line-height: 1.4 !important;
}

/* ---------- Other Components ---------- */
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

.app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(247, 246, 243, 0.95);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid #E5E7EB;
    text-align: center;
    padding: 8px 16px;
    font-size: 0.76rem;
    color: #6B7280;
    z-index: 99999;
    letter-spacing: 0.01em;
}
</style>
"""
