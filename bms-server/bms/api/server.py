from fastapi import FastAPI
from prometheus_client import make_asgi_app
from bms.api.routers import users

def make_server():
    app = FastAPI(root_path="/api")

    # Prometheus Client App
    app.mount("/metrics", make_asgi_app())

    # Application Routers
    app.include_router(users.router)

    return app
