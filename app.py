import os
import httpx
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
import io

app = FastAPI()

# CORS settings
origins = [
    "chrome-extension://kofboljnoibpmfefcfbhlifnkmkcflge",  # Your Chrome extension ID
    "http://localhost:8000",  # Allow requests from localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# Load the fake news detection model
pipe = pipeline("text-classification", model="MYC007/Real-and-Fake-News-Detection")

# Google Custom Search API configuration
GOOGLE_API_KEY = "AIzaSyBoK42KCXQgj0k37J3ALld1d5g1Ns0hMlQ"  # Replace with your actual API key
SEARCH_ENGINE_ID = "f39951dd7c3304ace"  # Replace with your actual Search Engine ID


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fake News Detection API! Use the /predict/ and /search/ endpoints."}


@app.post("/predict/")
async def predict(request: Request):
    data = await request.json()
    text = data.get('text', '')
    result = pipe(text)[0]
    return {"label": result['label'], "score": result['score']}


@app.get("/search/")
@app.get("/search/")
async def search(query: str):
    # Sanitize query to remove any unwanted characters
    query = query.strip()  # Remove leading/trailing whitespace and newlines

    logging.info(f"Received search query: {query}")

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    logging.info(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        results = response.json().get("items", [])
        return results
    else:
        logging.error(f"Error response: {response.text}")
        return {"error": "Search request failed", "status_code": response.status_code}
    pass

@app.post("/classify-image/")
async def classify_image(file: UploadFile = File(...)):
    # Read the image data
    image_data = await file.read()

    # Convert the image data to PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Perform image classification
    results = pipe(image)

    # Prepare the result
    if results:
        label = results[0]['label']
        confidence = results[0]['score']
        # Determine if AI-generated or not based on the label (you can customize this logic)
        ai_generated = "AI Generated" if "ai" in label.lower() else "Not AI Generated"

        return {
            "label": label,
            "confidence": confidence,
            "ai_generated": ai_generated
        }
    else:
        return {"error": "Unable to classify the image"}
    pass

# Optional: Add a root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Image Classification API"}