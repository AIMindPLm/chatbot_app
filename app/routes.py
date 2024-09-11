from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils.open_api import get_chat_response

# Initialize the router
router = APIRouter()

# Define the Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    role: str
    content: str

# Define the route for the chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Extract the list of messages from the request
    messages = request.messages
    
    try:
        # Get the last message content (assuming it's from the user)
        prompt = messages[-1].content
        
        # Get the assistant's response by calling the OpenAI function
        response_content = get_chat_response(prompt, messages)
        
        # Create a ChatResponse object with the assistant's reply
        response = ChatResponse(role="assistant", content=response_content)
        
        # Return the response
        return response
    except Exception as e:
        # Handle any exceptions that occur during the process
        raise HTTPException(status_code=500, detail=str(e))
