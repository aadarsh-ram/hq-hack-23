from typing import Optional
from fastapi import FastAPI, status, Response, Request
from curl_helper import SiteCurler

app = FastAPI()

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
