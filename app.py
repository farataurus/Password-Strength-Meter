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

# ========== Enhanced Custom Styling ==========
st.markdown("""
<style>
    /* Global styles that adapt to theme */
    [data-testid="stAppViewContainer"] {
        background: var(--background-color);
    }
    
    /* Main container styling */
    .main {
        background-color: transparent !important;
    }

    /* Color variables for themes */
    :root {
        --primary-color: #4b6cb7;
        --secondary-color: #6c8bda;
        --background-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #333333;
        --border-color: #cccccc;
        --placeholder-color: #aaaaaa;
        --heading-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --footer-bg: linear-gradient(135deg, #2c3e50 0%, #4b6cb7 100%);
    }

    /* Dark theme overrides */
    [data-theme="dark"] {
        --primary-color: #6c8bda;
        --secondary-color: #8a9ff1;
        --background-color: #1e1e1e;
        --card-bg: #2d2d2d;
        --text-color: #f0f2f6;
        --border-color: #555555;
        --placeholder-color: #bbbbbb;
        --heading-bg: linear-gradient(135deg, #434343 0%, #000000 100%);
        --footer-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Button styling */
    .stButton>button {
        background: var(--primary-color);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        height: 45px;
        font-size: 16px;
        padding: 10px;
        color: var(--text-color);
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
    }

    /* Placeholder text styling */
    .stTextInput>div>div>input::placeholder {
        color: var(--placeholder-color);
        opacity: 1;
    }

    /* Card styling */
    .card {
        background-color: var(--card-bg);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Styling for the main heading */
    .colorful-heading {
        background: var(--heading-bg);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Emoji styling */
    .emoji {
        font-size: 28px;
        text-align: center;
        margin: 10px 0;
    }
    
    /* Feedback styling */
    .tip {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    .success {
        color: #51cf66;
        font-weight: bold;
    }
    
    .warning {
        color: #fcc419;
        font-weight: bold;
    }
    
    .error {
        color: #ff6b6b;
        font-weight: bold;
    }

    /* Footer styling */
    .footer {
        background: var(--footer-bg);
        color: white !important;
        text-align: center;
        padding: 15px;
        border-radius: 0 0 10px 10px;
        margin-top: 30px;
        font-size: 14px;
    }
    
    /* Divider styling */
    .divider {
        border-top: 1px solid var(--border-color);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== Blacklist ==========
common_passwords = ["password123", "123456", "qwerty", "letmein", "admin", "welcome", "iloveyou", "password"]

# ========== Password Strength Checker ==========
def check_strength(password):
    tips = []
    score = 0

    if password.lower() in common_passwords:
        return 0, ["❌ This password is too common! Pick something more unique."]

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("🔑 Use at least 12 characters (8 minimum).")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("🔡 Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("🔢 Add at least one number.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        tips.append("💥 Add special characters (!@#$%^&*).")

    # Additional checks
    if len(password) >= 16:
        score += 1
    if re.search(r"(.)\1\1", password):
        tips.append("🔄 Avoid repeating characters multiple times in a row.")
        score = max(0, score-1)

    return min(5, score), tips  # Cap score at 5

# ========== Password Generator ==========
def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        score, _ = check_strength(password)
        if score >= 4:  # Only return strong passwords
            return password

# ========== UI ==========
# Colorful Main Heading
st.markdown(
    '<div class="colorful-heading">🔐 Password Strength Meter</div>', 
    unsafe_allow_html=True
)
st.markdown(
    "Check how strong your password is and get tips to make it better!", 
    unsafe_allow_html=True
)

# Password Input Field with Placeholder
password = st.text_input(
    "Enter your password", 
    type="password", 
    placeholder="Type your password here...",
    key="password_input"
)

if password:
    score, feedback = check_strength(password)
    
    with st.container():
        st.subheader("🔎 Password Analysis")
        
        if score >= 4:
            st.markdown(
                f'<div class="success">✅ <strong>Strong Password!</strong> '
                f'Score: {score}/5 - Your password is secure. Great job! 🔐</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji">💪🔒</div>', unsafe_allow_html=True)
        elif score >= 2:
            st.markdown(
                f'<div class="warning">⚠️ <strong>Moderate Password.</strong> '
                f'Score: {score}/5 - It\'s decent, but could be stronger.</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji">😐</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="error">❌ <strong>Weak Password!</strong> '
                f'Score: {score}/5 - Improve it using the tips below.</div>',
                unsafe_allow_html=True
            )
            st.markdown('<div class="emoji">🚫😢</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        if feedback:
            st.markdown("### 🔧 Suggestions:")
            for tip in feedback:
                st.markdown(f"- <span class='tip'>{tip}</span>", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 🛠 Need Help?")
        if st.button("🔁 Generate Strong Password", key="generate_btn"):
            new_password = generate_strong_password()
            st.success(f"Here's a strong password: `{new_password}`")
            st.info("🔒 Remember to store this password securely!")

# Footer
st.markdown("""
<div class="footer">
    Developed with ❤️ by Farah Asghar | © 2025 Password Meter Pro | v2.0
</div>
""", unsafe_allow_html=True)
