import os
import uuid
import logging
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.security import limiter, StartupIdeaInput, verify_app_token, get_gemini_api_key
from backend.orchestrator import execute_adk_workflow, execute_mock_workflow, ACTIVE_JOBS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title="Startup Studio AI Backend",
    description="Multi-agent business planner powered by Google ADK, Gemini, and MCP.",
    version="1.0.0"
)

# Configure Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.error(f"HTTP 422 Unprocessable Entity - Request Validation Error: {exc.errors()}")
    logger.error(f"Incoming Payload: {body.decode('utf-8')}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": body.decode('utf-8', errors='ignore')}
    )

# Configure CORS (strict production-quality list)
allowed_origins = [
    "http://localhost:5173",  # Local Vite Development
    "http://localhost:3000",  # Alternate local dev port
    "http://localhost:8080",  # Docker run port
]

# Allow Google Cloud Run subdomain suffix pattern if configured in env
cloud_run_origin = os.getenv("ALLOWED_ORIGIN")
if cloud_run_origin:
    allowed_origins.append(cloud_run_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Startup-Studio-Token"],
)

@app.post("/api/generate-plan")
@limiter.limit("5/minute")  # Limit idea generation calls to prevent API abuse
async def generate_plan(
    request: Request,
    input_data: StartupIdeaInput,
    background_tasks: BackgroundTasks,
    api_token: Optional[str] = Depends(verify_app_token)
):
    """Secure endpoint that validates startup inputs and triggers the ADK multi-agent workflow."""
    gemini_key = input_data.custom_gemini_key or get_gemini_api_key()
    is_mock = False
    
    if gemini_key:
        if gemini_key.lower().strip() in ("mock", "mock_key", "mock-key"):
            is_mock = True
        else:
            os.environ["GEMINI_API_KEY"] = gemini_key
    else:
        raise HTTPException(
            status_code=400,
            detail="Gemini API Key not set. Please supply custom_gemini_key or configure GEMINI_API_KEY in backend environment."
        )
        
    session_id = input_data.session_id
    is_resume = False
    if session_id and session_id in ACTIVE_JOBS:
        is_resume = True
        logger.info(f"Resuming existing session: {session_id} (is_mock={is_mock})")
    else:
        session_id = str(uuid.uuid4())
        logger.info(f"Received request. Initializing session: {session_id} (is_mock={is_mock})")
    
    if is_mock:
        background_tasks.add_task(
            execute_mock_workflow,
            session_id=session_id,
            raw_idea=input_data.idea,
            industry=input_data.industry,
            audience=input_data.target_audience,
            monetization=input_data.monetization
        )
    else:
        background_tasks.add_task(
            execute_adk_workflow,
            session_id=session_id,
            raw_idea=input_data.idea,
            industry=input_data.industry,
            audience=input_data.target_audience,
            monetization=input_data.monetization
        )
    
    return {
        "message": f"Workflow {'resumed' if is_resume else 'started'} successfully{' in demo mode' if is_mock else ''}",
        "session_id": session_id
    }

@app.get("/api/plan-status/{session_id}")
async def plan_status(session_id: str):
    """Retrieves real-time status and intermediate agent plan details for the session."""
    job = ACTIVE_JOBS.get(session_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
    return job

@app.get("/api/history")
async def get_history():
    """Retrieves metadata for all completed/failed historical business plans."""
    history = []
    for session_id, job in ACTIVE_JOBS.items():
        if "metadata" in job:
            history.append(job["metadata"])
    # Sort descending by creation date
    history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return history

@app.get("/api/health")
async def health_check():
    """Simple health check endpoint for Cloud Run container monitoring."""
    api_configured = bool(get_gemini_api_key() or os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_configured": api_configured
    }

if __name__ == "__main__":
    import uvicorn
    # Use standard Cloud Run environment port or default to 8080
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
