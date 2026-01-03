import streamlit as st
import joblib
import base64
import json
import pandas as pd
import os
from datetime import datetime

# -------- RESET STALE LOGINS (IMPORTANT FIX) --------
if os.path.exists("users.csv"):
    df_reset = pd.read_csv("users.csv")
    if "LoggedIn" in df_reset.columns:
        df_reset["LoggedIn"] = False
        df_reset.to_csv("users.csv", index=False)

# ---------------- SESSION STATE ----------------
if "issues_input" not in st.session_state:
    st.session_state.issues_input = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state:
    st.session_state.user_type = "User"
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- BACKGROUND ----------------
def set_bg(image_file=None):
    st.markdown(
        """
        <style>
        .stApp { background-color: white; color: black; }
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>div>select {
            background-color: #f0f0f0;
            color: black;
        }
        .stButton>button {
            background-color: #e0e0e0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- LOGIN TYPE ----------------
selected_type = st.selectbox(
    "Select Login Type",
    ["User", "Admin"],
    index=0 if st.session_state.user_type == "User" else 1
)

if selected_type != st.session_state.user_type:
    st.session_state.user_type = selected_type
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()

# ================= ADMIN LOGIN =================
if st.session_state.user_type == "Admin":
    set_bg()

    if st.session_state.page == "login":
        st.title("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.info(
            """
            **CivicEye AI – Administrative Portal**

            CivicEye AI is a digital grievance management system designed to help government
            authorities and administrators efficiently monitor, manage, and resolve citizen complaints.

            **Primary focus areas monitored through this system:**
            1. Road damage and public infrastructure issues  
            2. Water supply and sanitation problems  
            3. Streetlight and electricity faults  
            4. Waste management and cleanliness concerns  
            5. Public safety and civic facility maintenance  

            **How this portal is used:**
            - View all complaints submitted by citizens
            - Track complaint status in real time
            - Update resolution progress
            - Remove invalid or resolved complaints
            """
        )

    if st.session_state.page == "admin" and st.session_state.logged_in:
        st.title("Admin Dashboard")
        st.subheader("Citizen Complaints")

        if os.path.exists("complaints.csv"):
            df = pd.read_csv("complaints.csv").reset_index(drop=True)
            st.dataframe(df, use_container_width=True)

            st.markdown("### Manage Complaints")

            for i in range(len(df)):
                col1, col2, col3, col4 = st.columns([3, 2, 1.5, 1.5])

                with col1:
                    st.write(f"**Issue:** {df.loc[i, 'Issue']}")

                with col2:
                    current_status = df.loc[i, "Status"]
                    if current_status not in ["Pending", "In Progress", "Resolved"]:
                        current_status = "Pending"

                    new_status = st.selectbox(
                        "Status",
                        ["Pending", "In Progress", "Resolved"],
                        index=["Pending", "In Progress", "Resolved"].index(current_status),
                        key=f"status_{i}"
                    )

                with col3:
                    if st.button("Update", key=f"update_{i}"):
                        df.loc[i, "Status"] = new_status
                        df.to_csv("complaints.csv", index=False)
                        st.success("Status updated")
                        st.rerun()

                with col4:
                    if st.button("🗑️ Delete", key=f"del_btn_{i}"):
                        df = df.drop(index=i).reset_index(drop=True)
                        df.to_csv("complaints.csv", index=False)
                        st.warning("Complaint deleted")
                        st.rerun()
        else:
            st.warning("No complaints found")

# ================= USER LOGIN =================
if st.session_state.user_type == "User":
    set_bg()

    if st.session_state.page == "login":
        st.title("User Login")

        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):
            if username_input.strip() == "" or password_input.strip() == "":
                st.error("Invalid username or password")
                st.stop()

            if os.path.exists("users.csv"):
                df = pd.read_csv("users.csv")
            else:
                df = pd.DataFrame(columns=["Username", "Password", "LoggedIn"])

            if "LoggedIn" not in df.columns:
                df["LoggedIn"] = False

            user_row = df[df["Username"] == username_input]

            if not user_row.empty:
                if user_row.iloc[0]["Password"] != password_input:
                    st.error("Invalid username or password")
                elif user_row.iloc[0]["LoggedIn"]:
                    st.warning("This user is already logged in")
                else:
                    df.loc[df["Username"] == username_input, "LoggedIn"] = True
                    df.to_csv("users.csv", index=False)
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.page = "user"
                    st.rerun()
            else:
                df.loc[len(df)] = [username_input, password_input, True]
                df.to_csv("users.csv", index=False)
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.page = "user"
                st.rerun()

        st.info(
            """
            **Welcome to CivicEye AI – Citizen Complaint Portal**

            CivicEye AI allows citizens to report and track public service issues
            directly to the concerned authorities in a transparent and efficient manner.

            **You can report problems related to:**
            1. Damaged roads and unsafe infrastructure  
            2. Drinking water shortages and sanitation issues  
            3. Non-functioning streetlights or power problems  
            4. Garbage collection and cleanliness concerns  
            5. Public safety and basic civic facilities  

            **How to use this portal:**
            - Log in with your username and password
            - Submit a complaint with clear issue details
            - Track the status of your complaint
            - Ensure faster and accountable resolution
            """
        )

    # ================= USER COMPLAINT PAGE =================
    if st.session_state.page == "user" and st.session_state.logged_in:
        st.title("CivicEye AI - Submit Complaint")

        model = joblib.load("issue_classifier.pkl")
        vectorizer = joblib.load("vectorizer.pkl")

        with open("districts.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        with st.form("complaint_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            state = st.selectbox("State", data["states"])
            district = st.selectbox("District", data["districts"])
            village = st.text_input("Village")
            issues = st.text_area("Issues")
            submit = st.form_submit_button("Submit")

        if submit:
            row = {
                "Username": st.session_state.username,
                "Name": name,
                "Phone": phone,
                "District": district,
                "Issue": issues,
                "Status": "Pending"
            }
            pd.DataFrame([row]).to_csv(
                "complaints.csv",
                mode="a",
                header=not os.path.exists("complaints.csv"),
                index=False
            )
            st.success("Complaint submitted")

# ================= LOGOUT =================
if st.session_state.logged_in and st.session_state.user_type == "User":
    if st.button("Logout"):
        df = pd.read_csv("users.csv")
        df.loc[df["Username"] == st.session_state.username, "LoggedIn"] = False
        df.to_csv("users.csv", index=False)
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()
