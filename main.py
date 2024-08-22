from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from dotenv import load_dotenv
import google.generativeai as genai
import os                
from typing import List

# Create an instance of FastAPI
app = FastAPI()

# Database setup
DATABASE_URL = "postgresql://postgres:password@localhost:5432/chatdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.now())

Base.metadata.create_all(bind=engine)

# Pydantic model for incoming requests
class QueryInput(BaseModel):
    input: str

# Pydantic model for response
class ChatHistoryResponse(BaseModel):
    id: int
    user_input: str
    agent_response: str
    timestamp: str

    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            user_input=orm_obj.user_input,
            agent_response=orm_obj.agent_response,
            timestamp=orm_obj.timestamp.strftime("%d-%m-%Y at %H:%M:%S")  # Format here
        )
# Initialize memory
memory = ConversationBufferMemory()

# Endpoint for the agent
@app.post("/ask")
async def ask_agent(query: QueryInput, db: Session = Depends(get_db)):
    # Prepare the input for the agent
    inputs = {"input": query.input}
    # Invoke the agent executor with the inputs
    response = agent_executor.invoke(inputs)
    # Save the chat history to the database
    save_chat_history(query.input, response["output"], db)
    return {"response": response["output"]}

# Endpoint to get chat history
@app.get("/chat_history", response_model=List[ChatHistoryResponse])
async def get_chat_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    chat_history = db.query(ChatHistory).offset(skip).limit(limit).all()
    return [ChatHistoryResponse.from_orm(chat) for chat in chat_history]

# Function to save chat history in PostgreSQL
def save_chat_history(user_input: str, agent_response: str, db: Session):
    chat_record = ChatHistory(user_input=user_input, agent_response=agent_response)
    db.add(chat_record)
    db.commit()
    db.refresh(chat_record)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Load environment variables
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize tools
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
duckduckgo = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper, source="news")

loader = PyPDFLoader("Knowledgebase.pdf")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
vectordb = Chroma.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
retriever = vectordb.as_retriever()
retriever_tool = create_retriever_tool(retriever, "bus_information_search", "Search for information regarding bus schedules, routes, fares, and other relevant information. For any questions about Bus related information, you must use this tool!")

tools = [retriever_tool, wiki, duckduckgo]

# Initialize LLM and Agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_tools_agent(llm, tools, prompt)

# Initialize Agent Executor with memory
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

if __name__ == "__main__":
    # Example query with memory
    response = agent_executor.invoke({"input": "What is route for airport?"})
    print(response)