import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Medical Q&A Bot", page_icon="🩺", layout="wide")

st.title("🩺 MedQuAD Medical Assistant")
st.write("Ask any medical question. Powered by 15,000+ Q&A pairs from NIH sources.")

@st.cache_data
def load_data():
    return pd.read_csv("data/medquad_clean.csv").dropna()

df = load_data()

@st.cache_resource
def setup_search():
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
    matrix = vectorizer.fit_transform(df['question'])
    return vectorizer, matrix

vectorizer, matrix = setup_search()

query = st.text_input("Enter your medical question:", placeholder="What are symptoms of diabetes?")

if st.button("Get Answer", type="primary") and query:
    scores = cosine_similarity(vectorizer.transform([query]), matrix).flatten()
    idx = scores.argmax()

    if scores[idx] > 0.2:
        st.success("**Answer:**")
        st.write(df.iloc[idx]['answer'])
        with st.expander("Matched Question"):
            st.write(df.iloc[idx]['question'])
        st.info(f"Confidence: {scores[idx]:.1%}")
    else:
        st.error("No relevant answer found. Please rephrase your question.")

st.sidebar.metric("Total Q&A Pairs", f"{len(df):,}")
st.sidebar.caption("Dataset: MedQuAD v1.0 | Disclaimer: For educational use only")
