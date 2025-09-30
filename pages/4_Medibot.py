import os
import asyncio
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# LangChain & Groq Imports
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv(find_dotenv())
nest_asyncio.apply()

st.sidebar.markdown("<h2 style='color: #ffffff;'>📌 Description</h2>", unsafe_allow_html=True)
st.sidebar.image("utils/ph2.png", use_container_width=True)
st.sidebar.markdown("<p class='sidebar-text'>The LLM Medical Chatbot is an AI-powered assistant designed to provide instant, accurate, and reliable healthcare insights.</p>", unsafe_allow_html=True)

# Ensure async loop is running
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Constants
DB_FAISS_PATH = "vectorstore/db_faiss"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your environment.")
    st.stop()

@st.cache_resource
def load_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

vectorstore = load_vectorstore()

def get_prompt_template():
    return PromptTemplate(
        template="""Use the provided context to answer the user's question.
If you don't know the answer, say "I don't know" instead of making one up. Always stay within the given context.

**Context:**
{context}

**Question:**
{question}

Please provide a **concise and informative response**.
        """,
        input_variables=["context", "question"]
    )

def load_llm():
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    return ChatGroq(
        temperature=0.5,
        model_name="llama-3.3-70b-versatile"
    )

def format_sources(source_documents):
    if not source_documents:
        return "**Sources:** No sources found."
    formatted_sources = "\n\n**Sources:**"
    for idx, doc in enumerate(source_documents, start=1):
        formatted_sources += f"\n🔹 **Source {idx}:** {doc.metadata.get('source', 'Unknown Source')}"
    return formatted_sources

def main():
    st.title("💬 Medibot - AI Health Assistant")
    st.markdown("""
        **Ask any medical-related question, and I'll provide insights based on reliable information!**
        🤖🩺 *Powered by AI & Meta(llama)*
    """)

    with st.sidebar:
        st.markdown("""
        ### 🔍 About Medibot:
        - Uses **Meta-llama (Groq)** to answer medical queries
        - Retrieves relevant medical data from a knowledge base
        - Provides **fast, reliable, and contextual responses**
        """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    user_query = st.chat_input("Type your medical query...")

    if user_query:
        st.chat_message("user").markdown(f"**You:** {user_query}")
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.spinner("🤖 Medibot is thinking..."):
            try:
                if vectorstore is None:
                    st.error("❌ Error: Vector store failed to load.")
                    return

                qa_chain = RetrievalQA.from_chain_type(
                    llm=load_llm(),
                    chain_type="stuff",
                    retriever=vectorstore.as_retriever(search_kwargs={'k': 5}),
                    return_source_documents=True,
                    chain_type_kwargs={'prompt': get_prompt_template()}
                )

                response = qa_chain.invoke({'query': user_query})
                result = response.get("result", "⚠️ No response generated.")
                sources = response.get("source_documents", [])

                formatted_response = f"**Medibot:** {result}\n\n{format_sources(sources)}"
                st.chat_message("assistant").markdown(formatted_response)
                st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()
