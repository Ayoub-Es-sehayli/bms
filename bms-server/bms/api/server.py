from fastapi import FastAPI
from prometheus_client import make_asgi_app

def make_server(vault):
    app = FastAPI()

    # Prometheus Client App
    app.mount("/metrics", make_asgi_app())

    return app
