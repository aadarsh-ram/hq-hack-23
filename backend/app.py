import uvicorn
import aiofiles
import tempfile
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI, status, Response, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

# Import custom modules
from curl_helper import SiteCurler
from pdf_parser import parse_pdf

# Import all environment variables
load_dotenv()

app = FastAPI()

# Allow anyone to call the API from their own apps
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def hello():
    return {"message": "Hello user! Tip: open /docs or /redoc for documentation"}

@app.get("/candidate-profiles/indeed")
async def get_candidate_profiles(response: Response, keywords: str, offset: Optional[int] = 0):
    """
    Get candidate profiles from Indeed.com
    """
    site_curler = SiteCurler(keywords, offset)
    return site_curler.curl_indeed()

@app.post("/candidate-profiles/uploadpdf")
async def handle_pdf_upload(request: Request, response: Response, file: UploadFile = File(...)
):
    """
    Handle the pdf upload and returns content
    """
    try:
        with tempfile.TemporaryDirectory(prefix="jd-") as tmpdir:

            filepath = f"{tmpdir}/{file.filename}"

            if not filepath.endswith('.pdf'):
                filepath += '.pdf'

            async with aiofiles.open(filepath, 'wb') as out_file:
                content = await file.read()  # async read
                await out_file.write(content)
            
            content = parse_pdf(filepath) # JD Content
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
