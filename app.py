import re
import random
import string
import streamlit as st

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

# ========== Custom Styling ==========
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4b6cb7;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        /* Custom styling for the password input field */
        .stTextInput>div>input {
            border-radius: 10px;
            height: 45px;
            font-size: 16px;
            padding: 10px;
            color: #333; /* Text color inside the input */
            background-color: #fff; /* Input background color */
            border: 1px solid #ccc; /* Border color */
        }
        /* Placeholder text styling for light theme */
        .stTextInput>div>input::placeholder {
            color: #aaa; /* Light gray placeholder text */
            opacity: 1; /* Ensure full visibility */
        }
        /* Placeholder text styling for dark theme */
        @media (prefers-color-scheme: dark) {
            .stTextInput>div>input {
                background-color: #222; /* Dark mode background */
                color: #fff; /* Text color in dark mode */
                border: 1px solid #555; /* Dark mode border */
            }
            .stTextInput>div>input::placeholder {
                color: #ddd; /* Lighter gray for better visibility in dark mode */
            }
        }
        .emoji {
            font-size: 28px;
        }
        .tip {
            color: #d9534f;
            font-weight: bold;
        }
        .success {
            color: #28a745;
            font-weight: bold;
        }
        .warning {
            color: #ffc107;
            font-weight: bold;
        }
        /* Styling for the main heading */
        .colorful-heading {
            background-color: indigo; /* Indigo background */
            color: #fff;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

    if len(password) >= 8:
        score += 1
    else:
        tips.append("🔑 Use at least 8 characters.")

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

    return score, tips

# ========== Password Generator ==========
def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# ========== UI ==========
# Colorful Main Heading
st.markdown('<div class="colorful-heading">🔐 Password Strength Meter</div>', unsafe_allow_html=True)
st.markdown("Check how strong your password is and get tips to make it better!")

# Password Input Field with Placeholder
password = st.text_input("Enter your password", type="password", placeholder="Enter your password")

if password:
    score, feedback = check_strength(password)
    
    st.subheader("🔎 Password Analysis")

    if score == 4:
        st.success("✅ **Strong Password!** Your password is secure. Great job! 🔐")
        st.markdown('<div class="emoji">💪🔒</div>', unsafe_allow_html=True)

    elif score == 3:
        st.warning("⚠️ **Moderate Password.** It's decent, but could be stronger.")
        st.markdown('<div class="emoji">😐</div>', unsafe_allow_html=True)

    else:
        st.error("❌ **Weak Password!** Improve it using the tips below.")
        st.markdown('<div class="emoji">🚫😢</div>', unsafe_allow_html=True)

    st.markdown("---")
    if feedback:
        st.markdown("### 🔧 Suggestions:")
        for tip in feedback:
            st.markdown(f"- <span class='tip'>{tip}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠 Need Help?")
    if st.button("🔁 Suggest a Strong Password"):
        new_password = generate_strong_password()
        st.success(f"Here’s a strong password: `{new_password}`")

# Footer
st.markdown("""
<hr style="border-top: 1px solid #bbb;">
<div style='text-align: center; padding-top: 10px; font-size: 13px; color: gray;'>
    Developed with ❤️ by Farah Asghar | © 2025 Password Meter Pro
</div>
""", unsafe_allow_html=True)
