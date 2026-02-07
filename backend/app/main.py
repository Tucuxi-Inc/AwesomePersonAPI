"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.exceptions import APAPIException
from app.core.logging import setup_logging
from app.core.llm_context import LLMContextMiddleware
from app.api.v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging()
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Talent assessment platform with STAR+ methodology",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM context middleware (sets per-request LLM provider config)
app.add_middleware(LLMContextMiddleware)


# Exception handlers
@app.exception_handler(APAPIException)
async def apapi_exception_handler(request: Request, exc: APAPIException):
    """Handle custom AP API exceptions."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if exc.code == "NOT_FOUND":
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == "AUTHENTICATION_ERROR":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.code == "AUTHORIZATION_ERROR":
        status_code = status.HTTP_403_FORBIDDEN
    elif exc.code == "VALIDATION_ERROR":
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif exc.code == "CONFLICT":
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


# Include API routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
