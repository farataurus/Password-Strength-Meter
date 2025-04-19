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

# ========== DARK/LIGHT THEME STYLING ==========
st.markdown("""
<style>
    /* Force dark mode throughout the app */
    [data-testid="stAppViewContainer"], 
    .main,
    .stTextInput, 
    .stButton,
    .stMarkdown,
    .st-emotion-cache-1kyxreq,
    .st-emotion-cache-16txtl3,
    .st-emotion-cache-eczf16,
    .st-emotion-cache-18ni7ap {
        background-color: #1a202c !important;
        color: #f7fafc !important;
    }
    
    /* Style the header */
    .header {
        background: #2d3748;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Password input styling */
    .stTextInput>div>div>input {
        background-color: #2d3748 !important;
        color: white !important;
        border: 1px solid #4a5568 !important;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #a0aec0;
    }
    
    /* Hide duplicate label */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }

    /* Button styling */
    .stButton button {
        background-color: #4b6cb7 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #6c8bda !important;
    }

    /* Footer styling */
    .footer {
        background: #2d3748;
        color: white;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Results card */
    .results-card {
        background-color: #2d3748 !important;
        color: white !important;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #4a5568;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Warning/Error styling */
    .st-emotion-cache-1erivf3 {
        background-color: #2d3e4f !important;
        color: white !important;
    }
    
    /* Code block styling */
    pre {
        background-color: #2d3748 !important;
        color: #63b3ed !important;
        border: 1px solid #4a5568 !important;
        border-radius: 0.25rem;
    }
    
    code {
        color: #63b3ed !important;
    }
    
    /* Make all text white */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: white !important;
    }
    
    /* Fix sidebar */
    [data-testid="stSidebar"] {
        background-color: #2d3748 !important;
        border-right: 1px solid #4a5568;
    }
    
    /* Fix expandables */
    .streamlit-expanderHeader {
        background-color: #2d3748 !important;
        color: white !important;
    }
    
    /* Fix toggle visibility button */
    button[data-baseweb="button"] {
        background-color: #2d3748 !important;
        color: white !important;
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
            type="password",
            placeholder="Type your password here...",
            key="pwd_input"
        )
    
    with col2:
        if st.button("👁️"):
            st.session_state.pwd_visible = not st.session_state.get('pwd_visible', False)
    
    # Show password if visibility toggled
    if st.session_state.get('pwd_visible', False) and password:
        st.code(password)
    
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
