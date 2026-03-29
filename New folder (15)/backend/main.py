from fastapi import FastAPI
from rag import ask_rag

app = FastAPI()

@app.get("/chat")
def chat(q: str):
    response = ask_rag(q)
    return {"response": response}