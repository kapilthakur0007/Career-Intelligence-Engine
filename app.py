import streamlit as st
import requests
import time
import sqlite3
import hashlib
import random
import json

# ==========================================
# 1. CORE CONFIG & DATABASE 
# ==========================================
st.set_page_config(page_title="Universal Career Intelligence", layout="wide", page_icon="🌐", initial_sidebar_state="auto")

def init_db():
    conn = sqlite3.connect('secure_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS active_session (name TEXT, expiry REAL)''')
    conn.commit()
    conn.close()

def hash_password(password): return hashlib.sha256(str.encode(password)).hexdigest()

def verify_user(email, password):
    conn = sqlite3.connect('secure_users.db')
    c = conn.cursor()
    c.execute('SELECT name FROM users WHERE email=? AND password=?', (email, hash_password(password)))
    data = c.fetchone()
    conn.close()
    return data

def add_user(name, email, password):
    try:
        conn = sqlite3.connect('secure_users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, password) VALUES (?,?,?)', (name, email, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_active_session():
    conn = sqlite3.connect('secure_users.db')
    c = conn.cursor()
    c.execute('SELECT name, expiry FROM active_session LIMIT 1')
    data = c.fetchone()
    conn.close()
    if data and time.time() < data[1]: return data[0]
    return None

def create_active_session(name):
    conn = sqlite3.connect('secure_users.db')
    c = conn.cursor()
    c.execute('DELETE FROM active_session')  
    c.execute('INSERT INTO active_session (name, expiry) VALUES (?, ?)', (name, time.time() + 172800))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 2. 19-KEY POOL
# ==========================================
KEYS = [
    "AIzaSyDwTAitmjM_WPoRL_UPagAU906_5G5li4w", "AIzaSyCkYu3tUEBjn9rsBUhCuA0lFvnFTnRSCdQ", 
    "AIzaSyDqyy4z2kytjG-iZG9ijZScD-Cm_3X5mvE", "AIzaSyAQmHkob4iCRGhzD1f7dBWudhR6731WeGg", 
    "AIzaSyBLqF3NJH9jWiEl5Dc0-SHMKxWuodonlj4", "AIzaSyA_dv1YVLZcLsFs5KzNxDS_ZErLu9SSDcc", 
    "AIzaSyCpzL2y1shSIwHRtv5QHo1mZYdCZM0iiLI", "AIzaSyA72EDEFwXsHfMsw8EDINhpw6DYwfAwdRc", 
    "AIzaSyCvJYzlm_bGf5IAw6-odyxdN34D_6Dj8kY", "AIzaSyCVT7xB3tyeuhu0J5ocj5v6-MVUhj6SGU0", 
    "AIzaSyD8dfqIRSKgXnYKIGCO43c6cBdp1xpIuns", "AIzaSyAHbQ45JQkk5MFVscaJYny3Nsjqqxq4Ck4", 
    "AIzaSyCfnEqVFh9SmBBUR_A30TRN4gyw-Tuv0tg", "AIzaSyBr2aOXjLFxOeiCNReginSRWq1o9j_MTnM", 
    "AIzaSyDIUk3CZ0RAdS1Fb-M5uO-DZkoAtsCpiT0", "AIzaSyAN-iaAMwtqXM0X_zKMTaZm-cclVBErbz4", 
    "AIzaSyAXbsnkvb29c1QlJf_L6306VAV7GWM_DDQ", "AIzaSyC26OTVrzQzeMvr0j2Uv-eCKkIz8MWYh6U", 
    "AIzaSyBlVfYM21u6pApT8s1eL5tRjOJYnbcPWrg"
]

# ==========================================
# RESPONSIVE CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    .main { background: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Desktop Styles */
    .auth-container { background: rgba(30, 41, 59, 0.9); padding: 40px; border-radius: 15px; border-top: 4px solid #0ea5e9; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
    .welcome-text { font-size: 2.8rem; font-weight: 900; color: #f1f5f9; margin-bottom: 10px; line-height: 1.2;}
    .highlight { color: #0ea5e9; }
    .sub-text { font-size: 1.1rem; color: #94a3b8; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 15px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: #1e293b; border-radius: 8px; color: #94a3b8; padding: 0 20px; font-weight: 700; font-size: 14px; }
    .stTabs [aria-selected="true"] { background: #0ea5e9; color: #020617; box-shadow: 0 0 15px rgba(14, 165, 233, 0.4); }
    .bullet-point { margin-bottom: 15px; padding: 18px; background: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 4px solid #38bdf8; display: block; line-height: 1.7; font-size: 16px; transition: 0.3s; }
    .bullet-point:hover { background: rgba(56, 189, 248, 0.1); transform: translateX(8px); }
    .roadmap-card { padding: 15px; background: rgba(16, 185, 129, 0.05); border-radius: 10px; border-left: 4px solid #10b981; margin-bottom: 12px; font-size: 16px; color: #f1f5f9; }
    .section-header { color: #38bdf8; font-size: 26px; font-weight: 900; margin: 30px 0 20px 0; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
    
    /* PREMIUM BANNER STYLES */
    .premium-banner {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(139, 92, 246, 0.15));
        border: 1px solid rgba(14, 165, 233, 0.4);
        padding: 22px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.15);
        position: relative;
        overflow: hidden;
    }
    .premium-banner::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    @keyframes shine { 100% { left: 200%; } }
    .banner-text { color: #0ea5e9; font-size: 1.4rem; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; text-shadow: 0 0 10px rgba(14,165,233,0.3); }
    .banner-sub { color: #94a3b8; font-size: 0.95rem; margin-top: 5px; font-weight: 500; }

    /* MOBILE RESPONSIVE STYLES (iOS & Android) */
    @media (max-width: 768px) {
        .auth-container { padding: 20px; }
        .welcome-text { font-size: 2rem; }
        .sub-text { font-size: 0.95rem; }
        .section-header { font-size: 20px; margin: 20px 0 15px 0; }
        .bullet-point { padding: 12px; font-size: 14px; margin-bottom: 10px; }
        .roadmap-card { padding: 12px; font-size: 14px; }
        .stTabs [data-baseweb="tab-list"] { padding: 8px; gap: 5px; }
        .stTabs [data-baseweb="tab"] { height: 40px; padding: 0 10px; font-size: 12px; }
        .banner-text { font-size: 1.1rem; }
        img { border-radius: 10px; } 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. AUTHENTICATION INTERFACE
# ==========================================
if 'authenticated' not in st.session_state:
    saved_user = check_active_session()
    if saved_user:
        st.session_state.authenticated = True
        st.session_state.user_name = saved_user
    else:
        st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.write("<br><br>", unsafe_allow_html=True) 
    
    col_img, col_form = st.columns([1.2, 1], gap="large")
    
    with col_img:
        st.markdown("<div class='welcome-text'>Welcome to the <br><span class='highlight'>Universal Career Architect</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-text'>Your personalized AI engine for infinite domain intelligence, ATS optimization, and direct hiring access. Please authenticate to enter the global workspace.</div>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800", use_container_width=True, clamp=True)
        
    with col_form:
        # THE ANIMATED BANNER (Clean and active)
        st.markdown("""
            <div class='premium-banner'>
                <div class='banner-text'>⚡ Intelligence Matrix Online</div>
                <div class='banner-sub'>Live 2026 Global Market Data Sync Active</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.subheader("🔐 Secure Access Portal")
        
        auth_mode = st.radio("Choose Action", ["Login", "Register"], horizontal=True)
        st.divider()
        
        if auth_mode == "Login":
            with st.form("login_form"):
                log_email = st.text_input("Email Address", placeholder="Enter your registered email")
                log_pass = st.text_input("Password", type="password", placeholder="Enter your password")
                log_btn = st.form_submit_button("Login to Workspace", use_container_width=True)
                
                if log_btn:
                    user_data = verify_user(log_email, log_pass)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_name = user_data[0]
                        create_active_session(user_data[0]) 
                        st.rerun()
                    else:
                        st.error("Access Denied: Incorrect Email or Password.")
                        
        elif auth_mode == "Register":
            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. John Doe")
                reg_email = st.text_input("Email Address", placeholder="e.g. name@example.com")
                reg_pass = st.text_input("Create Password", type="password", placeholder="Minimum 6 characters")
                reg_btn = st.form_submit_button("Register Secure Account", use_container_width=True)
                
                if reg_btn:
                    if add_user(reg_name, reg_email, reg_pass):
                        st.success("Registration Successful! Please switch to 'Login' to enter.")
                    else:
                        st.error("This email is already registered. Please login instead.")
                            
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ==========================================
    # 4. MAIN APP: HYBRID ENGINE 
    # ==========================================
    colA, colB = st.columns([8, 1])
    with colB:
        if st.button("Logout", key="logout_btn", use_container_width=True):
            conn = sqlite3.connect('secure_users.db'); c = conn.cursor(); c.execute('DELETE FROM active_session'); conn.commit(); conn.close()
            st.session_state.authenticated = False
            st.rerun()

    st.title("🌐 Universal Career Architect & Strategy Engine")
    st.write("#### Infinite Domain Intelligence, ATS Optimization, & Direct Hiring Portal")

    def bullet_renderer(data_list):
        return "".join([f"<div class='bullet-point'>{item}</div>" for item in data_list])

    def generate_offline_fallback(f, g, l):
        strat = [
            f"Month 1: Establish a strong foundation in {f} principles and core {g} methodologies.",
            f"Month 2: Master the primary technical stack and tools required for a {l} level role.",
            f"Month 3: Develop 2-3 real-world projects directly related to {f} to showcase practical expertise.",
            f"Month 4: Optimize your portfolio, GitHub, and LinkedIn specifically targeting {g} positions.",
            f"Month 5: Engage in advanced problem-solving, mock interviews, and industry case studies.",
            f"Month 6: Initiate an aggressive application strategy and network with industry professionals."
        ]
        skills = [f"Advanced {f} Architecture", "Analytical & Critical Thinking", "Modern Industry Tools Implementation"]
        market = [f"High and consistent demand for {g} roles globally in 2026.", f"Average starting package varies based on {l} proficiency (approx ₹6L - ₹18L+ in India).", "Top hiring sectors: Tech, E-commerce, Finance, and Consulting.", "Remote and Hybrid roles are heavily expanding in this domain."]
        ats = [f"{g}", f"{f} Specialist", "Data-Driven Decision Making", "Cross-functional Collaboration", "Agile Methodologies"]
        return strat, skills, market, ats, "Intelligence Node Backup (System Optimized)"

    def generate_enterprise_report(field, goal, level):
        prompt_text = f"""
        CRITICAL TASK: Assess Role: '{goal}' in Industry: '{field}'.
        If this combination is entirely illogical, absurd, or fundamentally impossible, YOU MUST OUTPUT EXACTLY THE WORD 'INVALID' AND NOTHING ELSE.
        If it is a valid profession, generate a roadmap for {level}. Format strictly with exactly three '|||' separators:
        [6 lines of Strategy, one per month] |||
        [3 bullet points for Skills] |||
        [4 bullet points for Market Overview & Indian Salary] |||
        [5 bullet points for ATS Keywords & Interview Questions]
        """
        
        shuffled_keys = random.sample(KEYS, 2)
        
        for attempt, key in enumerate(shuffled_keys):
            try:
                if attempt > 0:
                    time.sleep(4)
                    
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                headers = {'Content-Type': 'application/json'}
                payload = {"contents": [{"parts":[{"text": prompt_text}]}], "generationConfig": {"temperature": 0.9}} 
                
                response = requests.post(url, headers=headers, json=payload, timeout=8)
                
                if response.status_code == 200:
                    data = response.json()
                    text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    if "INVALID" in text.upper(): return "INVALID", [], [], [], "AI Logic Gate"
                    
                    if "|||" in text:
                        parts = text.split("|||")
                        if len(parts) >= 4:
                            strat = [l.strip() for l in parts[0].strip().split('\n') if len(l.strip()) > 3][:6]
                            skills = [l.strip() for l in parts[1].strip().split('\n') if len(l.strip()) > 3][:3]
                            market = [l.strip() for l in parts[2].strip().split('\n') if len(l.strip()) > 3][:4]
                            ats = [l.strip() for l in parts[3].strip().split('\n') if len(l.strip()) > 3][:5]
                            return strat, skills, market, ats, "Direct API Engine (Fresh Data)"
            except Exception:
                continue 
                
        return generate_offline_fallback(field, goal, level)

    # SIDEBAR
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800", use_container_width=True)
        st.header(f"🏢 Profile: {st.session_state.user_name}")
        
        u_field = st.text_input("Industry Domain (Any Industry)", placeholder="e.g. Data Science, Law")
        u_goal = st.text_input("Target Designation", placeholder="e.g. Senior Analyst, Judge")
        u_level = st.radio("Proficiency Level", ["Beginner", "Intermediate", "Advanced"], index=0)
        
        st.divider()
        generate_btn = st.button("Architect Global Strategy", use_container_width=True)

    # DASHBOARD
    if generate_btn and u_field and u_goal:
        with st.spinner(f"Synthesizing intelligence through AI Nodes for {u_field}..."):
            strat_data, skills_data, market_data, ats_data, source = generate_enterprise_report(u_field, u_goal, u_level)
            
            if strat_data == "INVALID":
                st.error("🚨 **Logic Mismatch Detected:** The Industry and Target Designation combination seems invalid or absurd. Please enter a realistic career path.")
            else:
                st.image("https://images.unsplash.com/photo-1522071901873-411886a10004?w=1200", use_container_width=True)
                st.info(f"Report Intelligence Source: **{source}**")
                
                t1, t2, t3, t4, t5, t6 = st.tabs(["🎯 Gamified Roadmap", "🛠️ Skills", "💰 Market & Salary", "📝 ATS & Interview", "▶️ Free Masterclasses", "💼 Apply & Sponsors"])
                
                with t1:
                    st.markdown(f"<div class='section-header'>I. Execution Plan: {u_goal}</div>", unsafe_allow_html=True)
                    for i, month_task in enumerate(strat_data[:6]):
                        st.markdown(f"<div class='roadmap-card'><b>Phase {i+1}:</b> {month_task.replace('*', '')}</div>", unsafe_allow_html=True)

                with t2:
                    st.markdown("<div class='section-header'>II. Professional Skill Matrix</div>", unsafe_allow_html=True)
                    st.markdown(bullet_renderer(skills_data), unsafe_allow_html=True)

                with t3:
                    st.markdown(f"<div class='section-header'>III. Industry Economics & Expected Salary</div>", unsafe_allow_html=True)
                    st.markdown(bullet_renderer(market_data), unsafe_allow_html=True)

                with t4:
                    st.markdown("<div class='section-header'>IV. ATS Resume Optimizer & AI Interview Predictor</div>", unsafe_allow_html=True)
                    st.markdown(bullet_renderer(ats_data), unsafe_allow_html=True)

                with t5:
                    st.markdown("<div class='section-header'>V. Free Global Masterclasses</div>", unsafe_allow_html=True)
                    
                    safe_goal = u_goal.replace(" ", "+")
                    safe_field = u_field.replace(" ", "+")
                    
                    yt_link_1 = f"https://www.youtube.com/results?search_query=Full+{safe_goal}+Course+For+Beginners"
                    yt_link_2 = f"https://www.youtube.com/results?search_query={safe_field}+Masterclass"
                    yt_link_3 = f"https://www.youtube.com/results?search_query={safe_goal}+Interview+Questions"
                    
                    st.link_button(f"📺 Watch '{u_goal}' Beginner Full Course", yt_link_1, use_container_width=True)
                    st.link_button(f"📺 Watch '{u_field}' Masterclass Playlists", yt_link_2, use_container_width=True)
                    st.link_button(f"📺 Top '{u_goal}' Interview Answers", yt_link_3, use_container_width=True)

                with t6:
                    st.markdown("<div class='section-header'>VI. Direct Hiring Portal & Sponsors</div>", unsafe_allow_html=True)
                    
                    safe_goal_hyphen = u_goal.replace(' ', '-')
                    
                    c1, c2, c3 = st.columns(3)
                    with c1: 
                        st.link_button("Apply on LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={safe_goal}", use_container_width=True)
                        st.link_button("Enroll on Coursera", f"https://www.coursera.org/search?query={safe_field}", use_container_width=True)
                    with c2: 
                        st.link_button("Apply on Indeed", f"https://in.indeed.com/jobs?q={safe_goal}", use_container_width=True)
                        st.link_button("Certificates on edX", f"https://www.edx.org/search?q={safe_field}", use_container_width=True)
                    with c3:
                        st.link_button("Apply on Naukri", f"https://www.naukri.com/{safe_goal_hyphen}-jobs", use_container_width=True)
                    
                    st.divider()
                    st.success("📢 **Corporate Sponsorships Active:** Want to run your sponsorship Contact Mr Kapil Thakur.")

    else:
        st.image("https://images.unsplash.com/photo-1522071901873-411886a10004?w=1200", use_container_width=True)
        st.write("#### Welcome. Define your target role in the sidebar to generate a complete end-to-end career strategy.")
