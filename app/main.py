from fastapi import FastAPI

app = FastAPI(
    title = "DevPulse",
    description = "Developer activity & productivity tracking",
    version = "0.1.0"
)


@app.get("/")
def root():
    return {"message": "DevPulse API is running!"}

@app.get("/health")
def health_check():
    return {"status": "okay"}

