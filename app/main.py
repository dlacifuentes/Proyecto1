from fastapi import FastAPI

app = FastAPI(title="Demo CI/CD con FastAPI y Jenkins")

@app.get("/")
def read_root():
    return {"message": "Hola desde FastAPI con CI/CD en Jenkins!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
