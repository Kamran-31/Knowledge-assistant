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

/* Main container spacing to prevent bottom content from hiding behind sticky footer */
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

/* Header & action pill buttons */
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

/* Studio Panel Buttons (Third column grid) */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] button {
    min-height: 68px !important;
    height: auto !important;
    padding: 10px 8px !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FAFAFA !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    transition: all 0.15s ease-in-out !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(37,99,235,0.08) !important;
}

/* Studio Button Inner Text: Large Emoji, no truncation, word wrap */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] button p {
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    white-space: pre-line !important;
    text-overflow: clip !important;
    overflow: visible !important;
    word-break: break-word !important;
    text-align: center !important;
    margin: 0 !important;
}

/* Chat bubble styling */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #ECEAE4;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.6rem;
}

/* History item row */
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

/* Fixed bottom-centered footer */
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
