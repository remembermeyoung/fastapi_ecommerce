from fastapi import FastAPI
from app.routers import category, products
from app.routers import auth

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Me e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
