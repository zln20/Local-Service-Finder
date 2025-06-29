import streamlit as st
import time
import os
from qa_pipeline import answer_query

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

st.set_page_config(page_title="Service Finder", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
    <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }
        .subtitle {
            font-size: 18px;
            color: #7f8c8d;
        }
        .answer-box {
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;  /* preserve line breaks */
        }
        .question {
            font-weight: bold;
            margin-top: 1rem;
            color: #34495e;
        }
        a {
            color: #2e86de;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Local Service Finder</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask about top-rated local services</div>", unsafe_allow_html=True)
st.markdown("---")

question = st.text_area("What are you looking for?", height=100,
                        placeholder="e.g., Who are the best-rated dishwasher repair technicians in San Francisco?")

if st.button("🔍 Search"):
    if question.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Searching..."):
            time.sleep(0.5)
            answer = answer_query(question)

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer
        })
        st.success("Results ready!")

if st.session_state.chat_history:
    st.markdown("### Search History")
    for entry in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='question'>{entry['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='answer-box'>{entry['answer']}</div>", unsafe_allow_html=True)

st.markdown("---")