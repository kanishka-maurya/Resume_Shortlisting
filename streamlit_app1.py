import sqlite3
import pandas as pd
import streamlit as st
import smtplib
from email.mime.text import MIMEText

# --- Load Data from SQLite ---
def load_data():
    conn = sqlite3.connect('candidates.db')
    df = pd.read_sql_query("SELECT * FROM candidates", conn)
    conn.close()
    return df

# --- Remove Declined Candidate ---
def delete_candidate(candidate_id):
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
    conn.commit()
    conn.close()

# --- Streamlit App ---
st.title("Candidate Review Dashboard")

df = load_data()

if df.empty:
    st.warning("No candidates available.")
    st.stop()

# --- Review Table ---
st.subheader("Review Candidates")
accepted_ids = []
declined_ids = []

for i, row in df.iterrows():
    with st.expander(f"{row['full_name']} ({row['email']})"):
        st.markdown(f"**Skills:** {row['skills']}")
        st.markdown(f"**Experience:** {row['experience']}")
        st.markdown(f"**Tech Stack:** {row['tech_stack']}")

        col1, col2 = st.columns(2)
        if col1.checkbox(f"✅ Accept - {row['id']}", key=f"accept_{row['id']}"):
            accepted_ids.append(row['id'])
        if col2.checkbox(f"❌ Decline - {row['id']}", key=f"decline_{row['id']}"):
            declined_ids.append(row['id'])

# --- Delete Declined ---
if declined_ids:
    for cid in declined_ids:
        delete_candidate(cid)
    st.success(f"Removed {len(declined_ids)} declined candidates. Refresh to update.")
conn = sqlite3.connect("candidates.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM candidates")
count = cursor.fetchone()[0]
conn.close()

st.info(f"📦 {count} candidates remaining in the database.")

# --- Download CSV ---
if accepted_ids:
    accepted_df = df[df['id'].isin(accepted_ids)]
    csv = accepted_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Accepted as CSV", csv, "accepted_candidates.csv", "text/csv")

# --- Admin Authentication ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.subheader("🔐 Admin Login Required to Send Emails")
    with st.form("admin_login"):
        email_input = st.text_input("Admin Email")
        password_input = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

        if submit:
            if email_input == "admin@example.com" and password_input == "admin123":
                st.session_state['authenticated'] = True
                st.success("✅ Authentication successful! Scroll down to send emails.")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid email or password")
                
# --- Send Custom Email (Only after login and at the bottom) ---
if st.session_state['authenticated'] and accepted_ids:
    st.markdown("---")
    st.subheader("✉️ Send Email to Accepted Candidates")
    subject = st.text_input("Subject of Email", "Your Application Update")
    message_template = st.text_area("Email Body (use {{name}} placeholder)", 
        "Hi {{name}},\n\nThank you for applying. We're happy to inform you that you're shortlisted!\n\nBest,\nRecruitment Team")

    if st.button("📧 Send Email to Accepted"):
        for i, row in df[df['id'].isin(accepted_ids)].iterrows():
            msg = MIMEText(message_template.replace("{{name}}", row["full_name"]))
            msg['Subject'] = subject
            msg['From'] = "admin@example.com"
            msg['To'] = row["email"]

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("admin@example.com", "admin123")
                server.send_message(msg)
                server.quit()
                st.success(f"Email sent to {row['full_name']}")
            except Exception as e:
                st.error(f"Failed to send email to {row['full_name']}: {e}")
