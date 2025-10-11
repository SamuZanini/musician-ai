"""
Main FastAPI application for #Dô - Assistente de Prática Musical
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connection
from .database.connection import create_tables

# Import API routers
from .api.auth_api import router as auth_router
from .api.profile_api import router as profile_router
from .api.instruments_api import router as instruments_router
from .api.ml_api import router as ml_router
from .api.practice_api import router as practice_router
from .api.subscription_api import router as subscription_router

# Create FastAPI application
app = FastAPI(
    title="#Dô - Assistente de Prática Musical",
    description="Backend API para aplicativo de prática musical com detecção de áudio via ML",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
create_tables()

# Include API routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(instruments_router)
app.include_router(ml_router)
app.include_router(practice_router)
app.include_router(subscription_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bem-vindo ao #Dô - Assistente de Prática Musical",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "#Dô Backend"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
