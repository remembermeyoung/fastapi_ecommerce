from fastapi import FastAPI
from app.routers.category import cat_router
from app.routers.products import prod_router
from app.routers.auth import user_router
from app.routers.permissions import perm_router
import uvicorn


app = FastAPI()

app.include_router(cat_router)
app.include_router(prod_router)
app.include_router(user_router)
app.include_router(perm_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    