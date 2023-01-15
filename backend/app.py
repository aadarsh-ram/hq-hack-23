import os
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
from db_operations import Database
from keyword_extractor import get_jd_keywords

# Import all environment variables
load_dotenv()

# Postgres database variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Initialize database
db = Database(host=db_host, user=db_user, password=db_password, database=db_name)
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

@app.on_event("startup")
async def startup():
    await db.dbs_connect()
    await db.create_tables()

@app.on_event("shutdown")
async def shutdown():
    await db.dbs_disconnect()

@app.get("/", status_code=status.HTTP_200_OK)
async def hello():
    return {"message": "Hello user! Tip: open /docs or /redoc for documentation"}

@app.get("/jds")
async def get_all_jds():
    """
    Get all the job descriptions from the database
    """
    result = await db.get_all_jds()
    return (result)

@app.get("/jd/{jd_id}")
async def get_jd(jd_id: int):
    """
    Get a specific job description from the database
    """
    result = await db.get_jd(jd_id)
    return (result)

@app.get("/candidate-profiles/indeed")
async def get_candidate_profiles(response: Response, keywords: str, offset: Optional[int] = 0):
    """
    Get candidate profiles from Indeed.com
    """
    site_curler = SiteCurler(keywords, offset)
    return site_curler.curl_indeed()

@app.get("/candidate-profiles/pjf")
async def get_candidate_profiles_pjf(response: Response, keywords: str, offset: Optional[int] = 0):
    """
    Get candidate profiles from postjobfree.com
    """
    site_curler = SiteCurler(keywords, offset)
    return site_curler.curl_pjf()

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
            keywords = get_jd_keywords(content) # Keywords

            await db.insert_jd(content, keywords)

            return {"message": "File uploaded successfully"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload unsuccessful")

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
