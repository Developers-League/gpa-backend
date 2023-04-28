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

'''
Endpoints 

1. calc-fgpa
2. calc-gpa-and-cgpa
3. calc-required-grades-for-sgpa
4. calc-highest-reachable-gpa-per-sem
5. calc-lowest-reachable-gpa-per-sem

'''


@app.get('/api/')
async def root():
    a = 2
    b = 5
    c = a + b
    return {c}


