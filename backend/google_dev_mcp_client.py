import os
import logging
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_dev_mcp")

# Google Developer Knowledge MCP URL
GOOGLE_DEV_MCP_URL = os.getenv("GOOGLE_DEV_MCP_URL", "https://developerknowledge.googleapis.com/mcp/sse")

async def query_google_dev_docs(query: str) -> str:
    """Connects to Google Developer Knowledge MCP Server to query technical documentation.
    If the server is unavailable, returns a structured fallback of canonical recommendations.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {}
    if api_key:
        headers["x-goog-api-key"] = api_key
        
    logger.info(f"Querying Google Developer Knowledge MCP for: '{query}'")
    
    try:
        # Standard timeout for network safety
        async with asyncio.timeout(10.0):
            async with sse_client(GOOGLE_DEV_MCP_URL, headers=headers) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Search for search_documents tool
                    tools_result = await session.list_tools()
                    tool_names = [t.name for t in tools_result.tools]
                    logger.info(f"Remote MCP tools found: {tool_names}")
                    
                    # Invoke search tool if available
                    if "search_documents" in tool_names:
                        response = await session.call_tool("search_documents", {"query": query})
                        return str(response.content)
                    elif "answer_query" in tool_names:
                        response = await session.call_tool("answer_query", {"query": query})
                        return str(response.content)
                    else:
                        logger.warning("No known search tool found in Google Developer Knowledge MCP.")
    except Exception as e:
        logger.warning(f"Failed to query Google Developer Knowledge MCP: {e}. Utilizing fallback technical specs.")
        
    # Standard fallback content for FastAPI + React + Cloud Run setup
    return get_tech_stack_fallback(query)

def get_tech_stack_fallback(query: str) -> str:
    """Provides offline developer recommendations for FastAPI, React, and Google Cloud Run."""
    q = query.lower()
    if "fastapi" in q or "backend" in q:
        return """
        FastAPI Best Practices:
        - Structured endpoints using APIRouter.
        - Pydantic models for request/response validation.
        - CORS Middleware configured with specific allowed origins (no wildcard in prod).
        - Use SlowAPI or custom middleware for rate limiting (e.g. 10 req/min for plan generation).
        - Deploy on Cloud Run listening on $PORT (default 8080).
        """
    elif "react" in q or "frontend" in q:
        return """
        Vite + React Best Practices:
        - Separate components for layout, state, and UI.
        - Custom CSS variables for uniform typography and glassmorphism.
        - Utilize SSE or standard fetch polling with abort controllers.
        - Package using multi-stage Docker build serving static files via Nginx.
        """
    elif "cloud run" in q or "deploy" in q:
        return """
        Google Cloud Run Best Practices:
        - Inject secrets via environment variables linked to GCP Secret Manager.
        - Configure memory limits (typically 512MB-1GB) and concurrency (80).
        - Allow unauthenticated access if exposing public endpoints, protected by rate limiting.
        """
    return "Ensure clean modular project layout, CORS middleware restrictions, and Pydantic validation across all endpoints."
