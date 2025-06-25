from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from core.config import settings
# Import V2 router for PineScript trading assistant
try:
    from routers import chat_v2
    V2_AVAILABLE = True
except ImportError:
    print("Warning: chat_v2 router not found. Please create chat_v2.py in routers folder.")
    V2_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="PineScript Trading Assistant API",
    description="Backend API for PineScript Trading Strategy Assistant with Thread Management",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers based on availability
if V2_AVAILABLE:
    app.include_router(chat_v2.router, prefix="/api")
    print("✅ V2 chat router loaded")
else:
    print("❌ V2 chat router not available")

# Collections router disabled - not needed for PineScript trading assistant
# from routers import collections  # DISABLED

# Create storage directories on startup
@app.on_event("startup")
async def startup_event():
    # V2 storage structure (user folders)
    os.makedirs(f"{settings.STORAGE_PATH}/chat", exist_ok=True)
    
    # Other storage paths
    os.makedirs(f"{settings.STORAGE_PATH}/generated_pdfs", exist_ok=True)
    os.makedirs(f"{settings.STORAGE_PATH}/generated_word", exist_ok=True)
    
    print(f"🚀 PineScript Trading Assistant API started. Storage path: {settings.STORAGE_PATH}")
    
    if V2_AVAILABLE:
        print("🆕 V2 Features: Thread management, user folders, named conversations")
        print("📈 PineScript Features: Trading strategy consulting, PineScript code generation")
    
    print("📈 Available endpoints:")
    if V2_AVAILABLE:
        print("  - POST /api/chat/new (create conversation)")
        print("  - GET  /api/chat/list (list conversations)")
        print("  - POST /api/chat/{id}/message (send message with trading questions)")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "app_type": "PineScript Trading Assistant",
        "routers_loaded": {
            "v2_chat": V2_AVAILABLE
        },
        "features": [
            "Named conversation threads" if V2_AVAILABLE else "V2 not available",
            "User-organized storage" if V2_AVAILABLE else "Storage needs setup",
            "Thread management" if V2_AVAILABLE else "Missing V2 router",
            "PineScript code generation",
            "Trading strategy consulting"
        ]
    }

# Root endpoint
@app.get("/")
async def root():
    response = {
        "message": "PineScript Trading Assistant API", 
        "docs": "/docs",
        "version": "2.0.0",
        "app_type": "PineScript Trading Strategy Assistant",
        "status": {
            "v2_available": V2_AVAILABLE
        }
    }
    
    if V2_AVAILABLE:
        response["features"] = {
            "thread_management": "/api/chat/new, /api/chat/list",
            "user_organization": "Each user gets their own folder",
            "named_conversations": "Give your chats meaningful names",
            "pinescript_generation": "AI-powered PineScript code generation",
            "trading_consulting": "Expert trading strategy advice"
        }
        response["usage_guide"] = {
            "create_chat": "POST /api/chat/new",
            "send_message": "POST /api/chat/{returned-id}/message",
            "example_query": "Create a RSI strategy with MACD confirmation"
        }
    else:
        response["setup_needed"] = [
            "Create chat_v2.py in routers folder",
            "Create chat_service_v2.py in services folder", 
            "Create file_memory_v2.py in memory folder"
        ]
    
    return response