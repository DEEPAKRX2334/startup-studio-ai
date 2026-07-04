import os
import logging
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Request, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("security")

# Initialize SlowAPI Limiter
limiter = Limiter(key_func=get_remote_address)

# API Token Header
API_KEY_NAME = "X-Startup-Studio-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Input Validation Model
class StartupIdeaInput(BaseModel):
    idea: str = Field(..., min_length=10, max_length=1000, description="The raw startup idea to analyze.")
    industry: str = Field("General", min_length=2, max_length=100, description="The industry category of the startup.")
    target_audience: str = Field("General Public", min_length=2, max_length=200, description="Target customer base.")
    monetization: str = Field("Subscription", min_length=2, max_length=100, description="Primary monetization model.")
    custom_gemini_key: Optional[str] = Field(None, description="Optional custom Gemini API key provided by the user.")
    session_id: Optional[str] = Field(None, description="Optional existing session ID to resume progress.")

def get_secret(secret_name: str, project_id: str = None) -> str:
    """Retrieves a secret from GCP Secret Manager if configured."""
    project_id = project_id or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        logger.warning("GCP_PROJECT or GOOGLE_CLOUD_PROJECT not configured. Secret Manager retrieval bypassed.")
        return None
        
    try:
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8").strip()
    except Exception as e:
        logger.error(f"Error accessing Secret Manager for secret '{secret_name}': {e}")
        return None

def get_gemini_api_key() -> str:
    """Returns the Gemini API key, searching in Secret Manager or env vars."""
    # 1. Check local environment var
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key
        
    # 2. Check GCP Secret Manager if configured
    secret_name = os.getenv("GEMINI_API_KEY_SECRET_NAME", "GEMINI_API_KEY")
    secret_key = get_secret(secret_name)
    if secret_key:
        return secret_key
        
    # 3. Fallback/Error
    logger.error("Gemini API Key is not set in environment or GCP Secret Manager!")
    return ""

def verify_app_token(api_key: Optional[str] = Security(api_key_header)) -> Optional[str]:
    """Verifies the X-Startup-Studio-Token request header to protect endpoints."""
    expected_token = os.getenv("APP_SECRET_TOKEN")
    # If no expected token is configured in env, skip protection
    if not expected_token:
        return api_key
        
    if api_key != expected_token:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials. Invalid or missing X-Startup-Studio-Token."
        )
    return api_key
