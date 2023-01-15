from typing import Optional
from fastapi import FastAPI, status, Response, Request, UploadFile, File
from curl_helper import SiteCurler
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def handle_pdf_upload(request : Request,response: Response,file: UploadFile = File(...)):
    """
    Handle the pdf upload
    """
    async with aiofiles.open('example.pdf', 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)
    
    return {"message" : "gave pa"}

if __name__ == '__main__':
    uvicorn.run(app)
