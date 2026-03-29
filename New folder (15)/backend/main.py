from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag import ask_rag

app = FastAPI()

# FIXED CORS - allows ALL localhost ports + chrome-error frames
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
async def chat(q: str):
    try:
        response = ask_rag(q)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}