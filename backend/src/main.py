from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import io
from PIL import Image, UnidentifiedImageError

# Initialize the FastAPI app
app = FastAPI(title="SafeWalk API")

# 1. Health Check
@app.get("/")
def health_check():
    """Returns a simple status to confirm the backend is running."""
    return {"status": "online", "message": "SafeWalk Backend is active!"}

# 2. Post Hazard (With Form Data and Strict Image Validation)
@app.post("/hazards")
async def create_hazard(
    type: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    user_id: str = Form(...), 
    image: Optional[UploadFile] = File(None) 
):
    """
    Receives a new hazard report. If an image is attached, 
    it strictly validates it before proceeding.
    """
    image_filename = "No image provided"

    # Only run validation if a file was actually uploaded
    if image:
        try:
            # 1. Read the file into memory
            file_bytes = await image.read()
            
            # 2. Open with Pillow to verify it's a real image
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()
            
            # 3. Reset file pointer so Vishaal can upload it to Supabase later
            await image.seek(0)
            
            # If successful, record the filename
            image_filename = image.filename

        except UnidentifiedImageError:
            # If Pillow cannot identify it as an image (e.g., PDF, TXT), throw a 400 error
            raise HTTPException(
                status_code=400,
                detail="Error: The uploaded file is not a valid image."
            )
        except Exception as e:
            # Catch other potential server errors
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )

    # Return the clean JSON response (No UI, just data)
    return {
        "message": "Hazard reported successfully!",
        "data": {
            "type": type,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
            "user_id": user_id,
            "uploaded_image": image_filename
        }
    }