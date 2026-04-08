from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # 👈 THIS LINE IS REQUIRED

llm = ChatGoogleGenerativeAI(model="gemini-pro")

print(llm.invoke("Hello").content)