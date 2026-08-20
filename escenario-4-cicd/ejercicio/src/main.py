from fastapi import FastAPI
import os

app = FastAPI(title="App CI/CD FastAPI", version="1.0.0")


@app.get("/")
def root():
    return {
        "mensaje": "Hola desde FastAPI + CI/CD!",
        "version": os.environ.get("APP_VERSION", "1.0.0"),
        "entorno": os.environ.get("ENV", "development"),
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
