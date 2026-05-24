import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EduVerse Global AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("eduverse_global_ai.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT UNIQUE,
    password BLOB,
    country TEXT,
    institution TEXT,
    course TEXT,
    level TEXT,
    disability TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    title TEXT,
    deadline TEXT,
    status TEXT
)
''')

conn.commit()

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# FUNCTIONS
# =========================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


def register_user(fullname, email, password,
                  country, institution,
                  course, level, disability):

    hashed = hash_password(password)

    try:
        cursor.execute(
            '''
            INSERT INTO users
            (fullname, email, password,
             country, institution,
             course, level, disability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                fullname,
                email,
                hashed,
                country,
                institution,
                course,
                level,
                disability
            )
        )

        conn.commit()
        return True

    except:
        return False


def login_user(email, password):

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        stored_password = user[3]

        if verify_password(password, stored_password):
            return user

    return None


# =========================
# CUSTOM STYLING
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }

    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 15px;
    }

    .big-card {
        background: linear-gradient(135deg,#2563eb,#7c3aed);
        padding: 25px;
        border-radius: 20px;
        color: white;
    }

    .small-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🎓 EduVerse Global AI")
st.sidebar.caption("International Education Ecosystem")

# =========================
# LOGIN / REGISTER
# =========================
if not st.session_state.logged_in:

    auth_menu = st.sidebar.radio(
        "Navigation",
        ["Login", "Register"]
    )

    st.title("🌍 EduVerse Global AI")
    st.subheader("AI-Powered Global Learning Platform")

    st.write(
        "Supporting Universities, Colleges, TVET Institutions, "
        "Accessibility Learning, and International Curricula"
    )

    # =========================
    # REGISTER
    # =========================
    if auth_menu == "Register":

        st.markdown("## Create Account")

        fullname = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        country = st.selectbox(
            "Country",
            [
                "Kenya",
                "USA",
                "UK",
                "Canada",
                "India",
                "South Africa",
                "Germany",
                "Australia",
                "Nigeria",
                "Other"
            ]
        )

        institution = st.text_input("Institution")

        course = st.selectbox(
            "Course",
            [
                "Computer Science",
                "Engineering",
                "Medicine",
                "Business",
                "Law",
                "Data Science",
                "Nursing",
                "ICT",
                "Automotive Engineering",
                "Hospitality",
                "Fashion & Design",
                "Other"
            ]
        )

        level = st.selectbox(
            "Education Level",
            [
                "University",
                "College",
                "TVET",
                "Online Learning"
            ]
        )

        disability = st.selectbox(
            "Accessibility Support",
            [
                "None",
                "Visual Support",
                "Hearing Support",
                "Dyslexia Support",
                "ADHD Focus Mode"
            ]
        )

        if st.button("Create Account"):

            success = register_user(
                fullname,
                email,
                password,
                country,
                institution,
                course,
                level,
                disability
            )

            if success:
                st.success("Account created successfully")
            else:
                st.error("Email already exists")

    # =========================
    # LOGIN
    # =========================
    else:

        st.markdown("## Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("Invalid email or password")

# =========================
# MAIN APP
# =========================
else:

    user = st.session_state.user

    fullname = user[1]
    email = user[2]
    country = user[4]
    institution = user[5]
    course = user[6]
    level = user[7]
    disability = user[8]

    menu = st.sidebar.radio(
        "Platform Navigation",
        [
            "Dashboard",
            "AI Assistant",
            "Assignments",
            "Analytics",
            "Accessibility Portal",
            "Courses",
            "Settings",
            "Logout"
        ]
    )

    # =========================
    # DASHBOARD
    # =========================
    if menu == "Dashboard":

        hour = datetime.now().hour

        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        st.markdown(
            f'''
            <div class="big-card">
                <h1>{greeting}, {fullname} 👋</h1>
                <p>Welcome to EduVerse Global AI</p>
                <p>{institution} • {course}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.write("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Country", country)

        with col2:
            st.metric("Level", level)

        with col3:
            st.metric("Course", course)

        with col4:
            st.metric("Accessibility", disability)

        st.write("---")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                '''
                <div class="small-card">
                <h3>📚 Courses Progress</h3>
                <h1>78%</h1>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                '''
                <div class="small-card">
                <h3>🔥 Learning Streak</h3>
                <h1>12 Days</h1>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                '''
                <div class="small-card">
                <h3>📝 Assignments</h3>
                <h1>5 Pending</h1>
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.write("---")

        st.subheader("📈 Academic Performance")

        data = pd.DataFrame({
            "Subject": [
                "Course Work",
                "Assignments",
                "Attendance",
                "Projects",
                "Exams"
            ],
            "Score": [80, 75, 92, 68, 85]
        })

        fig = px.bar(data, x="Subject", y="Score")
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("⚡ Quick Actions")

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            st.button("🤖 Open AI")

        with q2:
            st.button("📅 Timetable")

        with q3:
            st.button("📚 My Courses")

        with q4:
            st.button("📝 Assignments")

    # =========================
    # AI ASSISTANT
    # =========================
    elif menu == "AI Assistant":

        st.title("🤖 EduVerse AI Assistant")

        st.info(
            "Ask anything: academics, coding, business, "
            "research, innovation, careers and more"
        )

        ai_mode = st.selectbox(
            "AI Learning Mode",
            [
                "Beginner Mode",
                "Advanced Mode",
                "Research Mode",
                "Practical Mode"
            ]
        )

        question = st.text_area(
            "Ask AI Anything"
        )

        if st.button("Generate AI Response"):

            st.success("AI Response Generated")

            st.write(f"### Mode: {ai_mode}")

            st.write(
                "This is where OpenAI/Gemini/local AI integration "
                "will generate intelligent responses based on the "
                "student's question and learning mode."
            )

            st.write("#### Example Features")
            st.write("- AI explanations")
            st.write("- Research assistance")
            st.write("- Coding help")
            st.write("- Career guidance")
            st.write("- Assignment support")
            st.write("- Innovation brainstorming")

    # =========================
    # ASSIGNMENTS
    # =========================
    elif menu == "Assignments":

        st.title("📝 Assignment Management")

        title = st.text_input("Assignment Title")
        deadline = st.date_input("Deadline")

        if st.button("Add Assignment"):

            cursor.execute(
                '''
                INSERT INTO assignments
                (user_email, title, deadline, status)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    email,
                    title,
                    str(deadline),
                    "Pending"
                )
            )

            conn.commit()
            st.success("Assignment Added")

        st.write("---")

        cursor.execute(
            "SELECT title, deadline, status FROM assignments WHERE user_email=?",
            (email,)
        )

        assignments = cursor.fetchall()

        if assignments:
            df = pd.DataFrame(
                assignments,
                columns=["Title", "Deadline", "Status"]
            )

            st.dataframe(df, use_container_width=True)

        else:
            st.warning("No assignments available")

    # =========================
    # ANALYTICS
    # =========================
    elif menu == "Analytics":

        st.title("📊 Student Analytics")

        analytics_data = pd.DataFrame({
            "Week": [
                "Week 1",
                "Week 2",
                "Week 3",
                "Week 4"
            ],
            "Study Hours": [5, 8, 7, 10]
        })

        fig = px.line(
            analytics_data,
            x="Week",
            y="Study Hours",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("AI Insights")

        st.success("You are improving consistently this month")
        st.info("Assignments performance increased by 15%")
        st.warning("Focus more on practical projects")

    # =========================
    # ACCESSIBILITY
    # =========================
    elif menu == "Accessibility Portal":

        st.title("♿ Accessibility Portal")

        mode = st.selectbox(
            "Choose Accessibility Mode",
            [
                "Normal",
                "High Contrast",
                "Large Text",
                "Dyslexia Friendly",
                "Focus Mode"
            ]
        )

        if mode == "High Contrast":
            st.markdown(
                '''
                <style>
                body {
                    background-color: black;
                    color: white;
                }
                </style>
                ''',
                unsafe_allow_html=True
            )

        if mode == "Large Text":
            st.markdown(
                '''
                <style>
                html, body, [class*="css"]  {
                    font-size: 22px;
                }
                </style>
                ''',
                unsafe_allow_html=True
            )

        st.success(f"{mode} enabled")

        st.write("### Accessibility Tools")

        st.write("- Voice learning support")
        st.write("- Read aloud integration")
        st.write("- ADHD focus mode")
        st.write("- Dyslexia-friendly layouts")
        st.write("- Keyboard navigation")

    # =========================
    # COURSES
    # =========================
    elif menu == "Courses":

        st.title("📚 Global Courses")

        courses = [
            "Computer Science",
            "Software Engineering",
            "Medicine",
            "Business Administration",
            "Electrical Engineering",
            "Cybersecurity",
            "Data Science",
            "Mechanical Engineering",
            "Hospitality",
            "Agriculture",
            "Fashion & Design",
            "Automotive Technology"
        ]

        for c in courses:
            st.markdown(
                f'''
                <div class="small-card">
                <h3>{c}</h3>
                <p>International curriculum support available.</p>
                </div>
                ''',
                unsafe_allow_html=True
            )

            st.write("")

    # =========================
    # SETTINGS
    # =========================
    elif menu == "Settings":

        st.title("⚙️ Settings")

        language = st.selectbox(
            "Language",
            [
                "English",
                "Swahili",
                "French",
                "Spanish",
                "Arabic"
            ]
        )

        theme = st.selectbox(
            "Theme",
            ["Dark", "Light"]
        )

        notifications = st.checkbox("Enable Notifications", value=True)

        st.success("Settings saved successfully")

    # =========================
    # LOGOUT
    # =========================
    elif menu == "Logout":

        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

        # ======================================================
# FOOTER
# ======================================================
st.markdown("""
<div class='footer'>
© 2026 EduVerse Global AI | Global AI Education Platform 🌍
</div>
""", unsafe_allow_html=True)

# ======================================================
# RUN:
# streamlit run app.py
# ======================================================
