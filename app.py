import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

st.set_page_config(page_title="ArXiv CS Assistant", layout="wide", page_icon="🎓")
st.title("🎓 ArXiv Computer Science AI Expert Assistant")

# Sidebar
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password", help="Get free key at console.groq.com")

tab1, tab2, tab3 = st.tabs(["💬 AI Expert Chatbot", "🔍 Search & Summarize Papers", "📊 Concept Graph"])

# TAB 1: CHATBOT
with tab1:
    st.header("Ask CS Research Questions")
    if not api_key:
        st.info("👈 Please enter your Groq API Key in the left sidebar to start chatting.")
    else:
        try:
            df = pd.read_csv('cs_papers_subset.csv').head(500)
            texts = [f"Title: {r['title']}\nAbstract: {r['abstract']}" for _, r in df.iterrows()]
            
            class TFIDFEmbeddings(Embeddings):
                def __init__(self, vec): self.vec = vec
                def embed_documents(self, d): return self.vec.transform(d).toarray().tolist()
                def embed_query(self, q): return self.vec.transform([q]).toarray()[0].tolist()

            vec = TfidfVectorizer(max_features=384)
            vec.fit(texts)
            embeddings = TFIDFEmbeddings(vec)
            
            vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
            llm = ChatGroq(temperature=0.3, groq_api_key=api_key, model_name="llama-3.1-8b-instant")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if prompt := st.chat_input("Ask about Neural Networks, Transformers, etc..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Searching relevant papers and generating answer..."):
                        docs = retriever.invoke(prompt)
                        context = "\n\n".join([d.page_content for d in docs])
                        system_msg = f"You are an AI research assistant. Answer the question using this context:\n{context}\n\nQuestion: {prompt}"
                        res = llm.invoke(system_msg)
                        
                        st.markdown(res.content)
                        with st.expander("📚 Referenced Papers"):
                            for doc in docs:
                                st.write(f"- **{doc.metadata.get('title', 'CS Paper')}**")
                                
                st.session_state.messages.append({"role": "assistant", "content": res.content})
        except Exception as e:
            st.error(f"Error: {e}")

# TAB 2: SEARCH
with tab2:
    st.header("Search CS Papers")
    query = st.text_input("Enter search keywords (e.g. Vision, Attention, Graph):")
    if query:
        df = pd.read_csv('cs_papers_subset.csv')
        matches = df[df['abstract'].str.contains(query, case=False, na=False)].head(5)
        if not matches.empty:
            for _, row in matches.iterrows():
                st.subheader(row['title'])
                st.caption(f"Authors: {row['authors']}")
                st.write(row['abstract'])
                st.divider()
        else:
            st.info("No matching papers found.")

# TAB 3: GRAPH
with tab3:
    st.header("Computer Science Concept Taxonomy")
    G = nx.Graph()
    G.add_edges_from([
        ("Machine Learning", "Deep Learning"),
        ("Deep Learning", "Transformers"),
        ("Deep Learning", "Computer Vision"),
        ("Transformers", "LLMs"),
        ("LLMs", "RAG Systems")
    ])
    fig, ax = plt.subplots(figsize=(7, 3.5))
    nx.draw_networkx(G, with_labels=True, node_color='#90caf9', node_size=1800, font_size=8, ax=ax)
    st.pyplot(fig)