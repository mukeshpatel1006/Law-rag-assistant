# ⚖️ Law Book RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** based legal document chatbot built using **LangChain, Groq, HuggingFace Embeddings, FAISS, PyPDF, and Streamlit**.

The application allows users to upload one or more law books or legal documents in PDF format, ask questions based on their content, generate practice questions, and receive answers grounded in the uploaded documents with source file and page information.

---

# ⚖️ Law Book RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot for interacting with law books and legal documents.

## 🚀 Live Demo

🔗 **[Open Law Book RAG Chatbot](https://frontendpy-dhtqcrhfxkmbuenxdk2rvx.streamlit.app/)**

### ✨ What you can do

- 📚 Upload law books and legal PDFs
- 💬 Ask questions based on uploaded documents
- 🔎 Retrieve relevant document content
- 🤖 Generate answers using Groq
- 📄 View source PDF and page information
- 📝 Generate practice questions

---

## 🚀 Project Overview

Reading and searching through large law books can be time-consuming. This project provides an AI-powered interface for interacting with legal documents.

Instead of directly asking an LLM to answer a question from its general knowledge, the application first searches the uploaded law books for relevant information and then provides that information as context to the LLM.

### Main Workflow

```text
Law Book / Legal PDF
        │
        ▼
   PDF Extraction
       PyPDF
        │
        ▼
   Text Chunking
RecursiveCharacterTextSplitter
        │
        ▼
 HuggingFace Embeddings
 all-MiniLM-L6-v2
        │
        ▼
      FAISS
 Vector Database
        │
        ▼
   User Question
        │
        ▼
    Retriever
        │
        ▼
 Relevant PDF Chunks
        │
        ▼
     RAG Prompt
        │
        ▼
      Groq LLM
        │
        ▼
 Answer + Sources
```

---

# ✨ Features

* 📚 Upload multiple law books or legal PDFs
* 🔎 Semantic search over uploaded documents
* 💬 Ask questions about uploaded law books
* 🤖 Generate answers using Groq LLM
* 📄 Display source PDF and page information
* 📝 Generate practice questions
* 🧠 HuggingFace local embeddings
* ⚡ FAISS vector database
* 🔗 LangChain-based RAG pipeline
* 🌐 Streamlit web interface
* 🔐 Secure API-key handling using `.env` and Streamlit Secrets
* 📖 Context-grounded responses
* ⚠️ Designed to reduce hallucination by instructing the model to use retrieved document context

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │     frontend.py     │
                    └──────────┬──────────┘
                               │
                     Upload PDF / Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │      backend.py     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    PDF Processing   │
                    │       PyPDF         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Text Chunking    │
                    │ Recursive Splitter  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embeddings      │
                    │ HuggingFace Model   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        FAISS        │
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
                        User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Retriever       │
                    │   Top-K Chunks      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     RAG Prompt      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Groq LLM      │
                    │ Llama 3.3 70B       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Answer + Sources  │
                    └─────────────────────┘
```

---

# 🧠 How RAG Works

RAG stands for **Retrieval-Augmented Generation**.

The system does not simply send the user's question directly to the LLM.

Instead:

```text
Question
   ↓
Search uploaded documents
   ↓
Retrieve relevant chunks
   ↓
Add chunks to prompt
   ↓
Send context + question to LLM
   ↓
Generate answer
```

For example:

```text
User Question:

"What are the essential elements of a valid contract?"
```

The retriever searches the uploaded law books and finds relevant passages.

Those passages are provided to the Groq LLM as context.

The LLM then generates the answer based on the retrieved content.

---

# 📂 Project File Structure

```text
law-book-rag-chatbot/
│
├── backend.py
│
├── frontend.py
│
├── requirements.txt
│
├── .gitignore
│
├── README.md
│
├── .env
│
└── myenv/
```

### Important

The following files/folders should **NOT be uploaded to GitHub**:

```text
.env
myenv/
```

They are excluded through `.gitignore`.

---

# 📄 File Description

## `backend.py`

Contains the complete backend/RAG pipeline.

Responsibilities:

```text
PDF Loading
     ↓
Document Processing
     ↓
Text Chunking
     ↓
Embeddings
     ↓
FAISS Vector Store
     ↓
Retriever
     ↓
RAG Prompt
     ↓
Groq LLM
     ↓
Answer Generation
```

It also contains the practice-question generation functionality.

---

## `frontend.py`

Contains the complete Streamlit interface.

Responsibilities:

* PDF upload
* Document processing
* Question input
* Answer display
* Source display
* Chat history
* Practice-question generation
* Application status

---

## `requirements.txt`

Contains all Python dependencies required by the project.

---

## `.env`

Contains the Groq API key during local development.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

This file must not be uploaded to GitHub.

---

## `.gitignore`

Prevents sensitive and unnecessary files from being committed.

Recommended:

```gitignore
# Virtual environments
myenv/
venv/
.venv/

# Environment variables
.env

# Python cache
__pycache__/
*.py[cod]

# Jupyter
.ipynb_checkpoints/

# Streamlit secrets
.streamlit/secrets.toml

# OS files
.DS_Store
Thumbs.db
```

---

# 🛠️ Technologies Used

| Technology            | Purpose                           |
| --------------------- | --------------------------------- |
| Python                | Core programming language         |
| Streamlit             | Web application/frontend          |
| LangChain             | RAG pipeline/orchestration        |
| Groq                  | Large Language Model              |
| HuggingFace           | Local text embeddings             |
| Sentence Transformers | Embedding model                   |
| FAISS                 | Vector similarity search          |
| PyPDF                 | PDF text extraction               |
| python-dotenv         | Environment variable management   |
| PyTorch               | Backend dependency for embeddings |

---

# 🤖 AI Model

The application uses a Groq-hosted LLM through LangChain.

Current configuration:

```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY
)
```

The temperature is set to `0` to encourage more deterministic responses.

> Model availability can change over time. If Groq retires or changes a model name, update the model name in `backend.py`.

---

# 🧠 Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

through LangChain's HuggingFace integration.

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)
```

The embedding model runs locally, so a separate HuggingFace API key is not required for this configuration.

---

# 🔎 Vector Database

The project uses **FAISS**.

FAISS stores the generated document embeddings and performs similarity search.

```text
PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
FAISS
```

When a user asks a question:

```text
Question
 ↓
Question embedding
 ↓
FAISS similarity search
 ↓
Top relevant chunks
```

The current retriever uses:

```python
search_kwargs={
    "k": 5
}
```

Therefore, the system retrieves the five most relevant chunks.

---

# 📚 PDF Processing

PDFs are loaded using:

```python
PyPDFLoader
```

Each uploaded PDF is processed and split into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

Current configuration:

```python
chunk_size=1200
chunk_overlap=200
```

The overlap helps preserve context between neighboring chunks.

---

# 💬 Question Answering Pipeline

The complete question-answering process is:

```text
1. User uploads PDF
        ↓
2. PDF text extraction
        ↓
3. Text is divided into chunks
        ↓
4. Chunks are converted into embeddings
        ↓
5. Embeddings are stored in FAISS
        ↓
6. User asks a question
        ↓
7. Retriever searches FAISS
        ↓
8. Top relevant chunks are retrieved
        ↓
9. Retrieved chunks become RAG context
        ↓
10. Context + question are sent to Groq
        ↓
11. Groq generates the answer
        ↓
12. Source PDF/page information is displayed
```

---

# 📝 Practice Question Generation

The application can also generate questions from uploaded documents.

Example:

```text
Uploaded Law Book
       ↓
Relevant Legal Content
       ↓
Groq LLM
       ↓
Practice Questions
```

Generated questions can cover:

* Definitions
* Legal principles
* Sections
* Concepts
* Exceptions
* Case laws
* Factual understanding
* Conceptual understanding

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/law-book-rag-chatbot.git
```

Move into the project:

```bash
cd law-book-rag-chatbot
```

---

# 🐍 2. Create Virtual Environment

```bash
python -m venv myenv
```

---

# ▶️ 3. Activate Virtual Environment

### Windows PowerShell

```powershell
.\myenv\Scripts\Activate.ps1
```

You should see:

```text
(myenv)
```

at the beginning of your terminal.

---

# 📦 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 5. Configure Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

The application reads the key using:

```python
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

Never hard-code the API key inside Python source code.

---

# ▶️ 6. Run the Application

Start Streamlit:

```bash
streamlit run frontend.py
```

The application will open in your browser.

---

# 📖 7. Using the Application

### Step 1

Upload one or more law books:

```text
Indian_Contract_Act.pdf
Indian_Constitution.pdf
Evidence_Act.pdf
Company_Law.pdf
```

### Step 2

Click:

```text
Process Documents
```

### Step 3

Wait for:

```text
Documents processed successfully
```

### Step 4

Ask a question.

Example:

```text
What are the essential elements of a valid contract?
```

### Step 5

Click:

```text
Ask Question
```

The application returns:

```text
Answer
+
Source PDF
+
Page number
```

---

# ☁️ Streamlit Deployment

The application can be deployed using Streamlit Community Cloud.

## GitHub Repository

The repository should contain:

```text
law-book-rag-chatbot/
│
├── backend.py
├── frontend.py
├── requirements.txt
├── .gitignore
└── README.md
```

Do not upload:

```text
.env
myenv/
```

---

# 🚀 Streamlit Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Create a new application.
5. Select the repository.
6. Select the `main` branch.
7. Set the main file to:

```text
frontend.py
```

8. Select a compatible Python version.
9. Add the Groq API key through Streamlit Secrets.
10. Deploy the application.

---

# 🔐 Streamlit Secrets

For deployment, do not upload `.env`.

Instead, add the secret through Streamlit:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

The application can then retrieve the secret securely.

---

# 🔒 Security

Never commit:

```text
GROQ_API_KEY
.env
```

to GitHub.

The API key should be stored using:

### Local development

```text
.env
```

### Streamlit Cloud

```text
Streamlit Secrets
```

If an API key is accidentally exposed, revoke it immediately and generate a new key.

---

# 📌 Important Document Considerations

The application allows users to upload PDF documents directly through Streamlit.

Law books should generally **not be uploaded to a public GitHub repository** unless you have the necessary rights to redistribute them.

Instead:

```text
GitHub
   │
   ├── Application Code
   ├── Requirements
   └── Documentation
       
Streamlit
   │
   └── User Uploads Legal PDFs
```

---

# ⚠️ Legal Disclaimer

This project is intended for **educational and research purposes only**.

The chatbot's responses should not be treated as professional legal advice.

AI-generated responses may contain errors or incomplete interpretations. Important legal information should always be verified against authoritative legal sources, legislation, case law, and qualified legal professionals.

---

# 🔮 Future Improvements

Potential improvements include:

* 🔐 Multi-user document isolation
* 💾 Persistent vector database
* 🧠 Conversation memory
* 📑 Better page-level citations
* 🔎 Hybrid keyword + semantic search
* 🎯 Reranking retrieved documents
* 📝 Automatic MCQ generation
* ✅ Interactive MCQ quiz mode
* 📊 Quiz score tracking
* 📚 Document-specific selection
* 🔄 Clear and re-index documents
* 📷 OCR support for scanned law books
* 🔍 Advanced legal entity extraction
* 📜 Section and case-law detection
* 🌐 Multi-language support
* 🎤 Voice-based questions
* 📥 Export answers and questions
* 👥 User authentication

---

# 📊 RAG Performance Improvements

Future versions can improve retrieval quality using:

```text
Current:

Question
   ↓
FAISS Similarity Search
   ↓
Top-K Documents
   ↓
LLM
```

Improved:

```text
Question
   ↓
Hybrid Search
 ┌───────────────┐
 │ BM25          │
 │ +             │
 │ Vector Search │
 └───────┬───────┘
         ↓
     Reranking
         ↓
 Relevant Context
         ↓
       LLM
         ↓
 Answer + Citations
```

This can improve retrieval accuracy for legal terminology, section numbers, and exact phrases.

---

# 👨‍💻 Author

**Mukesh Kumar**

Computer Science & Engineering

Built using:

```text
Python
LangChain
RAG
Groq
HuggingFace
FAISS
PyPDF
Streamlit
```

---

# ⭐ Project Goal

The goal of this project is to demonstrate how **Retrieval-Augmented Generation (RAG)** can be applied to large legal documents to create a document-grounded question-answering system.

```text
Large Legal Documents
        +
Semantic Retrieval
        +
Large Language Model
        ↓
AI-Powered Legal Document Assistant
```

> This project is a technical/educational demonstration of RAG and should not be used as a replacement for professional legal research or legal advice.
