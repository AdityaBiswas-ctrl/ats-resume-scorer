# streamlit_app.py

import streamlit as st
import requests

# Page config
st.set_page_config(page_title="ATS Resume Scorer", page_icon="📄", layout="centered")

st.title("📄 ATS Resume Scorer")
st.markdown("Upload your resume and paste a job description to get a semantic match analysis.")

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    jd_text = st.text_area("Paste Job Description", height=300, 
                            placeholder="Paste the full job description here...")

# --- Analysis Button ---
if st.button("Analyse Match", type="primary"):
    if not uploaded_file:
        st.error("Please upload a PDF resume.")
    elif not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analysing semantic similarity..."):
            try:
                # Send a multipart form request to the FastAPI backend
                response = requests.post(
                    "http://localhost:8000/score",
                    files={"resume_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                    data={"job_description": jd_text}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- Results Display ---
                    st.success(f"Analysis complete for **{data['filename']}**")
                    
                    # Big score metric
                    score = data['similarity_score']
                    st.metric("Semantic Match Score", f"{score}%", 
                              delta=data['rating'])
                    
                    # Progress bar for visual impact
                    st.progress(score / 100)
                    
                    # Matched vs Missing keywords side by side
                    col_match, col_miss = st.columns(2)
                    
                    with col_match:
                        st.markdown("### ✅ Matched Keywords")
                        if data['matched_keywords']:
                            st.write(", ".join(data['matched_keywords']))
                        else:
                            st.write("No keyword overlap found.")
                    
                    with col_miss:
                        st.markdown("### ⚠️ Missing Keywords")
                        if data['missing_keywords']:
                            st.write(", ".join(data['missing_keywords'][:20]))  # Top 20 only
                        else:
                            st.write("No significant gaps found.")
                    
                else:
                    st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.ConnectionError:
                st.error("Cannot connect to backend. Make sure FastAPI is running on port 8000.")