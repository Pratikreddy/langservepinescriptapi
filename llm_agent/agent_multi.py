import os
import json
from typing import Tuple, List, Any
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from llm_agent.prompts_multi import SIMPLE_PROMPT
from llm_agent.tools_multi import generate_pinescript

# ─────────── CONFIG ───────────
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# ─────────── NO MEMORY - STATELESS ───────────

# ─────────── LLM ───────────
llm = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    temperature=0,
    response_format={"type": "json_object"},
)

# ─────────── SIMPLE AGENT ───────────
agent = create_openai_tools_agent(
    llm=llm,
    tools=[generate_pinescript],
    prompt=SIMPLE_PROMPT,
)

executor = AgentExecutor(
    agent=agent,
    tools=[generate_pinescript],
    verbose=False,
    max_iterations=3,
    return_intermediate_steps=True,
)

# ─────────── MAIN FUNCTION ───────────
def run_pinescript_agent(
    user_input: str,
    previous_summary: str = "No previous conversation."
) -> Tuple[str, int, float, List[Any], List[Any]]:
    """Trading strategy chat with PineScript generation"""
    
    # Run the agent with both input and previous_summary
    result = executor.invoke({
        "input": user_input,
        "previous_summary": previous_summary
    })
    
    # Get the output - should already be JSON
    output = result["output"]
    
    # Verify and enhance the JSON response
    try:
        parsed = json.loads(output)
        
        # Ensure all required fields exist for PineScript response
        if "answer" not in parsed:
            parsed["answer"] = output
        
        json_str = json.dumps(parsed)
        
    except json.JSONDecodeError:
        # If it's not valid JSON, wrap it for PineScript response
        response = {
            "answer": output
        }
        json_str = json.dumps(response)
    
    # Return response - no memory buffer
    return json_str, 0, 0.0, [], []

