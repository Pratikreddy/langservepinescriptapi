import os
import pathlib
from langchain.tools import tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# PINESCRIPT GENERATION TOOL
# ──────────────────────────────────────────────────────────────────────────────
@tool
def generate_pinescript(strategy_description: str) -> str:
    """
    🎯 **Generate PineScript code for trading strategies**
    
    This tool calls a specialized PineScript agent that has deep knowledge
    of Pine Script v5 syntax, trading indicators, and strategy patterns.
    
    Args:
        strategy_description: Natural language description of the trading strategy
        
    Returns:
        JSON string containing the PineScript code and explanation
    """
    from langchain_openai import AzureChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    
    # Load PineScript knowledge file
    knowledge_path = pathlib.Path(__file__).parent / "pinescript_knowledge.txt"
    pinescript_knowledge = ""
    
    if knowledge_path.exists():
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            pinescript_knowledge = f.read()
    
    # Create specialized PineScript LLM
    pinescript_llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    # PineScript expert prompt
    system_message = """You are an expert PineScript v5 developer specializing in trading strategies and indicators.

PINESCRIPT KNOWLEDGE BASE:
""" + pinescript_knowledge + """

Your task is to generate clean, efficient, and well-commented PineScript code based on the user's strategy description.

Guidelines:
1. Always use PineScript v5 syntax
2. Include proper strategy() or indicator() declaration
3. Add clear comments explaining the logic
4. Use proper variable names and formatting
5. Include risk management parameters when applicable
6. Handle edge cases and errors properly
7. Optimize for performance

You must ALWAYS return your response as valid JSON with these fields:
- pinescript_code: Your complete PineScript code starting with //@version=5
- explanation: Brief explanation of what the script does and how to use it
- parameters: Array of key parameters that can be adjusted
- usage_notes: Any important notes about using this script

Never include any text before or after the JSON. The response must be valid JSON only."""
    
    pinescript_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{strategy_description}")
    ])
    
    # Generate PineScript code
    chain = pinescript_prompt | pinescript_llm
    result = chain.invoke({"strategy_description": strategy_description})
    
    return result.content