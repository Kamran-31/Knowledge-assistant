"""
UI Styles for Knowledge Assistant
Features unified 40px header widgets, untruncated colorful studio tiles,
clean rounded card containers, and a natural scrollable bottom footer.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background-color: #EEECE7;
}

/* Hide native Streamlit chrome */
header[data-testid="stHeader"] {
    display: none !important;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* ---------- UNIFIED 40PX HEADER BUTTONS & POPOVERS ---------- */
/* Applies to both standard buttons and popover trigger buttons in the header row */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button,
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPopover"] > button {
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    margin: 0 !important;
    width: 100% !important;
    transition: all 0.15s ease-in-out !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover,
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPopover"] > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    background-color: #F8FAFC !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.08) !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button p,
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPopover"] > button p {
    margin: 0 !important;
    line-height: 1 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
}

/* ---------- CARD CONTAINERS ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid #E2E0D8 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}

/* Section Headings */
h3, h4, [data-testid="stHeading"] {
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #0F172A !important;
}

/* ---------- STUDIO ACTION BUTTONS ---------- */
div[data-testid="stColumn"] div[data-testid="stButton"] button {
    min-height: 62px !important;
    height: auto !important;
    padding: 6px 4px !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FAFAFA !important;
    transition: all 0.15s ease-in-out !important;
}

/* Remove text truncation and allow multi-line labels */
div[data-testid="stColumn"] div[data-testid="stButton"] button,
div[data-testid="stColumn"] div[data-testid="stButton"] button *,
div[data-testid="stColumn"] div[data-testid="stButton"] button p,
div[data-testid="stColumn"] div[data-testid="stButton"] button span {
    white-space: pre-line !important;
    text-overflow: clip !important;
    overflow: visible !important;
    word-break: break-word !important;
    text-align: center !important;
    font-size: 0.82rem !important;
    line-height: 1.25 !important;
    color: #1F2937 !important;
}

div[data-testid="stColumn"] div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(37, 99, 235, 0.08) !important;
}

/* ---------- CHAT MESSAGES ---------- */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    border: 1px solid #ECEAE4 !important;
    padding: 0.6rem 0.8rem !important;
    margin-bottom: 0.6rem !important;
}

/* User Message Variation */
[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
}

/* ---------- SESSION HISTORY ITEMS ---------- */
.history-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.45rem 0.4rem;
    border-radius: 8px;
    font-size: 0.84rem;
    color: #374151;
    transition: background 0.12s ease;
}

.history-item:hover {
    background: #F1EFE8;
}

/* ---------- NATURAL BOTTOM FOOTER ---------- */
.app-footer {
    position: relative !important;
    display: block !important;
    width: 100%;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    padding-bottom: 0.8rem;
    border-top: 1px solid #DCD9CF;
    text-align: center;
    font-size: 0.76rem;
    color: #64748B;
    letter-spacing: 0.01em;
}
</style>
"""
