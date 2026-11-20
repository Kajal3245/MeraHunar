import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
   model="gemini-3S.5-flash-lite",
    temperature=0
)


def ask_gemini(question: str):
    response = llm.invoke(question)
    return response.content