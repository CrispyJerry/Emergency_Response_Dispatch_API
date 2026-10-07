from fastapi import FastAPI
from app.routes.units import router as units_router

app = FastAPI()
app.include_router(units_router)

@app.get("/")
def root():
    return{"message" : "Unit Management API is running"}