from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import home_route, filter_route



templates = Jinja2Templates(directory="templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



app.get("/health", status_code=200)
def heath():
    return "Health check ok"

app.include_router(home_route.router)
app.include_router(filter_route.router)


