import os
import sqlite3
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from duckduckgo_search import DDGS

# 1. Load Environment Variables
load_dotenv()

# Fetch Keys - Works for local .env or Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Please check your secrets or .env file.")

# 2. Clinic Configuration
CLINIC_CONFIG = {
    "name": "PawCare Veterinary Clinic",
    "city_state": "Austin, TX",
    "phone": "(555) 123-4567",
    "email": "hello@pawcarevet.com",
    "hours": "Mon–Fri 8am–6pm, Sat 9am–2pm",
    "services": "Wellness exams, vaccinations, surgery, dental, exotic pet care",
    "booking_link": "https://calendly.com/pawcarevet",
    "handles_emergencies": True,
    "accepts_exotics": True,
}

VET_SYSTEM_PROMPT = f"""You are PawPal 🐾, an AI for {CLINIC_CONFIG['name']}. 
Follow the personality: Warm, emotionally intelligent, and safety-focused.
If an emergency is detected (Difficulty breathing, seizures, bloating), 
use the EMERGENCY RESPONSE immediately."""

# 3. Agent State and Tools
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def search(query: str):
    """Search the web for veterinary or pet care information."""
    try:
        results = DDGS().text(query, max_results=3)
        return str(results)
    except Exception:
        return "Search currently unavailable."

tools = [search]
# Initialize model with the key explicitly
model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    groq_api_key=GROQ_API_KEY
).bind_tools(tools)

# 4. Graph Nodes
def model_call(state: AgentState):
    # Combine system prompt with history
    sys_msg = SystemMessage(content=VET_SYSTEM_PROMPT)
    response = model.invoke([sys_msg] + list(state["messages"]))
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

# 5. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("our_agent", model_call)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("our_agent")
workflow.add_conditional_edges("our_agent", should_continue, {
    "continue": "tools",
    "end": END
})
workflow.add_edge("tools", "our_agent")

# Use MemorySaver for session persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Database helper for Lead Tracking
def init_db():
    # Simple check for cloud environment writing
    try:
        conn = sqlite3.connect("leads.db")
        conn.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, name TEXT, pet TEXT)")
        conn.close()
    except:
        pass
