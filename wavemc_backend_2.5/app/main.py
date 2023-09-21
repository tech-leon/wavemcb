from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.modules import getData as getd

app = FastAPI(redoc_url=None)

# Define the origins that are allowed to access API 
origins = ["https://wavemocards.com"]

# Add CORS middleware with the specified configuration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/", response_class=RedirectResponse, status_code=302)
async def redirect_docs():
    
    # return RedirectResponse("http://wavemocards.com/docs")
    # return "http://api.wavemocards.com/docs"
    return "http://apiv2.wavemocards.com/docs"


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}

@app.get("/emotions")
async def get_emotions(require):
    """(method) get
    require: string (about, cards).
    Send a string to get a json of responses.
    Returns:
        json: a json may contents lists insite.
    """
    if require == "about":
        return getd.about_emotions()
    elif require == "cards":
        return getd.emotion_cards()


