"""
UI Styles for Knowledge Assistant
Features unified header widgets, matching action buttons, and responsive layout.
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

/* ---------- HEADER ROW & ALIGNMENT ---------- */
.header-wrapper {
    margin-bottom: 12px;
}

/* Pull the blue logo and title together with zero dead space */
.header-left-col div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    justify-content: flex-start !important;
}

.header-left-col div[data-testid="stColumn"]:first-child {
    flex: 0 0 42px !important;
    min-width: 42px !important;
    max-width: 42px !important;
}

.header-left-col div[data-testid="stColumn"]:last-child {
    flex: 0 1 auto !important;
}

/* ---------- MAKE ALL 4 RIGHT BUTTONS & TITLE THE EXACT SAME LEVEL & BOX SIZE ---------- */
.header-wrapper div[data-testid="stButton"] > button,
.header-wrapper div[data-testid="stPopover"] > button {
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    border-radius: 12px !important;
    border: 1px solid #ECEAE4 !important;
    background: #FFFFFF !important;
    color: #1F2937 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0 14px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin: 0 !important;
    transition: all 0.15s ease-in-out !important;
}

.header-wrapper div[data-testid="stButton"] > button:hover,
.header-wrapper div[data-testid="stPopover"] > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    background-color: #F8FAFC !important;
    box-shadow: 0 2px 6px rgba(37,99,235,0.08) !important;
}

.header-wrapper div[data-testid="stButton"] > button p,
.header-wrapper div[data-testid="stPopover"] > button p {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    margin: 0 !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}

/* Card wrappers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid #E2E0D8 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}

/* Studio action tiles */
div[data-testid="stColumn"] div[data-testid="stButton"] button {
    min-height: 60px !important;
    height: auto !important;
    padding: 6px 4px !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FAFAFA !important;
}

div[data-testid="stColumn"] div[data-testid="stButton"] button *,
div[data-testid="stColumn"] div[data-testid="stButton"] button p {
    white-space: normal !important;
    text-overflow: clip !important;
    overflow: visible !important;
    word-break: break-word !important;
    text-align: center !important;
    font-size: 0.82rem !important;
    line-height: 1.25 !important;
}

div[data-testid="stColumn"] div[data-testid="stButton"] button:hover {
    border-color: #2563EB !important;
    background-color: #EFF6FF !important;
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
    background: #F1EFE8;
}

/* Bottom natural footer */
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
