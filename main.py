from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from controllers import auth, user, poi, route, file
import os

import app.models as models

app = FastAPI(
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

models.Base.metadata.create_all(bind=engine)

origins = os.environ.get("FRONTEND_URL").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(poi.router)
app.include_router(route.router)
app.include_router(file.router)

@app.get("/")
async def root():
    return {"message": "BiX Rest API"}
