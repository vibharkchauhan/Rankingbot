# main.py
import streamlit as st
from rankingbot import rank_responses

st.set_page_config(page_title="Ranking Chatbot", layout="wide")

st.title("Ranking Chatbot")
st.write("Enter a prompt and multiple responses. The chatbot will evaluate and rank them.")

prompt = st.text_area("Enter Prompt", value="Top qualities of a strong leader")

responses_input = st.text_area("Enter Responses (one per line, format: A: text)", height=200)
submitted = st.button("Rank Responses")

if submitted:
    if not prompt.strip() or not responses_input.strip():
        st.warning("Please enter both a prompt and at least one response.")
    else:
        # Parse responses
        responses = {}
        for line in responses_input.strip().splitlines():
            if ':' in line:
                label, text = line.split(':', 1)
                responses[label.strip()] = text.strip()

        with st.spinner("Ranking responses..."):
            ranked = rank_responses(prompt, responses)

        st.subheader("📊 Ranking Results:")
        for r in ranked:
            st.markdown(f"**Response {r['id']} – Score: {r['score']}**")
            st.markdown(f"> {r['text']}")
            st.markdown(f"*Comment:* {r['scores']['comment']}")
            with st.expander("See Criteria Scores"):
                st.write(r['scores'])
