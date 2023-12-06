from  fastapi import FastAPI
from routes.ia import ia

app = FastAPI(
    title = "REST API con FastAPI ",
    description = "Modelo entrenado para pozos de hidrocarburos",
    version = "0.0.1"
)

app.include_router(ia)