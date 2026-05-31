# PDF Question Answering API

A FastAPI-based PDF Question Answering system that allows users to upload a PDF and ask a question about its contents. The application extracts text from the PDF, stores semantic embeddings in a vector database, retrieves the most relevant section, and uses OpenAI to generate an answer based only on the retrieved content.

## Features

* Upload PDF files through a REST API
* Extract text from PDFs using PyPDF
* Split documents into paragraphs
* Generate embeddings using Sentence Transformers
* Store embeddings in ChromaDB
* Perform semantic similarity search
* Retrieve the most relevant PDF section
* Generate answers with OpenAI GPT-4o
* Prevent hallucinations by restricting answers to retrieved PDF content

---

## Tech Stack

* FastAPI
* PyPDF
* ChromaDB
* Sentence Transformers
* OpenAI API
* Python
* dotenv

---

## How It Works

### 1. Upload PDF

The user sends:

* A PDF file
* A question about the PDF

### 2. Extract Text

The PDF is read using `PdfReader` and all page text is combined into a single string.

### 3. Split into Paragraphs

The extracted text is cleaned and split into paragraphs using double line breaks (`\n\n`).

### 4. Create Embeddings

Each paragraph containing at least 5 words is converted into a vector embedding using:

```python
all-MiniLM-L6-v2
```

### 5. Store in ChromaDB

Each paragraph is stored in a Chroma collection along with:

* Paragraph text
* Embedding vector
* PDF filename
* Unique upload code

### 6. Search for Relevant Context

The user's question is converted into an embedding.

ChromaDB performs semantic search to find the most relevant paragraph from the uploaded PDF.

### 7. Generate Answer

The retrieved paragraph is sent to OpenAI GPT-4o with a prompt that instructs the model to:

* Answer only from the provided PDF context
* Avoid making up information
* State when information is missing

### 8. Return Response

The API returns:

```json
{
  "results": "Generated answer"
}
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install fastapi
pip install uvicorn
pip install pypdf
pip install chromadb
pip install sentence-transformers
pip install openai
pip install python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### POST `/uploadfile/`

Upload a PDF and ask a question.

#### Form Data

| Field    | Type     | Description   |
| -------- | -------- | ------------- |
| file     | PDF File | PDF document  |
| question | String   | User question |

#### Example Request

```bash
curl -X POST \
  "http://127.0.0.1:8000/uploadfile/" \
  -F "file=@example.pdf" \
  -F "question=What is the main topic of this document?"
```

#### Example Response

```json
{
  "results": "The document explains..."
}
```

---

## Project Structure

```text
project/
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Current Limitations

* Uses an in-memory ChromaDB client (data is lost when the application stops)
* Retrieves only 1 paragraph (`n_results=1`)
* Simple paragraph chunking may not work well for all PDF formats
* Large PDFs may require more advanced chunking strategies
* No support for multiple simultaneous document collections

---

## Possible Improvements

* Persistent ChromaDB storage
* Better chunking with overlap
* Retrieve multiple relevant chunks
* Streaming responses
* Citation support
* Multi-document querying
* Conversation memory
* PDF upload history
* Authentication and user accounts

---

## License

This project is provided for educational purposes and can be modified and extended as needed.
