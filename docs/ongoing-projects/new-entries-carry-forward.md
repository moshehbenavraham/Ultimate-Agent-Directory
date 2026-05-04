# New Entries Carry-Forward

This file preserves the actionable follow-up from the May 4, 2026 new-entry research pass.
The raw research file was intentionally removed after verified entries were added.

## Completed Baseline

- Verified candidates that fit existing categories were added to the YAML source data.
- Generated outputs were refreshed:
  - `README.md` was rebuilt with 714 agent entries.
  - `BOILERPLATES.md` was rebuilt with 133 boilerplate entries.
- Full validation passed after the add pass:
  - 725 agent/category files.
  - 156 boilerplate/category files.

## Entry Add Process

The durable process for adding entries now lives in `CONTRIBUTING.md` under
"Adding a New Entry". Use that process instead of the old research file.

Key rules:

- Verify candidates from current official sources before adding.
- Check for duplicates across existing YAML data before creating a new file.
- Prefer existing categories and tags unless a deliberate taxonomy change is in scope.
- Run `make validate` and regenerate the relevant generated docs before committing.

## Housekeeping Resolution

- Resolved the duplicate/misplaced Flowise source by keeping the richer verified record at `data/agents/no-code-platforms/flowise.yml` and removing `data/agents/platforms/flowise.yml`.
- Removed empty legacy agent folders: `data/agents/autonomous`, `data/agents/enterprise`, `data/agents/frameworks`, `data/agents/learning`, `data/agents/specialized`, and the now-empty `data/agents/platforms`.
- Cleaned fixable link-check failures by removing a dead Self-Operating Computer documentation URL, replacing Orchestra's documentation URL with the live docs page, replacing the dead Atla signup URL with the live Atla Insights SDK repository, accepting the upstream ReactifyRails replacement repository, and removing stale Godmode, Freedom Stack, and deleted Svelte starter entries.
- Current post-cleanup counts:
  - `README.md` now generates with 712 agent entries.
  - `BOILERPLATES.md` now generates with 131 boilerplate entries.
  - Agent/category validation now covers 723 files.
  - Boilerplate/category validation now covers 154 files.

## Review Decisions

- Agent taxonomy splits to implement first:
  - `mcp-ecosystem` for MCP registries, SDKs, servers, and integration surfaces.
  - `voice-agents` for voice-agent platforms and infrastructure.
  - `agent-evaluation-observability` instead of `agent-observability-eval` for evaluation, tracing, QA, and observability tools.
- Agent taxonomy splits to defer for now: `personal-ai`, `agent-identity-auth`, `agent-payments`, and `agent-marketplaces`.
- Boilerplate taxonomy splits to prioritize first: `browser-extension`, `tauri`, `flutter`, `bun`, and possibly `mcp-server`.
- Boilerplate taxonomy splits to defer pending a stronger verification pass: `ai-saas`, `monorepo`, `deno`, `swiftui`, and `kotlin-compose`.
- OpenClaw README/category treatment needs a separate review and is intentionally deferred.

## Taxonomy Backlog

These category ideas were not part of the completed add pass. They need a separate taxonomy
decision before moving existing entries or adding new category-specific candidates.

### Agent Categories

- `personal-ai`: personal assistants, AI companions, AI memory wearables, personal productivity agents, and AI mental-health assistants.
  - Candidate anchors to review: Pi, Character.AI, Replika, Personal.ai, Limitless Pendant, Rabbit R1, Friend, Bee AI, Granola, Mem AI, Shortwave, Superhuman AI, Mindsera, Rosebud, Woebot, Wysa, Youper.
- `mcp-servers` or `mcp-ecosystem`: MCP registries, SDKs, servers, and integration surfaces.
  - Candidate anchors to review or possibly move: Smithery, Glama, mcp.so, PulseMCP, official MCP SDKs, FastMCP, Apify MCP, Zapier MCP, Stripe MCP, Cloudflare MCP, GitHub MCP, Linear MCP, Notion MCP, Slack MCP, Atlassian MCP, JetBrains MCP, Figma MCP, Playwright MCP.
- `voice-agents`: voice-agent platforms and infrastructure.
  - Candidate anchors to review or possibly move: Vapi, Retell, Bland AI, Synthflow, AirAI, ElevenLabs Conversational AI, Hume EVI, Cartesia Sonic, Pipecat, LiveKit Agents, Vocode, Deepgram Voice Agent API, OpenAI Realtime API, PolyAI, Sesame CSM.
- `agent-observability-eval`: evaluation, tracing, QA, and observability platforms currently clustered in `specialized-tools`.
  - Candidate anchors to review or possibly move: LangSmith, LangFuse, Braintrust, Arize Phoenix, Helicone, Galileo, Patronus AI, Weave, Opik, Langtrace, Lunary, AgentOps, Maxim AI, Athina, DeepEval, HoneyHive, PromptLayer.
- `agent-identity-auth`: auth and identity infrastructure for agents.
  - Candidate areas: Auth0 for AI Agents, WorkOS for AI Agents, Anon, Stytch Agent Auth, ScaleKit Agents, Open Agent Identity, AgentDID, ACK-ID, IETF agent identity drafts.
- `agent-payments`: agentic commerce and payment infrastructure.
  - Candidate areas: x402, Coinbase AgentKit and agentic wallets, Crossmint Agent Wallets, AgentPay, Stripe AgentPay, Mastercard Agent Pay, Visa Agent Pay, Skyfire.
- `agent-marketplaces`: discovery and marketplace surfaces for agents.
  - Candidate anchors to review: Agent.ai, GPT Store, Claude Skills/marketplace surfaces, Hugging Face Spaces, Replicate marketplace, Pickaxe Marketplace, Lindy templates, Smithery, Glama.

### Boilerplate Categories

Add these only after creating corresponding `data/boilerplate-categories/*.yml` files and
deciding how they should appear in `BOILERPLATES.md` and the static site.

- `flutter`: Flutter Bloc Starter, Flutter Riverpod, Flutter Clean Architecture, Brick, GetX templates, Serverpod starters.
- `swiftui`: Swift Composable Architecture starters, SwiftLee templates, Swift Testing starters.
- `kotlin-compose`: Compose Multiplatform and Kotlin Multiplatform Mobile templates.
- `browser-extension`: Plasmo, WXT, CRXJS Vite, Extension.js, Chrome Extension Boilerplate React Vite.
- `mcp-server`: official MCP starter templates and FastMCP starters.
- `ai-saas`: AI-first SaaS, RAG, and chatbot starter kits that are not better represented under an existing framework stack.
- `tauri`: Tauri plus SvelteKit, React, Yew, and related desktop app templates.
- `bun` / `deno`: Bun plus Elysia, Bun plus Hono, and Deno Fresh starters.
- `monorepo`: Turborepo, Nx, Bazel, Moon, and other framework-agnostic monorepo templates.

## Manual Review Backlog

These were explicitly deferred or skipped during the add pass and should be revisited only
with fresh official-source checks.

- Bee Agent Framework cleanup: existing `data/agents/specialized-tools/ibm-beeai.yml` points at `i-am-bee/beeai-framework`, has incomplete metadata, and may belong under open-source frameworks.
- Agents4j: live but low signal during the pass.
- Same.new / Same.dev: official access was rate-limited or unreliable during verification.
- Open SWE: live but low signal during the pass.
- Smol Developer: notable but stale against the pass quality gate.
- Adept ACT-1/Fuyu and robotics or embodied-agent products: need a robotics/embodied-agent taxonomy decision.
- Memary: live repo but stale against the pass quality gate.
- AirAI: official domain and reliability signals were ambiguous; needs careful review before inclusion.
- Skool community pages: direct verification returned 403.
- Papers with Code Agents: researched URL redirected or canonicalized to Hugging Face Papers rather than an active Papers with Code autonomous-agent index.
- Convergence commercial Proxy: `Convergence Proxy Lite` is listed; direct checks of the commercial Proxy URLs returned 403/TLS issues during the follow-up pass.
- Django/Flask boilerplate candidates: `mdn-javier/django-ninja-starter` and `mattvalentine/quart-saas-starter` returned 404.
- Tauri boilerplate candidates: `noxue/tauri-svelte-starter` and `maximousblk/tauri-react-starter` returned 404.
- SvelteKit/Nuxt candidates: MakerKit SvelteKit URL returned 404; `dichioniccolo/sveltekit-supabase-stripe-starter`, `fireship-io/sveltekit-pocketbase`, and `devato/inits` returned 404; `nuxt-saas-kit.com` failed DNS/HTTP verification.

## Maintenance Follow-Up

- Run `make refresh-github-metadata` when GitHub API quota is available to fill in or refresh GitHub stars, last-updated dates, and archived status for entries added during the rate-limited pass.
- If a taxonomy split is implemented, move existing YAML files rather than duplicating products across categories, then run `make validate`, `make generate`, and `make generate-boilerplates` if boilerplates changed.
