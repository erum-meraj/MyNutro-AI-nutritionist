from flask import Flask, render_template, request, jsonify
import flask_cors 
import warnings
from pathlib import Path as p
from pprint import pprint

import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

GOOGLE_API_KEY = "AIzaSyCYeE0wT2nMhNV5aIwp1tpLrdKc37GRizM"
warnings.filterwarnings("ignore")
model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)

pdf_loader = PyPDFLoader("python-server/info.pdf")
pages = pdf_loader.load_and_split()
# print(pages[3].page_content)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})


template = """You are a helpful Nutritionist Assistant who makes diet plans according to the user's need. Use the following pieces of context to make a daily diet plan with the food suggestions addhearing to the concerns. Keep the answer as concise as possible.
    {context}
    write a clear diet plan in a short concise manner.
    these are the requirements for the diet: {question}
    """

question = """    Make the diet plan such that it can fix this problem: {issue}

    The food should be of the cuisine of this country: {cusine}

    and the food prefenrence is: {pref}"""

    
app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    print(text)
    user_issue = "I am iron deficient"
    user_cuise = "Indian"
    user_pref = "Vegetarian"
    question.format(issue= user_issue, cusine= user_cuise, pref= user_pref)
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    result = qa_chain({"query": question})
    return jsonify(result["result"])

if __name__ == "__main__":
    app.run()