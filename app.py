import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. ENTERPRISE GLOBAL UI DESIGN
# ==========================================
st.set_page_config(page_title="Universal Career Intelligence", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    .main { background: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 15px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: #1e293b; border-radius: 8px; color: #94a3b8; padding: 0 20px; font-weight: 700; font-size: 14px; }
    .stTabs [aria-selected="true"] { background: #0ea5e9; color: #020617; box-shadow: 0 0 15px rgba(14, 165, 233, 0.4); }
    
    .info-card { background: rgba(30, 41, 59, 0.8); padding: 35px; border-radius: 20px; border-left: 8px solid #0ea5e9; margin-bottom: 30px; box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5); }
    
    /* Atomic Bullet System */
    .bullet-point { 
        margin-bottom: 15px; padding: 18px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px; border-left: 4px solid #38bdf8;
        display: block; line-height: 1.7; font-size: 16px; transition: 0.3s;
    }
    .bullet-point:hover { background: rgba(56, 189, 248, 0.1); transform: translateX(8px); }
    
    .section-header { color: #38bdf8; font-size: 26px; font-weight: 900; margin: 30px 0 20px 0; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
    
    /* Gamification Checkbox Styling */
    .stCheckbox > label { font-size: 16px !important; font-weight: bold; color: #f1f5f9; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #10b981; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Universal Career Architect & Strategy Engine")
st.write("#### Infinite Domain Intelligence, ATS Optimization, & Direct Hiring Portal")

# ==========================================
# 2. DYNAMIC ALGORITHMIC FALLBACK ENGINE
# ==========================================
def generate_dynamic_fallback(field, goal, level):
    strategy = [
        f"Month 1: The {field} Ecosystem – Understanding core principles and industry history.",
        f"Month 2: {goal} Tooling & Software – Mastering primary software/tools.",
        f"Month 3: Practical Application – Executing beginner-level theoretical projects.",
        f"Month 4: Advanced Skill Acquisition – Complex, industry-specific problem solving.",
        f"Month 5: Portfolio & Proof of Work – Compiling a professional body of work.",
        f"Month 6: Market Readiness – Interview prep and LinkedIn optimization."
    ] 
    
    skills = [
        f"✅ **Core Technical:** Industry-standard frameworks required for {field}.",
        f"✅ **Role-Specific:** Advanced analytical techniques for a {goal}.",
        f"✅ **Soft Skills:** Cross-functional communication and strategic adaptability."
    ]
    
    market = [
        f"🏢 **Top Employers:** Global corporations and high-growth startups in {field}.",
        f"🚀 **Internship Focus:** Target associate trainee programs for {goal} roles.",
        f"💰 **Expected Salary Package:** ₹4,00,000 - ₹12,00,000+ LPA (Varies heavily by tier and location).",
        f"📈 **Market Growth:** High demand projected for the next 5 years."
    ]
    
    ats_interview = [
        f"📄 **ATS Resume Keywords:** {field} fundamentals, {goal} optimization, strategic execution, cross-functional collaboration, data-driven analysis.",
        f"❓ **Interview Q1:** Tell me about a time you solved a complex problem related to {field}?",
        f"❓ **Interview Q2:** What specific tools do you use to execute {goal} tasks efficiently?",
        f"❓ **Interview Q3:** Where do you see the future of {field} heading?",
        f"❓ **Interview Q4:** Describe a project where you demonstrated {goal} capabilities."
    ]
    
    return strategy, skills, market, ats_interview

def bullet_renderer(data_list):
    return "".join([f"<div class='bullet-point'>{item}</div>" for item in data_list])

# ==========================================
# 3. AI CORE WITH STRICT FORMATTING
# ==========================================
KEYS = ["AIzaSyARhf3cA6ErwUKfDlptu9z9-2X8pjZq5cw", "AIzaSyAxyoNetrPlWDg6n4Zpp1vILVvefLzGWZo", "AIzaSyDWpiB-E89bHSAVA_ckIthNPp0_EaypH-E"]

def generate_enterprise_report(field, goal, level):
    prompt = f"""
    Create a massive, highly structured roadmap for a {level} in '{field}' targeting the role of '{goal}'.
    Return exactly 4 sections separated by '|||':
    1. 6-month Strategy (1 clean sentence per month, no asterisks)
    2. Required Skills (3 bullet points)
    3. Market Overview, Top Companies, & Expected Indian Salary Package in INR/LPA (4 bullet points)
    4. Top 5 ATS Resume Keywords & Top 4 Technical Interview Questions (5 bullet points)
    """
    
    for key in KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            time.sleep(1)
            response = model.generate_content(prompt)
            if "|||" in response.text:
                parts = response.text.split("|||")
                strat = [l.strip() for l in parts[0].split('\n') if len(l.strip()) > 5]
                skills = [l.strip() for l in parts[1].split('\n') if len(l.strip()) > 5]
                market = [l.strip() for l in parts[2].split('\n') if len(l.strip()) > 5]
                ats = [l.strip() for l in parts[3].split('\n') if len(l.strip()) > 5]
                return strat, skills, market, ats, "Global AI Supercluster"
        except:
            continue
            
    strat, skills, market, ats = generate_dynamic_fallback(field, goal, level)
    return strat, skills, market, ats, "Dynamic Algorithmic Engine (Fail-Safe)"

# ==========================================
# 4. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800", use_container_width=True)
    st.header("🏢 Strategic Profile")
    
    u_field = st.text_input("Industry Domain (Any Industry)", placeholder="e.g. Data Science, Culinary Arts", value="Data Analysis")
    u_goal = st.text_input("Target Designation", placeholder="e.g. Senior Analyst", value="Data Analyst")
    u_level = st.radio("Proficiency Level", ["Beginner (Zero Knowledge)", "Intermediate", "Advanced"], index=0)
    
    st.divider()
    generate_btn = st.button("Architect Global Strategy", use_container_width=True)

# ==========================================
# 5. DASHBOARD & MEGA-TAB RENDERING
# ==========================================
if generate_btn and u_field and u_goal:
    with st.spinner(f"Synthesizing universal data, salaries, and ATS keywords for {u_field}..."):
        time.sleep(1.5)
        strat_data, skills_data, market_data, ats_data, source = generate_enterprise_report(u_field, u_goal, u_level)
        
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200", use_container_width=True)
        st.info(f"Report Intelligence Source: **{source}**")
        
        t1, t2, t3, t4, t5, t6 = st.tabs(["🎯 Gamified Roadmap", "🛠️ Skills", "💰 Market & Salary", "📝 ATS & Interview", "▶️ Free Masterclasses", "💼 Apply & Sponsors"])
        
        with t1:
            st.markdown(f"<div class='section-header'>I. Interactive Execution Plan: {u_goal}</div>", unsafe_allow_html=True)
            st.write("Track your progress. Check off each month as you conquer it:")
            for i, month_task in enumerate(strat_data[:6]):
                st.checkbox(f"✔️ Phase {i+1}: {month_task.replace('*', '')}", key=f"check_{i}")

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
            st.write("Access free, high-quality education directly via YouTube:")
            
            # FORMAT FIX: Safely encoding spaces for the URL to prevent broken links
            safe_goal = u_goal.replace(" ", "+")
            safe_field = u_field.replace(" ", "+")
            
            yt_link_1 = f"https://www.youtube.com/results?search_query=Full+{safe_goal}+Course+For+Beginners"
            yt_link_2 = f"https://www.youtube.com/results?search_query={safe_field}+Masterclass"
            yt_link_3 = f"https://www.youtube.com/results?search_query={safe_goal}+Interview+Questions"
            
            # RENDER FIX: Replaced markdown links inside HTML with high-visibility Streamlit Buttons
            st.link_button(f"📺 Watch '{u_goal}' Beginner Full Course", yt_link_1, use_container_width=True)
            st.link_button(f"📺 Watch '{u_field}' Masterclass Playlists", yt_link_2, use_container_width=True)
            st.link_button(f"📺 Top '{u_goal}' Interview Answers", yt_link_3, use_container_width=True)

        with t6:
            st.markdown("<div class='section-header'>VI. Direct Hiring Portal & Sponsors</div>", unsafe_allow_html=True)
            st.write("Apply directly to top organizations and certifications:")
            
            safe_goal_hyphen = u_goal.replace(' ', '-')
            
            c1, c2, c3 = st.columns(3)
            with c1: 
                st.link_button("Apply on LinkedIn Jobs", f"https://www.linkedin.com/jobs/search/?keywords={safe_goal}", use_container_width=True)
                st.link_button("Enroll on Coursera", f"https://www.coursera.org/search?query={safe_field}", use_container_width=True)
            with c2: 
                st.link_button("Apply on Indeed", f"https://in.indeed.com/jobs?q={safe_goal}", use_container_width=True)
                st.link_button("Certificates on edX", f"https://www.edx.org/search?q={safe_field}", use_container_width=True)
            with c3:
                st.link_button("Apply on Naukri", f"https://www.naukri.com/{safe_goal_hyphen}-jobs", use_container_width=True)
            
            st.divider()
            st.success("📢 **Corporate Sponsorships Active:** Want to run your advertisment Contact Mr Kapil Thakur.")

else:
    st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200", use_container_width=True)
    st.write("#### Welcome. Define your target role in the sidebar to generate a complete end-to-end career strategy.")
