from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



#  API class
app = FastAPI()

# To combine the frontend and backend since both are on different domains

origins = ['http://localhost:3000/'] # frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Default function for the API default path

@app.get('/')
async def root():
    return {"ping": "pong"}


# # FGPA calculation endpoint
# @app.post('/api/calc-fgpa')


# # GPA and CGPA calculation endpoint
# @app.post('/api/calc-gpa-and-cgpa')


# # Required grades calculation endpoint
# @app.post('/api/calc-req-grades-for-sgpa')


# # Minimum and Maximum GPA calculation endpoint
# @app.post('/api/calc-min-max-gpa-per-sem')
