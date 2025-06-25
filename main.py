from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from typing import Dict, Any
import json
from llm_agent.agent_multi import run_pinescript_agent

# Create FastAPI app
app = FastAPI(
    title="Finance Trading Assistant API",
    description="LangServe API for trading strategy consultation and PineScript generation",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a runnable that processes chat queries
def process_chat(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process chat input and return formatted response
    """
    query = input_dict.get("query", "")
    previous_summary = input_dict.get("previous_summary", "No previous conversation.")
    
    # Call the agent
    result, _, _, _, _ = run_pinescript_agent(query, previous_summary)
    
    # Parse the JSON response
    try:
        parsed = json.loads(result)
        return {
            "answer": parsed.get("answer", ""),
            "code": parsed.get("code"),
            "chatsummary": parsed.get("chatsummary", "")
        }
    except json.JSONDecodeError:
        return {
            "answer": result,
            "code": None,
            "chatsummary": f"User asked: {query}"
        }

# Create a LangChain runnable
chat_runnable = RunnableLambda(process_chat)

# Add LangServe routes
add_routes(
    app,
    chat_runnable,
    path="/chat",
)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "3.0.0",
        "type": "LangServe API",
        "features": [
            "Stateless chat processing",
            "PineScript code generation", 
            "Trading strategy consultation",
            "Conversation summaries"
        ]
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Finance Trading Assistant LangServe API",
        "version": "3.0.0",
        "endpoints": {
            "chat": "/chat",
            "invoke": "/chat/invoke",
            "batch": "/chat/batch",
            "stream": "/chat/stream",
            "playground": "/chat/playground"
        },
        "docs": "/docs",
        "example": {
            "url": "POST /chat/invoke",
            "request": {
                "input": {
                    "query": "Create a simple RSI strategy",
                    "previous_summary": "Previously discussed MACD strategies"
                }
            },
            "response": {
                "output": {
                    "answer": "The RSI strategy explanation...",
                    "code": "//@version=5\\n...",
                    "chatsummary": "User requested RSI strategy after MACD discussion"
                }
            }
        }
    }