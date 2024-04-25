from fastapi import FastAPI

from main.routers import auth, images, prompts


app = FastAPI()

app.include_router(auth.router)
app.include_router(prompts.router)
app.include_router(images.router)
