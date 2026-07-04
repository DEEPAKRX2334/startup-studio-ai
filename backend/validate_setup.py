import sys
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("validation")

def main():
    logger.info("=========================================")
    logger.info("Startup Studio AI - Verification Sequence")
    logger.info("=========================================")
    
    # 1. Test Library Imports
    logger.info("1. Verifying Core Library Imports...")
    try:
        import fastapi
        import uvicorn
        import google.adk
        import google.genai
        import mcp
        import slowapi
        logger.info("✅ All packages successfully imported.")
    except ImportError as e:
        logger.error(f"❌ Dependency check failed: {e}")
        sys.exit(1)

    # 2. Test Agent Definitions & Initialization
    logger.info("2. Verifying Google ADK Agent Instances...")
    try:
        from backend.agents.idea_analyzer import get_idea_analyzer_agent
        from backend.agents.competitor_researcher import get_competitor_researcher_agent
        from backend.agents.feature_planner import get_feature_planner_agent
        from backend.agents.business_planner import get_business_planner_agent
        from backend.agents.planner_agent import get_planner_agent
        
        idea = get_idea_analyzer_agent()
        comp = get_competitor_researcher_agent()
        feat = get_feature_planner_agent()
        biz = get_business_planner_agent()
        plan = get_planner_agent()
        
        logger.info(f"✅ IdeaAnalyzer initialized (output_key={idea.output_key})")
        logger.info(f"✅ CompetitorResearcher initialized (output_key={comp.output_key})")
        logger.info(f"✅ FeaturePlanner initialized (output_key={feat.output_key})")
        logger.info(f"✅ BusinessPlanner initialized (output_key={biz.output_key})")
        logger.info(f"✅ PlannerAgent coordinator initialized (output_key={plan.output_key})")
    except Exception as e:
        logger.error(f"❌ Agent definition failed: {e}")
        sys.exit(1)

    # 3. Test Workflow Graph Compilation
    logger.info("3. Verifying ADK Workflow Orchestration graph...")
    try:
        from backend.orchestrator import adk_workflow
        logger.info(f"✅ ADK Workflow compiled successfully: {adk_workflow.name}")
    except Exception as e:
        logger.error(f"❌ Workflow compilation failed: {e}")
        sys.exit(1)
        
    # 4. Test MCP Local Server Tools
    logger.info("4. Verifying MCP Server endpoints...")
    try:
        from backend.mcp_server import mcp, search_competitors, fetch_market_stats
        comp_matches = search_competitors(industry="AI", idea="custom chatbot assistant")
        stats_match = fetch_market_stats(domain="healthcare")
        
        logger.info(f"✅ MCP search_competitors returned {len(comp_matches)} competitors.")
        logger.info(f"✅ MCP fetch_market_stats resolved CAGR value of {stats_match.get('cagr_percent')}%")
    except Exception as e:
        logger.error(f"❌ MCP verification failed: {e}")
        sys.exit(1)
        
    logger.info("=========================================")
    logger.info("🎉 All checks passed! Ready for local dev launch.")
    logger.info("=========================================")

if __name__ == "__main__":
    main()
