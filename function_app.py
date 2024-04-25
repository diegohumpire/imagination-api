import azure.functions as func

from main import app as fastapi_app

app = func.AsgiFunctionApp(
    http_auth_level=func.AuthLevel.FUNCTION, app=fastapi_app)
