"""Main file."""
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.gpa import router as gpa_router

app = FastAPI()

# To combine the frontend and backend since both are on different domains
origins = ["http://localhost:3000", "http://192.168.43.48:3000"]  # frontend URL


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(gpa_router)


@app.get("/", name="index")
def home() -> Dict[str, str]:
    return {"msg": "Welcome to the GPA app"}
