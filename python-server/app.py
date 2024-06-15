from flask import Flask, render_template, request, jsonify
import flask_cors 
import openai
import sys
import os
import re
import langchain
import langchain.embeddings
import langchain_community
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI


default_prompt = """You are a helpful Nutritionist Assistant who makes diet plans according to the user's need.

    Make the food such that it can fix this problem: {issue}

    The food should be of the cuisine: {cusine}

    and the food prefenrence is: {pref}

    make a daily diet plan with the food suggestions addhearing to the concerns.

    write a clear diet plan in a short concise manner.
    
    """

prompt_temp = """You are a helpful Nutritionist Assistant who makes diet plans according to the user's need.

    Make the food such that it can fix this problem: {issue}

    The food should be of the cuisine: {cusine}

    and the food prefenrence is: {pref}
"""



os.environ["OPENAI_API_KEY"] = "AIzaSyCYeE0wT2nMhNV5aIwp1tpLrdKc37GRizM"
loader = PyPDFLoader("chatdata.pdf")
pages = loader.load_and_split()
chunks = pages
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(chunks, embeddings)
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, verbose=True)
qa = ConversationalRetrievalChain.from_llm(llm = chat_model, retriever=db.as_retriever())


def res(user_issue, user_cusine, user_pref):
    result = qa({"question": prompt_temp(user_issue, user_cusine, user_pref), "system": default_prompt})
    print(result)
    return result['answer']
    
app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = res(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run()