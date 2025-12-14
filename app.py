import streamlit as st
import os
import zipfile
import shutil
from pipreqs import pipreqs
import time

# --- CONFIGURATION (EDIT THIS LATER) ---
# 1. Go to Stripe -> Create a "Payment Link" for $5.
# 2. Set the "After payment" message in Stripe to: "Thanks! Your License Key is: PY-PRO-2025"
STRIPE_LINK = "https://buy.stripe.com/test_..." # Replace with your real link
SECRET_KEY = "PY-PRO-2025"  # The code you give them after paying

# --- PAGE SETUP & CUSTOM CSS ---
st.set_page_config(page_title="AutoReqs Pro", page_icon="⚡", layout="centered")

# --- PROFESSIONAL 'VERCEL-STYLE' CSS ---
st.markdown("""
    <style>
    /* Main Background - Dark Grey/Black for contrast */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* The Header */
    .main-header {
        background: linear-gradient(180deg, #fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #eaeaea;
        transform: translateY(-1px);
    }
    
    /* The Success Box */
    .success-box {
        background: #111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #111;
        color: white;
        border: 1px solid #333;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
# --- HEADER ---
st.markdown('<div class="main-header">⚡ AutoReqs Pro</div>', unsafe_allow_html=True)
st.markdown("### The Instant `requirements.txt` Generator for Professionals.")
st.markdown("---")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📂 Drop your Python project (.zip) here", type="zip")

if uploaded_file is not None:
    # 1. Processing Animation (Adds perceived value)
    with st.spinner('🚀 Analyzing dependency tree...'):
        time.sleep(1.5) # Fake delay to make it feel "powerful"
        
        extract_path = "temp_workspace"
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        os.makedirs(extract_path)

        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        try:
            # Run pipreqs
            imports = pipreqs.get_all_imports(extract_path)
            import_info = pipreqs.get_imports_info(imports)
            
            reqs_content = ""
            for item in import_info:
                reqs_content += f"{item['name']}=={item['version']}\n"
            
            # --- SUCCESS STATE ---
            st.markdown(f"""
            <div class="success-box">
                <b>✅ Analysis Complete!</b><br>
                We found <b>{len(import_info)}</b> libraries in your project.
            </div>
            """, unsafe_allow_html=True)

            # --- THE PAYWALL ---
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🔒 Preview Locked")
                # Show blurred preview or just first 2 lines
                preview = "\n".join(reqs_content.split("\n")[:3]) + "\n... [LOCKED]"
                st.code(preview, language="text")
                
                st.markdown(f"""
                <a href="{STRIPE_LINK}" target="_blank">
                    <button style="
                        background-color: #00C9FF; 
                        color: black; 
                        padding: 10px 20px; 
                        border: none; 
                        border-radius: 5px; 
                        font-weight: bold; 
                        cursor: pointer; 
                        width: 100%;">
                        💳 Buy License Key ($5)
                    </button>
                </a>
                """, unsafe_allow_html=True)

            with col2:
                st.write("### 🔓 Unlock Download")
                license_input = st.text_input("Enter License Key:", type="password")
                
                if license_input == SECRET_KEY:
                    st.success("Access Granted!")
                    st.download_button(
                        label="⬇️ Download requirements.txt",
                        data=reqs_content,
                        file_name="requirements.txt",
                        mime="text/plain"
                    )
                elif license_input:
                    st.error("Invalid Key. Please purchase access.")

        except Exception as e:
            st.error(f"Error parsing project: {e}")