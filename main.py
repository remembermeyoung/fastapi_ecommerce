from fastapi import FastAPI
from app.routers.category import cat_router
from app.routers.products import prod_router
import uvicorn


app = FastAPI()

app.include_router(cat_router)
app.include_router(prod_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    