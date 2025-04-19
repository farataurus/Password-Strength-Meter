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

# ========== THEME-COMPATIBLE STYLING ==========
st.markdown("""
<style>
    /* Let Streamlit handle the base background colors */
    .main {
        background-color: transparent !important;
    }
    
    /* Header styling */
    .header {
        background: #4b6cb7;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style text based on theme */
    .streamlit-dark {
        color: #f7fafc !important;
    }
    
    .streamlit-light {
        color: #2d3748 !important;
    }
    
    /* Input styles that work in both themes */
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    
    /* Hide duplicate label */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    
    /* Button hover effect */
    .stButton button:hover {
        opacity: 0.9;
    }

    /* Footer styling */
    .footer {
        background: #2d3748;
        color: white;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Results card - styled based on theme */
    .results-card {
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Light theme card */
    .light-card {
        background-color: white;
        border: 1px solid #e2e8f0;
        color: #2d3748;
    }
    
    /* Dark theme card */
    .dark-card {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        color: #f7fafc;
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

# ========== THEME DETECTION ==========
def get_theme():
    # Check if we're in streamlit lite
    try:
        if st._is_running_with_streamlit:
            # Use session state to remember theme
            if 'theme' not in st.session_state:
                st.session_state.theme = 'light'  # Default
            return st.session_state.theme
    except:
        pass
    
    # Default to light theme
    return 'light'

# ========== UI COMPONENTS ==========
def main():
    # Detect current theme for styling
    theme = get_theme()
    card_class = "light-card" if theme == "light" else "dark-card"
    text_class = "streamlit-light" if theme == "light" else "streamlit-dark"
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🔐 Password Strength Meter</h1>
        <p>Check how strong your password is and get tips to make it better!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle (for testing)
    col_theme, _ = st.columns([2, 8])
    with col_theme:
        if st.button("Toggle Theme (Dev)"):
            st.session_state.theme = "dark" if theme == "light" else "light"
            st.rerun()
    
    # Password input
    st.markdown(f'<p class="{text_class}"><strong>Enter your password</strong></p>', unsafe_allow_html=True)
    
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
            st.markdown(f'<div class="results-card {card_class}">', unsafe_allow_html=True)
            
            if score >= 4:
                st.success("✅ Strong password!")
            elif score >= 2:
                st.warning("⚠️ Moderate password")
            else:
                st.error("❌ Weak password")
            
            if tips:
                st.markdown(f'<p class="{text_class}"><strong>Improve your password:</strong></p>', unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<p class="{text_class}">- {tip}</p>', unsafe_allow_html=True)
            
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
