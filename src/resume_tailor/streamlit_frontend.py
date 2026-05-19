import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from resume_tailor.main import load_resume

from resume_tailor.crew import ResumeTailor


def main():
    st.title("Resume Tailor")
    st.sidebar.title("Upload")
    uploaded_file = st.sidebar.file_uploader("Upload your resume", type=["pdf", "docx"])
    jd_input = st.sidebar.text_area("Enter your job description", height="content")
    if st.sidebar.button("Tailor"):
        if uploaded_file is not None and jd_input:
            tmp_path = "tmp/resume_upload.pdf"
            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            resume_text = load_resume(tmp_path)

            inputs = {"jd_text": jd_input, "resume_text": resume_text}
            with st.spinner("Tailoring your resume..."):
                result = ResumeTailor().crew().kickoff(inputs=inputs)

            tailored_resume = result.tasks_output[2].raw
            cover_letter = result.tasks_output[3].raw

            st.success("Done!")

            tab1, tab2 = st.tabs(["Tailored Resume", "Cover Letter"])
            with tab1:
                st.text_area("Tailored Resume", tailored_resume, height=500)
                st.download_button("Download", tailored_resume, "tailored_resume.txt")
            with tab2:
                st.text_area("Cover Letter", cover_letter, height=500)
                st.download_button("Download", cover_letter, "cover_letter.txt")

        else:
            st.sidebar.error("Please upload a resume and enter a job description.")


if __name__ == "__main__":
    main()