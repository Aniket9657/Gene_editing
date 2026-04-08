from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

# Schema
class Review(TypedDict):
    summary: str
    sentiment: str

# Correct model name ✅
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0
)

structured_model = model.with_structured_output(Review)

prompt = """
Extract:
1. Summary
2. Sentiment (positive, negative, neutral)

Review:
Carlos was the best! He was very patient and honest. Great experience!
"""

result = structured_model.invoke(prompt)

print(result)