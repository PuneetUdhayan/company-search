from fastapi import FastAPI

from app.routers.company_search import router as company_search_router


app = FastAPI()

app.include_router(company_search_router)

@app.get("/")
async def root():
    return {"message": "Comapnies API is up"}