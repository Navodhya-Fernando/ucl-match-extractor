import streamlit as st
import fitz  # PyMuPDF
import re
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["UCL_Matches"]
collection = db["matches"]

def get_next_id():
    last = collection.find_one(sort=[("_id", -1)])
    return f"M{int(last['_id'][1:]) + 1:02d}" if last else "M01"

def extract_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()

    att = re.search(r"Attendance:\s?([\d,]+)", text)
    attendance = int(att.group(1).replace(",", "")) if att else None

    goal_match = re.search(r"\d{2}\.00CET\s*(\d)\s+(\d)", text)
    if goal_match:
        g1, g2 = int(goal_match.group(1)), int(goal_match.group(2))
        goals = g1 + g2
        goal_diff = abs(g1 - g2)
    else:
        goals = goal_diff = None

    return {
        "Goals": goals,
        "Goal_diff": goal_diff,
        "Shots_taken": 25,
        "Fouls": 31,
        "RedC": 0,      # Manual
        "YellowC": 0,   # Manual
        "Attendance": attendance,
        "Injuries": 0   # Manual
    }

# Streamlit UI
st.title("🏆 UCL Match Data Extractor")

pdf = st.file_uploader("📄 Upload Match Report (PDF)", type="pdf")

# Format and Round
format_option = st.selectbox("📋 Select Format", ["New", "Old"])
round_option = st.selectbox("⚽ Select Round", ["Qualifiers", "Group/League", "Knockouts"])

# Manual Inputs: Yellow / Red Cards (Team A + B)
st.markdown("### 🟨 Yellow Cards")
yellow_team_a = st.number_input("Team A Yellow Cards", min_value=0, value=0)
yellow_team_b = st.number_input("Team B Yellow Cards", min_value=0, value=0)

st.markdown("### 🟥 Red Cards")
red_team_a = st.number_input("Team A Red Cards", min_value=0, value=0)
red_team_b = st.number_input("Team B Red Cards", min_value=0, value=0)

st.markdown("### 💶 Market Value (in Million Euros)")
mv_team_a = st.number_input("Team A Starting XI Market Value (M€)", min_value=0.0, format="%.2f")
mv_team_b = st.number_input("Team B Starting XI Market Value (M€)", min_value=0.0, format="%.2f")

st.markdown("### ⚠ Injuries")
injuries = st.number_input("Total Injuries", min_value=0, value=0)

# Process Button
if st.button("🚀 Extract and Upload to MongoDB"):
    if not pdf:
        st.error("Please upload the match report PDF.")
    else:
        doc_data = extract_from_pdf(pdf)

        # Override with manual inputs
        doc_data["YellowC"] = yellow_team_a + yellow_team_b
        doc_data["RedC"] = red_team_a + red_team_b
        doc_data["Injuries"] = injuries
        mv_diff = round(abs(mv_team_a - mv_team_b), 2)

        final_data = {
            "_id": get_next_id(),
            "Format": format_option,
            "Round": round_option,
            **doc_data,
            "MV_diff": mv_diff
        }

        collection.insert_one(final_data)
        st.success("✅ Data inserted successfully!")
        st.json(final_data)