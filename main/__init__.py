import fastapi

app = fastapi.FastAPI()


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }


@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }


@app.get("/bye/{name}")
async def say_bye(name: str):
    return {
        "name": name,
    }
