#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from resume_tailor.crew import ResumeTailor
from pypdf import PdfReader

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_resume(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def run():
    """
    Run the crew.
    """
    resume_text = load_resume("src/resume_tailor/resume/resume_upload.pdf")
    jd_text = open("src/resume_tailor/jd/jd.txt", "r").read()
    inputs = {
        "jd_text": jd_text,
        "resume_text": resume_text
    }

    result = ResumeTailor().crew().kickoff(inputs=inputs)

    tailored_resume = result.tasks_output[2].raw
    cover_letter = result.tasks_output[3].raw

    print("\n" + "=" * 60)
    print("TAILORED RESUME")
    print("=" * 60)
    print(tailored_resume)

    print("\n" + "=" * 60)
    print("COVER LETTER")
    print("=" * 60)
    print(cover_letter)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        ResumeTailor().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResumeTailor().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        ResumeTailor().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
