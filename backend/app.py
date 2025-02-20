from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_state():
    """Load data from state.json"""
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(data):
    """Save data to state.json"""
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/api/company")
async def get_companies():
    """Get all companies from state.json"""
    state = load_state()
    return state

@app.get("/api/company/{company_id}")
async def get_company(company_id: str):
    """Get specific company data including threads"""
    state = load_state()
    if company_id not in state:
        raise HTTPException(status_code=404, detail="Company not found")
    return state[company_id]

@app.post("/api/company/{company_id}/threads")
async def create_thread(company_id: str):
    """Create a new thread for a company"""
    state = load_state()
    if company_id not in state:
        raise HTTPException(status_code=404, detail="Company not found")

    thread_id = f"thread_{len(state[company_id]['threads']) + 1}"
    state[company_id]["threads"][thread_id] = {
        "name": f"Thread {thread_id[-5:]}", 
        "messages": []
    }
    save_state(state)
    return {"threadId": thread_id, "name": f"Thread {thread_id[-5:]}"}

@app.get("/api/company/{company_id}/threads")
async def get_threads(company_id: str):
    """Get all threads for a company"""
    state = load_state()
    if company_id not in state:
        raise HTTPException(status_code=404, detail="Company not found")
    return state[company_id].get("threads", {})



@app.post("/api/company/{company_id}/threads/{thread_id}/message")
async def post_message(company_id: str, thread_id: str, message: dict = Body(...)):
    state = load_state()
    
    if company_id not in state:
        print(f"❌ Company {company_id} not found")
        raise HTTPException(status_code=404, detail="Company not found")
    
    if "threads" not in state[company_id]:
        print(f"❌ No threads found for {company_id}")
        raise HTTPException(status_code=404, detail="No threads found")

    if thread_id not in state[company_id]["threads"]:
        print(f"❌ Thread {thread_id} not found for {company_id}")
        raise HTTPException(status_code=404, detail="Thread not found")

    state[company_id]["threads"][thread_id]["messages"].append(message)
    save_state(state)
    print(f"✅ Message added to {thread_id} in {company_id}")
    
    return {"status": "Message added"}

