import re
import random
import string
import streamlit as st

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Password Strength Meter", 
    page_icon="🔐", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== RESPONSIVE THEME STYLING ==========
st.markdown("""
<style>
    /* Theme variables - Light theme (default) */
    :root {
        --bg-color: #f5f7fa;
        --card-bg: #ffffff;
        --text-color: #2d3748;
        --border-color: #e2e8f0;
        --primary: #4b6cb7;
        --heading-bg: #4b6cb7;
        --footer-bg: #2d3748;
        --input-bg: #ffffff;
        --input-border: #cbd5e0;
        --placeholder-color: #a0aec0;
    }

    /* Dark theme overrides */
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 {
        --bg-color: #1a202c;
        --card-bg: #2d3748;
        --text-color: #f7fafc;
        --border-color: #4a5568;
        --primary: #6c8bda;
        --heading-bg: #2d3748;
        --footer-bg: #1a202c;
        --input-bg: #2d3748;
        --input-border: #4a5568;
        --placeholder-color: #a0aec0;
    }
    
    /* Apply theme colors to container */
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
    
    .main {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Header styling */
    .header {
        background: var(--heading-bg);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Password input styling */
    .stTextInput>div>div>input {
        background-color: var(--input-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--placeholder-color);
    }
    
    /* Hide duplicate label */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }

    /* Basic text styling */
    .stMarkdown p {
        color: var(--text-color) !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    
    .stButton button:hover {
        opacity: 0.9;
    }

    /* Footer styling */
    .footer {
        background: var(--footer-bg);
        color: white;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Results card */
    .results-card {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Warning/Error styling - let Streamlit handle these */
    
    /* Eye button */
    .eye-button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 0.3rem;
        padding: 0.5rem 1rem;
        cursor: pointer;
        text-align: center;
        font-size: 1.2rem;
    }
    
    /* Code block styling */
    pre {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
        border-radius: 0.25rem;
    }
    
    /* Light/Dark mode detection */
    .light-theme-text { color: #2d3748 !important; }
    .dark-theme-text { color: #f7fafc !important; }
    
    /* Ensure all text is properly visible */
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 p,
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 h1,
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 h2,
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 h3,
    [data-testid="stAppViewContainer"].st-emotion-cache-1wrcr25 li {
        color: #f7fafc !important;
    }
    
    /* Default (light) text colors */
    p, h1, h2, h3, li {
        color: #2d3748 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== PASSWORD LOGIC ==========
def check_strength(password):
    score = 0
    tips = []
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("Use at least 12 characters")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("Mix uppercase and lowercase")
    
    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("Add numbers")
    
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        tips.append("Add special characters")
    
    return score, tips

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(16))

# ========== UI COMPONENTS ==========
def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>🔐 Password Strength Meter</h1>
        <p>Check how strong your password is and get tips to make it better!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Password input
    st.markdown("<p><strong>Enter your password</strong></p>", unsafe_allow_html=True)
    
    # Create a container for the password input and visibility toggle
    col1, col2 = st.columns([6, 1])
    
    with col1:
        password = st.text_input(
            "",  # Empty label since we're showing our own
            type="password" if not st.session_state.get('pwd_visible', False) else "default",
            placeholder="Type your password here...",
            key="pwd_input"
        )
    
    with col2:
        if st.button("👁️"):
            st.session_state.pwd_visible = not st.session_state.get('pwd_visible', False)
    
    # Results
    if password:
        score, tips = check_strength(password)
        
        with st.container():
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            
            if score >= 4:
                st.success("✅ Strong password!")
            elif score >= 2:
                st.warning("⚠️ Moderate password")
            else:
                st.error("❌ Weak password")
            
            if tips:
                st.markdown("<p><strong>Improve your password:</strong></p>", unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f"- {tip}")
            
            if st.button("Generate Strong Password"):
                new_pwd = generate_password()
                st.code(new_pwd)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed with ❤️ by Farah Asghar | © 2025 Password Meter Pro | v2.0
    </div>
    """, unsafe_allow_html=True)

# Initialize session state for password visibility
if 'pwd_visible' not in st.session_state:
    st.session_state.pwd_visible = False

if __name__ == "__main__":
    main()
