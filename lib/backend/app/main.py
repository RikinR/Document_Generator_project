from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import root, process

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(root.router)
app.include_router(process.router)