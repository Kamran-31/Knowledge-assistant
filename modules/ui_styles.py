"""
UI Styles for Knowledge Assistant
Contains custom CSS for cards, header, studio buttons, and the fixed footer.
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

/* Hide default Streamlit chrome */
#MainMenu, footer {
    visibility: hidden;
}

/* Prevents bottom content from being hidden behind the sticky footer */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4.5rem !important;
    max-width: 100% !important;
}

/* ---------- Top Header ---------- */
.notebook-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1rem;
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #ECEAE4;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.notebook-header .brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 600;
    font-size: 1.05rem;
    color: #1F2937;
}

/* ---------- Container Cards ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 16px !important;
    border: 1px solid #ECEAE4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

/* ---------- Standard Action Buttons ---------- */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid #E4E1D8 !important;
    background: #FFFFFF;
    color: #1F2937;
    font-weight: 500;
    padding: 0.45rem 1rem;
    transition: all 0.15s ease;
}

div.stButton > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    background: #F5F8FF !important;
}

/* ---------- Studio Grid Action Buttons (Full Visibility) ---------- */
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
    border-radius: 10px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #F9FAFB !important;
    transition: all 0.15s ease-in-out !important;
}

.studio-grid div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    box-shadow: 0 2px 4px rgba(37,99,235,0.08) !important;
}

/* ---------- Chat Messages ---------- */
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
