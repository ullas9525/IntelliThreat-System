import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, predict

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IntelliThreat System API",
    description="Asynchronous FastAPI REST Engine for Unsupervised Insider Threat & Vendor Anomaly Analytics",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(predict.router)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "system": "IntelliThreat System FastAPI Backend",
        "documentation": "/docs"
    }

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
