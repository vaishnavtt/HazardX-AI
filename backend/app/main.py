"""
HAZARDX AI — Production-Grade FastAPI Application Entrypoint
Integrates all 12 trained XGBoost models, TreeSHAP explainability,
and multi-hazard early warning decision support.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .utils.logging_config import get_logger
from .services.model_registry import registry
from .api.v1.router import api_router
from .alerts.alert_monitor import alert_monitor
from .ingestion.scheduler import scheduler

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup: verify model artifacts
    logger.info("Initializing HAZARDX AI application...")
    total_models = len(registry.models)
    logger.info(f"Loaded {total_models} models into ModelRegistry.")
    if total_models < 12:
        logger.warning(f"Expected 12 models in registry, found {total_models}.")
    else:
        logger.info("All 12 hazard models verified and operational.")

    # Start background alert monitor worker if enabled
    if getattr(settings, "ALERT_MONITOR_ENABLED", True):
        alert_monitor.start()

    # Start background ingestion scheduler if enabled
    if getattr(settings, "INGESTION_SCHEDULER_ENABLED", False):
        await scheduler.start()

    yield

    # Application shutdown
    logger.info("HAZARDX AI application shutting down...")
    await alert_monitor.stop()
    if getattr(settings, "INGESTION_SCHEDULER_ENABLED", False):
        await scheduler.stop()

app = FastAPI(
    title="HAZARDX AI Multi-Hazard Early Warning Backend",
    version="1.0.0",
    description=(
        "Production-grade REST API serving machine learning inference, real-time TreeSHAP "
        "explainability, and multi-hazard intelligence for Floods, Landslides, Earthquakes, "
        "Cyclones, and Wildfires."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err.get("loc", [])])
        msg = err.get("msg", "Validation error")
        errors.append({"field": loc, "error": msg})
        
    logger.warning(f"Request validation failure on {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed. Please check feature bounds and required fields.",
            "details": errors
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    details_msg = str(exc) if getattr(settings, "DEBUG", False) else "An unexpected error occurred. Please contact the system administrator."
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred while processing the hazard evaluation.",
            "details": details_msg
        }
    )

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "service": "HAZARDX AI Multi-Hazard Early Warning Backend",
        "status": "ONLINE",
        "version": "1.0.0",
        "docs_url": "/docs",
        "api_v1_prefix": "/api/v1"
    }

# Register API v1 routes
app.include_router(api_router, prefix="/api/v1")

