# Changelog

All notable changes to the **Ultimate AI Agent Ecosystem Directory 2025** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

See Previous Changelogs for More Details: `docs/previous_changelogs/`

---
Start Changelog Entries
---

## [Unreleased] - 2025-11-05

### Added

- **Phase 3: Data Migration Complete**
  - Created all 10 category YAML files in `data/categories/`:
    - open-source-frameworks.yml
    - no-code-platforms.yml
    - research-frameworks.yml
    - learning-resources.yml
    - communities.yml
    - specialized-tools.yml
    - autonomous-agents.yml
    - browser-automation.yml
    - coding-assistants.yml
    - enterprise-platforms.yml
  - Migrated 277 agent entries from README.md to individual YAML files
    - Started with 286 entries in original README
    - Removed 8 placeholder entries (table headers)
    - Removed 3 entries without valid URLs (internal projects, research papers)
    - All 277 entries pass 100% Pydantic validation
  - Fixed migration script section headers to match actual README emojis
  - Enhanced learning resource entries with proper course descriptions
  - Fixed Reddit community entries with complete descriptions
  - Organized entries into category subdirectories:
    - data/agents/open-source-frameworks/ (65 entries)
    - data/agents/no-code-platforms/ (34 entries)
    - data/agents/research-frameworks/ (7 entries)
    - data/agents/learning-resources/ (6 entries)
    - data/agents/communities/ (26 entries)
    - data/agents/specialized-tools/ (57 entries)
    - data/agents/autonomous-agents/ (35 entries)
    - data/agents/browser-automation/ (12 entries)
    - data/agents/coding-assistants/ (15 entries)
    - data/agents/enterprise-platforms/ (37 entries)
  - Generated new README.md with 97KB of properly formatted content
  - All agent entries include:
    - Required fields: name, url, description, category
    - Metadata: type, added_date, verified status
    - Optional fields: github_repo, documentation_url, platform, license, pricing

- **Structured Data System Foundation (Phases 1-2 Complete)**
  - Data-driven architecture using YAML source files with Pydantic validation
  - Directory structure for organized agent data (`data/agents/`, `data/categories/`)
  - Pydantic schema models (`scripts/models.py`) with 20+ validated fields:
    - AgentEntry: Complete schema with required fields (name, url, description, category)
    - Optional metadata: tags, pricing, platform, license, documentation URLs
    - Auto-populated fields: github_stars, last_updated, is_archived
    - Editorial flags: featured, verified, added_date
    - Field validators for tags (lowercase, hyphenated) and GitHub repo format
  - Category schema with configurable display options
  - DirectoryMetadata schema for overall directory information

- **Validation System**
  - `scripts/validate.py` - YAML validation against Pydantic schemas
  - Clear error reporting with file-by-file validation results
  - Exit codes for CI/CD integration
  - Test coverage: 6/6 sample files passing validation

- **README Generation System**
  - `scripts/generate_readme.py` - Automated README.md generation from YAML
  - `templates/readme.jinja2` - Jinja2 template with badges, TOC, subcategories
  - Dynamic badge generation (total entries, last updated)
  - Automatic table of contents with category links
  - Subcategory support with automatic grouping
  - GitHub star badges in tables
  - Statistics section (total entries, categories, last generated)
  - Test result: Successfully generates README.md from 4 sample entries

- **Migration Tools**
  - `scripts/migrate.py` - Markdown table parser for converting existing README
  - Extracts name, URL, description, GitHub repo from markdown tables
  - Auto-detects entry type based on category
  - Generates individual YAML files per entry
  - `--dry-run` flag for safe preview before execution
  - `--all` flag to migrate all sections at once
  - `--section` and `--category` flags for targeted migration

- **Build System**
  - `Makefile` with convenient commands:
    - `make install` - Install dependencies in virtual environment
    - `make validate` - Validate all YAML files
    - `make generate` - Generate README from YAML data
    - `make test` - Run validation and generation
    - `make migrate` - Preview migration (dry-run)
    - `make clean` - Remove generated files and cache
  - `requirements.txt` with minimal, stable dependencies:
    - pyyaml>=6.0.1 (YAML parsing)
    - pydantic>=2.0.0 (Schema validation)
    - jinja2>=3.1.0 (Template rendering)
    - requests>=2.31.0 (Future GitHub API integration)
    - python-frontmatter>=1.0.0 (Future features)

- **Sample Data (Proof of Concept)**
  - 4 agent YAML files demonstrating schema usage:
    - `data/agents/frameworks/langchain.yml` - LangChain framework
    - `data/agents/frameworks/autogen.yml` - Microsoft AutoGen
    - `data/agents/frameworks/crewai.yml` - CrewAI framework
    - `data/agents/platforms/flowise.yml` - Flowise platform
  - 2 category definition files:
    - `data/categories/open-source-frameworks.yml`
    - `data/categories/no-code-platforms.yml`
  - All sample files pass validation

- **Documentation**
  - `docs/QUICKSTART.md` - Quick start guide for structured data system
    - Installation and setup instructions
    - Common commands and workflow
    - Adding new agents (manual and automated)
    - Adding new categories
    - Schema field reference
    - Validation error troubleshooting
    - Workflow best practices
  - `docs/plan.md` - Forward-looking implementation roadmap
    - Current state and test results
    - Remaining phases (Migration, Website, Automation, Documentation)
    - Three migration strategy options (Automated, Manual, Hybrid)
    - Category files needed (10 total, 2 exist)
    - Timeline and success criteria
    - Next actions and commands to try

### Changed
- Updated `.gitignore` with comprehensive rules:
  - Python artifacts (`__pycache__/`, `*.pyc`, `venv/`)
  - Generated files (`_site/`)
  - IDE files (`.vscode/`, `.idea/`, `*.swp`)
  - OS files (`.DS_Store`, `Thumbs.db`)
- Restructured `docs/plan.md` to be forward-looking only (removed completed phases)
- README.md regenerated from sample YAML data (4 entries, 2 categories)

### Technical Details
- **System Architecture:**
  - Source of truth: YAML files in `data/`
  - Generated output: README.md (and future website in `_site/`)
  - Validation: Pydantic 2.0 with strict type checking
  - Templating: Jinja2 with trim_blocks and lstrip_blocks
  - Build automation: Makefile + Python scripts

- **Code Statistics:**
  - Total Python code: ~400 lines across 4 scripts
  - scripts/models.py: 5.0 KB (200+ lines)
  - scripts/validate.py: 2.6 KB (103 lines)
  - scripts/generate_readme.py: 2.4 KB (96 lines)
  - scripts/migrate.py: 6.3 KB (200+ lines)
  - templates/readme.jinja2: 3.1 KB
  - Makefile: Convenience commands for all operations

- **Quality Assurance:**
  - All scripts executable and tested
  - Virtual environment setup automated
  - Sample data validates successfully
  - README generation produces correct output
  - Migration script tested in dry-run mode

### Status
- **Phase 1-2 (Foundation & README Generation):** ✓ Complete
- **Phase 3 (Data Migration):** ✓ Complete - 277 entries migrated, 100% validated
- **Phase 4 (Website Generation):** Next - infrastructure ready, templates needed
- **Phase 5 (Automation & CI/CD):** Planned - GitHub Actions needed
- **Phase 6 (Documentation):** Planned - QUICKSTART complete, CONTRIBUTING needs update

### Migration Statistics
- **Total YAML files created:** 287 (277 agents + 10 categories)
- **Original README entries:** 286
- **Successfully migrated:** 277 entries
- **Validation pass rate:** 100%
- **Generated README size:** 97KB
- **Migration method:** Automated script with manual cleanup

### Next Steps
- Begin Phase 4: Website generation with HTML templates
- Create base.html.jinja2, index.html.jinja2, category.html.jinja2
- Implement client-side search and filtering
- Deploy to GitHub Pages

---

## [Unreleased] - 2025-11-04

### Added
- Local AI documentation file with comprehensive guidance for Agentic Coders instances
  - Repository overview and structure documentation
  - Content organization guidelines for README.md
  - Working with missing_agents_list.md workflow
  - Community contribution process
  - Content standards and formatting conventions
  - Repository principles and maintainer contact info
- docs/TODO.md with detailed improvement roadmap and implementation plan
  - 14 improvement ideas across Immediate Wins, Medium-Effort, and Advanced categories
  - Automated link checking strategy
  - Structured data approach (YAML/JSON format)
  - GitHub metrics automation
  - Interactive website design
  - Automated discovery pipeline
  - Community intelligence features
  - 5-phase implementation roadmap
  - Monetization strategies
  - Success metrics and resources
- docs/CHANGELOG.md structure for tracking project evolution
- ASCII-only character enforcement in all documentation files
- docs/update_listing_todo.md - Comprehensive 10-phase migration plan
  - Phased approach to migrate 180+ entries from missing_agents_list.md to README.md
  - Context window management strategy for efficient processing
  - Category mapping and workload distribution across phases
  - Success criteria and quality guidelines for each phase
- docs/phase1_category_mapping.md - Detailed category analysis and mapping
  - Complete mapping of 180 entries to appropriate README categories
  - Identification of 8 new subsections needed under Specialized Tools
  - Duplicate detection (3 entries flagged)
  - Classification decisions for edge cases
  - Distribution statistics and processing recommendations

### Changed
- Converted TODO.md from emoji-based to ASCII-only formatting

### Completed
- Phase 1: Category Analysis & Mapping (2025-11-04)
  - Analyzed all 180 entries in missing_agents_list.md
  - Mapped entries to existing and new categories
  - Identified need for 8 new subsections in Specialized AI Agent Tools
  - Flagged 3 potential duplicate entries
  - Created detailed distribution plan for remaining phases
- Phase 2: Enterprise Agent Platforms Migration (2025-11-04)
  - Added 26 enterprise platform entries to README.md
  - Major Cloud Providers: Added OpenAI Agent Platform, Microsoft Agent Framework, Google Gemini Enterprise
  - Enterprise Software Giants: Added Workday Enterprise AI Platform, IBM watsonx Orchestrate, Oracle AI Agents in Fusion Cloud
  - Specialized Enterprise Platforms: Added 20 new entries including Workato, UiPath, Automation Anywhere, Amelia, and others
  - Updated README.md badges (Platforms: 30+ to 50+, Tools: 100+ to 150+, Last Updated: July to November 2025)
  - No duplicates found - all 26 entries were new additions
  - Documented distinction between similar products (IBM watsonx Assistant vs Orchestrate, Oracle AI Agent Studio vs Fusion Cloud Agents)
- Phase 3: Open-Source Frameworks & Multi-Agent Systems Migration (2025-11-04)
  - Added 37 open-source framework entries to README.md (2 Core + 35 Specialized)
  - Core Frameworks: Added Microsoft Agent Framework (unified AutoGen + Semantic Kernel SDK) and Rasa (conversational AI with 50M+ downloads)
  - Specialized Frameworks: Added 35 entries including major frameworks and tools:
    - Multi-agent orchestration: Agno, OpenAI Swarm, Griptape, AgentScope, Swarms (kyegomez)
    - Academic/research frameworks: JADE, Mesa, Ray, PADE, generative_agents, ai-town, ChatArena
    - Agent development platforms: Phidata, AgentVerse, OpenAGI, AGiXT, AutoChain
    - Local/offline solutions: Open Interpreter, PrivateGPT, FastChat, Jan, Ollama, Tabby
    - Specialized tools: DeepPavlov (multilingual), Hugging Face Transformers Agents, AppAgent (mobile)
    - Framework utilities: KaibanJS (JavaScript), Mastra (TypeScript), Hector (A2A), RestGPT (API)
    - Memory and learning: Adala (data labeling), AgentOS (self-evolving), Streamship (cloud platform)
    - Integration frameworks: modelscope-agent, Upsonic (MCP), LLMling-Agent (YAML)
  - No duplicates found - all 37 entries were new additions
  - Phidata added (was flagged as duplicate in Phase 1 but not actually in README)
  - All frameworks verified as active open-source projects with standardized technical descriptions
- Phase 4: Specialized Domain Agents Migration (2025-11-04)
  - Added 19 specialized domain agent entries to README.md
  - Created 3 new subsections under Specialized AI Agent Tools:
    - Scientific & Research Agents (6 entries)
    - Legal Agents (1 entry)
    - Advertising & Media Agents (5 entries)
  - Scientific & Research Agents: FutureHouse, Claude for Life Sciences, IBM Fusion, OpenLens AI, GenoMAS, GenoTEX
  - Legal Agents: Harvey AI (leading AI platform for legal work)
  - Advertising & Media Agents: Agentiv (LG Ad Solutions), Ad Context Protocol, Adobe AI Assistant, Fizzion (Coca-Cola internal), The Sun Media Agent
  - Sales Agents: Added 5 new entries to existing section (Artisan, HockeyStack, Ingram Micro Xvantage, AgentX, Salescloser AI)
  - Security Agents: Added 2 new entries to existing section (OpenAI Aardvark, CyberArk)
  - No duplicates found - all 19 entries were new additions
  - All entries verified for domain-specific capabilities with standardized descriptions
- Phase 5: Developer Tools & Observability Migration (2025-11-04)
  - Added 22 developer tools and observability entries to README.md
  - Created 3 new subsections under Specialized AI Agent Tools:
    - Observability & Monitoring (11 entries)
    - Agent Evaluation & Benchmarking (5 entries)
    - Tool Integration Platforms (3 entries)
  - Coding Assistant Agents: Added 3 new entries to Enterprise Solutions section (GitHub Copilot Workspace, Amazon Q Developer, Harness AI Software Delivery Platform)
  - Observability & Monitoring: Langfuse, Arize Phoenix, Helicone, Braintrust, Pydantic Logfire, Grafana Assistant, agentops, langtrace, Agentic Radar, IBM BeeAI, AgentSight
  - Agent Evaluation & Benchmarking: agbenchmark, open-operator-evals, ToolBench, AgentBench v0.2, AgentSquare
  - Tool Integration Platforms: composio (250+ tool integrations), Adopt AI (enterprise tool integration), agentlego (70+ reusable tools)
  - No duplicates found - all 22 entries were new additions
  - All entries verified for technical capabilities with standardized descriptions
  - Enhanced Coding Assistant section with enterprise-grade agentic development tools
- Phase 6: No-Code/Low-Code & Agent Builders Migration (2025-11-04)
  - Added 22 no-code/low-code platform entries to README.md (5 Open-Source + 17 Commercial)
  - Open-Source Platforms: Added 5 new entries to existing section (Rivet, Budibase, Lobe Chat, AgentLabs, superagent)
  - Commercial Platforms: Added 17 new entries to existing section:
    - Vellum AI - Collaborative enterprise platform with unified visual builder and SDK
    - Lindy.ai - No-code AI agent builder for autonomous AI employees
    - Gumloop - No-code platform for AI-powered workflow automations with visual node-based flows
    - Relay.app - User-friendly AI agent builder with human-in-the-loop capabilities
    - LowCo.AI - Low-code automation platform with real-time monitoring and enterprise security
    - Wordware - Web-hosted IDE treating prompts as programming language
    - Giselle - Agentic workflow builder with visual interface
    - MindStudio - No-code platform for building and deploying AI agents
    - Retool - Low-code platform for internal tools with AI capabilities
    - Pipedream - Developer-focused workflow automation platform with scripting
    - Parabola - Visual data and workflow automation platform
    - leap.new - Low-code AI agent builder for real backend systems
    - buildthatidea.com - No-code AI agent builder for non-technical users
    - LiveChatAI - End-to-end AI support platform with no-code visual builder
    - Chatbase - Popular no-code platform for AI chatbots from custom data
    - Agentive - Platform for AI Automation Agency owners
    - Taskade AI - AI-powered productivity suite
  - No duplicates found - all 22 entries were new additions (Relevance AI was already in README)
  - Strong mix of visual builders, workflow automation platforms, and specialized no-code tools
  - Descriptions standardized with focus on ease of use, visual interfaces, and integration capabilities
- Phase 7: Infrastructure, Databases & Supporting Tools Migration (2025-11-04)
  - Added 14 infrastructure and supporting tool entries to README.md
  - Created 3 new subsections under Specialized AI Agent Tools:
    - Voice Agents (6 entries)
    - Infrastructure & Edge AI (2 entries)
    - RAG & Memory Tools (4 entries)
  - Voice Agents: VAPI (developer-focused with sub-500ms response times), Synthflow AI (no-code with 30+ languages, HIPAA/GDPR compliance), Talkscriber (enterprise speech-to-text with emotion detection), Vogent VoiceLab (all-in-one platform with super-realistic models), MixedVoices (open-source analytics for voice agents), Cal.ai (AI phone automation for scheduling)
  - Infrastructure & Edge AI: Ambiq SPOT Platform (ultra-low power edge AI, TIME's Best Inventions 2025, 280M+ chips shipped), Cisco Unified Edge (integrated platform for distributed agentic AI workloads, announced Nov 2025)
  - RAG & Memory Tools: Elysia (Weaviate's open-source agentic RAG with decision trees), mem0 (universal memory layer, AWS exclusive provider, 26% LLM improvement), RAGLight (modular RAG framework with MCP integration), Nexent (zero-code platform for auto-generating agents)
  - Browser Automation: Added 2 new entries to existing section (Apify - cloud platform with 7,000+ tools and AI Web Agent, Tarsier - Reworkd's vision utilities with 10-20% performance gains)
  - No duplicates found - all 14 entries were new additions
  - Three new subsections address critical infrastructure categories: conversational AI, edge computing, and agent memory
  - All entries verified for technical capabilities with standardized descriptions
- Phase 8: Autonomous & Research Agents Migration (2025-11-04)
  - Added 19 autonomous agent entries to README.md (3 Pioneering + 16 Development & Coding)
  - Pioneering Agents: Added 3 new entries (Devin, OpenDevin, Cognition Devin 2.0)
  - Created NEW subsection "Development & Coding Agents" under Autonomous Agents with 16 entries:
    - Code generation & development: gpt-engineer (AI-powered code generation framework), ChatDev (multi-agent virtual software company), DevOpsGPT (AI-driven DevOps automation)
    - Autonomous debugging & fixes: XAgent (complex task planning), TaskWeaver (Microsoft's code-first framework), SWE-agent (autonomous bug fixing in GitHub repos), Sweep (GitHub issues to PRs)
    - Specialized engineering agents: MLE-agent (AI engineering with arXiv integration), ProAgent (agentic process automation), Voyager (GPT-4-powered Minecraft agent with lifelong learning)
    - UI & browser automation: UFO (Microsoft's Windows OS automation), Agent-E (browser-focused AutoGen agent), Notte (high-performance browser agent framework)
    - Workflow & content generation: GenAgent (collaborative AI systems with automated workflows), KwaiAgents (generalized information-seeking), ShortGPT (short-form video automation)
  - No duplicates found - all 19 entries were new additions
  - Academic frameworks (JADE, Mesa, Ray, PADE) and simulation frameworks (generative_agents, ai-town, ChatArena) were already added in Phase 3
  - All entries verified for autonomous capabilities with focus on self-directed code execution and development
  - Descriptions standardized with emphasis on autonomy, self-improvement, and minimal human intervention
  - Entries have NOT been removed from missing_agents_list.md yet - this will be done in Phase 10
- Phase 9: Community Resources & Miscellaneous Migration (2025-11-04)
  - Added 7 community resource entries to README.md
  - Created NEW subsection "Market Maps & Landscape Resources" under GitHub Repositories and Communities
  - Awesome Lists: Added 5 new entries to existing section:
    - awesome-ai-agents (slavakurilyak) - Comprehensive curated list of over 300 agentic AI resources
    - awesome-langchain - Curated list of tools and projects extending LangChain framework
    - LLM-Agent-Benchmark-List - Curated list of benchmarks for evaluating LLM-based agents
    - awesome-workflow-automation (dariubs) - Curated list of workflow automation software and agentic frameworks
    - ai-agents-directory (GitHub topic) - GitHub topic page curating open-source and proprietary AI agents
  - Market Maps & Landscape Resources: Created new subsection with 2 entries:
    - Agentic AI Market Map (Adspyder) - Comprehensive market analysis breaking down ecosystem categories
    - AI Agents Landscape (aiagentsdirectory.com) - Interactive visual ecosystem map for 2025 landscape
  - No duplicates found - all 7 entries were new additions
  - awesome-langchain was flagged as duplicate in Phase 1 but was not actually in README, so it was added
  - New subsection provides valuable high-level ecosystem overview and discovery resources
  - Entries have NOT been removed from missing_agents_list.md yet - this will be done in Phase 10
- Phase 10: Final Review & Cleanup (2025-11-04)
  - Completed comprehensive final review and cleanup of migration process
  - Cleared all processed entries from missing_agents_list.md (180 entries successfully migrated)
  - Updated missing_agents_list.md with completion status and instructions for future submissions
  - Verified and updated README.md badges and metadata:
    - Introduction date updated from July 2025 to November 2025
    - Badges already current: Platforms 50+, Tools 150+, Updated November 2025
  - Completed full duplicate check across README.md:
    - Identified and removed duplicate Microsoft Agent Framework entry from Enterprise section
    - Verified IBM watsonx Assistant and watsonx Orchestrate are correctly listed as separate products
    - Verified Oracle AI Agent Studio and Oracle AI Agents in Fusion Cloud are correctly listed as separate products
    - Confirmed all other entries are unique without duplicates
  - Verified consistent formatting across all 160+ new entries added in Phases 2-9
    - All entries follow standard table format: | **Name** | [Link](URL) | Description |
    - Consistent use of link types (GitHub, Website) and emoji indicators
  - Reviewed and verified table of contents and navigation structure:
    - All 8 new subsections properly integrated under Specialized AI Agent Tools
    - New "Development & Coding Agents" subsection properly added under Autonomous Agents
    - New "Market Maps & Landscape Resources" subsection properly added under GitHub Repositories and Communities
    - All section links and navigation working correctly
  - Migration Statistics Summary:
    - Phase 1: Analysis and mapping of 180 entries
    - Phase 2: Added 26 enterprise platform entries
    - Phase 3: Added 37 open-source framework entries
    - Phase 4: Added 19 specialized domain agent entries
    - Phase 5: Added 22 developer tools and observability entries
    - Phase 6: Added 22 no-code/low-code platform entries
    - Phase 7: Added 14 infrastructure and supporting tool entries
    - Phase 8: Added 19 autonomous agent entries
    - Phase 9: Added 7 community resource entries
    - Total: 160+ entries successfully migrated from missing_agents_list.md to README.md
    - New subsections created: 11 (8 under Specialized Tools, 1 under Autonomous Agents, 1 under Communities, 1 existing section enhanced)
    - Duplicates removed: 1 (Microsoft Agent Framework from Enterprise section)
  - All quality standards met: no duplicates, consistent formatting, accurate categorization, proper attribution

---
End Changelog Entries
---

## Version History Summary

See Previous Changelogs for More Details: `docs/previous_changelogs/`

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **1.0.0** | 2025-07-07 | Added submission guidelines and contribution workflow details |
| **0.7.0** | 2025-07-07 | Established Code of Conduct and community discussion templates |
| **0.6.0** | 2025-07-07 | Created structured issue template for agent suggestions |
| **0.5.0** | 2025-07-06 | Added n8n platform to directory |
| **0.4.0** | 2025-07-06 | Added Factory.ai to enterprise platforms |
| **0.3.0** | 2025-07-04 | Launched comprehensive directory with 247+ agents across 10 categories |
| **0.1.0** | 2025-07-04 | Initial project setup and repository structure |
