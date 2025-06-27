import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from generation.generate_response import GenerateResponse
from fastapi.responses import JSONResponse


app = FastAPI()

# Allow CORS (optional for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get",response_class=HTMLResponse)
async def chat(query:str=Form(...)):
    
    try:
        result=response = GenerateResponse().generate_response(query)
        print(f"Response: {result}")
        return JSONResponse(
            status_code=200,
            content={"response": result}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))