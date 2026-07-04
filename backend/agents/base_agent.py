import os
import sys
import logging
import asyncio
from typing import Optional, Any, AsyncGenerator
from google.adk.agents import Agent
import google.adk
from google.genai.errors import APIError, ClientError, ServerError
from backend.security import get_gemini_api_key

logger = logging.getLogger("caching_agent")

class CachingAgent(Agent):
    output_key: Optional[str] = None

    async def run_async(self, parent_context: Any) -> AsyncGenerator[Any, None]:
        # 1. Access the context state to see if output key is already present
        state = parent_context.state if hasattr(parent_context, "state") else {}
        
        # If output key exists and has content in the cached state, return it and bypass LLM call
        if self.output_key and state.get(self.output_key):
            logger.info(f"Agent '{self.name}' output key '{self.output_key}' is cached in session. Reusing cached output and bypassing Gemini API call.")
            # Yield a completed event with the cached output
            yield google.adk.Event(
                output=state[self.output_key],
                author=self.name,
                nodeInfo=google.adk.events.event.NodeInfo(node_name=self.name)
            )
            return

        # 2. Run live agent with exponential backoff on 429/503 rate limit / service unavailable errors
        retries = 6
        delay = 10.0
        for attempt in range(retries):
            try:
                # Consume from the original generator
                async for event in super().run_async(parent_context):
                    yield event
                return
            except Exception as e:
                # Check for rate limiting / 429 / 503
                is_retryable = False
                code = getattr(e, "code", getattr(e, "status_code", None))
                if code in (429, 503):
                    is_retryable = True
                elif any(word in str(e).lower() for word in ["429", "503", "resource_exhausted", "limit", "unavailable"]):
                    is_retryable = True
                    
                # Daily limit is not retryable (e.g. GenerateRequestsPerDayPerProjectPerModel-FreeTier)
                if any(word in str(e).lower() for word in ["perday", "per_day", "daily"]):
                    is_retryable = False
                    
                if is_retryable and attempt < retries - 1:
                    logger.warning(f"Agent '{self.name}' encountered retryable error ({code or 'unknown'}): {e}. Retrying in {delay} seconds (Attempt {attempt+1}/{retries})...")
                    await asyncio.sleep(delay)
                    delay *= 2.0
                else:
                    logger.error(f"Agent '{self.name}' failed: {e}")
                    raise e

def create_adk_agent(name: str, instruction: str, tools: list = None, output_key: str = None) -> CachingAgent:
    """Helper to initialize a CachingAgent with standard configuration and api key validation."""
    api_key = get_gemini_api_key()
    
    # Ensure api key is injected in environment for google-genai client internally used by ADK
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    return CachingAgent(
        name=name,
        model=model_name,
        instruction=instruction,
        tools=tools or [],
        output_key=output_key
    )
