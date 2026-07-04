# Mock data generator for Startup Studio AI demo mode

def get_mock_data(industry: str, raw_idea: str, audience: str, monetization: str) -> dict:
    """Generates detailed, customized mock startup analysis data for demo mode."""
    ind = industry.upper()
    
    # 1. Base default values
    idea_preview = raw_idea[:100] + "..." if len(raw_idea) > 100 else raw_idea
    
    if "HEALTH" in ind or "BIOTECH" in ind:
        category = "Healthcare & Biotech"
        refined = f"An enterprise digital healthcare platform targeting {audience}. The core concept focuses on: {raw_idea}."
        value_prop = f"Eliminates patient intake bottlenecks and administrative scheduling overhead for clinics serving {audience} while remaining fully HIPAA compliant."
        strengths = "Secure data processing; direct integrations with legacy Electronic Health Record (EHR) platforms; tailored interface for patient accessibility."
        weaknesses = "Complex healthcare regulatory frameworks; long B2B enterprise sales cycles with hospital networks."
        opportunities = "Integration with emerging AI-guided triage models; expansion into telemedicine; remote monitoring capabilities."
        threats = "Shifting compliance rules (HIPAA/HITECH); data breach liability; legacy EHR vendor pushback."
        
        comps = [
            {"name": "SymptomSage", "description": "AI-powered patient intake and scheduling automation for local clinics.", "strengths": "HIPAA compliance built-in, clean EHR integrations", "weaknesses": "Slow dashboard load times, high onboarding friction"},
            {"name": "FitFocus", "description": "Mobile app connecting users with live fitness coaches and posture feedback.", "strengths": "Premium customer engagement", "weaknesses": "Expensive consumer subscriptions, high churn"}
        ]
        
        market_stats = {
            "market_size_billions": 280.5,
            "cagr_percent": 18.2,
            "trends": ["HIPAA-compliant generative AI triage", "Aging-in-place patient technologies", "Wearable health device data pipelines"]
        }
        
        diff = f"Specifically optimized for {audience}, using secondary verification models to eliminate errors while adopting the {monetization} model to keep cost of ownership low."
        
        mvp = [
            {"feature_name": "Compliant Patient Intake Portal", "description": "Secure interface capturing symptoms, consent, and identity verification.", "priority": "High"},
            {"feature_name": "EHR Sync Gateway", "description": "Secure bidirectional data pipe exporting intake records to clinic legacy databases.", "priority": "High"},
            {"feature_name": "Doctor Review Dashboard", "description": "Clean practitioner console displaying structured intake summaries and triage scoring.", "priority": "Medium"}
        ]
        
        tech = {
            "frontend": "React + Vite + CSS (with strict accessibility standards)",
            "backend": "FastAPI + Pydantic v2 (HIPAA audit logging middleware)",
            "database": "PostgreSQL with column-level encryption",
            "cloud_services": "Google Cloud Run + Cloud SQL + GCP Secret Manager (Enterprise KMS keys)"
        }
        
        roadmap = [
            {"phase": "Phase 1: Foundation & HIPAA Audit", "milestones": ["Set up secure database schemas", "Conduct third-party pen-tests", "Build patient UI prototype"]},
            {"phase": "Phase 2: EHR Integrations & Beta Pilot", "milestones": ["Build HL7/FHIR api endpoints", "Launch closed pilot with 3 local clinics", "Refine intake triage algorithms"]},
            {"phase": "Phase 3: Scale & Rollout", "milestones": ["Establish sales channels", "Automate compliance reporting", "Expand telemetry integration"]}
        ]
        
        pricing = [
            {"tier_name": "Starter Clinic Plan", "price": "$199 / month", "features": ["Up to 3 practitioners", "500 digital intakes / month", "Email & Chat support"]},
            {"tier_name": "Premium Clinic Plan", "price": "$499 / month", "features": ["Up to 15 practitioners", "Unlimited digital intakes", "Direct EHR FHIR database sync", "Priority 24/7 support"]},
            {"tier_name": "Enterprise Network", "price": "Custom Quote", "features": ["Unlimited seats", "Custom multi-tenant infrastructure", "BAA contracts", "Dedicated support manager"]}
        ]
        
        gtm = f"B2B direct sales reps pitching to clinic managers; partnerships with medical association vendors; content marketing highlighting security, HIPAA audits, and time savings of the {monetization} model."
        
        metrics = {
            "breakeven_timeframe": "9 Months",
            "estimated_cost_structure": "Product Dev & QA: 40%, Legal, Compliance & Insurance: 25%, Hosting & Security infrastructure: 15%, B2B Sales & Marketing: 20%"
        }
        
        # Visual metrics
        swot_radar_data = [
            {"subject": "Market Opportunity", "value": 85},
            {"subject": "Execution Feasibility", "value": 60},
            {"subject": "Technology Advantage", "value": 80},
            {"subject": "Financial Viability", "value": 75},
            {"subject": "Defensibility", "value": 70}
        ]
        market_growth_projection = [
            {"year": "2026", "market_size": 280.5},
            {"year": "2027", "market_size": 331.5},
            {"year": "2028", "market_size": 391.8},
            {"year": "2029", "market_size": 463.1},
            {"year": "2030", "market_size": 547.4}
        ]
        competitor_comparison_scores = [
            {"name": "Us (Target)", "market_share": 5, "pricing_score": 75, "feature_score": 90},
            {"name": "SymptomSage", "market_share": 45, "pricing_score": 50, "feature_score": 70},
            {"name": "FitFocus", "market_share": 25, "pricing_score": 40, "feature_score": 60}
        ]
        financial_forecast = [
            {"year": "Year 1", "revenue": 120000, "costs": 150000},
            {"year": "Year 2", "revenue": 380000, "costs": 260000},
            {"year": "Year 3", "revenue": 950000, "costs": 480000},
            {"year": "Year 4", "revenue": 2200000, "costs": 950000},
            {"year": "Year 5", "revenue": 4800000, "costs": 1800000}
        ]
        
    elif "ECOMMERCE" in ind or "RETAIL" in ind or "SHOP" in ind:
        category = "E-Commerce & Retail"
        refined = f"An AI-driven personalization and commerce engine tailored for merchants. The core concept focuses on: {raw_idea}."
        value_prop = f"Increases customer conversion lift and average order value (AOV) for digital stores selling to {audience}."
        strengths = "One-click install plugins for Shopify; real-time catalog personalization loops; low-bandwidth script execution."
        weaknesses = "High reliance on third-party commerce platform APIs; merchant churn in the SMB space."
        opportunities = "Integrations with social commerce systems; global multi-currency personalized routing; visual search features."
        threats = "Rapid platform API breaking changes; consumer privacy law adjustments (GDPR/CCPA); copycat widgets."
        
        comps = [
            {"name": "CartCraft", "description": "Shopify plugin for personalizing store frontends using simple behavioral logic.", "strengths": "Fast installation, low cost", "weaknesses": "Simplistic recommendation algorithms, frequent visual layout conflicts"},
            {"name": "ShopGenie", "description": "Conversational assistant for high-end fashion and lifestyle brands.", "strengths": "High engagement rates, good natural dialogs", "weaknesses": "Requires labor-intensive catalog setup and custom tagging"}
        ]
        
        market_stats = {
            "market_size_billions": 850.1,
            "cagr_percent": 12.5,
            "trends": ["Conversational commerce", "Hyper-personalized landing pages", "AI-driven inventory routing"]
        }
        
        diff = f"Differentiates by utilizing lightweight multi-agent reasoning to recommend products based on intent rather than simple historical cookies, powered by the {monetization} pricing model."
        
        mvp = [
            {"feature_name": "Shopify App Integration Setup", "description": "Zero-code plugin enabling one-click installs and auto-script injection.", "priority": "High"},
            {"feature_name": "Intent Analyzer Engine", "description": "Real-time tracker analyzing customer browsing behavior to predict conversion intent.", "priority": "High"},
            {"feature_name": "Dynamic Recommendation Block", "description": "Highly responsive frontend widget displaying custom product layouts in the storefront.", "priority": "Medium"}
        ]
        
        tech = {
            "frontend": "Preact/React (optimized payload sizes under 50kb)",
            "backend": "FastAPI + Redis (ultra-low latency recommendation caching)",
            "database": "MongoDB + Redis",
            "cloud_services": "Google Cloud Run + Cloud Memorystore (Redis) + GCP CDN"
        }
        
        roadmap = [
            {"phase": "Phase 1: App Store Compliance", "milestones": ["Build app storefront scripts", "Pass Shopify/WooCommerce review checklists", "Design Merchant Dashboard UI"]},
            {"phase": "Phase 2: Recommendation Tuning", "milestones": ["Optimize response latency to <50ms", "Deploy dynamic widget templates", "Onboard 50 initial trial stores"]},
            {"phase": "Phase 3: Enterprise Expand", "milestones": ["Support multi-currency systems", "Design analytics export systems", "Integrate automated A/B test routing"]}
        ]
        
        pricing = [
            {"tier_name": "Growth Store Plan", "price": "$49 / month", "features": ["Up to 1,000 monthly orders", "Standard recommendation blocks", "Email support"]},
            {"tier_name": "Scale Store Plan", "price": "$129 / month", "features": ["Up to 10,000 monthly orders", "Full visual custom widgets", "A/B testing tools", "Priority chat support"]},
            {"tier_name": "Enterprise Brand", "price": "Custom Quote", "features": ["Unlimited orders", "Dedicated database clusters", "Custom recommendation algorithms", "Dedicated account manager"]}
        ]
        
        gtm = f"App store marketplace SEO optimization; affiliate programs targeting e-commerce web agencies; targeted digital ads showcasing customer case studies and the positive ROI of the {monetization} model."
        
        metrics = {
            "breakeven_timeframe": "5 Months",
            "estimated_cost_structure": "Cloud Hosting & CDN: 20%, API Integrations: 15%, Sales commissions & partnerships: 30%, R&D / Product Dev: 35%"
        }
        
        swot_radar_data = [
            {"subject": "Market Opportunity", "value": 75},
            {"subject": "Execution Feasibility", "value": 85},
            {"subject": "Technology Advantage", "value": 65},
            {"subject": "Financial Viability", "value": 70},
            {"subject": "Defensibility", "value": 60}
        ]
        market_growth_projection = [
            {"year": "2026", "market_size": 850.1},
            {"year": "2027", "market_size": 956.3},
            {"year": "2028", "market_size": 1075.9},
            {"year": "2029", "market_size": 1210.4},
            {"year": "2030", "market_size": 1361.7}
        ]
        competitor_comparison_scores = [
            {"name": "Us (Target)", "market_share": 3, "pricing_score": 85, "feature_score": 95},
            {"name": "CartCraft", "market_share": 50, "pricing_score": 90, "feature_score": 50},
            {"name": "ShopGenie", "market_share": 35, "pricing_score": 60, "feature_score": 80}
        ]
        financial_forecast = [
            {"year": "Year 1", "revenue": 80000, "costs": 95000},
            {"year": "Year 2", "revenue": 290000, "costs": 180000},
            {"year": "Year 3", "revenue": 720000, "costs": 390000},
            {"year": "Year 4", "revenue": 1650000, "costs": 720000},
            {"year": "Year 5", "revenue": 3800000, "costs": 1400000}
        ]
        
    elif "FINTECH" in ind or "FINANCE" in ind:
        category = "Financial Technology"
        refined = f"An autonomous financial assistant and auditing platform optimized for {audience}. The core concept focuses on: {raw_idea}."
        value_prop = f"Saves users hours in financial tracking, transaction reconciliation, and compliance auditing with the {monetization} model."
        strengths = "Encrypted bank-sync integration APIs; intelligent transaction auto-categorization models; clear, actionable tax-readiness scoring."
        weaknesses = "High security audit compliance requirements; banking integration APIs can be brittle."
        opportunities = "Integrations with corporate card systems; auto-invoicing tools; predictive seasonal cash-flow reporting."
        threats = "Strict regulatory requirements (SEC/FINRA/IRS); security breach risk; legacy tax tool competition."
        
        comps = [
            {"name": "PennyWise AI", "description": "Consumer budgeting app that links bank accounts and flags categorizations.", "strengths": "Clean user interface, simple budgeting tools", "weaknesses": "Frequent bank-link drops, lacks advanced tax planner functionality"},
            {"name": "LedgerAI", "description": "Bookkeeping and tax generator for freelancers and single-member LLCs.", "strengths": "Simplifies tax preparation, receipt scanning", "weaknesses": "No multi-state corporate support, limited API endpoints"}
        ]
        
        market_stats = {
            "market_size_billions": 312.4,
            "cagr_percent": 22.4,
            "trends": ["Autonomous micro-budgeting agents", "Real-time fraud audit loops", "AI freelance bookkeeping assistant"]
        }
        
        diff = f"Offers specialized agents that cross-reference transaction histories with local tax codes to provide advice specific to {audience}, structured under the {monetization} model."
        
        mvp = [
            {"feature_name": "Secure Bank Aggregator Sync", "description": "Integrates Plaid API to fetch real-time transaction statements securely.", "priority": "High"},
            {"feature_name": "Agent Categorizer & Auditor", "description": "Parser agent matching transactions with local tax codes and flag suspicious lines.", "priority": "High"},
            {"feature_name": "Tax Preparedness Report", "description": "Generates complete IRS/Local tax-ready summary sheets in CSV and PDF formats.", "priority": "Medium"}
        ]
        
        tech = {
            "frontend": "React + Vite + CSS (with strict financial chart layouts)",
            "backend": "FastAPI + Pydantic v2 (AES-256 GCM encryption helpers)",
            "database": "PostgreSQL with enterprise column-level encryption",
            "cloud_services": "Google Cloud Run (VPC peered) + Cloud SQL + GCP Secret Manager + Cloud HSM"
        }
        
        roadmap = [
            {"phase": "Phase 1: Bank Aggregator Sync", "milestones": ["Integrate Plaid SDK sandbox", "Configure encryption databases", "Build basic transactions panel"]},
            {"phase": "Phase 2: Tax Code Mapping", "milestones": ["Build local tax code tables", "Onboard initial alpha users", "Implement PDF exporter"]},
            {"phase": "Phase 3: Public SaaS Integration", "milestones": ["Complete SOC2 audit", "Activate direct ledger filings", "Expand bank API coverages"]}
        ]
        
        pricing = [
            {"tier_name": "Individual Freelancer", "price": "$15 / month", "features": ["1 connected bank account", "Automatic tax categorizations", "Quarterly PDF exports"]},
            {"tier_name": "SMB Growth LLC", "price": "$49 / month", "features": ["Up to 5 accounts", "Priority auditor alerts", "Direct accounting software export", "Priority support"]},
            {"tier_name": "Enterprise Audit", "price": "Custom Quote", "features": ["Unlimited accounts", "Custom tax tables", "Dedicated auditor audit logs", "SLA guarantees"]}
        ]
        
        gtm = f"Co-marketing programs with freelance marketplaces; targeted search ads for tax seasonal queries; content guides focused on tax deductions using the {monetization} model."
        
        metrics = {
            "breakeven_timeframe": "8 Months",
            "estimated_cost_structure": "Plaid/Financial API fees: 30%, Cloud hosting & Security: 20%, Sales & Content marketing: 25%, Product R&D: 25%"
        }
        
        swot_radar_data = [
            {"subject": "Market Opportunity", "value": 90},
            {"subject": "Execution Feasibility", "value": 55},
            {"subject": "Technology Advantage", "value": 85},
            {"subject": "Financial Viability", "value": 80},
            {"subject": "Defensibility", "value": 75}
        ]
        market_growth_projection = [
            {"year": "2026", "market_size": 312.4},
            {"year": "2027", "market_size": 382.3},
            {"year": "2028", "market_size": 467.9},
            {"year": "2029", "market_size": 572.7},
            {"year": "2030", "market_size": 701.0}
        ]
        competitor_comparison_scores = [
            {"name": "Us (Target)", "market_share": 2, "pricing_score": 90, "feature_score": 90},
            {"name": "PennyWise AI", "market_share": 55, "pricing_score": 80, "feature_score": 60},
            {"name": "LedgerAI", "market_share": 35, "pricing_score": 70, "feature_score": 75}
        ]
        financial_forecast = [
            {"year": "Year 1", "revenue": 150000, "costs": 140000},
            {"year": "Year 2", "revenue": 520000, "costs": 310000},
            {"year": "Year 3", "revenue": 1400000, "costs": 650000},
            {"year": "Year 4", "revenue": 3100000, "costs": 1200000},
            {"year": "Year 5", "revenue": 6800000, "costs": 2400000}
        ]
        
    else:  # AI / GENERAL SaaS / Default fallback
        category = "Artificial Intelligence & SaaS"
        refined = f"An advanced multi-agent business planning and analysis coordinator designed to help {audience}. The core concept focuses on: {raw_idea}."
        value_prop = f"Orchestrates specialized, coordinated agent squads to analyze concepts, competitor landscapes, and generate blueprints under a {monetization} model."
        strengths = "Uses graph-based multi-agent coordination; aggregates multiple specialized agent outputs; provides responsive interactive roadmaps."
        weaknesses = "Relies on external model api endpoints; requires detailed input prompts for optimal outcomes."
        opportunities = "Custom enterprise MCP connections; automated fine-tuning prompts; edge-agent deployments."
        threats = "Increasing token pricing models; large corporate copycats; model safety compliance alignment laws."
        
        comps = [
            {"name": "Agentic Corp", "description": "Enterprise-grade multi-agent workflow systems.", "strengths": "Robust enterprise security", "weaknesses": "Complex setup, extremely expensive"},
            {"name": "ChatFlow AI", "description": "No-code builder for simple chatbot applications.", "strengths": "Easy interface", "weaknesses": "Lacks reasoning capabilities, does not support multi-agent collaboration"}
        ]
        
        market_stats = {
            "market_size_billions": 196.7,
            "cagr_percent": 37.3,
            "trends": ["Multi-agent orchestration", "Local/edge model deployment", "Privacy-first applications"]
        }
        
        diff = f"Differentiates by using the Google Agent Development Kit (ADK) to build a collaborative node graph, bringing deep market insights and technical stacks under a {monetization} plan."
        
        mvp = [
            {"feature_name": "Multi-Agent Coordinator Node", "description": "Graph-based workflow engine that routes sub-tasks to specialized agent nodes.", "priority": "High"},
            {"feature_name": "Audit Logging", "description": "Encrypted real-time trail of agent tool queries and intermediate decisions.", "priority": "High"},
            {"feature_name": "Interactive Dashboard Plan", "description": "Executive visual panel showing safety compliance scores and PDF reports.", "priority": "Medium"}
        ]
        
        tech = {
            "frontend": "React + Vite + Vanilla CSS",
            "backend": "FastAPI + Pydantic v2 + Uvicorn",
            "database": "PostgreSQL + Redis",
            "cloud_services": "Google Cloud Run + GCP Secret Manager + Artifact Registry"
        }
        
        roadmap = [
            {"phase": "Phase 1: System Architecture", "milestones": ["Set up FastAPI backend schema", "Connect local FastMCP mock servers", "Design core React container UI"]},
            {"phase": "Phase 2: MVP Launch & Deploy", "milestones": ["Integrate live Google ADK runner", "Secure endpoints with rate limiting", "Deploy to Google Cloud Run"]},
            {"phase": "Phase 3: Commercial Growth", "milestones": ["Offer premium API seats", "Publish custom plugin SDK", "Scale multi-cloud database routing"]}
        ]
        
        pricing = [
            {"tier_name": "SaaS Starter Plan", "price": "$29 / month", "features": ["1 User Seat", "500 analyses / month", "Standard support"]},
            {"tier_name": "SaaS Growth Plan", "price": "$89 / month", "features": ["5 User Seats", "Unlimited analyses", "Custom MCP connections", "Priority chat support"]},
            {"tier_name": "Enterprise Package", "price": "Custom Quote", "features": ["Unlimited seats", "Dedicated agent clusters", "SLA guarantees", "Dedicated account manager"]}
        ]
        
        gtm = f"Developer advocate outreach; content marketing demonstrating agent workflows; direct sales to mid-market teams highlighting efficiency gains using the {monetization} model."
        
        metrics = {
            "breakeven_timeframe": "6 Months",
            "estimated_cost_structure": "LLM API usage tokens: 45%, Cloud hosting & security: 20%, Sales & Marketing: 15%, Product R&D: 20%"
        }
        
        swot_radar_data = [
            {"subject": "Market Opportunity", "value": 95},
            {"subject": "Execution Feasibility", "value": 70},
            {"subject": "Technology Advantage", "value": 90},
            {"subject": "Financial Viability", "value": 85},
            {"subject": "Defensibility", "value": 65}
        ]
        market_growth_projection = [
            {"year": "2026", "market_size": 196.7},
            {"year": "2027", "market_size": 270.0},
            {"year": "2028", "market_size": 370.7},
            {"year": "2029", "market_size": 508.9},
            {"year": "2030", "market_size": 698.7}
        ]
        competitor_comparison_scores = [
            {"name": "Us (Target)", "market_share": 4, "pricing_score": 80, "feature_score": 95},
            {"name": "Agentic Corp", "market_share": 65, "pricing_score": 30, "feature_score": 85},
            {"name": "ChatFlow AI", "market_share": 25, "pricing_score": 85, "feature_score": 45}
        ]
        financial_forecast = [
            {"year": "Year 1", "revenue": 110000, "costs": 130000},
            {"year": "Year 2", "revenue": 420000, "costs": 280000},
            {"year": "Year 3", "revenue": 1150000, "costs": 550000},
            {"year": "Year 4", "revenue": 2600000, "costs": 1100000},
            {"year": "Year 5", "revenue": 5800000, "costs": 2100000}
        ]

    # Simple project roadmap duration representation
    roadmap_timeline = [
        {"name": "Phase 1: Foundation", "start": 0, "duration": 3},
        {"name": "Phase 2: MVP Launch", "start": 3, "duration": 3},
        {"name": "Phase 3: Scale & Expand", "start": 6, "duration": 4}
    ]

    # 2. Build the Final Synthesized Report in Markdown format
    swot_table = f"""
| SWOT Category | Factors | Strategic Implications |
| :--- | :--- | :--- |
| **Strengths** | {strengths} | Leverage direct integration channels to secure pilot accounts quickly. |
| **Weaknesses** | {weaknesses} | Mitigate by standardizing data models and creating clean configuration wizards. |
| **Opportunities** | {opportunities} | Position as the primary innovator mapping to new technology expansions. |
| **Threats** | {threats} | Maintain high agility and secure regulatory seals early in the roadmap. |
"""

    competitors_rows = ""
    for c in comps:
        competitors_rows += f"| **{c['name']}** | {c['description']} | {c['strengths']} | {c['weaknesses']} |\n"

    competitor_table = f"""
| Competitor Name | Core Description | Key Strength | Key Weakness |
| :--- | :--- | :--- | :--- |
{competitors_rows}"""

    roadmap_list = ""
    for r in roadmap:
        milestones_list = "".join([f"    * {m}\n" for m in r["milestones"]])
        roadmap_list += f"* **{r['phase']}**\n{milestones_list}"

    pricing_rows = ""
    for p in pricing:
        features_str = ", ".join(p["features"])
        pricing_rows += f"| **{p['tier_name']}** | {p['price']} | {features_str} |\n"

    pricing_table = f"""
| Pricing Plan Tier | Cost Structure | Features Included |
| :--- | :--- | :--- |
{pricing_rows}"""

    revenue_projection_table = f"""
| Forecast Year | Projected Gross Revenue | Projected Total Costs | Net Profit Margin |
| :--- | :--- | :--- | :--- |
| **Year 1** | ${financial_forecast[0]['revenue']:,} | ${financial_forecast[0]['costs']:,} | -{(financial_forecast[0]['costs']-financial_forecast[0]['revenue'])/financial_forecast[0]['revenue'] * 100:.1f}% |
| **Year 2** | ${financial_forecast[1]['revenue']:,} | ${financial_forecast[1]['costs']:,} | +{(financial_forecast[1]['revenue']-financial_forecast[1]['costs'])/financial_forecast[1]['revenue'] * 100:.1f}% |
| **Year 3** | ${financial_forecast[2]['revenue']:,} | ${financial_forecast[2]['costs']:,} | +{(financial_forecast[2]['revenue']-financial_forecast[2]['costs'])/financial_forecast[2]['revenue'] * 100:.1f}% |
| **Year 4** | ${financial_forecast[3]['revenue']:,} | ${financial_forecast[3]['costs']:,} | +{(financial_forecast[3]['revenue']-financial_forecast[3]['costs'])/financial_forecast[3]['revenue'] * 100:.1f}% |
| **Year 5** | ${financial_forecast[4]['revenue']:,} | ${financial_forecast[4]['costs']:,} | +{(financial_forecast[4]['revenue']-financial_forecast[4]['costs'])/financial_forecast[4]['revenue'] * 100:.1f}% |
"""

    final_report = f"""# Executive Startup Blueprint: {category} Innovation

---

## 1. Executive Summary

This blueprint represents a detailed, multi-agent business plan for **{category} Innovation**.

* **Startup Concept Summary**: {refined}
* **Target Audience Focus**: {audience}
* **Primary Monetization Method**: {monetization}
* **Unique Value Proposition**: {value_prop}

---

## 2. SWOT Analysis

The following matrix represents the strengths, weaknesses, opportunities, and threats (SWOT) of the proposed startup:

{swot_table}

---

## 3. Market Analysis & Competitor Landscape

The market segment is expanding rapidly, with high CAGR and substantial customer pain points remaining unaddressed.

### Market Dynamics
* **Estimated Segment Valuation**: ${market_stats['market_size_billions']} Billion
* **Sector CAGR (Growth Rate)**: {market_stats['cagr_percent']}%
* **Key Industry Trends**:
{chr(10).join([f"  * {trend}" for trend in market_stats['trends']])}

### Competitor Comparison Matrix

{competitor_table}

### Our Competitive Differentiator
{diff}

---

## 4. Product Roadmap & Technical Architecture

To validate product-market fit rapidly, the startup will deploy a Minimum Viable Product (MVP) using a modular technical architecture.

### Technical Stack Configuration
* **Frontend**: {tech['frontend']}
* **Backend API**: {tech['backend']}
* **Database Storage**: {tech['database']}
* **Hosting & Cloud Services**: {tech['cloud_services']}

### MVP Feature Scope
{chr(10).join([f"* **{f['feature_name']}** ({f['priority']} Priority): {f['description']}" for f in mvp])}

### System Milestones
{roadmap_list}

---

## 5. Revenue Model & Pricing Strategy

The revenue architecture balances affordability for early adopters with margins to support ongoing execution costs.

### Revenue Channels
* **Model**: {monetization}
* **Strategy**: {metrics['estimated_cost_structure']}

### Pricing Tiers Matrix

{pricing_table}

### Five-Year Financial Forecast

{revenue_projection_table}

### Go-To-Market Plan
{gtm}

### Target Key Metrics
* **Break-Even Target**: {metrics['breakeven_timeframe']}
* **Estimated Cost Breakdown**: {metrics['estimated_cost_structure']}
"""

    return {
        "status": "completed",
        "current_step": "Generation Completed",
        "progress_percent": 100,
        "idea_analysis": {
            "refined_concept": refined,
            "target_audience": audience,
            "value_proposition": value_prop,
            "swot_summary": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "opportunities": opportunities,
                "threats": threats
            },
            "swot_radar_data": swot_radar_data
        },
        "competitor_research": {
            "competitors": comps,
            "market_stats": market_stats,
            "differentiator": diff,
            "market_growth_projection": market_growth_projection,
            "competitor_comparison_scores": competitor_comparison_scores
        },
        "feature_plan": {
            "mvp_features": mvp,
            "tech_stack": tech,
            "roadmap": roadmap,
            "roadmap_timeline": roadmap_timeline
        },
        "business_plan": {
            "monetization_strategy": f"Structured {monetization} model to drive high user retention.",
            "pricing_model": pricing,
            "gtm_strategy": gtm,
            "financial_metrics": metrics,
            "financial_forecast": financial_forecast
        },
        "final_report": final_report,
        "error": None
    }
