from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro")

app = FastAPI()

# Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Outfit Model
class OutfitRequest(BaseModel):
    gender: str
    occasion: str
    season: str
    preferred_colors: str
    budget: str


@app.post("/generate-outfit")
async def generate_outfit(request: OutfitRequest):

    prompt = f"""
    You are a professional fashion stylist.

    Suggest a complete outfit for:
    Gender: {request.gender}
    Occasion: {request.occasion}
    Season: {request.season}
    Preferred colors: {request.preferred_colors}
    Budget: {request.budget}

    Provide:
    - Top
    - Bottom
    - Footwear
    - Accessories
    - Styling Tips
    """

    response = model.generate_content(prompt)

    return {"result": response.text}


# Chat Model
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = f"""
    You are an AI fashion stylist.
    Give trendy and practical advice.

    Question:
    {request.message}
    """

    response = model.generate_content(prompt)

    return {"reply": response.text}


# Image Analysis
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):

    contents = await file.read()

    prompt = """
    Analyze this outfit image and provide:
    1. Clothing type
    2. Color palette
    3. Style category
    4. Suggestions for improvement
    5. Matching accessories
    """

    response = model.generate_content(
        [
            prompt,
            {
                "mime_type": file.content_type,
                "data": contents
            }
        ]
    )

    return {"analysis": response.text}