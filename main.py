from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer
import os
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile, Form
from io import BytesIO
from dotenv import load_dotenv
import uuid


app = FastAPI()

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.Client()

model = SentenceTransformer('all-MiniLM-L6-v2')

collection = client.create_collection("my_notes")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(), question: str = Form()):
    code = str(uuid.uuid4())

    contents = await file.read()
    pdf_file_like = BytesIO(contents)

    reader = PdfReader(pdf_file_like)

    full_text = ''

    for page in reader.pages:
        full_text += page.extract_text()

    text = full_text.replace("\r", "")
    paragraphs = text.split("\n\n")

    print(text)

    for i, paragraph in enumerate(paragraphs):
        words = len(paragraph.split())
        if words >= 5:
            embedding = model.encode(paragraph).tolist()

            collection.add(
                documents=[paragraph],
                embeddings=[embedding],
                ids=[str(i)],
                metadatas=[{'filename': file.filename, 'code': code}]
            )
        else:
            continue

    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1,
        where={"$and": [{'filename': file.filename}, {'code': code}]})

    answer = results["documents"]

    client_2 = OpenAI(api_key=api_key)

    response = client_2.responses.create(
        model="gpt-4o",
        input=f'''
        You are an AI assistant for a PDF question-answering system.

    Your job is to answer the user's question using ONLY the retrieved PDF context below.

    If the answer is clearly contained in the context:
    - Give a concise and accurate answer.
    - Explain simply when needed.
    - Quote small relevant parts if useful.

    If the context is incomplete or does not contain the answer:
    - Say that the PDF does not provide enough information.
    - Do NOT make up facts or hallucinate.

    User Question:
    {question}

    Retrieved PDF Context:
    {answer}

    Answer:
    '''
    )

    return {'results': response.output_text}
