from fastapi import FastAPI

from app.routers.company_search import router as company_search_router
from app.database import models, engine

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(company_search_router)


@app.get("/")
async def root():
    return {"message": "Comapnies API is up"}