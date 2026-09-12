"""
Injected CSS that reshapes Streamlit's default widgets into the
rounded-card, pill-button, soft-shadow aesthetic from the UI mockup.
Includes fixed-footer support and multi-line responsive studio action buttons.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Overall canvas background */
.stApp {
    background-color: #F7F6F3;
}

/* Hide default Streamlit header and default footer */
#MainMenu, footer {
    visibility: hidden;
}

/* Main container spacing so content clears the fixed bottom footer */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 100% !important;
}

/* ---------- Professional Sticky Header ---------- */
.notebook-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1rem;
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #ECEAE4;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 0.5rem;
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
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #60A5FA);
    display: inline-block;
}
.pro-badge {
    background: #EAF1FF;
    color: #2563EB;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 999px;
    margin-left: 6px;
    letter-spacing: 0.04em;
}

/* ---------- Cards / Native Containers ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 18px !important;
    border: 1px solid #ECEAE4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

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

/* ---------- Global Pill Buttons (Top Bar & General) ---------- */
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

/* ---------- Studio Panel Buttons (Larger & Multi-line) ---------- */
.studio-grid div[data-testid="stButton"] button {
    min-height: 52px !important;
    height: auto !important;
    padding: 8px 10px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    word-break: normal !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    border-radius: 12px !important;
    border: 1px solid #E8E6DF !important;
    background-color: #FAFAFA !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    transition: all 0.15s ease-in-out !important;
}
.studio-grid div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    box-shadow: 0 2px 4px rgba(37,99,235,0.08) !important;
}

/* ---------- Quick Prompt Chips ---------- */
.chip-row { 
    display: flex; 
    gap: 0.6rem; 
    justify-content: center; 
    flex-wrap: wrap; 
}
.chip {
    background: #EEF3FF;
    color: #2563EB;
    border-radius: 999px;
    padding: 0.5rem 1.1rem;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
}

/* ---------- Empty State / Welcome Screen ---------- */
.welcome-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
}
.welcome-wrap .emoji { 
    font-size: 2.2rem; 
}
.welcome-wrap h2 {
    font-weight: 600;
    color: #1F2937;
    margin: 0.4rem 0 0.3rem 0;
}
.welcome-wrap p {
    color: #6B7280;
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
    line-height: 1.45;
}

/* ---------- Source Tag / Badges ---------- */
.source-tag {
    background: #EFEFEA;
    color: #4B5563;
    border-radius: 8px;
    padding: 0.4rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
    text-align: center;
}

/* ---------- Workspace & History Items ---------- */
.history-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.3rem;
    border-radius: 8px;
    font-size: 0.84rem;
    color: #374151;
    transition: background 0.12s ease;
}
.history-item:hover { 
    background: #F3F2EC; 
}
.history-time { 
    color: #9CA3AF; 
    font-size: 0.75rem; 
    margin-left: auto; 
}

/* ---------- Chat Message Wrappers ---------- */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #ECEAE4;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.6rem;
}

/* ---------- Fixed Bottom-Center Footer ---------- */
.app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(247, 246, 243, 0.94);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid #ECEAE4;
    text-align: center;
    padding: 7px 14px;
    font-size: 0.76rem;
    color: #6B7280;
    z-index: 99999;
    letter-spacing: 0.01em;
}
</style>
"""
