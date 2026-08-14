import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

print("1. Loading CSV dataset...")
df = pd.read_csv('cs_papers_subset.csv')

# Fast and accurate 500 papers
df = df.head(500)

documents = []
texts = []
for idx, row in df.iterrows():
    content = f"Title: {row['title']}\nAuthors: {row['authors']}\nAbstract: {row['abstract']}"
    doc = Document(
        page_content=content,
        metadata={"id": str(row['id']), "title": str(row['title'])}
    )
    documents.append(doc)
    texts.append(content)

print(f"Total documents prepared: {len(documents)}")

# Standalone Lightweight Custom Embedder (Bypasses HuggingFace snapshot bugs)
print("2. Generating local mathematical vector embeddings...")
class TFIDFEmbeddings(Embeddings):
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
    def embed_documents(self, docs):
        vecs = self.vectorizer.transform(docs).toarray()
        return vecs.tolist()
    def embed_query(self, query):
        vec = self.vectorizer.transform([query]).toarray()
        return vec[0].tolist()

vectorizer = TfidfVectorizer(max_features=384)
vectorizer.fit(texts)
embeddings = TFIDFEmbeddings(vectorizer)

print("3. Storing into Chroma Vector Database...")
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("\nSUCCESS: Chroma Vector Database created successfully!")