import sys
import os
import logging
from mcp.server.fastmcp import FastMCP

# Setup logging to stderr because stdio transport uses stdout for JSON-RPC
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("startup_research_mcp")

mcp = FastMCP("StartupResearchServer")

# Simulated startup database
COMPETITORS_DB = [
    # AI / LLMs
    {"name": "ChatFlow AI", "industry": "AI", "description": "No-code platform for building LLM agents and customer service chatbots.", "strengths": "Easy UI, quick deployments", "weaknesses": "Limited advanced reasoning, high cost per token"},
    {"name": "MindScribe", "industry": "AI", "description": "AI-powered note-taking and knowledge base companion.", "strengths": "Deep integrations, offline mode", "weaknesses": "Mobile app is laggy, poor search functionality"},
    {"name": "Agentic Corp", "industry": "AI", "description": "Enterprise multi-agent automation workflows.", "strengths": "Robust security, GCP integration", "weaknesses": "Complex setup, extremely expensive"},
    
    # Healthcare / Wellness
    {"name": "FitFocus", "industry": "Healthcare", "description": "Mobile app connecting users with live fitness coaches and AI posture tracking.", "strengths": "Personal touch, good UI", "weaknesses": "Expensive monthly subscription, limited AI functionality"},
    {"name": "SymptomSage", "industry": "Healthcare", "description": "AI-powered triage and symptom analysis tool for clinic patient intake.", "strengths": "High accuracy, HIPAA compliant", "weaknesses": "Clinicians find the dashboard cluttered, slow integration with legacy EHRs"},
    {"name": "ElderlyCompanion", "industry": "Healthcare", "description": "Tablet-based digital companion for seniors providing medication reminders and basic video calls.", "strengths": "Very simple UI, physical emergency button integration", "weaknesses": "No advanced AI reasoning, relies heavily on family input"},

    # E-commerce
    {"name": "CartCraft", "industry": "E-commerce", "description": "AI personalization engine for small Shopify merchants.", "strengths": "Low cost, quick install", "weaknesses": "Weak recommendation engine, conflicts with other apps"},
    {"name": "ShopGenie", "industry": "E-commerce", "description": "Interactive conversational shopper assistant for apparel websites.", "strengths": "Natural dialogues, high conversion lift", "weaknesses": "Requires custom catalog sync which fails frequently"},
    
    # Finance / Fintech
    {"name": "PennyWise AI", "industry": "Fintech", "description": "Personal budgeting agent that automatically categorizes transactions and suggests savings plans.", "strengths": "Excellent transaction categorization, clean UI", "weaknesses": "Frequent bank syncing issues, no investment tracking"},
    {"name": "LedgerAI", "industry": "Fintech", "description": "Automated accounting and tax filing platform for freelancers and gig workers.", "strengths": "Simplifies tax preparation, handles receipts automatically", "weaknesses": "Does not support complex multi-state corporate taxes"},
]

MARKET_STATS_DB = {
    "ai": {"market_size_billions": 196.7, "cagr_percent": 37.3, "trends": ["Multi-agent orchestration", "Local/edge model deployment", "Privacy-first LLM applications"]},
    "healthcare": {"market_size_billions": 280.5, "cagr_percent": 18.2, "trends": ["HIPAA-compliant generative AI triage", "Aging-in-place technologies", "Wearable data integrations"]},
    "ecommerce": {"market_size_billions": 850.1, "cagr_percent": 12.5, "trends": ["Conversational commerce", "AI-driven inventory routing", "Dynamic hyper-personalized landing pages"]},
    "fintech": {"market_size_billions": 312.4, "cagr_percent": 22.4, "trends": ["Autonomous micro-budgeting agents", "Real-time fraud audit loops", "AI freelance bookkeeping assistant"]},
}

@mcp.tool()
def search_competitors(industry: str, idea: str) -> list[dict]:
    """Search for potential competitors based on startup industry and core idea keywords.
    Args:
        industry: The industry of the startup (e.g. AI, Healthcare, E-commerce, Fintech, General)
        idea: A text summary of the startup idea.
    """
    logger.info(f"MCP search_competitors called for industry: '{industry}', idea: '{idea[:40]}...'")
    matches = []
    
    search_industry = industry.lower()
    
    # First search by industry matches
    for comp in COMPETITORS_DB:
        if comp["industry"].lower() in search_industry or search_industry in comp["industry"].lower():
            matches.append(comp)
            
    # Then check for keyword overlaps to find additional hits
    keywords = set(idea.lower().replace(",", "").replace(".", "").split())
    for comp in COMPETITORS_DB:
        overlap = len(set(comp["description"].lower().split()).intersection(keywords))
        if comp not in matches and overlap > 0:
            matches.append(comp)
            
    return matches[:5]

@mcp.tool()
def fetch_market_stats(domain: str) -> dict:
    """Retrieve market statistics (Market Size, CAGR, trends) for a specific business domain.
    Args:
        domain: The domain of the market (e.g. ai, healthcare, ecommerce, fintech)
    """
    logger.info(f"MCP fetch_market_stats called for domain: '{domain}'")
    search_domain = domain.lower()
    
    for key, stats in MARKET_STATS_DB.items():
        if key in search_domain or search_domain in key:
            return stats
            
    # Default fallback data if domain is unique
    return {
        "market_size_billions": 15.0,
        "cagr_percent": 15.0,
        "trends": ["Digital-first adoption", "SaaS automation", "AI-augmented personalization"]
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
