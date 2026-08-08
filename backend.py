# ============================================================
# LAW BOOK RAG CHATBOT - BACKEND
# LangChain + Groq + HuggingFace Embeddings + FAISS
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import os
from typing import List

from dotenv import load_dotenv

# LangChain - Groq
from langchain_groq import ChatGroq

# LangChain - HuggingFace embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# PDF loader and FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# LangChain document and prompt classes
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add GROQ_API_KEY to your .env file."
    )


# ============================================================
# 3. INITIALIZE GROQ LLM
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY
)


# ============================================================
# 4. INITIALIZE HUGGINGFACE EMBEDDING MODEL
# ============================================================

# This model runs locally.
# Therefore, no HuggingFace API key is required.

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)


# ============================================================
# 5. TEXT SPLITTER
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# ============================================================
# 6. LOAD PDF
# ============================================================

def load_pdf(pdf_path: str) -> List[Document]:
    """
    Load text from a PDF file.

    Each PDF page becomes a LangChain Document.
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents


# ============================================================
# 7. ADD SOURCE METADATA
# ============================================================

def add_metadata(
    documents: List[Document],
    filename: str
) -> List[Document]:
    """
    Add filename information to every document.
    """

    for document in documents:

        document.metadata["source_file"] = filename

    return documents


# ============================================================
# 8. CREATE FAISS VECTOR DATABASE
# ============================================================

def create_vectorstore(
    pdf_paths: List[str],
    filenames: List[str]
):
    """
    Process multiple PDFs:

    PDF
      ↓
    Text extraction
      ↓
    Text chunks
      ↓
    Embeddings
      ↓
    FAISS vector database
    """

    all_documents = []

    # --------------------------------------------------------
    # Load every uploaded PDF
    # --------------------------------------------------------

    for pdf_path, filename in zip(
        pdf_paths,
        filenames
    ):

        documents = load_pdf(
            pdf_path
        )

        documents = add_metadata(
            documents,
            filename
        )

        all_documents.extend(
            documents
        )

    # --------------------------------------------------------
    # Check if PDF contains text
    # --------------------------------------------------------

    if not all_documents:

        raise ValueError(
            "No text could be extracted from the uploaded PDFs."
        )

    # --------------------------------------------------------
    # Split documents into chunks
    # --------------------------------------------------------

    chunks = text_splitter.split_documents(
        all_documents
    )

    # --------------------------------------------------------
    # Create FAISS vector database
    # --------------------------------------------------------

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore


# ============================================================
# 9. CREATE RETRIEVER
# ============================================================

def create_retriever(vectorstore):
    """
    Create a similarity-based retriever.

    k = 5 means retrieve the 5 most relevant chunks.
    """

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5
        }
    )

    return retriever


# ============================================================
# 10. RAG PROMPT
# ============================================================

rag_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are a legal-book question answering assistant.

Your task is to answer questions using ONLY the
provided context from the uploaded law books.

IMPORTANT RULES:

1. Use the provided context as the primary source.

2. Do not invent sections, cases, articles,
   judgments, legal principles, dates, or facts.

3. If the answer is not present in the uploaded
   documents, clearly say:

   "The answer was not found in the uploaded documents."

4. Explain the answer clearly and simply.

5. If the context contains a section number,
   chapter name, case name, page number, or other
   source information, mention it when relevant.

6. Do not create fake legal citations.

7. Do not claim that information came from the
   uploaded book unless it is actually supported
   by the retrieved context.

8. If the question is unrelated to the uploaded
   documents, explain that the uploaded documents
   do not contain the required information.

CONTEXT:

{context}
"""
    ),

    (
        "human",
        "{question}"
    )

])


# ============================================================
# 11. FORMAT RETRIEVED DOCUMENTS
# ============================================================

def format_documents(
    documents: List[Document]
) -> str:
    """
    Convert retrieved documents into a formatted
    context string for the LLM.
    """

    formatted_documents = []

    for document in documents:

        source = document.metadata.get(
            "source_file",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        text = document.page_content

        formatted_documents.append(
            f"""
Source File: {source}
Page: {page}

{text}
"""
        )

    return "\n\n".join(
        formatted_documents
    )


# ============================================================
# 12. ASK QUESTION USING RAG
# ============================================================

def ask_question(
    question: str,
    vectorstore
):
    """
    Complete RAG pipeline:

    Question
       ↓
    Retriever
       ↓
    Relevant chunks
       ↓
    Context
       ↓
    Groq LLM
       ↓
    Answer + Sources
    """

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    retriever = create_retriever(
        vectorstore
    )

    # --------------------------------------------------------
    # Retrieve relevant documents
    # --------------------------------------------------------

    retrieved_documents = retriever.invoke(
        question
    )

    # --------------------------------------------------------
    # No relevant documents
    # --------------------------------------------------------

    if not retrieved_documents:

        return {
            "answer": (
                "The answer was not found in "
                "the uploaded documents."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # Create context
    # --------------------------------------------------------

    context = format_documents(
        retrieved_documents
    )

    # --------------------------------------------------------
    # Create RAG prompt
    # --------------------------------------------------------

    prompt = rag_prompt.invoke({

        "context": context,

        "question": question

    })

    # --------------------------------------------------------
    # Ask Groq
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )

    # --------------------------------------------------------
    # Collect source information
    # --------------------------------------------------------

    sources = []

    for document in retrieved_documents:

        source = document.metadata.get(
            "source_file",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        source_info = {
            "file": source,
            "page": page
        }

        if source_info not in sources:

            sources.append(
                source_info
            )

    # --------------------------------------------------------
    # Return answer and sources
    # --------------------------------------------------------

    return {

        "answer": response.content,

        "sources": sources

    }


# ============================================================
# 13. QUESTION GENERATION PROMPT
# ============================================================

question_generation_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an expert law professor.

Using ONLY the provided context from the uploaded
law book, generate useful study questions.

Questions can test:

- Definitions
- Legal principles
- Sections
- Concepts
- Exceptions
- Case laws
- Factual understanding
- Conceptual understanding

Do not create information that is not present
in the provided context.

Generate exactly {number} questions.

Return ONLY a numbered list.

CONTEXT:

{context}
"""
    )

])


# ============================================================
# 14. GENERATE QUESTIONS FROM LAW BOOK
# ============================================================

def generate_questions(
    vectorstore,
    number: int = 10
):
    """
    Generate practice questions from the uploaded
    law books.
    """

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    retriever = create_retriever(
        vectorstore
    )

    # --------------------------------------------------------
    # Retrieve important legal content
    # --------------------------------------------------------

    documents = retriever.invoke(
        """
        important legal concepts,
        definitions,
        sections,
        case laws,
        principles,
        exceptions
        """
    )

    # --------------------------------------------------------
    # Format context
    # --------------------------------------------------------

    context = format_documents(
        documents
    )

    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = question_generation_prompt.invoke({

        "context": context,

        "number": number

    })

    # --------------------------------------------------------
    # Generate questions
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )

    return response.content


# ============================================================
# 15. SAVE FAISS VECTOR DATABASE
# ============================================================

def save_vectorstore(
    vectorstore,
    path="law_vectorstore"
):
    """
    Save FAISS vector database locally.
    """

    vectorstore.save_local(
        path
    )


# ============================================================
# 16. LOAD FAISS VECTOR DATABASE
# ============================================================

def load_vectorstore(
    path="law_vectorstore"
):
    """
    Load an existing FAISS vector database.

    Only load FAISS files that you trust.
    """

    vectorstore = FAISS.load_local(

        path,

        embeddings,

        allow_dangerous_deserialization=True

    )

    return vectorstore