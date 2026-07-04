import os
import json
import logging
import asyncio
from google.adk import Workflow
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agents.planner_agent import get_planner_agent
from backend.agents.idea_analyzer import get_idea_analyzer_agent
from backend.agents.competitor_researcher import get_competitor_researcher_agent
from backend.agents.feature_planner import get_feature_planner_agent
from backend.agents.business_planner import get_business_planner_agent
from backend.agents.synthesizer_agent import get_synthesizer_agent
from backend.mock_data import get_mock_data

import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

# In-memory dictionary tracking active jobs (persisted to history.json)
ACTIVE_JOBS = {}
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

def load_history():
    global ACTIVE_JOBS
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                ACTIVE_JOBS.update(data)
                logger.info(f"Loaded {len(data)} past sessions from {HISTORY_FILE}")
        except Exception as e:
            logger.error(f"Failed to load history file: {e}")

def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(ACTIVE_JOBS, f, indent=2)
            logger.info(f"Saved active jobs database to {HISTORY_FILE}")
    except Exception as e:
        logger.error(f"Failed to save history file: {e}")

# Load history on startup
load_history()

# Instantiate the agents
planner_agent = get_planner_agent()
idea_agent = get_idea_analyzer_agent()
competitor_agent = get_competitor_researcher_agent()
feature_agent = get_feature_planner_agent()
business_agent = get_business_planner_agent()
synthesizer_agent = get_synthesizer_agent()

# Define the Workflow graph (DAG - Directed Acyclic Graph)
# The flow runs START -> Planner -> Idea -> Competitor -> Feature -> Business -> Synthesizer
adk_workflow = Workflow(
    name="StartupStudioOrchestrator",
    edges=[
        ("START", planner_agent),
        (planner_agent, idea_agent),
        (idea_agent, competitor_agent),
        (competitor_agent, feature_agent),
        (feature_agent, business_agent),
        (business_agent, synthesizer_agent)
    ]
)

# Initialize Session Service & Runner
session_service = InMemorySessionService()
runner = Runner(
    agent=adk_workflow,
    session_service=session_service,
    app_name="StartupStudioApp",
    auto_create_session=True
)

async def execute_adk_workflow(session_id: str, raw_idea: str, industry: str, audience: str, monetization: str):
    """Executes the Google ADK multi-agent workflow in the background and updates ACTIVE_JOBS."""
    logger.info(f"Starting ADK Workflow for session: {session_id}")
    
    if session_id not in ACTIVE_JOBS:
        ACTIVE_JOBS[session_id] = {
            "status": "running",
            "current_step": "Initializing Planner Agent",
            "progress_percent": 10,
            "idea_analysis": None,
            "competitor_research": None,
            "feature_plan": None,
            "business_plan": None,
            "final_report": None,
            "error": None,
            "agent_statuses": {
                "planner": "running",
                "idea_analyzer": "pending",
                "competitor_researcher": "pending",
                "feature_planner": "pending",
                "business_planner": "pending",
                "synthesizer": "pending"
            },
            "metadata": {
                "session_id": session_id,
                "raw_idea_preview": raw_idea[:60] + "..." if len(raw_idea) > 60 else raw_idea,
                "industry": industry,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    else:
        ACTIVE_JOBS[session_id]["status"] = "running"
        ACTIVE_JOBS[session_id]["error"] = None
        ACTIVE_JOBS[session_id]["current_step"] = "Resuming Agent Pipeline"
        statuses = ACTIVE_JOBS[session_id].get("agent_statuses", {})
        for k, v in statuses.items():
            if v != "completed":
                statuses[k] = "pending"
        ACTIVE_JOBS[session_id]["agent_statuses"] = statuses
        
    save_history()

    # Reconstruct/restore session state in session_service from ACTIVE_JOBS history if present
    past_job = ACTIVE_JOBS.get(session_id)
    if past_job:
        past_state = {}
        for key in ["idea_analysis", "competitor_research", "feature_plan", "business_plan", "final_report"]:
            if past_job.get(key):
                past_state[key] = past_job.get(key)
        if past_state:
            logger.info(f"Restoring session service state for session {session_id}: {list(past_state.keys())}")
            await session_service.create_session(
                app_name="StartupStudioApp",
                user_id="anonymous_user",
                session_id=session_id,
                state=past_state
            )
    
    # Structure the message content
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(
            text=f"Startup Idea: {raw_idea}\nIndustry: {industry}\nTarget Audience: {audience}\nMonetization model: {monetization}"
        )]
    )
    
    try:
        # Run workflow asynchronously
        async for event in runner.run_async(
            user_id="anonymous_user",
            session_id=session_id,
            new_message=user_message
        ):
            # Parse event and update state
            author = getattr(event, "author", None)
            node_info = getattr(event, "node_info", None)
            node_name = ""
            
            if author:
                node_name = str(author)
            elif node_info and hasattr(node_info, "node_name"):
                node_name = str(node_info.node_name)
            elif node_info and hasattr(node_info, "name"):
                node_name = str(node_info.name)
                
            if node_name:
                # Update current active agent based on node execution events
                if "PlannerAgent" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Planning Milestones"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 15
                    ACTIVE_JOBS[session_id]["agent_statuses"]["planner"] = "running"
                elif "IdeaAnalyzer" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Analyzing Idea & SWOT"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 30
                    ACTIVE_JOBS[session_id]["agent_statuses"]["planner"] = "completed"
                    ACTIVE_JOBS[session_id]["agent_statuses"]["idea_analyzer"] = "running"
                elif "CompetitorResearcher" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Performing Competitor Research"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 50
                    ACTIVE_JOBS[session_id]["agent_statuses"]["idea_analyzer"] = "completed"
                    ACTIVE_JOBS[session_id]["agent_statuses"]["competitor_researcher"] = "running"
                elif "FeaturePlanner" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Scoping Features & Architecture"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 70
                    ACTIVE_JOBS[session_id]["agent_statuses"]["competitor_researcher"] = "completed"
                    ACTIVE_JOBS[session_id]["agent_statuses"]["feature_planner"] = "running"
                elif "BusinessPlanner" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Formulating Monetization & GTM"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 85
                    ACTIVE_JOBS[session_id]["agent_statuses"]["feature_planner"] = "completed"
                    ACTIVE_JOBS[session_id]["agent_statuses"]["business_planner"] = "running"
                elif "SynthesizerAgent" in node_name:
                    ACTIVE_JOBS[session_id]["current_step"] = "Synthesizing Final Business Plan"
                    ACTIVE_JOBS[session_id]["progress_percent"] = 95
                    ACTIVE_JOBS[session_id]["agent_statuses"]["business_planner"] = "completed"
                    ACTIVE_JOBS[session_id]["agent_statuses"]["synthesizer"] = "running"

            # Periodically copy intermediate results from session state to active job (for real-time frontend mapping)
            try:
                session_obj = await session_service.get_session(user_id="anonymous_user", session_id=session_id, app_name="StartupStudioApp")
                state = session_obj.state if session_obj else {}
                for key in ["idea_analysis", "competitor_research", "feature_plan", "business_plan", "final_report"]:
                    if state.get(key) and not ACTIVE_JOBS[session_id].get(key):
                        ACTIVE_JOBS[session_id][key] = state.get(key)
                save_history()
            except Exception as e:
                logger.warning(f"Failed to fetch session state during async run: {e}")
                    
        # Once complete, extract values from the session's compiled state
        session_obj = await session_service.get_session(user_id="anonymous_user", session_id=session_id, app_name="StartupStudioApp")
        state = session_obj.state if session_obj else {}
        
        logger.info(f"ADK Workflow finished successfully for session: {session_id}. Retaining states: {list(state.keys())}")
        
        # Populate ACTIVE_JOBS with final outputs
        ACTIVE_JOBS[session_id]["idea_analysis"] = state.get("idea_analysis")
        ACTIVE_JOBS[session_id]["competitor_research"] = state.get("competitor_research")
        ACTIVE_JOBS[session_id]["feature_plan"] = state.get("feature_plan")
        ACTIVE_JOBS[session_id]["business_plan"] = state.get("business_plan")
        ACTIVE_JOBS[session_id]["final_report"] = state.get("final_report")
        
        ACTIVE_JOBS[session_id]["status"] = "completed"
        ACTIVE_JOBS[session_id]["current_step"] = "Generation Completed"
        ACTIVE_JOBS[session_id]["progress_percent"] = 100
        ACTIVE_JOBS[session_id]["agent_statuses"] = {
            "planner": "completed",
            "idea_analyzer": "completed",
            "competitor_researcher": "completed",
            "feature_planner": "completed",
            "business_planner": "completed",
            "synthesizer": "completed"
        }
        save_history()
        
    except Exception as e:
        logger.error(f"Error during ADK workflow execution for session {session_id}: {e}", exc_info=True)
        err_msg = str(e)
        is_daily_limit = any(word in err_msg.lower() for word in ["perday", "per_day", "daily"])
        
        if is_daily_limit:
            err_msg = "Gemini API Daily Quota Exceeded (Limit: 20 requests/day). Please enter 'mock' in the Gemini API Key input field to run in mock demo mode, or supply your own valid Gemini API Key."
            ACTIVE_JOBS[session_id]["status"] = "failed"
            ACTIVE_JOBS[session_id]["current_step"] = "Daily Quota Exceeded (Failed)"
        else:
            is_quota = "429" in err_msg or "resource_exhausted" in err_msg.lower() or "limit" in err_msg.lower()
            ACTIVE_JOBS[session_id]["status"] = "paused" if is_quota else "failed"
            ACTIVE_JOBS[session_id]["current_step"] = "Quota Exceeded (Paused)" if is_quota else "Execution Failed"
            
        ACTIVE_JOBS[session_id]["error"] = err_msg
        # Retain incomplete agent statuses as pending for clean resume visual indications
        statuses = ACTIVE_JOBS[session_id].get("agent_statuses", {})
        for k, v in statuses.items():
            if v == "running":
                statuses[k] = "pending"
        ACTIVE_JOBS[session_id]["agent_statuses"] = statuses
        save_history()

async def execute_mock_workflow(session_id: str, raw_idea: str, industry: str, audience: str, monetization: str):
    """Simulates the ADK multi-agent workflow in the background and updates ACTIVE_JOBS with customized mock data."""
    logger.info(f"Starting simulated mock ADK Workflow for session: {session_id}")
    
    mock_dataset = get_mock_data(industry, raw_idea, audience, monetization)
    
    ACTIVE_JOBS[session_id] = {
        "status": "running",
        "current_step": "Initializing Planner Agent",
        "progress_percent": 10,
        "idea_analysis": None,
        "competitor_research": None,
        "feature_plan": None,
        "business_plan": None,
        "final_report": None,
        "error": None,
        "agent_statuses": {
            "planner": "running",
            "idea_analyzer": "pending",
            "competitor_researcher": "pending",
            "feature_planner": "pending",
            "business_planner": "pending",
            "synthesizer": "pending"
        },
        "metadata": {
            "session_id": session_id,
            "raw_idea_preview": raw_idea[:60] + "..." if len(raw_idea) > 60 else raw_idea,
            "industry": industry,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    save_history()
    
    try:
        # Step 1: Planner Agent complete, Idea Analyzer start
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["current_step"] = "Analyzing Idea & SWOT"
        ACTIVE_JOBS[session_id]["progress_percent"] = 30
        ACTIVE_JOBS[session_id]["agent_statuses"]["planner"] = "completed"
        ACTIVE_JOBS[session_id]["agent_statuses"]["idea_analyzer"] = "running"
        save_history()
        
        # Step 2: Idea Analyzer complete, Competitor Researcher start
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["idea_analysis"] = mock_dataset["idea_analysis"]
        ACTIVE_JOBS[session_id]["current_step"] = "Performing Competitor Research"
        ACTIVE_JOBS[session_id]["progress_percent"] = 50
        ACTIVE_JOBS[session_id]["agent_statuses"]["idea_analyzer"] = "completed"
        ACTIVE_JOBS[session_id]["agent_statuses"]["competitor_researcher"] = "running"
        save_history()
        
        # Step 3: Competitor Researcher complete, Feature Planner start
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["competitor_research"] = mock_dataset["competitor_research"]
        ACTIVE_JOBS[session_id]["current_step"] = "Scoping Features & Architecture"
        ACTIVE_JOBS[session_id]["progress_percent"] = 70
        ACTIVE_JOBS[session_id]["agent_statuses"]["competitor_researcher"] = "completed"
        ACTIVE_JOBS[session_id]["agent_statuses"]["feature_planner"] = "running"
        save_history()
        
        # Step 4: Feature Planner complete, Business Planner start
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["feature_plan"] = mock_dataset["feature_plan"]
        ACTIVE_JOBS[session_id]["current_step"] = "Formulating Monetization & GTM"
        ACTIVE_JOBS[session_id]["progress_percent"] = 85
        ACTIVE_JOBS[session_id]["agent_statuses"]["feature_planner"] = "completed"
        ACTIVE_JOBS[session_id]["agent_statuses"]["business_planner"] = "running"
        save_history()
        
        # Step 5: Business Planner complete, Synthesizer Agent start
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["business_plan"] = mock_dataset["business_plan"]
        ACTIVE_JOBS[session_id]["current_step"] = "Synthesizing Final Business Plan"
        ACTIVE_JOBS[session_id]["progress_percent"] = 95
        ACTIVE_JOBS[session_id]["agent_statuses"]["business_planner"] = "completed"
        ACTIVE_JOBS[session_id]["agent_statuses"]["synthesizer"] = "running"
        save_history()
        
        # Step 6: Complete
        await asyncio.sleep(1.2)
        ACTIVE_JOBS[session_id]["final_report"] = mock_dataset["final_report"]
        ACTIVE_JOBS[session_id]["status"] = "completed"
        ACTIVE_JOBS[session_id]["current_step"] = "Generation Completed"
        ACTIVE_JOBS[session_id]["progress_percent"] = 100
        ACTIVE_JOBS[session_id]["agent_statuses"]["synthesizer"] = "completed"
        save_history()
        
    except Exception as e:
        logger.error(f"Error during simulated mock execution: {e}")
        ACTIVE_JOBS[session_id]["status"] = "failed"
        ACTIVE_JOBS[session_id]["current_step"] = "Execution Failed"
        ACTIVE_JOBS[session_id]["error"] = str(e)
        save_history()
