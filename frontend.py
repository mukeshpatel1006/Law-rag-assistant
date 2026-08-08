# ============================================================
# LAW BOOK RAG CHATBOT - FRONTEND
# Streamlit User Interface
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import os
import tempfile

import streamlit as st

# Import backend functions
from backend import (
    create_vectorstore,
    ask_question,
    generate_questions
)


# ============================================================
# 2. STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="Law Book RAG Assistant",

    page_icon="⚖️",

    layout="wide"

)


# ============================================================
# 3. APPLICATION TITLE
# ============================================================

st.title(
    "⚖️ Law Book RAG Assistant"
)

st.write(
    """
Upload your law books or legal PDFs and ask questions
based on their content.
"""
)

st.caption(
    "For educational and research purposes only. "
    "This application is not a substitute for professional "
    "legal advice."
)


# ============================================================
# 4. SESSION STATE
# ============================================================

if "vectorstore" not in st.session_state:

    st.session_state.vectorstore = None


if "documents_ready" not in st.session_state:

    st.session_state.documents_ready = False


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ============================================================
# 5. SIDEBAR
# ============================================================

st.sidebar.title(
    "📚 Law Books"
)


# ------------------------------------------------------------
# PDF uploader
# ------------------------------------------------------------

uploaded_files = st.sidebar.file_uploader(

    "Upload Law Book PDFs",

    type=["pdf"],

    accept_multiple_files=True

)


# ============================================================
# 6. PROCESS DOCUMENTS
# ============================================================

if uploaded_files:

    st.sidebar.write(
        f"📄 {len(uploaded_files)} PDF(s) selected"
    )

    process_button = st.sidebar.button(
        "🔍 Process Documents",
        type="primary"
    )

    if process_button:

        pdf_paths = []

        filenames = []

        try:

            with st.spinner(
                "Processing law books..."
            ):

                # ------------------------------------------------
                # Save uploaded files temporarily
                # ------------------------------------------------

                for uploaded_file in uploaded_files:

                    temp_file = tempfile.NamedTemporaryFile(

                        delete=False,

                        suffix=".pdf"

                    )

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_file.close()

                    pdf_paths.append(
                        temp_file.name
                    )

                    filenames.append(
                        uploaded_file.name
                    )

                # ------------------------------------------------
                # Create vector database
                # ------------------------------------------------

                vectorstore = create_vectorstore(

                    pdf_paths,

                    filenames

                )

                # ------------------------------------------------
                # Store vector database in Streamlit session
                # ------------------------------------------------

                st.session_state.vectorstore = (
                    vectorstore
                )

                st.session_state.documents_ready = (
                    True
                )

                # Clear previous chat
                st.session_state.chat_history = []

            st.sidebar.success(
                "✅ Documents processed successfully!"
            )

        except Exception as error:

            st.sidebar.error(
                f"❌ Error: {error}"
            )

        finally:

            # ------------------------------------------------
            # Delete temporary files
            # ------------------------------------------------

            for path in pdf_paths:

                if os.path.exists(path):

                    os.remove(path)


# ============================================================
# 7. DOCUMENT STATUS
# ============================================================

if st.session_state.documents_ready:

    st.success(
        "✅ Your law books are ready. "
        "You can now ask questions."
    )

else:

    st.info(
        "👈 Upload one or more law-book PDFs "
        "from the sidebar and process them."
    )


# ============================================================
# 8. ASK QUESTIONS
# ============================================================

st.header(
    "💬 Ask Your Law Book"
)


question = st.text_input(

    "Enter your question",

    placeholder=(
        "Example: What are the essential elements "
        "of a valid contract?"
    )

)


# ------------------------------------------------------------
# Ask question button
# ------------------------------------------------------------

if st.button(
    "🤖 Ask Question",
    type="primary"
):

    if not st.session_state.documents_ready:

        st.warning(
            "Please upload and process your law books first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching the law books..."
            ):

                result = ask_question(

                    question,

                    st.session_state.vectorstore

                )

            # ------------------------------------------------
            # Store conversation
            # ------------------------------------------------

            st.session_state.chat_history.append({

                "question": question,

                "answer": result["answer"],

                "sources": result["sources"]

            })

        except Exception as error:

            st.error(
                f"❌ Error: {error}"
            )


# ============================================================
# 9. DISPLAY CONVERSATION
# ============================================================

if st.session_state.chat_history:

    st.header(
        "📖 Conversation"
    )

    for chat in st.session_state.chat_history:

        # ----------------------------------------------------
        # Question
        # ----------------------------------------------------

        st.markdown(
            "### 👤 Question"
        )

        st.write(
            chat["question"]
        )

        # ----------------------------------------------------
        # Answer
        # ----------------------------------------------------

        st.markdown(
            "### 🤖 Answer"
        )

        st.write(
            chat["answer"]
        )

        # ----------------------------------------------------
        # Sources
        # ----------------------------------------------------

        if chat["sources"]:

            st.markdown(
                "### 📚 Sources"
            )

            for source in chat["sources"]:

                st.write(
                    f"📄 {source['file']} "
                    f"— Page {source['page']}"
                )

        st.divider()


# ============================================================
# 10. GENERATE QUESTIONS
# ============================================================

st.header(
    "📝 Generate Practice Questions"
)


number_of_questions = st.slider(

    "Number of questions",

    min_value=5,

    max_value=20,

    value=10

)


if st.button(
    "🧠 Generate Questions"
):

    if not st.session_state.documents_ready:

        st.warning(
            "Please upload and process your law books first."
        )

    else:

        try:

            with st.spinner(
                "Generating questions from your law books..."
            ):

                questions = generate_questions(

                    st.session_state.vectorstore,

                    number_of_questions

                )

            st.markdown(
                questions
            )

        except Exception as error:

            st.error(
                f"❌ Error: {error}"
            )


# ============================================================
# 11. FOOTER
# ============================================================

st.divider()

st.caption(
    "⚖️ Law Book RAG Assistant | "
    "LangChain + Groq + FAISS + HuggingFace"
)