from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ia import ia

app = FastAPI(
    title="REST API con FastAPI",
    description="Modelo entrenado para pozos de hidrocarburos",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(ia)
