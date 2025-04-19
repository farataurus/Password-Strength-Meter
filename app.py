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

# ========== Perfect Theme-Compatible Styling ==========
st.markdown("""
<style>
    /* Base styles that work with both themes */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-color);
    }
    
    .main {
        background-color: transparent !important;
        padding: 0 1rem;
    }

    /* Theme variables */
    :root {
        --bg-color: #f5f7fa;
        --card-bg: #ffffff;
        --text-color: #2d3748;
        --border-color: #e2e8f0;
        --primary: #4b6cb7;
        --secondary: #6c8bda;
        --heading-bg: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        --footer-bg: linear-gradient(135deg, #2c3e50 0%, #4b6cb7 100%);
        --input-bg: #ffffff;
        --input-text: #2d3748;
        --input-border: #cbd5e0;
        --input-placeholder: #a0aec0;
        --divider-color: #e2e8f0;
    }

    /* Dark theme overrides */
    [data-theme="dark"] {
        --bg-color: #1a202c;
        --card-bg: #2d3748;
        --text-color: #f7fafc;
        --border-color: #4a5568;
        --primary: #6c8bda;
        --secondary: #8a9ff1;
        --heading-bg: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        --footer-bg: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        --input-bg: #2d3748;
        --input-text: #f7fafc;
        --input-border: #4a5568;
        --input-placeholder: #a0aec0;
        --divider-color: #4a5568;
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
    
    .header h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* Input field styling */
    .stTextInput>div>div>input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 0.5rem;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--input-placeholder) !important;
        opacity: 1 !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(75, 108, 183, 0.2) !important;
    }

    /* Button styling */
    .stButton>button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background: var(--secondary) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }

    /* Results card */
    .results-card {
        background-color: var(--card-bg);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
    }

    /* Feedback styling */
    .strength-feedback {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .strength-strong {
        color: #48bb78;
    }
    
    .strength-medium {
        color: #ed8936;
    }
    
    .strength-weak {
        color: #f56565;
    }
    
    .suggestion-item {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Divider */
    .divider {
        border-top: 1px solid var(--divider-color);
        margin: 1.5rem 0;
    }

    /* Footer */
    .footer {
        background: var(--footer-bg);
        color: white !important;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 0 0 0.5rem 0.5rem;
        font-size: 0.875rem;
    }
    
    /* Emoji styling */
    .emoji-feedback {
        font-size: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== Password Logic ==========
common_passwords = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]

def check_strength(password):
    tips = []
    score = 0
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("Use at least 12 characters (8 minimum)")
    
    # Complexity checks
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("Include both uppercase and lowercase letters")
    
    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("Add at least one number")
    
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        tips.append("Add special characters (!@#$% etc.)")
    
    # Blacklist check
    if password.lower() in common_passwords:
        score = 0
        tips = ["This password is too common - choose something more unique"]
    
    return min(5, score), tips

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# ========== UI Components ==========
def show_header():
    st.markdown("""
    <div class="header">
        <h1>🔐 Password Strength Meter</h1>
        <p>Check how strong your password is and get tips to make it better!</p>
    </div>
    """, unsafe_allow_html=True)

def show_password_input():
    password = st.text_input(
        "Enter your password", 
        type="password", 
        placeholder="Type your password here...",
        key="pwd_input"
    )
    return password

def show_results(score, tips):
    with st.container():
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        
        if score >= 4:
            st.markdown(
                f'<div class="strength-feedback strength-strong">'
                f'✅ Strong Password! (Score: {score}/5)</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji-feedback">🔒💪</div>', unsafe_allow_html=True)
        elif score >= 2:
            st.markdown(
                f'<div class="strength-feedback strength-medium">'
                f'⚠️ Moderate Password (Score: {score}/5)</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji-feedback">😐</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="strength-feedback strength-weak">'
                f'❌ Weak Password (Score: {score}/5)</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji-feedback">🚨</div>', unsafe_allow_html=True)
        
        if tips:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("**🔧 Suggestions to improve:**")
            for tip in tips:
                st.markdown(f'<div class="suggestion-item">🔹 {tip}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**🛠 Need a strong password?**")
        if st.button("Generate Secure Password", key="generate_btn"):
            new_pwd = generate_password()
            st.success(f"Generated password: `{new_pwd}`")
            st.info("Remember to store this securely!")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_footer():
    st.markdown("""
    <div class="footer">
        Developed with ❤️ by Farah Asghar | © 2025 Password Meter Pro | v2.0
    </div>
    """, unsafe_allow_html=True)

# ========== Main App ==========
def main():
    show_header()
    
    password = show_password_input()
    
    if password:
        score, tips = check_strength(password)
        show_results(score, tips)
    
    show_footer()

if __name__ == "__main__":
    main()
