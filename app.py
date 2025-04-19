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

# ========== PERFECT DARK/LIGHT THEME STYLING ==========
st.markdown("""
<style>
    /* Base styles */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-color);
        color: var(--text-color);
    }
    
    .main {
        background-color: transparent !important;
        color: var(--text-color);
    }

    /* Theme variables - Light mode default */
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

    /* Dark mode styles */
    [data-testid="stAppViewContainer"][data-theme="dark"],
    [data-testid="stAppViewContainer"] [data-theme="dark"] {
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
    
    /* Explicit dark mode overrides */
    .dark-mode {
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
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background: var(--input-bg) !important;
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

    /* Footer styling */
    .footer {
        background: var(--footer-bg);
        color: white;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 0.5rem;
    }
    
    /* Results card */
    .results-card {
        background: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Fix text colors in dark mode */
    [data-theme="dark"] p, 
    [data-theme="dark"] h1, 
    [data-theme="dark"] h2, 
    [data-theme="dark"] h3, 
    [data-theme="dark"] li, 
    [data-theme="dark"] span,
    [data-theme="dark"] .stMarkdown {
        color: var(--text-color) !important;
    }
    
    /* Fix code display in dark mode */
    [data-theme="dark"] code {
        background-color: #1e2734 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568;
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
    
    # Password input - SINGLE LABEL
    st.markdown('<p class="dark-mode"><strong>Enter your password</strong></p>', unsafe_allow_html=True)
    password = st.text_input(
        "",  # Empty label since we're showing our own
        type="password",
        placeholder="Type your password here...",
        key="pwd_input"
    )
    
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
                st.markdown('<p class="dark-mode"><strong>Improve your password:</strong></p>', unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<p class="dark-mode">- {tip}</p>', unsafe_allow_html=True)
            
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

if __name__ == "__main__":
    main()
