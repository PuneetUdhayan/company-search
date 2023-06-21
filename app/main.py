from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Comapnies API is up"}