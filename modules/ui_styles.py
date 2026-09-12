"""
UI Styles for Knowledge Assistant
Features Plus Jakarta Sans typography, vibrant studio tile accents,
and modern soft-depth surface cards.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Base canvas background */
.stApp {
    background-color: #EEECE7;
}

header[data-testid="stHeader"] {
    display: none !important;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.6rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* ---------- Vibrant Header Card ---------- */
.notebook-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    margin-bottom: 0.75rem;
}

.notebook-header .brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 700;
    font-size: 1.1rem;
    color: #0F172A;
    letter-spacing: -0.02em;
}

.notebook-header .brand .logo-dot {
    width: 28px;
    height: 28px;
    border-radius: 9px;
    background: linear-gradient(135deg, #6366F1 0%, #3B82F6 50%, #06B6D4 100%);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
}

.pro-badge {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    color: #FFFFFF !important;
    font-size: 0.65rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 999px;
    letter-spacing: 0.06em;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);
}

/* ---------- Rounded Border Cards ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 20px !important;
    border: 1px solid #E2E0D8 !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(0,0,0,0.02) !important;
    transition: box-shadow 0.2s ease;
}

/* Section Headings */
h3, h4, [data-testid="stHeading"] {
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #0F172A !important;
}

/* ---------- Top Pill Action Buttons ---------- */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid #DCD9CF !important;
    background: #FFFFFF !important;
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.1rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
    transition: all 0.18s ease-in-out !important;
}

div.stButton > button:hover {
    border-color: #6366F1 !important;
    color: #4F46E5 !important;
    background: #EEF2FF !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    transform: translateY(-1px);
}

/* ---------- Colorful Studio Grid Action Buttons ---------- */
div[data-testid="stColumn"] div[data-testid="stButton"] button {
    min-height: 64px !important;
    height: auto !important;
    padding: 8px 6px !important;
    border-radius: 14px !important;
    border: 1px solid #E5E7EB !important;
    background: #FAFAFB !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* Remove Ellipsis & Enhance Typography */
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
    font-weight: 600 !important;
    line-height: 1.3 !important;
    color: #1E293B !important;
}

/* Lift on hover */
div[data-testid="stColumn"] div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08) !important;
}

/* Custom Accent Colors for Studio Tools */
button[key*="Audio"] { border-color: #DDD6FE !important; background: linear-gradient(180deg, #FFFFFF 0%, #F5F3FF 100%) !important; }
button[key*="Audio"]:hover { border-color: #8B5CF6 !important; background: #EDE9FE !important; }

button[key*="Slide"] { border-color: #BAE6FD !important; background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%) !important; }
button[key*="Slide"]:hover { border-color: #0284C7 !important; background: #E0F2FE !important; }

button[key*="Video"] { border-color: #FED7AA !important; background: linear-gradient(180deg, #FFFFFF 0%, #FFF7ED 100%) !important; }
button[key*="Video"]:hover { border-color: #EA580C !important; background: #FFEDD5 !important; }

button[key*="Mind"] { border-color: #FBCFE8 !important; background: linear-gradient(180deg, #FFFFFF 0%, #FDF2F8 100%) !important; }
button[key*="Mind"]:hover { border-color: #DB2777 !important; background: #FCE7F3 !important; }

button[key*="Reports"] { border-color: #C7D2FE !important; background: linear-gradient(180deg, #FFFFFF 0%, #EEF2FF 100%) !important; }
button[key*="Reports"]:hover { border-color: #4F46E5 !important; background: #E0E7FF !important; }

button[key*="Flashcards"] { border-color: #FEF08A !important; background: linear-gradient(180deg, #FFFFFF 0%, #FEFCE8 100%) !important; }
button[key*="Flashcards"]:hover { border-color: #CA8A04 !important; background: #FEF9C3 !important; }

button[key*="Quiz"] { border-color: #FECDD3 !important; background: linear-gradient(180deg, #FFFFFF 0%, #FFF1F2 100%) !important; }
button[key*="Quiz"]:hover { border-color: #E11D48 !important; background: #FFE4E6 !important; }

button[key*="Infographic"] { border-color: #A7F3D0 !important; background: linear-gradient(180deg, #FFFFFF 0%, #ECFDF5 100%) !important; }
button[key*="Infographic"]:hover { border-color: #059669 !important; background: #D1FAE5 !important; }

button[key*="Data"] { border-color: #E2E8F0 !important; background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%) !important; }
button[key*="Data"]:hover { border-color: #475569 !important; background: #E2E8F0 !important; }

/* ---------- Chat Messages ---------- */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid #E8E6DE !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
}

/* User vs Assistant distinction */
[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
}

/* ---------- History Items ---------- */
.history-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0.6rem;
    border-radius: 10px;
    font-size: 0.85rem;
    color: #334155;
    font-weight: 500;
    transition: all 0.15s ease;
}

.history-item:hover {
    background: #F1EFE8;
    color: #0F172A;
}

/* ---------- Bottom Footer ---------- */
.app-footer {
    position: relative !important;
    display: block !important;
    width: 100%;
    margin-top: 2.5rem;
    padding-top: 1.5rem;
    padding-bottom: 0.8rem;
    border-top: 1px solid #DCD9CF;
    text-align: center;
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748B;
    letter-spacing: 0.01em;
}
</style>
"""
