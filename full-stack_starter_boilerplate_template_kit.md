# Full-Stack Starter, Boilerplate & Template Kit Guide

> **Master Reference for Production-Ready Full-Stack Starter Repositories (2025)**

---

## Discovery & Aggregation Resources

### Ecosystem Trends (2024-2025)

The software development landscape has undergone a paradigm shift, moving away from the assembly of disparate libraries toward the adoption of integrated, opinionated "superstacks." Three dominant trends are driving the popularity and maintenance of starter repositories:

1. **The Rise of the "Meta-Framework" Monorepo**: Tightly coupled frontends and backends (e.g., Next.js, Nuxt, SvelteKit) are dominating over decoupled architectures for early-stage SaaS and rapid prototyping. This is driven by the efficiency of Server Actions, shared type definitions, and unified deployment pipelines.

2. **The "Rails-ification" of Systems Languages**: The Rust ecosystem is aggressively targeting web development friction. Frameworks like Loco and platforms like Shuttle are explicitly mimicking the developer experience (DX) of Ruby on Rails and Node.js to bring memory safety to the web without the historic learning curve.

3. **Authentication & Billing as Infrastructure**: Modern starters no longer treat authentication and payments as "features" to be built, but as critical infrastructure to be configured. Integrations with Clerk, Supabase Auth, Stripe, and Lemon Squeezy are now standard hard requirements for a repository to be considered "production-ready".

### Awesome Lists & Curated Collections

| List | URL | Focus | Items Listed |
|------|-----|-------|--------------|
| **awesome-saas-boilerplates** | [smirnov-am/awesome-saas-boilerplates](https://github.com/smirnov-am/awesome-saas-boilerplates) | Multi-language SaaS starters | 50+ |
| **awesome-saas-boilerplates-and-starter-kits** | [tyaga001/awesome-saas-boilerplates-and-starter-kits](https://github.com/tyaga001/awesome-saas-boilerplates-and-starter-kits) | SaaS, categorized by stack | Active |
| **awesome-nextjs** | [unicodeveloper/awesome-nextjs](https://github.com/unicodeveloper/awesome-nextjs) | Next.js ecosystem | 60+ boilerplates |
| **awesome-opensource-boilerplates** | [EinGuterWaran/awesome-opensource-boilerplates](https://github.com/EinGuterWaran/awesome-opensource-boilerplates) | Free options only | 20+ |
| **awesome-fullstack** | [liberocks/awesome-fullstack](https://github.com/liberocks/awesome-fullstack) | Full-stack tools & starters | Active |
| **awesome-fullstack** (kevindeasis) | [kevindeasis/awesome-fullstack](https://github.com/kevindeasis/awesome-fullstack) | Language-specific learning resources | Active |
| **awesome-stacks** | [stackshareio/awesome-stacks](https://github.com/stackshareio/awesome-stacks) | React+Firebase, curated stacks | Active |
| **awesome-starters** | [devpose/awesome-starters](https://github.com/devpose/awesome-starters) | MEAN/Meteor starters | Active |
| **awesome-supabase** | [lyqht/awesome-supabase](https://github.com/lyqht/awesome-supabase) | Supabase starters (Supanext, etc.) | Active |
| **awesome-projects-boilerplates** | [melvin0008/awesome-projects-boilerplates](https://github.com/melvin0008/awesome-projects-boilerplates) | Web/mobile, multi-stack | Active |
| **awesome-nestjs** | [nestjs/awesome-nestjs](https://github.com/nestjs/awesome-nestjs) | NestJS boilerplates section | Active |
| **awesome-svelte** | [TheComputerM/awesome-svelte](https://github.com/TheComputerM/awesome-svelte) | Svelte/SvelteKit | 10+ starters |
| **awesome-vue** | [vuejs/awesome-vue](https://github.com/vuejs/awesome-vue) | Vue/Nuxt ecosystem | 15+ scaffolds |

### Aggregator Sites & Search Tools

- **BoilerplateList.com** — Filtering by tech stack, 70+ Next.js SaaS boilerplates catalogued
- **BoilerplateSearch.com** — "Top Best 2025" curated lists
- **BoilerplateHub.com** — SvelteKit collection and multi-framework starters
- **SaaSHub.com** — Alternatives comparisons and reviews
- **saasstarters.com** — Filter by stack/features, active curation
- **starterindex.com** — Multiple frameworks comparison and discovery

### Community Forums & Discussion Channels

- **Reddit**: r/webdev, r/nextjs, r/SaaS for community recommendations
- **Hacker News**: Periodic "Show HN" starter announcements
- **Dev.to**: Framework-specific starter discussions

**Common community advice**: "Choose framework first, then boilerplate." Paid options typically save 2-4 weeks of development time. Always verify last commit date—many free options become unmaintained.

---

## JavaScript / TypeScript Ecosystem

### Next.js & T3 Stack

#### Minimal / CLI-Based Starters

##### create-t3-app
The TypeScript standard for Next.js development, offering an interactive CLI with modular architecture.

| Attribute | Details |
|-----------|---------|
| Repository | [t3-oss/create-t3-app](https://github.com/t3-oss/create-t3-app) |
| Stars | ~28,300 |
| License | MIT |
| Last Updated | December 2025 |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Next.js (App Router) | Industry standard for React full-stack |
| Type Safety | tRPC | End-to-end type safety without code generation |
| Database | Prisma or Drizzle | User choice during scaffold |
| Auth | NextAuth.js | Flexible authentication with multiple providers |
| Styling | Tailwind CSS | Utility-first CSS framework |

**Key Features:**
- Interactive CLI for modular component selection
- Full type-safety end-to-end with tRPC
- Largest community with best documentation (create.t3.gg)
- 378+ contributors, created by Theo (t3dotgg)

**Use Case:** Perfect for those who want a solid foundation without extra cruft. If you value developer experience and type safety, T3 is ideal – many indie SaaS projects start with T3 Stack. Ideal for small teams/startups who plan to build out features themselves but want authentication and a robust structure pre-set. Also a great learning tool with lots of tutorials and community help.

**Pros:** Maximum flexibility, only use what you need, excellent documentation. Extremely popular & well-supported with huge Discord community. The type-safe end-to-end approach means fewer runtime errors. Very flexible – you opt into only what you need (can exclude NextAuth or Prisma). Maintainers keep it updated promptly with new Next.js and library versions.
**Cons:** No payments/email built-in, requires manual SaaS feature additions. Focuses on dev-stack rather than features. Reliance on tRPC and NextAuth means a learning curve if unfamiliar. Because it's minimal, you'll spend time adding UI components. Not a turnkey SaaS solution, but a high-quality starting scaffold.

**Community:** Active Discord (~30k members), weekly community calls, many contributors. "T3 Axiom" and other forks extend it. Lots of content (blogs, YouTube) about building with T3. If you run into an issue, chances are someone in the community has encountered it. The T3 team values best practices with constant improvements (e.g., adopting new Next.js app directory features quickly). Created by Theo (t3dotgg).

##### create-t3-turbo
The monorepo variant of T3 Stack, extending create-t3-app to support web and mobile (Expo) applications in a unified codebase.

| Attribute | Details |
|-----------|---------|
| Repository | [t3-oss/create-t3-turbo](https://github.com/t3-oss/create-t3-turbo) |
| Stars | ~5,900 |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | React/Next.js + Expo (React Native) | Unified web + mobile development |
| Type Safety | tRPC | End-to-end type safety across platforms |
| Database | Drizzle ORM, Supabase | Lightweight ORM with BaaS option |
| Auth | Better-Auth | Modern, cross-platform auth |
| Build | Turborepo | Monorepo build optimization |

**Key Features:**
- Monorepo structure with Turborepo for shared UI/tooling packages
- Cross-platform development: Next.js (web) + Expo (iOS/Android)
- shadcn/ui CLI integration for component library
- CI workflow pre-configured
- EAS (Expo Application Services) for mobile deployment

**Deployment:** Vercel (web), EAS (mobile).

**Use Case:** Ideal for teams building both web and mobile apps from a shared codebase. Perfect for startups wanting to launch on web and mobile simultaneously with maximum code reuse.

**Pros:** Cross-platform with shared code, typesafe across all platforms, leverages proven T3 patterns
**Cons:** Separate deployment targets for web/mobile, auth configuration required for Expo

**Community:** No dedicated Discord; uses T3 community channels. Maintained by Julius Marminge.

#### Batteries-Included / SaaS-Ready

##### Vercel SaaS Starter (Next.js SaaS Starter)
Official Next.js pattern from Vercel, minimal but authoritative. Intentionally minimal, serving as a clean foundation to build upon.

| Attribute | Details |
|-----------|---------|
| Repository | [nextjs/saas-starter](https://github.com/nextjs/saas-starter) |
| Stars | ~15.1k |
| License | MIT |
| Last Updated | October 2025 (actively maintained by Vercel Next.js team) |

**Technical Stack:** Next.js 13 (App Router), PostgreSQL (via Drizzle ORM), Stripe payments, shadcn/UI components, JWT auth (email/password with signup/login pages)

**Key Features:**
- Official Vercel-maintained template with Next.js 13 best practices
- Basic SaaS structure: user accounts (seeded admin user), teams/org support
- Subscription checkout & webhooks with Stripe integration
- Tailwind UI with shadcn components
- Activity logging, Zod schema validation
- Minimal UI (no extra bloat) – type-safe (TypeScript + Zod)
- CI workflow and testing setup included

**Deployment:** Optimized for Vercel (one-click deploy) with env var setup for Stripe and Postgres. Also Dockerizable.

**Use Case:** Ideal for learning or starting a new SaaS with Next.js – intentionally minimal (authentication & payments included, but few extras). Great for indie hackers & small teams who want modern Next.js 13 patterns out-of-the-box.

**Pros:** Highly popular & community-vetted (15k+ stars); official Next.js conventions; type-safe and minimal design makes it easy to understand and customize. Integrates essential SaaS needs without heavy complexity. 20+ contributors with strong community support.
**Cons:** Being minimal, it omits advanced features (no built-in admin panel, RBAC, file storage). No social login by default (email/pass only). Uses Drizzle instead of Prisma. Stripe integration is basic (checkout + webhook) – no subscription management UI.

**Community:** Maintained by Vercel team with prompt issue responses. Active discussions on Reddit (r/nextjs). No dedicated Discord, but Next.js community and GitHub serve as support channels.

##### React Starter Kit (Kriasoft)
Performance-focused edge-native starter with Cloudflare Workers deployment.

| Attribute | Details |
|-----------|---------|
| Repository | [kriasoft/react-starter-kit](https://github.com/kriasoft/react-starter-kit) |
| Stars | ~23,400 |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | React 19, TanStack Router | Latest React with modern routing |
| Styling | Tailwind CSS v4 | Performance gains with v4 |
| Backend | Hono, tRPC | Edge-compatible, type-safe APIs |
| Database | Drizzle ORM, Neon PostgreSQL | Serverless Postgres, lightweight ORM |
| Auth | Better Auth | Modern auth solution |

**Key Features:**
- Monorepo with Turborepo for shared code efficiency
- Edge deployment optimized for Cloudflare Workers
- Multi-tenancy support
- Email templates via React Email
- WebSocket support
- Terraform infrastructure-as-code
- VitePress documentation site

**Deployment:** Cloudflare Workers (edge-native).

**Use Case:** Fast, global SaaS/API apps prioritizing edge performance and shared code. Ideal for developers comfortable with Bun runtime and Cloudflare ecosystem.

**Pros:** Performance-focused (Bun, edge-native), type-safe APIs, comprehensive DX tools, large community (23k+ stars)
**Cons:** Bun runtime requirement, Cloudflare-specific deployment

**Community:** Discord ([discord.gg/2nKEnKq](https://discord.gg/2nKEnKq)), maintained by Konstantin Tarkus with 10+ contributors.

##### ixartz SaaS-Boilerplate
Modern App Router implementation with multi-tenancy support.

| Attribute | Details |
|-----------|---------|
| Repository | [ixartz/SaaS-Boilerplate](https://github.com/ixartz/SaaS-Boilerplate) |
| Stars | ~6,500 |
| License | MIT (Free + Pro tiers) |

**Technical Stack:** Next.js (App Router), Drizzle ORM, Clerk auth, Tailwind CSS

**Key Features:**
- Multi-tenancy support
- Storybook integration for component development
- Free tier available with Pro upgrade option

##### next-saas-stripe-starter
Beautiful UI implementation with comprehensive auth and email.

| Attribute | Details |
|-----------|---------|
| Repository | [mickasmt/next-saas-stripe-starter](https://github.com/mickasmt/next-saas-stripe-starter) |
| Stars | ~4,000 |
| License | MIT |

**Technical Stack:** Next.js, Prisma, Auth.js v5, Stripe, Resend email

**Key Features:**
- Beautiful Shadcn UI components
- Auth.js v5 implementation
- Resend for transactional emails
- Stripe payment integration

##### Relivator
Modern SaaS e-commerce starter leveraging the latest Next.js 15 and React 19 features.

| Attribute | Details |
|-----------|---------|
| Repository | [relivator/relivator](https://github.com/relivator/relivator) |
| Stars | ~1,200+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** Next.js 15, React 19, Drizzle ORM, PostgreSQL, Stripe, NextAuth, shadcn/ui, Tailwind CSS

**Key Features:**
- E-commerce focused SaaS with payments integration
- App Router architecture with React Server Components
- Stripe checkout and subscription flows
- Modern shadcn/ui component library
- Type-safe database operations with Drizzle

**Use Case:** Ideal for e-commerce SaaS applications, marketplace MVPs, or any product-based startup needing modern Next.js patterns with payment integration.

**Pros:** Cutting-edge stack (Next.js 15, React 19), active maintenance, comprehensive e-commerce features
**Cons:** E-commerce focused (may require stripping features for non-commerce apps)

##### Next.js Boilerplate (ixartz)
The "bleeding edge" of the Next.js ecosystem, aggressively adopting new standards like Drizzle ORM and Clerk authentication to maximize developer velocity.

| Attribute | Details |
|-----------|---------|
| Repository | [ixartz/Next-js-Boilerplate](https://github.com/ixartz/Next-js-Boilerplate) |
| Stars | ~12.4k |
| License | MIT |
| Last Updated | December 2025 (v6.0.4) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Next.js 16+ (App Router) | Leverages React Server Components for performance |
| Styling | Tailwind CSS 4 | Standard for utility-first styling; v4 brings performance gains |
| Backend | Next.js Server Actions | Eliminates the need for a separate API layer for many CRUD tasks |
| Database | Drizzle ORM | Lighter and faster than Prisma; SQL-like syntax appeals to purists |
| Auth | Clerk | Outsourced auth reduces maintenance burden for MFA/Social login |
| Env Management | T3 Env | Enforces type safety for environment variables at build time |

**Key Features:**
- Sentry for error tracking, LogTape and Better Stack for logging
- Arcjet for security features (bot protection, rate limiting)
- Built-in i18n support via next-intl and Crowdin
- Vitest (replacing Jest) and Playwright for E2E testing
- PGlite for local development (in-memory Postgres)

**Production Readiness:** Highly opinionated, favoring SaaS integrations (Clerk, Arcjet, Sentry) over self-hosted alternatives. Ideal "solopreneur" stack where speed is the primary metric. Heavy reliance on third-party services means developers targeting air-gapped or self-hosted environments would need significant modifications.

##### Supabase + Next.js Starter
High-quality SaaS starter leveraging Supabase as a backend-as-a-service for authentication, database, and storage.

| Attribute | Details |
|-----------|---------|
| Repository | [KolbySisk/next-supabase-stripe-starter](https://github.com/KolbySisk/next-supabase-stripe-starter) |
| Stars | ~720 |
| License | MIT |
| Last Updated | 2025 (maintainer actively responding to issues) |

**Technical Stack:** Next.js 13, Supabase (Postgres + Auth) for backend-as-a-service, Stripe payments, Shadcn/UI (Radix + Tailwind) for components, TypeScript throughout. Uses Supabase Auth (magic link email by default, plus OAuth via Supabase), Supabase storage for file uploads, tRPC for typed API calls.

**Key Features:**
- Supabase user auth setup with email verification links
- Database schema for SaaS (projects, teams, etc.)
- Integration with Stripe for subscriptions
- Dashboard UI and account settings pages built with shadcn/ui library
- Multi-tenancy via organization/team management (pricing model allows setting max team invites per plan)
- Example blog using MDX or Supabase data
- Testing and CI configured for Vercel
- All-in-one starter using Supabase as heavy lifter (no custom Node backend to maintain)

**Deployment:** Optimized for Vercel + Supabase. Deploy Next app to Vercel and create Supabase project for backend (guide provided to set env vars for Supabase keys, Stripe keys). Supabase handles DB, auth, storage; no standalone database to manage. Can also deploy anywhere Next runs with Supabase cloud as backend.

**Use Case:** Great for developers who want to move fast by outsourcing backend complexity to Supabase. If you prefer not to manage your own database or auth service, this gives you a SaaS scaffold with minimal DevOps. Good example of integrating Next.js with popular Supabase stack (which many startups use). Ideal for MVPs and small SaaS where using a BaaS (Backend-as-a-Service) is acceptable.

**Pros:** Very developer-friendly – using Supabase means a lot of functionality (auth, DB, storage) is ready out-of-the-box with nice UI (Supabase Studio) to manage data. Praised for high code quality ("highest quality SaaS starter with Next.js, Supabase, Stripe…" per author). Good use of modern libraries: tRPC for type-safe API, Tailwind + Radix UI for sleek design. Fairly lightweight – no custom server components beyond Next API routes for Stripe webhooks. Community-supported: Supabase community references this starter, author engages on Reddit/GitHub.

**Cons:** Ties you to Supabase – while Supabase is open source, moving off it (to self-host Postgres) requires effort. Must be comfortable with Supabase Auth constraints (magic link flows, etc.). Might not include advanced enterprise features (no SAML SSO, roles beyond basic admin/member out of the box). Smaller community (hundreds of stars, not thousands yet), though growing. Supabase is evolving, so keep template updated with any Supabase API changes.

**Community:** Gained attention through Reddit post ("couldn't find a clean Next+Supabase+Stripe starter so I made one"). Has attracted contributors and is listed on Supabase's community resources. Issues get responses from maintainer. No dedicated Discord, but discussed in Supabase forums and Next.js subreddit. Part of trend of Supabase-based starters.

#### Enterprise & B2B Focused

##### BoxyHQ Enterprise SaaS Starter Kit
Creates a unique niche by targeting the B2B enterprise market with compliance features, Single Sign-On (SSO), and auditability.

| Attribute | Details |
|-----------|---------|
| Repository | [boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit) |
| Stars | ~4.6k |
| License | Apache 2.0 |
| Last Updated | December 2024 (v1.6.0) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Next.js (React) | Industry standard for enterprise web apps |
| Backend | Next.js API Routes | Serverless-ready backend logic |
| Database | PostgreSQL + Prisma | Robust relational data modeling |
| Auth | NextAuth.js + SAML Jackson | Specifically designed for Enterprise SSO (SAML/OIDC) |
| Compliance | Retraced | Audit logs service for SOC2 compliance |

**Key Features:**
- **Enterprise SSO** via SAML Jackson (Okta, Azure AD, OneLogin integration)
- **Directory Sync (SCIM)** for automatic user provisioning/de-provisioning
- Full authentication suite: email/password login, magic links, Google/GitHub OAuth
- Immutable audit logs via Retraced (finance/healthcare compliance)
- Team management primitives: create teams, invite/manage members, assign roles
- Role-Based Access Control (RBAC) with built-in roles and permission management
- Webhooks & event system via Svix
- Internationalization (i18n) support
- Dark mode UI toggle
- Email notifications (transactional emails via SMTP)
- File uploads (avatar upload)
- Cypress e2e tests pre-configured
- Docker Compose provided for local dev (with Postgres, etc.)
- Prisma Studio for DB browsing
- Docker and Playwright E2E testing integration

**Additional Features:**
- Stripe payments integration (subscription billing coming soon)
- Tailwind CSS + Tabler UI

**Deployment:** Meant for cloud deployment on Vercel or AWS. Docker setup for any container platform. CI/CD examples for GitHub Actions. Suitable for Kubernetes or Heroku.

**Use Case:** Best for startups targeting enterprise customers – if you need SSO (SAML/OIDC), team management, audit trails from day one. Great for launching a production-grade SaaS with minimal custom auth coding, especially if selling to orgs with compliance needs (SSO, SCIM user provisioning).

**Pros:** Feature-complete for multi-tenant SaaS – covers rarely-included features like SAML SSO, SCIM directory sync, audit logs. Solid architecture using Next.js and Prisma (familiar stack). Active maintenance by BoxyHQ with frequent releases and quick issue resolution. Good docs and Discord for community support. UI is clean (Tabler + Tailwind). Highly modular – turn features on/off as needed. ~40 contributors.

**Cons:** Breadth of features adds complexity – initial setup involves many env variables. Some features (billing) labeled "coming soon." If your SaaS is simple (just email auth), might be overkill. Uses Pages Router (not App Router). Apache 2.0 license requires attribution.

**Production Readiness:** Heavy-duty kit best suited for B2B startups aiming for upmarket customers. Less suited for simple B2C apps due to enterprise feature complexity.

**Community:** Active Discord channel, ~40 contributors on GitHub. Often recommended on HackerNews/Reddit for "enterprise SaaS boilerplate." Maintainers are responsive and take feature suggestions. Featured on "awesome SaaS boilerplates" lists. Acquired by Ory in 2025.

#### Multi-Tenant & Platform Starters

##### Vercel Platforms Starter Kit
Official Vercel example for building multi-tenant applications with custom subdomain routing.

| Attribute | Details |
|-----------|---------|
| Repository | [vercel/platforms](https://github.com/vercel/platforms) |
| Stars | ~6.6k |
| License | MIT |
| Last Updated | October 2025 (Next.js 15 compatible) |

**Technical Stack:** Next.js 15 (App Router) with React 19, Tailwind CSS + ShadCN UI, Upstash Redis as DB (for demo purposes). Built by Vercel.

**Key Features:**
- Multi-tenant architecture example with custom subdomain routing via Next.js Middleware
- Per-tenant content and branding (even emoji logos)
- Base Admin interface for managing tenants
- Local dev support for wildcard subdomains
- Simplified data layer using Redis (each tenant's data stored by subdomain key)
- Next.js best practices (App Router, Server Components)
- Production-ready for deployment on Vercel with wildcard domain support

**Deployment:** Vercel is the target – instructions provided for deploying and setting up wildcard domains on Vercel. Can be self-hosted with wildcard DNS.

**Use Case:** Ideal for multi-tenant SaaS (e.g., franchise or B2B SaaS where each customer has their own subdomain and isolated content). Reference implementation for subdomain routing in Next – great for learning multi-tenancy patterns or as starting point for platforms like Shopify that require tenant separation.

**Pros:** Official Vercel example – well-architected and up-to-date with latest Next.js features. Simplifies complex problem (multi-tenancy) into working template – saves time implementing routing, wildcard domain config. Lightweight and framework-idiomatic (no heavy additional libraries). Good DX with TypeScript and Admin UI to see tenants.

**Cons:** Focuses narrowly on multi-tenancy – lacks many SaaS essentials (no built-in auth, no database beyond Redis for demo, no billing integration). Meant to be extended, not a full SaaS out-of-box. If your app needs relational data or complex backend logic, you'll need to integrate those (swap Redis for Postgres/Prisma). Somewhat Vercel-specific deployment (though adaptable).

**Community:** Backed by Vercel – issues get attention from Vercel engineers. Active user base since many Next.js developers fork it to implement multi-tenant setups. Discussed in Next.js community forums and adapted in blog tutorials (multi-tenancy is a common question). Questions often appear on Reddit referencing this kit.

##### Nextacular
Open-source starter kit for building full-stack multi-tenant SaaS platforms with workspaces and custom domain support.

| Attribute | Details |
|-----------|---------|
| Repository | [nextacular/nextacular](https://github.com/nextacular/nextacular) |
| Stars | ~1.3k |
| License | MIT |
| Last Updated | Mid-2025 (active, with recent commits) |

**Technical Stack:** Next.js 13, Tailwind CSS UI, Prisma + PostgreSQL for DB, NextAuth for auth (email/password, social logins), Stripe for subscriptions, supports custom domain mapping. Monorepo template.

**Key Features:**
- Full-stack SaaS template emphasizing multi-tenancy and workspaces
- User authentication with JWT sessions or NextAuth
- Teams & workspaces (users can belong to multiple workspaces)
- Multi-tenant structure (each workspace data is isolated; includes custom domains for each tenant)
- Subscription billing and Stripe integration for paid plans
- Built-in landing page and pricing page for marketing site
- Basic email sending via Nodemailer (for welcomes, etc.)
- SEO optimizations and simple blog
- ESLint/Prettier and VSCode config included
- One-click deploy to Vercel with instructions

**Deployment:** Vercel (one-click button provided). Docker-friendly if self-hosting. Configure environment vars (database URL, Stripe keys, etc.) post-deploy.

**Use Case:** Good for founders building B2B SaaS where each customer has their own workspace or subdomain. Middle-ground – more features than minimal Next.js starter, but lighter than BoxyHQ's enterprise kit. If you want multi-tenancy with custom domains, basic billing, and pre-built landing site in one package. Structure is also educational for Next.js monorepo with shared code between app and marketing site.

**Pros:** Covers multi-tenancy cleanly (workspace model with role-based access). Has Stripe subscription flow built-in. Community-driven with positive reviews (Vercel's Steven Tey praised it: "super helpful for folks to bootstrap their MVPs"). Documentation site provided, includes custom domain configuration examples – rare and useful for SaaS. MIT licensed and free for commercial use. README showcases live SaaS products built on Nextacular.

**Cons:** At 1.3k stars, community is smaller – support exists but not as large as others. Some features require manual setup (email needs SMTP configured; custom domains require DNS setup). Relatively new, expect occasional bugs or need to update for latest Next versions. Lacks very advanced features like SSO or SCIM (integrate those if needed). Integrates many pieces (auth, Stripe), understanding full codebase takes time for newcomers.

**Community:** Active Discord channel ("Team Nextacular") and OpenCollective sponsors. Maintainers engaged, releasing updates and merging PRs. Users have built real projects with it. Mentioned on Product Hunt and GitHub discussions around multi-tenant SaaS.

### Remix

##### Remix Framework
Full-stack React framework with web standards-first philosophy and multi-runtime support.

| Attribute | Details |
|-----------|---------|
| Repository | [remix-run/remix](https://github.com/remix-run/remix) |
| Stars | ~32,000+ |
| License | MIT |
| Last Updated | November 2025 (Remix 3) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | React | Industry standard with Remix enhancements |
| Backend | Node.js/Deno/Cloudflare/Bun | Multi-runtime flexibility |
| Build | Vite | Modern build tooling |
| Philosophy | Web API standards | Progressive enhancement, form handling |

**Key Features:**
- Multi-runtime support (Node.js, Deno, Cloudflare Workers, Bun)
- Server functions and actions for data mutations
- Built-in form handling with progressive enhancement
- Loader/action pattern for data fetching
- Official stacks available (Blues Stack, Greys Stack, Indie Stack)
- Web standards-first philosophy
- Nested routing with parallel data loading

**Deployment:** Vercel, Netlify, Fly.io, AWS, Cloudflare Workers.

**Use Case:** Ideal for developers who want flexibility in deployment targets and are building modern web applications with complex forms and data interactions. Great for those who value web fundamentals and progressive enhancement.

**Pros:** Excellent developer experience, great documentation, official deployment templates (stacks), growing ecosystem, multi-runtime flexibility
**Cons:** Learning curve for newcomers to the loader/action pattern, newer patterns may feel unfamiliar to traditional React developers

**Community:** Active development, 236+ watchers, community stacks ecosystem. Discord support and extensive documentation.

#### Official Remix Stacks

##### Remix Indie Stack (Official)
Official Remix starter stack for indie developers and small teams, maintained by the Remix team.

| Attribute | Details |
|-----------|---------|
| Repository | [remix-run/indie-stack](https://github.com/remix-run/indie-stack) |
| Stars | ~2,200+ |
| License | MIT |
| Deployment | Fly.io, Docker |

**Technical Stack:** Remix, TypeScript, Prisma, SQLite, Tailwind CSS, Cypress, Vitest

**Key Features:**
- Built-in authentication with email/password
- SQLite database with Prisma ORM (easily swappable)
- CI/CD pipeline with GitHub Actions
- Docker deployment configuration
- End-to-end tests with Cypress
- Unit tests with Vitest
- ESLint and Prettier pre-configured

**Use Case:** Perfect for SaaS MVPs, CRUD applications, and rapid prototyping. Official Remix recommendation for getting started quickly.

**Pros:** Official Remix stack with batteries-included, comprehensive testing setup, CI/CD ready
**Cons:** SQLite default (can swap to Postgres), less focus on multi-tenancy features

**Community:** Official Remix documentation, Discord support, active maintainers

##### Epic Stack
Production-tested by Kent C. Dodds with comprehensive security and testing.

| Attribute | Details |
|-----------|---------|
| Repository | [epicweb-dev/epic-stack](https://github.com/epicweb-dev/epic-stack) |
| Stars | ~5,400+ |
| License | MIT |
| Deployment | Fly.io with Docker |

**Technical Stack:** Remix, React, SQLite + LiteFS, Prisma, Tailwind + Radix UI

**Key Features:**
- Full OAuth auth with role-based permissions
- Image uploads
- Email via Resend
- Honeypot spam protection
- CSP headers
- Feature flags
- Sentry monitoring
- Playwright tests
- GitHub Actions CI/CD

**Pros:** Battle-tested patterns, comprehensive feature set, security-first
**Cons:** Can be overwhelming for beginners, Fly.io-specific deployment

**Community:** epicweb.dev ecosystem, active development

### Blitz.js

##### Blitz.js Framework
Rails-inspired React framework with "Zero-API" data layer.

| Attribute | Details |
|-----------|---------|
| Repository | [blitz-js/blitz](https://github.com/blitz-js/blitz) |
| Stars | ~14,100+ |
| License | MIT |
| Last Updated | December 2025 |

**Technical Stack:** React, Next.js, Prisma, built-in session auth

**Key Features:**
- "Zero-API" data layer (import server code directly in client)
- Built-in authentication
- Code scaffolding CLI
- "Recipes" for integrations

**Deployment:** Vercel, Railway, Fly.io, Render

**Pros:** Eliminates API boilerplate, built-in auth, strong opinions reduce decisions, 66+ contributors
**Cons:** Blitz-specific patterns create lock-in, less modular than T3 variants

**Community:** Active Discord ([discord.blitzjs.com](https://discord.blitzjs.com)), comprehensive docs at [blitzjs.com/docs](https://blitzjs.com/docs). Maintained by Brandon Bayer and community.

### RedwoodJS

##### RedwoodJS Framework
GraphQL-first full-stack framework with strong conventions. An opinionated full-stack framework inspired by Ruby on Rails, using Yarn/Pnpm workspaces for a monorepo containing "web" and "api" directories.

| Attribute | Details |
|-----------|---------|
| Repository | [redwoodjs/redwood](https://github.com/redwoodjs/redwood) |
| Stars | ~17,600+ |
| License | MIT |
| Last Updated | October 2025 (v8.9.0) |

**Note:** Core team has also launched "RedwoodSDK" (React framework for Cloudflare). Original Redwood framework remains stable and maintained.

**Technical Stack:** React frontend (with Redwood Router and Cells system), GraphQL API backend (Apollo Server) running on Node.js, Prisma ORM + PostgreSQL by default, builtin GraphQL client for React side. Authentication via Redwood's auth integration (supports DB auth, Auth0, Clerk, etc. via @redwoodjs/auth package). Includes Jest for testing and Storybook for components.

**Key Features:**
- **Generators** (CLI commands to scaffold pages, components, services, etc.)
- **"Cells"** for declarative data fetching UI patterns
- Secure GraphQL API layer with services and SDL files for schema
- Access control via directives
- Prisma migrations for DB
- Built-in Storybook/Jest with VSCode extensions
- One-command auth setup (Auth0, Clerk, Firebase, DB auth)
- React Server Components (Bighorn epoch)
- Flash messaging system for toast notifications
- Background job support via Redwood Cells/Queue
- Redwood Studio admin UI for database browsing
- Realtime subscriptions (v8+) and newer React features

**Deployment:** Serverless (Netlify, Vercel) or self-hosted (Render, Fly.io, AWS). Deployment presets and CLI commands available. Integration with Prisma Data Proxy for serverless DB. Redwood Cloud (hosted solution) in development.

**Use Case:** Ideal for teams who want a Rails-like developer experience in JavaScript. Great for SaaS or applications that benefit from GraphQL with lots of structure and tooling. Especially good for startups that need to scale – architecture is scalable (API and Web separate, can be scaled independently). Shines in CRUD-heavy apps, marketplaces, or internal tools.

**Pros:** Complete end-to-end framework – front-end and back-end in one package with consistent development approach. Generators and CLI significantly speed up development (scaffold pages, layouts, CRUD for models). GraphQL API with services provides clean separation and built-in security. Thriving community and detailed documentation including tutorials. Encourages good practices (type safety, test coverage, storybook). Founded by Tom Preston-Werner (GitHub co-founder) – well-funded and here to stay. 250+ contributors.

**Cons:** Heavyweight & opinionated – must embrace Redwood's way (file structure, GraphQL). If unfamiliar with GraphQL or don't need it, may feel complex. Learning curve for Redwood conventions (Cells, Routes, Services). Bundle size larger due to GraphQL client. Debugging across GraphQL boundary adds complexity vs tRPC. Auth requires configuration for providers. Newer paradigm – fewer developers know it compared to plain Next.js, so hiring/training considerations.

**Community:** Very active – forums on community.redwoodjs.com where core devs answer questions, Discord server, weekly "Redwood Office Hours" chats. Many startups building on Redwood (some raised funding). GitHub repo has 250+ contributors with frequent releases. Redwood Conference and significant content (blogs, videos). Community explicitly welcoming to newcomers with Contributor's guide.

### Meteor (Real-Time JavaScript)

##### Meteor Framework
The original real-time full-stack JavaScript framework with the largest star count of any starter on this list.

| Attribute | Details |
|-----------|---------|
| Repository | [meteor/meteor](https://github.com/meteor/meteor) |
| Stars | ~44,800 |
| License | Open Source |
| Last Updated | December 2025 |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | JavaScript (React/Blaze/Vue) | Flexible frontend choice |
| Backend | Node.js | Unified JavaScript runtime |
| Database | MongoDB | Real-time data synchronization |
| Auth | Built-in accounts system | Zero-config authentication |

**Key Features:**
- **Real-time sync**: Data changes propagate instantly to all connected clients
- Cross-platform development (web, iOS, Android, desktop)
- Zero-config build system with npm integration
- Built-in user accounts and authentication
- Reactive programming model throughout
- Hot code reloading during development
- Isomorphic JavaScript (same code runs client/server)

**Deployment:** Meteor Galaxy (managed hosting), any web/mobile platform.

**Use Case:** Perfect for real-time applications (chat, collaboration tools, live dashboards) where data synchronization is critical. Ideal for teams building across multiple platforms (web + mobile + desktop) from a single codebase.

**Pros:** Simple setup, reactive data by default, cross-platform from day one, massive community (776+ contributors, 44k+ stars), mature ecosystem
**Cons:** Reactive programming paradigm has a learning curve, MongoDB-centric by default

**Community:** Active Discord ([discord.gg/hZkTCaVjmT](https://discord.gg/hZkTCaVjmT)), comprehensive documentation at [docs.meteor.com](https://docs.meteor.com). Large contributor base with frequent releases.

### Wasp & Open SaaS (DSL-Based)

##### Wasp Framework
Closest to Rails in JavaScript with DSL configuration.

| Attribute | Details |
|-----------|---------|
| Repository | [wasp-lang/wasp](https://github.com/wasp-lang/wasp) |
| Stars | ~18,000+ |
| License | MIT |
| Last Updated | Active (daily commits) |

**Technical Stack:** React, Node.js/Express, Prisma, TanStack Query

**Key Features:**
- DSL configuration file
- Full-stack type safety
- **8-line auth setup**
- Cron jobs and background workers
- Email sending
- One-command deployment
- AI code generator (Mage)

**Deployment:** Fly.io, Railway, Netlify, Vercel

**Pros:** Fastest path to production, abstracts all boilerplate, YC-backed
**Cons:** Requires learning Wasp DSL, less mainstream than pure frameworks

**Community:** 16,000+ Discord members, extensive documentation

##### Open SaaS
Best free complete SaaS starter. Represents a shift towards "configuration-as-code" frameworks. Built on Wasp, a distinct DSL (Domain Specific Language) that compiles to a React/Node.js/Prisma stack. "Batteries-included" starter covering nearly every SaaS requirement out-of-box.

| Attribute | Details |
|-----------|---------|
| Repository | [wasp-lang/open-saas](https://github.com/wasp-lang/open-saas) |
| Stars | ~13.1k |
| License | MIT |
| Last Updated | December 2025 (very active, latest release Dec 18, 2025) |
| Deployment | Railway, Fly.io, Netlify |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Framework | Wasp DSL (React 18 + Node.js/Express) | Abstract glue code into a unified config file |
| Database | PostgreSQL + Prisma | Standard relational stack |
| Auth | Wasp Auth (Email verification + OAuth via Google/GitHub) | Configurable via Wasp DSL (no manual wiring) |
| Payments | Stripe / Lemon Squeezy | Pre-configured webhooks and checkout flows |
| Admin | Shadcn UI Dashboard | Pre-built analytics and user management views |
| Docs | Astro Starlight | Integrated documentation site for marketing/blog |

**Key Features:**
- Automates boilerplate via the Wasp compiler (define in `.wasp` file)
- User accounts with email verification, social login (Google/GitHub OAuth)
- Multi-tenant support (extendable), team management, role-based access
- AI-ready setup with OpenAI API integration examples and vector embeddings support
- Cron Jobs and Queues via simple configuration (background workers)
- Built-in Blog (via Astro) and Documentation with rich marketing site
- SendGrid/MailGun email integration
- AWS S3 file uploads
- Playwright E2E tests
- Excellent AI/Cursor integration (AI-ready dev setup with pre-defined prompts)
- Analytics (Plausible/GA) integration
- One-command deploy to Railway or Fly.io via Wasp CLI (handles provisioning DB, server, client)
- Update mechanism to pull new template changes

**Use Case:** Perfect for founders who want a "complete" SaaS boilerplate covering all standard features – "superstack" approach. If you want to launch a product quickly with minimal coding of common features (auth, billing, etc.), OpenSaaS is ideal. Great if you appreciate end-to-end type safety and are open to using the Wasp framework.

**Pros:** Incredibly feature-rich (covers nearly every SaaS requirement out-of-box) – saves months of dev time. Strong type-safety and developer experience via Wasp (auto-generates types for front/back). Active development and large contributor base (50+ contributors). Backed by Wasp's growing community and Discord support. Excellent docs and update mechanism to pull new template changes.

**Cons:** Highly opinionated – tied to Wasp DSL, which adds a learning curve (developers must learn Wasp syntax and conventions). Less flexible if you need custom architecture – stepping outside Wasp's abstractions may be tricky. Breadth of features means more complexity – initial setup/config is heavier. Requires comfort with full-stack JS and DevOps (to manage keys for Stripe, S3, etc.). Wasp is newer than plain Next.js, so smaller ecosystem.

**Production Readiness:** 100% free, most feature-complete open-source option. Primary risk is the abstraction layer (must learn Wasp DSL). However, generated code is standard React/Node, preventing total vendor lock-in. One of the most complete starters available, targeting developers who want to ship "in days, not weeks".

**Community:** Very active Discord (#wasp community, 16,000+ members). GitHub discussions and responsive Wasp team (YC-funded, indicating long-term support). OpenSaaS has become a top-trending repo in 2025, with many users adopting it – blog posts and ProductHunt discussions reference it. Maintainers regularly merge contributions and release updates. Comprehensive docs at opensaas.sh.

### Vue / Nuxt.js

##### Nuxt UI SaaS Template (Official)
Official Nuxt template with premium UI components.

| Attribute | Details |
|-----------|---------|
| Repository | Official Nuxt Template |
| License | MIT (free tier) |

**Technical Stack:** Nuxt 3, Nuxt UI Pro components, Tailwind CSS

**Key Features:**
- Nuxt UI Pro components
- Landing pages
- Pricing pages
- Documentation and blog templates
- Auth flows

**Pros:** Official Nuxt ecosystem support
**Cons:** Some advanced components require Nuxt UI Pro license

##### SupaNuxt SaaS
Comprehensive boilerplate for the "Supa-stack" (Supabase + Nuxt), bringing TypeScript full-stack development to Vue. A Vue counterpart to the Supabase/Next starters.

| Attribute | Details |
|-----------|---------|
| Repository | [JavascriptMick/supanuxt-saas](https://github.com/JavascriptMick/supanuxt-saas) |
| Stars | ~522 |
| License | MIT |
| Last Updated | Active (2025) |

**Technical Stack:**
- Frontend: Nuxt 3, Tailwind, DaisyUI, Pinia (Vue's store)
- Backend: Nuxt Server Routes + TRPC
- Database: Supabase (PostgreSQL) + Prisma
- Auth: Supabase Auth (OAuth, Magic Link)

**Key Features:**
- **TRPC implementation** in Nuxt ecosystem for end-to-end type safety (bringing tRPC to Vue)
- Multi-Tenancy (Teams) support
- Stripe integration for subscriptions
- Dashboard and settings pages
- Default landing page template
- OpenAI API example usage (geared towards AI-powered SaaS)
- Pinia set up for global state (e.g., user session)

**Deployment:** Netlify or Vercel for Nuxt app, plus Supabase instance for backend. Uses Nuxt's server routes for custom API. Environment variables for Supabase and Stripe need configuration.

**Use Case:** If you prefer Vue/Nuxt over React or Svelte, this is one of the few robust open SaaS starters. Good for small SaaS projects, especially those involving AI (given OpenAI integration). Developers comfortable with Vue find this a quicker starting point than learning Next.js starters. Interesting for those who want to experiment with tRPC in a Vue environment.

**Pros:** Fills a gap for Vue – there are many Next.js starters, but fewer Nuxt ones. 500+ stars shows demand. Nuxt 3 brings SSR and structure similar to Next with Vue's approachable syntax. Integration with Supabase means no custom auth or basic CRUD backend coding needed. Pinia provides simple global store for managing user and team state. Uses Vue composition API best practices.

**Cons:** Not as battle-tested as some others. tRPC with Nuxt is less common, meaning less community knowledge for specific issues. Supabase does heavy lifting – any limitations there affect your app. Feature set might not be as extensive yet (no audit logs or complex role support without custom work). Vue's ecosystem for SaaS-specific components is smaller than React's.

**Community:** Listed on SaaS starters sites, author participates in Supabase and Vue communities. Vue/Nuxt developers helpful on forums; Nuxt Discord or GitHub for guidance. Supabase Discord has #vue channel for integration questions.

##### Supersaas (Commercial)
Comprehensive Nuxt 3 SaaS starter with all major features and multi-database support.

| Attribute | Details |
|-----------|---------|
| Website | [supersaas.dev](https://supersaas.dev/) |
| Stars | ~1,000+ |
| License | Commercial |
| Users | 280+ developers |

**Technical Stack:** Nuxt 3, TypeScript, Drizzle ORM, PostgreSQL, Supabase, Stripe, Tailwind CSS

**Key Features:**
- Authentication with multiple providers
- Stripe payments integration
- Role-based access control (RBAC)
- Team management
- Admin panel
- File storage integration
- Multi-database support (Postgres, Supabase)

**Deployment:** Vercel, Docker, Netlify

**Use Case:** Comprehensive SaaS applications needing all major features out-of-the-box.

**Pros:** All major SaaS features included, multi-DB support, strong documentation, Discord support
**Cons:** Paid/commercial, not fully open source

##### Supastarter (Paid)
Premium Nuxt 3 + Supabase boilerplate with comprehensive features.

| Attribute | Details |
|-----------|---------|
| Price | $349 |
| Users | 400+ |

**Key Features:**
- Lifetime updates
- One of the best Vue options available (commercial)

**Note:** Consider as an alternative if budget allows and feature set matches needs.

### Svelte / SvelteKit

##### CMSaasStarter
Full-featured SvelteKit + Supabase SaaS starter with marketing pages. A modern SaaS template leveraging Svelte's simplicity and full-stack capabilities.

| Attribute | Details |
|-----------|---------|
| Repository | [scosman/CMSaasStarter](https://github.com/scosman/CMSaasStarter) |
| Stars | ~2.3k |
| License | MIT |
| Last Updated | November 2025 (maintained by author & contributors) |

**Technical Stack:** SvelteKit (Svelte 4) front-end + back-end, Supabase (Postgres DB + Auth) as database and auth layer, Tailwind CSS, tRPC for API type-safety, Prisma ORM (with Supabase), Stripe for payments, MDX for blog content management.

**Key Features:**
- Marketing homepage and blog (with markdown/MDX content)
- Authentication (Supabase Auth with OAuth support)
- Subscription management with Stripe (plan page, pricing component)
- User dashboard after login with profile/settings pages
- Team management system (invite users, manage roles)
- Pre-built pricing page and components for features, FAQs
- Email sending via Supabase Edge Functions or 3rd-party SMTP
- SvelteKit endpoints handle server-side logic

**Deployment:** Easily deployable to Vercel, Netlify, or Supabase's hosting for Edge Functions. SvelteKit runs serverless or Node adapter – README provides platform-specific instructions. Docker supported (Dockerfile included).

**Use Case:** Perfect if you prefer Svelte's reactivity and simplicity over React. Great way to start a SaaS with smaller bundle size and simpler state management. Ideal for solo devs or small teams who want an all-in-one starter with marketing and app combined, and are comfortable using a BaaS (Supabase). Also suitable for learning SvelteKit + Supabase integration.

**Pros:** Very feature-rich for a Svelte starter – few templates include this breadth (marketing site, auth, billing). Clean and modern UI (Tailwind + prebuilt components). SvelteKit offers excellent performance. Using Supabase means less server code (focus on client logic). Solid following (2k+ stars) indicating it solved a need in Svelte community. TypeScript support ensures type safety. Follows SvelteKit best practices.

**Cons:** Supabase lock-in – moving off it to self-host Postgres requires effort. SvelteKit has smaller ecosystem than React/Next – fewer ready-made packages. If team is unfamiliar with Svelte, that's a learning curve (though many find Svelte easier than React). May not have enterprise features like SAML SSO or elaborate RBAC – those would be custom add-ons.

**Community:** Svelte community is enthusiastic; starter shared on Svelte Discords and "Awesome SvelteKit" lists. Author Scott (scosman) engages with GitHub issues and updates for new SvelteKit versions. Supabase has growing Svelte user base with support in Supabase forums.

##### svelte-starter-kit
Comprehensive monorepo-ready SvelteKit starter.

| Attribute | Details |
|-----------|---------|
| Repository | [svelte-starter-kit](https://github.com/nicholascostadev/svelte-starter-kit) |
| Stars | ~800+ |
| License | MIT |

**Technical Stack:** SvelteKit, Tailwind, GraphQL (Houdini), Auth.js

**Key Features:**
- PWA (Progressive Web App) support
- GraphQL via Houdini
- i18n internationalization
- Docker deployment ready
- Monorepo-ready architecture

##### Startino SaaS Starter
High-potential, bleeding-edge SvelteKit starter adopting Svelte 5.

| Attribute | Details |
|-----------|---------|
| Repository | [startino/saas-starter](https://github.com/startino/saas-starter) |
| Stars | ~34 (High Potential) |
| License | MIT |

**Technical Stack:**
- Frontend: SvelteKit (Svelte 5), Tailwind, Shadcn-svelte
- Backend: SvelteKit Server (Edge compatible)
- Database: Supabase Postgres
- Auth: Supabase Auth

**Key Features:**
- Adopts Svelte 5 and Shadcn-svelte (popular UI component architecture for Svelte)
- Superforms for robust server-side validation
- Built-in Blog Engine optimized for SEO
- Self-Serve Billing portal via Stripe Integration

##### SvelteKit Blog App
Full-featured SvelteKit starter with blog functionality and modern tooling.

| Attribute | Details |
|-----------|---------|
| Repository | [pro7tech/sveltekit-blog-app](https://github.com/pro7tech/sveltekit-blog-app) |
| Stars | ~1,100+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** SvelteKit, TypeScript, EdgeDB, Tailwind CSS

**Key Features:**
- Authentication with RBAC (role-based access control)
- CRUD operations with admin panel
- Mobile-responsive design
- 100% Lighthouse score optimization
- Modern blog functionality

**Use Case:** Ideal for blogs, admin dashboards, and CRUD-heavy applications using SvelteKit.

**Pros:** Modern stack with EdgeDB, comprehensive RBAC, admin UI included
**Cons:** Blog-focused (may need customization for other use cases)

##### SvelteKit Auth Starter
Authentication-focused SvelteKit starter with Lucia Auth and Prisma.

| Attribute | Details |
|-----------|---------|
| Repository | [delay/sveltekit-auth](https://github.com/delay/sveltekit-auth) |
| Stars | ~1,000+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** SvelteKit, Lucia Auth, Prisma, shadcn-svelte, Zod

**Key Features:**
- Lucia Auth implementation (modern auth library)
- Prisma ORM integration
- shadcn-svelte UI components
- Zod schema validation
- RBAC (role-based access control)

**Use Case:** Perfect for SaaS, CRUD apps, and MVPs that need solid authentication foundations.

**Pros:** Modern Lucia Auth, Prisma ORM, comprehensive RBAC, beautiful shadcn UI
**Cons:** Auth-focused (needs extension for full SaaS features)

##### sveltekit-saas (Glench)
Community SvelteKit SaaS starter with authentication and payments.

| Attribute | Details |
|-----------|---------|
| Repository | [Glench/sveltekit-saas](https://github.com/Glench/sveltekit-saas) |
| License | MIT (Open Source) |

**Key Features:**
- Auth dashboards for user management
- Stripe payments integration
- Admin panels for content management
- SvelteKit server-side rendering

**Use Case:** SaaS MVPs, subscription-based applications, and admin dashboards using SvelteKit.

### Node.js / Express (Traditional)

##### Brocoders NestJS Boilerplate
Comprehensive NestJS boilerplate with multi-database support.

| Attribute | Details |
|-----------|---------|
| Repository | [Brocoders/nestjs-boilerplate](https://github.com/Brocoders/nestjs-boilerplate) |
| Stars | ~2,800+ |
| License | MIT |

**Technical Stack:** NestJS, TypeORM or Mongoose, PostgreSQL or MongoDB

**Key Features:**
- Social auth (Apple, Facebook, Google)
- File uploads (S3)
- Swagger API docs
- Docker + CI integration
- JWT authentication

##### hackathon-starter
The classic Node.js boilerplate with comprehensive OAuth integrations, one of the most starred full-stack starters on GitHub.

| Attribute | Details |
|-----------|---------|
| Repository | [sahat/hackathon-starter](https://github.com/sahat/hackathon-starter) |
| Stars | ~35,200 |
| License | MIT |
| Last Updated | December 2025 |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Bootstrap 5, Pug templates | Classic server-rendered approach |
| Backend | Node.js, Express | Industry standard for Node.js APIs |
| Database | MongoDB | Flexible document store |
| Auth | Passport.js (OAuth) | Multiple provider support |

**Key Features:**
- Multiple OAuth providers (Google, Microsoft, Facebook, GitHub, etc.)
- AI examples with OpenAI and LangChain integration
- API integrations: Stripe, PayPal, Twilio
- Contact form with reCAPTCHA
- File upload capabilities
- Rate limiting and CSRF protection
- Cluster mode and HTTPS support

**Deployment:** Docker, AWS/Azure, MongoDB Atlas.

**Use Case:** Ideal for hackathons, rapid prototyping, and Node.js projects needing comprehensive API integrations. Perfect for developers who want a traditional server-rendered approach with extensive OAuth support.

**Pros:** Comprehensive API integrations, well-documented, massive community (35k+ stars), battle-tested
**Cons:** Pug templating may feel outdated, requires API keys for many integrations

**Community:** No dedicated Discord; uses GitHub for support. Maintained by Sahat Yalkabov.

##### MEAN Stack Starter (Linnovate)
Classic full-stack JavaScript starter with Angular and MongoDB.

| Attribute | Details |
|-----------|---------|
| Repository | [linnovate/mean](https://github.com/linnovate/mean) |
| Stars | ~12,100 |
| License | Open Source |
| Last Updated | 2025 (active) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Angular 6 | Enterprise-grade frontend framework |
| Backend | Express, Node.js | Standard Node.js API layer |
| Database | MongoDB | Document database for flexibility |
| Auth | Built-in | Session-based authentication |

**Key Features:**
- Docker support for containerized deployment
- ESLint/Prettier for code quality
- Git hooks via Husky
- Full TypeScript support
- Open component architecture

**Deployment:** Docker.

**Use Case:** Scalable full-stack JavaScript applications, especially suited for teams familiar with Angular and MongoDB ecosystems.

**Pros:** Open components, Docker-ready, established MEAN stack patterns
**Cons:** Angular 6 may require updates, less modern auth compared to JWT solutions

**Community:** Maintained by Linnovate. Part of the broader MEAN stack ecosystem.

### Astro & HTML-First Approaches

Astro has emerged as a leading framework for content-heavy sites with optional interactive "islands." These starters leverage Astro's HTML-first philosophy with selective hydration.

##### Freedom Stack
HTML-first approach combining Astro with HTMX and Alpine.js for minimal JavaScript interactivity.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Astro, Alpine.js, HTMX, Astro DB, Drizzle ORM |
| License | MIT |

**Key Features:**
- HTML-first approach with progressive enhancement
- Astro DB for data persistence
- Drizzle ORM for type-safe database queries
- HTMX for dynamic updates without heavy JavaScript
- Alpine.js for lightweight client-side interactivity

**Use Case:** Content sites, blogs, and applications prioritizing minimal JavaScript and fast load times.

##### bSaaS
Astro SaaS landing page template with extensive pre-built pages.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Astro, Tailwind CSS |
| License | MIT/Commercial |

**Key Features:**
- 10+ pre-built landing page sections
- Marketing-focused design
- SEO optimized out of the box
- Responsive design templates

**Use Case:** SaaS marketing sites, product launches, landing pages.

##### LaunchFa.st
Multi-framework SaaS starter kit supporting multiple frontend frameworks.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Astro, Next.js, or SvelteKit variants |
| License | Commercial |

**Key Features:**
- Choose your framework (Astro, Next.js, SvelteKit)
- Payment integration
- Authentication flows
- Pre-built marketing components

**Use Case:** Teams who want framework flexibility with consistent SaaS infrastructure.

### HTMX-Based Full-Stack

---

## Python Ecosystem

### FastAPI

#### FastAPI + React

##### Full Stack FastAPI Template (Tiangolo)
Maintained by the creator of FastAPI, this template defines the standard for modern Python web development. One of the most popular full-stack templates (40k+ stars), created by Sebastián Ramírez.

| Attribute | Details |
|-----------|---------|
| Repository | [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) |
| Stars | ~40k |
| License | MIT |
| Last Updated | December 2025 (updated for FastAPI, Python 3.11+) |

**Technical Stack:**
- Frontend: React (Create React App or Next.js optional), TypeScript, Vite, Tailwind, Shadcn/ui
- Backend: FastAPI (modern high-performance Python API framework), SQLModel/SQLAlchemy, Pydantic, Alembic for migrations
- Database: PostgreSQL
- Auth: OAuth2 (JWT) – signup/login endpoints issuing JWTs, password hashing with Passlib
- Nginx as reverse proxy in production, optional Celery for background tasks + Flower for task monitoring, Traefik for container orchestration

**Key Features:**
- **Automatic Client Generation**: Uses OpenAPI (Swagger) spec to automatically build TypeScript client, ensuring frontend types are always in sync with backend Pydantic models
- Production-ready out-of-the-box: user registration & login with JWT auth (and refresh tokens)
- Secure password reset via email (integrated with SMTP)
- Role-based security (users vs superusers)
- Example CRUD for items (with React components and API calls)
- Highly optimized Docker Compose setup with Traefik as reverse proxy/load balancer
- Automatic HTTPS with Traefik and Let's Encrypt for Docker deploys
- Supports multi-container cloud deployment – one command stands up Postgres, backend, frontend, proxy by reading .env files
- Async support
- GitHub Actions CI/CD configured
- Copier-based generation (cookiecutter to generate new code with same pattern)

**Deployment:** Docker Compose files for Dev and Production. In prod, docker-compose.prod.yml sets up all services (backend, frontend, db, proxy). Deployable to any Docker-friendly host (AWS EC2, DigitalOcean, etc.). Also compatible with Azure. Containerized for portability; can push frontend to Netlify/Vercel and host FastAPI on Heroku/Fly.

**Use Case:** Ideal for Python enthusiasts building a SaaS or web app who want a robust starting point. Especially useful in organizations preferring Python for business logic (data science, etc.) with snappy JS front-end. Top choice for learning: demonstrates well-structured FastAPI project and React SPA integration. Many production services built on it.

**Pros:** Extremely well-architected by FastAPI's author – follows best practices for security (JWT auth with refresh, hashed passwords), API design, and DevOps (Dockerization). Feature completeness: user management, CRUD patterns, tests, background tasks. Popularity (40k stars) means lots of community support – Q&A on GitHub and third-party articles. Type hints everywhere (FastAPI's strength) with Pydantic/SQLModel for data validation. Template can be generated via Cookiecutter or GitHub template.

**Cons:** Heavy on Docker and config – initial learning curve if unfamiliar with containers or JWT auth flows. Assumes DevOps knowledge (e.g., Traefik configuration). React front-end is fairly basic (no sophisticated state management by default). If you prefer all-Python stack (Django templating), this is more complex with two languages. While JWT is flexible, some prefer session/cookie auth (requires adjustments for SSR apps). Updates from template must be manually merged into your project.

**Production Readiness:** Most popular full-stack template overall. No payments built-in; requires adding SaaS features manually.

**Community:** Huge – FastAPI community uses this template extensively. Discussions on whether people use it in production (many do). Issues answered by community and sometimes Sebastián himself. Referenced in conference talks and tutorials. Ask questions on FastAPI's Discord/Stack Overflow with high chance of answers from template users. Cookiecutter has been forked and customized by many (different frontends or ORMs).

#### FastAPI + Other Frontends

### Django

#### Django + React

##### Apptension SaaS Boilerplate
Full SaaS with Django + React, used by Netflix/Uber projects.

| Attribute | Details |
|-----------|---------|
| Repository | [apptension/saas-boilerplate](https://github.com/apptension/saas-boilerplate) |
| Stars | ~2,800+ |
| License | MIT |
| Last Updated | September 2024 |

**Technical Stack:** Django + DRF + GraphQL (Graphene), React + TypeScript, PostgreSQL, Celery, AWS CDK

**Key Features:**
- **Multi-tenancy**
- OAuth (Google, Facebook)
- 2FA authentication
- **Stripe subscriptions**
- Email templates
- CMS integration (Contentful)
- OpenAI API integration
- NX monorepo
- Storybook

**Deployment:** AWS-based architecture with CDK

**Pros:** Used by Netflix/Uber projects, completely free, comprehensive feature set
**Cons:** Complex AWS setup (3-day onboarding estimated), requires AWS knowledge

**Community:** Comprehensive documentation

##### Django React Boilerplate (Vinta Software)
Hybrid approach leveraging Django's mature backend with a modern React frontend.

| Attribute | Details |
|-----------|---------|
| Repository | [vintasoftware/django-react-boilerplate](https://github.com/vintasoftware/django-react-boilerplate) |
| Stars | ~2.2k |
| License | MIT |

**Technical Stack:**
- Backend: Django 5, Django REST Framework (DRF)
- Frontend: React, TypeScript, Tailwind 4
- Tooling: openapi-ts (Client Gen), Celery (Tasks), Redis

**Key Features:**
- Uses drf-spectacular to generate OpenAPI schemas and openapi-ts to generate TypeScript clients
- Pre-configured Celery and Redis for background tasks (emails, processing uploads)
- CSP (Content Security Policy) out of the box
- Brute-force protection via django-defender

##### Django React Starter (Jordan-Kowal)
Advanced Django + React starter with comprehensive integrations for data-heavy applications.

| Attribute | Details |
|-----------|---------|
| Repository | [Jordan-Kowal/django-react-starter](https://github.com/Jordan-Kowal/django-react-starter) |
| Stars | ~1,100 |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:**
- Backend: Django + Django REST Framework + Celery
- Frontend: Vite + React
- Database: PostgreSQL + PostGIS (geospatial)
- Search: Meilisearch
- Messaging: RabbitMQ
- Deployment: Docker, Fly.io

**Key Features:**
- Full-text search with Meilisearch integration
- Geospatial capabilities with PostGIS
- Message queue with RabbitMQ
- Background tasks with Celery
- Fly.io deployment configuration

**Use Case:** Ideal for data/search/geospatial applications requiring advanced integrations beyond typical CRUD.

**Pros:** Advanced integrations (search, geospatial, messaging), Docker-ready, Fly.io deployment
**Cons:** Complex setup due to multiple services, steeper learning curve

#### Django + Vue

#### Django + HTMX

##### django-htmx-patterns
Best practices repository for Django + HTMX.

| Attribute | Details |
|-----------|---------|
| Repository | [spookylukey/django-htmx-patterns](https://github.com/spookylukey/django-htmx-patterns) |
| License | Public Domain (copy-paste encouraged) |

**Key Features:**
- Best practices and patterns for Django + HTMX
- Represents the growing "hypermedia-driven" movement in Django community
- Copy-paste encouraged (public domain)

#### Cookiecutter Django & Templates

##### Cookiecutter Django
Python community standard for Django scaffolding. The go-to Django project template, maintained by open-source community (originally by @pydanny et al.). Long-standing project updated frequently for new Django versions.

| Attribute | Details |
|-----------|---------|
| Repository | [cookiecutter/cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) |
| Stars | ~13,300+ |
| License | BSD-3-Clause |
| Last Updated | December 2025 |

**Technical Stack:** Django 5.2 (latest) with modular settings setup (using django-environ for 12-factor config). PostgreSQL as default DB (others optional). Front-end uses Django Templates with Bootstrap 5 (or integrate SPA separately). Celery for async tasks (optional), Redis for caching/message broker (if Celery used). Docker-compose for dev and production (with Nginx, Django app, Postgres, etc.), plus Traefik if chosen. Email via any SMTP (Anymail integration for Mailgun by default). Uses django-allauth for robust user registration (email verification, social login if configured). Default user model is custom AbstractUser (easy to extend). Built-in Whitenoise for static files, or storing static/media on AWS S3/GC Storage. Testing uses Pytest. Pre-configured Sentry for error logging, Pre-commit hooks (Black, Flake8). GitHub Actions CI included.

**Key Features:**
- **100% starting test coverage** (ships with tests to ensure template was generated correctly)
- Secure by default (SSL redirect, secure cookies)
- Docker + Traefik deployment with Let's Encrypt SSL
- Multiple cloud providers (AWS, GCP)
- Multiple email services
- Highly configurable via prompts at creation (choose options: "use Celery?", "use Docker?", "DB: Postgres/MySQL?")
- Optional Celery/DRF/Sentry/Heroku
- Pre-commit hooks (Black, Flake8)
- User authentication flows with email confirmation via allauth
- Robust settings management for multiple environments
- Role-based user groups examples (social auth groups)

**Deployment:** Multi-faceted – Docker route with production docker-compose.yml (Django with gunicorn + Nginx + Postgres, with Traefik for Let's Encrypt SSL). Traditional deployment with Procfile for Heroku and instructions for PythonAnywhere. Docker config optimized for single server or adaptable to ECS/Kubernetes. Environment variables and config well-abstracted for AWS, DigitalOcean deployment.

**Use Case:** Ideal for Django developers starting a SaaS or web product who want all best practices pre-configured. Great for content-heavy SaaS (Django admin for content management) or when you need multi-environment settings and Celery tasks. Perfect if you deploy on Docker or Heroku and want a reliable setup. Doesn't include SaaS billing or teams specifically, but can integrate Stripe fairly easily on this solid base.

**Pros:** Mature and battle-tested – has been around for years, each new Django release supported quickly. Embodies ton of community knowledge: email config, static file storage, CI done in robust way. Highly customizable at creation – pick only what you need (skip Docker or Celery if not needed). Excellent documentation and ecosystem of recipes. Security is a priority (SSL, secure settings defaults). Django's built-in admin and allauth means admin panel and user auth ready on day one – huge time saver. 250+ contributors over time.

**Cons:** More of a backend starter – frontend is server-rendered Django with Bootstrap (for fancy reactive frontend, build that or integrate JS framework separately). Multitude of options can be overwhelming for beginners. Docker usage might be overkill for simple projects (but can disable it). One-time project generator – won't easily pull in upstream updates, maintain your project as Django evolves.

**Community:** Very active. GitHub repo issue tracker is lively with support requests and discussions. Discord for Django where cookiecutter-django often comes up. Many contributors (250+). Well-known tool with many blogs and StackOverflow answers. Maintainers fundraise via OpenCollective to sustain development. Community keeps it up-to-date with Docker and CI enhancements. Maintained by pydanny (Two Scoops of Django author).

### Flask

##### React Flask Authentication (AppSeed)
Simple decoupled Flask + React starter with JWT authentication.

| Attribute | Details |
|-----------|---------|
| Repository | [app-generator/react-flask-authentication](https://github.com/app-generator/react-flask-authentication) |
| Stars | ~1,000+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** Flask, React, SQLite/PostgreSQL, JWT authentication, Material UI

**Key Features:**
- JWT-based authentication
- Material UI components
- Docker deployment ready
- Test coverage included
- Decoupled frontend/backend architecture

**Deployment:** Docker, Heroku

**Use Case:** Ideal for admin panels, CRUD applications, and rapid prototyping with Flask.

**Pros:** Simple and decoupled, good documentation, Material UI included
**Cons:** Less batteries-included compared to Django starters

**Community:** AppSeed ecosystem, active maintenance

---

## PHP Ecosystem

### Laravel

#### Laravel + Vue / Inertia

##### laravel/vue-starter-kit (Official)
Official Laravel starter with Vue 3 and Inertia.

| Attribute | Details |
|-----------|---------|
| Repository | [laravel/vue-starter-kit](https://github.com/laravel/vue-starter-kit) |
| License | MIT |

**Technical Stack:** Laravel, Vue 3 Composition API, Inertia 2, TypeScript, Tailwind CSS

**Key Features:**
- Official Laravel-maintained template
- Full auth scaffolding
- SSR support
- Vue 3 Composition API

#### Laravel + React

##### laravel/react-starter-kit (Official)
Official Laravel starter with React 19 and modern tooling.

| Attribute | Details |
|-----------|---------|
| Repository | [laravel/react-starter-kit](https://github.com/laravel/react-starter-kit) |
| License | MIT |

**Technical Stack:** Laravel, React 19, Inertia 2, TypeScript, Tailwind 4, shadcn/ui

**Key Features:**
- Official Laravel-maintained template
- Full auth scaffolding
- SSR support
- shadcn/ui components

##### nunomaduro/laravel-starter-kit
Ultra-strict TypeScript Laravel starter.

| Attribute | Details |
|-----------|---------|
| Repository | [nunomaduro/laravel-starter-kit](https://github.com/nunomaduro/laravel-starter-kit) |
| License | MIT |

**Technical Stack:** Laravel, React/Vue, TypeScript

**Key Features:**
- 100% type coverage
- PHPStan level 9
- "Cruddy by Design" patterns
- Ultra-strict TypeScript configuration

#### Laravel SaaS Starters (Wave, etc.)

##### Wave (The DevDojo)
Less of a boilerplate and more of a "SaaS-in-a-Box." Provides a fully functional application that requires customization rather than construction. Complete "SaaS in a box" for Laravel, arguably the most feature-complete starter in any language.

| Attribute | Details |
|-----------|---------|
| Repository | [thedevdojo/wave](https://github.com/thedevdojo/wave) |
| Stars | ~6.4k |
| License | MIT (free open source, DevDojo Pro sells extra videos/support) |
| Last Updated | September 2025 (v3.1.1, Wave has been around since 2018, updated for Laravel 10) |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Blade + Tailwind + Alpine.js | The "TALL" stack offers high interactivity with low JS complexity |
| Backend | Laravel 10 (PHP framework) | Mature, robust framework with immense ecosystem support |
| Database | MySQL / PostgreSQL | Standard, reliable relational storage (Eloquent ORM) |
| Auth | Laravel Sanctum (API) + Session (web) | DevDojo Auth (Native), deeply integrated |

**Key Features:**
- User registration with email verification, login, profile management
- Fully functional Voyager Admin Panel (BREAD operations GUI) for managing users, posts, pages, and running custom CRUD
- Subscription billing: plans & payments via Stripe or Paddle (with trials, tier limits)
- Teams/Organizations (Wave v1.5 added team accounts support)
- Roles & permissions: define roles (admin, user, etc.) and gate content
- Production-ready Subscription Architecture (plan management, user impersonation, automated invoicing via Stripe)
- Notifications system (users get notifications via on-site bell icon)
- Ready-to-use API with Sanctum tokens (serve JS front-end or mobile app)
- Blog and page builder: create blog posts or site pages via admin (useful for marketing content)
- User impersonation: Admins can log in as other users to assist them
- "Themes" system for swapping UI skins (DevDojo offers some plugins)
- Modular plugin system for extending features
- Beautiful UI for landing page and dashboard

**Deployment:** Standard Laravel deployment – LAMP/LEMP server or services like Laravel Forge, Ploi, Vapor. Docker setup for local dev. Many use DigitalOcean or AWS with Forge. Configure env variables for database, mail (email verification and notifications), Stripe keys.

**Use Case:** Best for PHP/Laravel developers who want a huge head start. Building a SaaS that needs user management, subscriptions, admin dashboards – Wave gives you that to immediately start adding domain-specific features. Perfect for membership sites, content SaaS, or products where users login and pay for premium features. Good if you want combined CMS + SaaS (Voyager admin can manage content).

**Pros:** All-inclusive – arguably the most feature-complete starter in any language. Polished UI and tons of functionality (user avatars, API tokens UI, etc.). Laravel's strength in authentication and billing (via Cashier) shines. Rapid setup: SaaS with logins, subscriptions, and blog by just configuring .env settings and running migrations. Active maintenance by DevDojo (founder created Wave for community). Theming ability for customizing look & feel. 1k+ forks on GitHub.

**Cons:** With so many features, learning curve is real – need to understand Laravel and Voyager admin to customize effectively. Can feel bloated if you don't need everything (e.g., blog or marketing site). Voyager admin has its own patterns that not every Laravel dev likes. Being PHP, real-time features (notifications currently on-page only) might need Pusher or Echo setup. Default front-end uses Blade and jQuery for some interactions; integrating modern Vue or React requires manual work. Long-term support tied to DevDojo (though it's open source, community could fork).

**Production Readiness:** Arguably the fastest path to revenue for a solo developer. User Impersonation feature demonstrates maturity. Opinionated nature (Voyager, Blade) makes it difficult to decouple for React frontend later.

**Community:** DevDojo has dedicated Wave community – forums where users ask questions, share how they built on Wave. GitHub repo active with 1k+ forks. DevDojo's founder Tony engages often. Many YouTube videos and tutorials on using Wave (has been around for years). Wave's popularity in Laravel circles is high – often recommended as starting point for new SaaS apps. Many have launched startups on Wave, attesting to robustness.

---

## Ruby Ecosystem

### Rails

#### Rails + React

##### ReactifyRails
Rails + React integration starter.

| Attribute | Details |
|-----------|---------|
| Repository | [akhilgkrishnan/reactify-rails](https://github.com/akhilgkrishnan/reactify-rails) |
| License | MIT |

**Technical Stack:** Rails 7+, React, Webpacker/Shakapacker

##### rails-react-boilerplate
Another Rails + React integration option.

| Attribute | Details |
|-----------|---------|
| Repository | [giannisp/rails-react-boilerplate](https://github.com/giannisp/rails-react-boilerplate) |
| License | MIT |

##### tabler-rails
Rails admin dashboard starter.

| Attribute | Details |
|-----------|---------|
| Repository | tabler-rails |
| License | MIT |

**Key Features:** Admin dashboard UI components

##### Rails Vite Starterkit
Modern Rails 8.1 starter with Vite, React 18, and comprehensive SaaS features.

| Attribute | Details |
|-----------|---------|
| Repository | [carlweis/rails-vite-starterkit](https://github.com/carlweis/rails-vite-starterkit) |
| Stars | ~1,100+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** Rails 8.1, Vite, React 18, TypeScript, Tailwind CSS, PostgreSQL, Devise

**Key Features:**
- Two-factor authentication (2FA)
- Role-based access control (RBAC)
- Background jobs with Sidekiq
- Docker deployment configuration
- Admin UI included
- Kamal deployment support

**Use Case:** Modern Rails SaaS applications needing Vite build tooling with React frontend.

**Pros:** Batteries-included with 2FA, RBAC, background jobs, Docker ready
**Cons:** Heavier setup for minimal applications

#### Rails + Vue

##### templatus-vue
Modern Rails 8.1 + Vue 3 starter with comprehensive testing and PWA support.

| Attribute | Details |
|-----------|---------|
| Repository | [templatus/templatus-vue](https://github.com/templatus/templatus-vue) |
| Stars | ~1,100+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** Rails 8.1, Vue 3, Vite, TypeScript, Tailwind CSS, PostgreSQL

**Key Features:**
- Progressive Web App (PWA) support
- CI/CD pipeline included
- Error tracking integration
- Comprehensive test coverage
- Docker production deployment

**Use Case:** Modern Rails + Vue applications needing PWA capabilities and strong testing.

**Pros:** Small footprint, well-tested, PWA support
**Cons:** Docker production deployment only

#### Rails + Hotwire / Turbo

Rails 7 ships with **Hotwire** (Turbo + Stimulus) as the default frontend, providing real-time interactivity without JavaScript framework overhead.

**Core Components:**
- **Turbo Drive** — AJAX navigation without full reloads
- **Turbo Frames** — Independent page section updates
- **Turbo Streams** — Real-time updates via ActionCable

##### Bullet Train (Open Source)
Andrew Culver's open-source Rails SaaS starter.

| Attribute | Details |
|-----------|---------|
| Repository | [bullet-train-co/bullet_train](https://github.com/bullet-train-co/bullet_train) |
| License | MIT |

**Key Features:**
- Complete SaaS foundation
- Multi-tenancy
- Roles and permissions
- Webhooks
- OAuth integrations

**Note:** Open-source alternative to paid Jumpstart Pro ($150)

---

## Systems Languages (Performance-Focused)

### Go / Golang

#### Go + HTMX

| Name | Stack | Key Features | Status |
|------|-------|--------------|--------|
| **go-htmx-starter** (carsonkrueger) | Go, HTMX, PostgreSQL, Templ, go-jet | Session auth with RBAC, type-safe templates | Active |
| **go-htmx-starter** (FelipeAfonso) | Go, HTMX, Tailwind, Bun, Vite | Hot reloading, frontend-first DX | Production use |
| **go-echo-templ-htmx** (emarifer) | Go (Echo), Templ, HTMX, SQLite | Session auth, onion architecture, hot reload | ~1.0k stars |

**Ideal for**: Applications prioritizing minimal JavaScript, fast server rendering, and single-binary deployment.

##### go-echo-templ-htmx
Full-stack Go starter with Echo framework and HTMX for minimal JavaScript interactivity.

| Attribute | Details |
|-----------|---------|
| Repository | [emarifer/go-echo-templ-htmx](https://github.com/emarifer/go-echo-templ-htmx) |
| Stars | ~1,000 |
| License | MIT |
| Last Updated | December 2023 (maintained) |

**Technical Stack:** Go (Echo framework), Templ (type-safe templates), HTMX, SQLite, Tailwind CSS, DaisyUI

**Key Features:**
- CRUD operations with session-based authentication
- Onion architecture (clean code structure)
- Hot reloading for development
- Tailwind CSS + DaisyUI for modern UI
- Minimal JavaScript approach

**Use Case:** Learning full-stack Go, CRUD applications, prototyping with minimal JavaScript.

**Pros:** Minimal JS, modern UX, strong documentation, clean architecture
**Cons:** SQLite only (not SaaS-oriented), smaller ecosystem

#### Go + React / Vue

##### fiber-go-template (Official)
Official Go Fiber template with full-stack features.

| Attribute | Details |
|-----------|---------|
| Repository | Go Fiber Official |
| License | MIT |

**Technical Stack:** Go Fiber, PostgreSQL, Redis, JWT

**Key Features:**
- Swagger docs
- Database migrations
- Docker deployment
- Official Fiber template

##### gofiber/recipes
Official Go Fiber examples with React SPA patterns.

| Attribute | Details |
|-----------|---------|
| Repository | [gofiber/recipes](https://github.com/gofiber/recipes) |
| License | MIT |

**Key Features:**
- SPA example with React
- Clean Architecture patterns
- Official examples repository

##### SaaS Startup Kit (Go)
Golang microservices architecture option.

| Attribute | Details |
|-----------|---------|
| Repository | Community maintained |
| License | MIT |

**Key Features:** Microservices architecture for Go-based SaaS

##### Go React TypeScript Template
Minimalist starter prioritizing simplicity and the standard library.

| Attribute | Details |
|-----------|---------|
| Repository | [AkashRajpurohit/go-react-typescript-template](https://github.com/AkashRajpurohit/go-react-typescript-template) |
| Stars | ~15 |
| License | MIT |

**Technical Stack:**
- Backend: Go (Standard Lib)
- Frontend: React, Vite, TanStack Router
- Tooling: Air (Hot Reload), GoReleaser

**Key Features:**
- Air Integration for backend hot-reloading (critical DX feature)
- GoReleaser and multi-platform Dockerfiles for binary distribution
- Avoids complex ORMs, adhering to Go's philosophy of simplicity

### Rust

#### Loco Framework

##### Loco (The One-Person Framework)
Explicitly aims to replicate the developer experience of Rails within Rust.

| Attribute | Details |
|-----------|---------|
| Repository | [loco-rs/loco](https://github.com/loco-rs/loco) |
| Stars | ~8.4k |
| License | Apache 2.0 |
| Last Updated | July 2025 (v0.16.3) |

**Technical Stack:**
- Backend: Rust (Axum based)
- Database: Sea-ORM (Async)
- Auth: Built-in Loco Auth (Session/JWT)

**Key Features:**
- **CLI Scaffolding** (`loco generate model`, `loco generate controller`) familiar to Rails developers
- Integrated Task Queues (Redis/Threads), Mailers, and Scheduler (cron replacement)
- Dedicated "SaaS Starter" mode generating user registration, verification, and password reset flows

#### Axum-Based Starters

##### Rustzen Admin
Decoupled starter focusing on the React/Rust interface.

| Attribute | Details |
|-----------|---------|
| Repository | [idaibin/rustzen-admin](https://github.com/idaibin/rustzen-admin) |
| Stars | ~112 |
| License | MIT |

**Key Features:**
- Mock Data endpoints for parallel frontend/backend development
- Complete Role-Based Access Control (RBAC) system in Rust

#### Leptos & Dioxus (Rust Full-Stack)

##### Leptos start-axum (Official)
Official Leptos template with Axum backend.

| Attribute | Details |
|-----------|---------|
| Repository | [leptos-rs/start-axum](https://github.com/leptos-rs/start-axum) |
| License | Unlicense |

**Technical Stack:** Leptos 0.8+, Axum

**Key Features:**
- Server-side rendering with hydration
- Isomorphic server functions
- Hot reloading

**Deployment:** AWS Lambda, Fly.io, Cloud Run

##### Dioxus
Full-stack Rust for web, desktop, and mobile from one codebase.

| Attribute | Details |
|-----------|---------|
| Repository | [DioxusLabs/dioxus](https://github.com/DioxusLabs/dioxus) |
| Stars | ~24,500+ |
| License | MIT |

**Key Features:**
- React-like RSX syntax
- Built-in Tailwind support
- <50kb web apps
- Cross-platform (web, desktop, mobile)

**Production Readiness:** Most production-viable Rust option. Maximum type-safety, WebAssembly performance, cross-platform applications.

---

## .NET / C# Ecosystem

### Blazor

##### Official Blazor Template
Official .NET template with multiple render modes.

| Attribute | Details |
|-----------|---------|
| Command | `dotnet new blazor --interactivity Auto --auth Individual` |
| License | MIT |

**Key Features:**
- Static SSR
- Interactive server (SignalR)
- WebAssembly modes
- Built-in Identity UI

##### ServiceStack Blazor Template
Enhanced Blazor template with additional features.

| Attribute | Details |
|-----------|---------|
| Repository | ServiceStack Blazor |
| License | Commercial/Free tier |

**Key Features:**
- Tailwind theming
- AutoQueryGrid components
- Dual ORM support
- Kamal deployments

### ASP.NET + React

##### NetCoreTemplates React SPA
Modern .NET 10 + React 19 starter with ServiceStack integration.

| Attribute | Details |
|-----------|---------|
| Repository | [NetCoreTemplates/react-spa](https://github.com/NetCoreTemplates/react-spa) |
| Stars | ~1,100+ |
| License | MIT |
| Last Updated | 2025 (active) |

**Technical Stack:** .NET 10, React 19, Vite, TypeScript, Tailwind CSS, ServiceStack

**Key Features:**
- Authentication with ServiceStack
- Background jobs support
- Docker deployment ready
- Cross-platform (Windows, Linux)
- Modern Vite build tooling

**Use Case:** Modern .NET + React SPA applications with ServiceStack integration.

**Pros:** Modern stack (.NET 10, React 19), production-ready, Docker support
**Cons:** ServiceStack-specific patterns (requires familiarity)

### ASP.NET + Vue

---

## Elixir / Phoenix

### Phoenix LiveView

Phoenix's built-in **LiveView** eliminates most JavaScript needs with server-rendered real-time UX.

##### Phoenix SaaS Kit (Commercial)
Complete SaaS foundation for Phoenix.

**Key Features:**
- Payments integration
- Multi-tenancy
- AI functionality

##### LiveSAASKit
SaaS starter with comprehensive features.

**Key Features:**
- Complete SaaS foundations
- Real-time by default via Erlang VM scalability

##### Petal Stack
Phoenix + Tailwind + HEEX component library with extensive pre-built components.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Phoenix, Tailwind CSS, HEEX components |
| License | MIT |

**Key Features:**
- 100+ pre-built HEEX components
- Tailwind CSS integration
- LiveView compatible
- Form components, tables, modals
- Consistent design system

**Use Case:** Phoenix applications needing a rich component library for rapid UI development.

##### Cozystack SaaS Template
Full Phoenix SaaS boilerplate with authentication and billing.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Phoenix, LiveView, Tailwind CSS, Stripe |
| License | Commercial/MIT |

**Key Features:**
- Complete authentication system
- Stripe subscription billing
- User management dashboard
- LiveView real-time features
- Deployment configurations

**Use Case:** SaaS applications built with Phoenix/Elixir stack.

**Production Readiness:** Phoenix LiveView is ideal for real-time applications with Erlang VM scalability.

### Phoenix + React / Vue

---

## Mobile & Cross-Platform

### React Native

##### Ignite (Infinite Red)
The de-facto standard for React Native development.

| Attribute | Details |
|-----------|---------|
| Repository | [infinitered/ignite](https://github.com/infinitered/ignite) |

**Key Features:**
- Uses MobX-State-Tree for state management
- CLI for generating components and screens
- Battle-tested on real client projects, ensuring architecture scales

### Expo

##### Obytes Starter
Focused on the Expo ecosystem with modern tooling.

| Attribute | Details |
|-----------|---------|
| Repository | [obytes/react-native-template-obytes](https://github.com/obytes/react-native-template-obytes) |

**Key Features:**
- Expo Router and NativeWind (Tailwind for Mobile)
- Environment variable management across Dev/Staging/Prod
- GitHub Actions for OTA (Over-the-Air) updates via EAS (Expo Application Services)

### Cross-Platform Web + Mobile (Monorepo)

---

## Specialized Categories

### Enterprise & B2B Solutions

#### SAML SSO & SCIM Integration
- **[boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit)** - Enterprise SSO via SAML Jackson with Directory Sync (SCIM) for automatic user provisioning

#### Audit Logging & Compliance

#### Multi-Tenancy & Team Management
- **[vercel/platforms](https://github.com/vercel/platforms)** - Multi-tenant subdomain routing for Next.js
- **[nextacular/nextacular](https://github.com/nextacular/nextacular)** - Workspaces and custom domain support
- **[boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit)** - Team management with RBAC

### AI / LLM Integration Starters
- **Open SaaS** includes AI-ready setup with OpenAI API integration examples and vector embeddings support

### Real-Time & WebSocket Focused

### Headless CMS + Full-Stack

##### Directus
Open-source data platform and headless CMS with REST & GraphQL APIs.

| Attribute | Details |
|-----------|---------|
| Repository | [directus/directus](https://github.com/directus/directus) |
| Stars | ~33,700+ |
| License | BSL 1.1 (free for <$5M revenue) |
| Last Updated | Active (2025) |

**Technical Stack:** Node.js backend, Vue.js admin dashboard, SQL database agnostic (PostgreSQL, MySQL, SQLite, etc.)

**Key Features:**
- REST & GraphQL APIs auto-generated from database schema
- SQL database agnostic (works with any SQL database)
- Vue.js admin dashboard with customizable interface
- Official starter templates for Next.js, Nuxt, etc.
- User roles and permissions system
- File management and asset transformation
- Webhooks and flows automation

**Use Case:** Content-heavy applications, backend for JAMstack sites, custom admin panels, API-first projects.

**Pros:** Database agnostic, beautiful admin UI, extensive API options
**Cons:** BSL license requires license for >$5M revenue, self-hosted complexity

##### Payload CMS
Modern Node.js headless CMS with TypeScript-first approach.

| Attribute | Details |
|-----------|---------|
| Repository | [payloadcms/payload](https://github.com/payloadcms/payload) |
| Stars | ~30,000+ |
| License | MIT |
| Last Updated | Active (2025) |

**Technical Stack:** Node.js, TypeScript, React admin panel, MongoDB or PostgreSQL

**Key Features:**
- TypeScript-first configuration
- Code-first schema definition
- Built-in authentication and access control
- Rich text editor with Lexical
- Official Next.js website and blog templates
- Live preview and draft system
- Extensible with hooks and plugins

**Use Case:** Content-heavy applications, blogs, e-commerce backends, enterprise CMS needs.

**Pros:** TypeScript native, code-first approach, MIT license, excellent DX
**Cons:** Learning curve for complex configurations, resource-intensive

### Admin Dashboard Templates

##### shadcn/ui Admin Dashboard
Component collection for building admin dashboards with Next.js and React.

| Attribute | Details |
|-----------|---------|
| Tech Stack | Next.js, React, shadcn/ui, Tailwind CSS |
| License | MIT (Free + Premium versions) |

**Key Features:**
- Pre-built admin pages and layouts
- Data tables with sorting/filtering
- Charts and analytics components
- Form components with validation
- Dark mode support
- Premium versions available (Shadcn UI Kit)

**Use Case:** Admin panels, internal tools, data dashboards, backoffice applications.

### Browser Extensions

##### Extro (TurboStarter)
Specialized starter for building cross-browser extensions.

| Attribute | Details |
|-----------|---------|
| Repository | [turbostarter/extro](https://github.com/turbostarter/extro) |

**Key Features:**
- Builds cross-browser extensions (Chrome, Firefox, Edge)
- Uses WXT (Web Extension Framework) for manifest version handling (MV2/MV3)
- Hot-reloading for extension development

---

## Feature-Specific Resources

### Authentication Solutions

#### NextAuth / Auth.js
- Used by [boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit) with SAML Jackson for enterprise SSO
- Used by [nextacular/nextacular](https://github.com/nextacular/nextacular) for multi-tenant auth

#### Supabase Auth
- Used by [supanuxt-saas](https://github.com/JavascriptMick/supanuxt-saas), [startino/saas-starter](https://github.com/startino/saas-starter), [scosman/CMSaasStarter](https://github.com/scosman/CMSaasStarter), and [KolbySisk/next-supabase-stripe-starter](https://github.com/KolbySisk/next-supabase-stripe-starter)

#### Clerk
- Used by [ixartz/Next-js-Boilerplate](https://github.com/ixartz/Next-js-Boilerplate) for managed auth with MFA/Social login

#### Custom / Self-Hosted
- **Loco** (Rust) includes built-in Loco Auth (Session/JWT)
- **Wave** (Laravel) uses DevDojo Auth (Native)

### Payment & Billing Integration

#### Stripe Integration
- **[ixartz/Next-js-Boilerplate](https://github.com/ixartz/Next-js-Boilerplate)** - Full Stripe integration
- **[wasp-lang/open-saas](https://github.com/wasp-lang/open-saas)** - Pre-configured Stripe webhooks and checkout flows
- **[thedevdojo/wave](https://github.com/thedevdojo/wave)** - Automated invoicing via Stripe
- **[startino/saas-starter](https://github.com/startino/saas-starter)** - Self-serve billing portal
- **[nextacular/nextacular](https://github.com/nextacular/nextacular)** - Subscription billing with Stripe
- **[KolbySisk/next-supabase-stripe-starter](https://github.com/KolbySisk/next-supabase-stripe-starter)** - Supabase + Stripe integration
- **[scosman/CMSaasStarter](https://github.com/scosman/CMSaasStarter)** - SvelteKit + Stripe payments

#### Lemon Squeezy
- **[wasp-lang/open-saas](https://github.com/wasp-lang/open-saas)** - Alternative to Stripe

#### Paddle

### Database & ORM Options

#### Prisma
- Used by: boxyhq/saas-starter-kit, wasp-lang/open-saas, supanuxt-saas, nextacular/nextacular, scosman/CMSaasStarter

#### Drizzle
- Used by: ixartz/Next-js-Boilerplate, nextjs/saas-starter (lighter and faster than Prisma, SQL-like syntax)

#### SQLModel / SQLAlchemy
- Used by: fastapi/full-stack-fastapi-template (SQLModel)

#### TypeORM / Sequelize

### Deployment & DevOps

#### Vercel / Netlify Optimized

#### Docker & Container-Ready
- **[fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)** - Optimized Docker Compose with Traefik reverse proxy
- **[boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit)** - Docker integration

#### Railway / Fly.io

#### Self-Hosted / VPS

---

## Pricing & Licensing

### Fully Open Source (MIT, Apache, BSD)

| Repository | License | Stars |
|------------|---------|-------|
| meteor/meteor | Open Source | ~44.8k |
| fastapi/full-stack-fastapi-template | MIT | ~40k |
| sahat/hackathon-starter | MIT | ~35.2k |
| remix-run/remix | MIT | ~32k |
| t3-oss/create-t3-app | MIT | ~28.3k |
| DioxusLabs/dioxus | MIT | ~24.5k |
| kriasoft/react-starter-kit | MIT | ~23.4k |
| wasp-lang/wasp | MIT | ~18k |
| redwoodjs/redwood | MIT | ~17.6k |
| nextjs/saas-starter | MIT | ~15.1k |
| blitz-js/blitz | MIT | ~14.1k |
| cookiecutter/cookiecutter-django | BSD-3-Clause | ~13.3k |
| wasp-lang/open-saas | MIT | ~13.1k |
| ixartz/Next-js-Boilerplate | MIT | ~12.4k |
| linnovate/mean | Open Source | ~12.1k |
| loco-rs/loco | Apache 2.0 | ~8.4k |
| vercel/platforms | MIT | ~6.6k |
| thedevdojo/wave | MIT | ~6.4k |
| t3-oss/create-t3-turbo | MIT | ~5.9k |
| epicweb-dev/epic-stack | MIT | ~5.4k |
| boxyhq/saas-starter-kit | Apache 2.0 | ~4.6k |
| brocoders/nestjs-boilerplate | MIT | ~2.8k |
| apptension/saas-boilerplate | MIT | ~2.8k |
| scosman/CMSaasStarter | MIT | ~2.3k |
| vintasoftware/django-react-boilerplate | MIT | ~2.2k |
| remix-run/indie-stack | MIT | ~2.2k |
| nextacular/nextacular | MIT | ~1.3k |
| relivator/relivator | MIT | ~1.2k |
| pro7tech/sveltekit-blog-app | MIT | ~1.1k |
| Jordan-Kowal/django-react-starter | MIT | ~1.1k |
| carlweis/rails-vite-starterkit | MIT | ~1.1k |
| templatus/templatus-vue | MIT | ~1.1k |
| NetCoreTemplates/react-spa | MIT | ~1.1k |
| delay/sveltekit-auth | MIT | ~1.0k |
| app-generator/react-flask-authentication | MIT | ~1.0k |
| emarifer/go-echo-templ-htmx | MIT | ~1.0k |
| KolbySisk/next-supabase-stripe-starter | MIT | ~720 |
| supanuxt-saas | MIT | ~522 |
| rustzen-admin | MIT | ~112 |
| startino/saas-starter | MIT | ~34 |
| go-react-typescript-template | MIT | ~15 |

### Open Core / Freemium

- **ixartz/SaaS-Boilerplate** — Free tier with Pro upgrade available

### Paid / Premium Starters

| Paid Starter | Price | Stack | Key Features | Free Alternative |
|--------------|-------|-------|--------------|------------------|
| **ShipFast** | $199-299 | Next.js, Stripe, MongoDB/Supabase | Rapid deployment, email integration, SEO setup, detailed tutorials | Open SaaS, ixartz SaaS |
| **SaaS Starter** | $199-499 | Next.js 15, Stripe, Supabase | Admin dashboard, production-ready, subscription plans | Open SaaS, Vercel SaaS Starter |
| **Supastarter** | $349 | Next.js, Nuxt, or Astro + Supabase | Lifetime updates, multi-framework, 400+ users | Open SaaS, SupaNuxt SaaS |
| **MakerKit** | ~$199 | Next.js/Remix + Firebase/Supabase | Multi-tenant, team features | Open SaaS, BoxyHQ |
| **SaaS Pegasus** | $249-999 | Django + React or HTMX | Enterprise features, extensive docs | Cookiecutter Django, Apptension |
| **Jumpstart Pro** | ~$150 | Rails | Hotwire, multitenancy | Bullet Train (open-source) |
| **ASPnetzero** | $2,999-9,999 | .NET | Enterprise-grade, Angular/MVC | Blazor official template |

### Community-Recommended "Hidden Gems"

Based on Reddit (r/webdev, r/nextjs, r/SaaS), Hacker News, and Dev.to discussions:

- **Achromatic** — Next.js 15 + React 19 + shadcn/ui (~40k SLOC), comprehensive but lesser-known
- **Bullet Train** (Rails) — Andrew Culver's open-source Rails SaaS, MIT licensed
- **SaaS Startup Kit** (Go) — Golang microservices architecture option
- **Taxonomy** (by shadcn/ui creator) — Simple micro-SaaS starter

---

## Comparison & Selection

### Framework Comparison Tables

### Feature Matrix

| Repository | Auth Provider | Database (ORM) | Stars |
|------------|---------------|----------------|-------|
| meteor/meteor | Built-in Accounts | MongoDB | ~44.8k |
| fastapi/full-stack-fastapi-template | OAuth2 / JWT | PostgreSQL (SQLModel) | ~40k |
| sahat/hackathon-starter | Passport.js (OAuth) | MongoDB | ~35.2k |
| remix-run/remix | Flexible (per stack) | Flexible (per stack) | ~32k |
| t3-oss/create-t3-app | NextAuth | PostgreSQL (Prisma/Drizzle) | ~28.3k |
| DioxusLabs/dioxus | Custom | Any | ~24.5k |
| kriasoft/react-starter-kit | Better Auth | Neon PostgreSQL (Drizzle) | ~23.4k |
| wasp-lang/wasp | Wasp Auth | PostgreSQL (Prisma) | ~18k |
| redwoodjs/redwood | Auth0/Clerk/Firebase | PostgreSQL (Prisma) | ~17.6k |
| nextjs/saas-starter | JWT | PostgreSQL (Drizzle) | ~15.1k |
| blitz-js/blitz | Built-in Session | PostgreSQL (Prisma) | ~14.1k |
| cookiecutter/cookiecutter-django | django-allauth | PostgreSQL (Django ORM) | ~13.3k |
| wasp-lang/open-saas | Wasp Auth | PostgreSQL (Prisma) | ~13.1k |
| ixartz/Next-js-Boilerplate | Clerk | PostgreSQL (Drizzle) | ~12.4k |
| linnovate/mean | Built-in | MongoDB | ~12.1k |
| loco-rs/loco | Loco Auth | PostgreSQL (Sea-ORM) | ~8.4k |
| vercel/platforms | None (demo) | Redis (Upstash) | ~6.6k |
| thedevdojo/wave | Native | MySQL / SQLite | ~6.4k |
| t3-oss/create-t3-turbo | Better-Auth | Supabase/Drizzle | ~5.9k |
| epicweb-dev/epic-stack | OAuth | SQLite (Prisma) | ~5.4k |
| boxyhq/saas-starter-kit | NextAuth + SAML | PostgreSQL (Prisma) | ~4.6k |
| brocoders/nestjs-boilerplate | JWT | PostgreSQL/MongoDB | ~2.8k |
| apptension/saas-boilerplate | OAuth/2FA | PostgreSQL (DRF) | ~2.8k |
| scosman/CMSaasStarter | Supabase Auth | PostgreSQL (Supabase) | ~2.3k |
| vintasoftware/django-react-boilerplate | Native / Token | PostgreSQL (Django ORM) | ~2.2k |
| remix-run/indie-stack | Email/Password | SQLite (Prisma) | ~2.2k |
| nextacular/nextacular | NextAuth | PostgreSQL (Prisma) | ~1.3k |
| relivator/relivator | NextAuth | PostgreSQL (Drizzle) | ~1.2k |
| pro7tech/sveltekit-blog-app | Custom | EdgeDB | ~1.1k |
| Jordan-Kowal/django-react-starter | Token | PostgreSQL+PostGIS (Django ORM) | ~1.1k |
| carlweis/rails-vite-starterkit | Devise | PostgreSQL | ~1.1k |
| templatus/templatus-vue | Custom | PostgreSQL | ~1.1k |
| NetCoreTemplates/react-spa | ServiceStack | Any | ~1.1k |
| delay/sveltekit-auth | Lucia Auth | PostgreSQL (Prisma) | ~1.0k |
| emarifer/go-echo-templ-htmx | Session | SQLite | ~1.0k |
| KolbySisk/next-supabase-stripe-starter | Supabase Auth | PostgreSQL (Supabase) | ~720 |
| supanuxt-saas | Supabase | PostgreSQL (Prisma) | ~522 |

### Recommendations by Use Case

#### Rapid MVP / Indie Hackers
- **Open SaaS** (wasp-lang/open-saas): Most complete free option with payments, email, admin dashboard
- **Laravel Wave** (thedevdojo/wave): Best for non-technical founders or solo devs who know PHP
- **Next.js Boilerplate** (ixartz): Best for React devs wanting a modern, SaaS-ready stack with Clerk auth

#### TypeScript Purists
- **create-t3-app + manual SaaS additions**: Maximum type-safety with flexibility

#### Enterprise / Series A+
- **boxyhq/saas-starter-kit**: Clear winner due to SSO/SAML support, Directory Sync (SCIM), and audit logging

#### Python Developers
- **FastAPI Full-Stack Template** (API-first) or **Cookiecutter Django** (traditional)

#### Rails-like DX in JavaScript
- **Wasp** or **Blitz.js**: Convention-over-configuration

#### GraphQL-first
- **RedwoodJS**: Strong conventions, excellent tooling

#### Performance-Critical Apps
- **Go + HTMX** or **Rust Leptos**: Minimal JavaScript, maximum speed

#### Vue Developers
- **Nuxt UI SaaS Template** (free) or **Supastarter** (paid)

#### Real-time Applications
- **Meteor** (meteor/meteor): Original real-time JavaScript framework, 44k+ stars, cross-platform
- **Phoenix LiveView**: Erlang VM scalability, real-time by default

#### Hackathons & Rapid Prototyping
- **hackathon-starter** (sahat/hackathon-starter): Classic Node.js with comprehensive OAuth and API integrations

#### Learning & Education
- **hackathon-starter**: Well-documented, extensive OAuth examples
- **Full Stack FastAPI Template**: Clean architecture for learning Python API development

#### Content-Heavy / CMS

#### Cross-Platform Web + Mobile
- **create-t3-turbo** (t3-oss/create-t3-turbo): Monorepo for Next.js + Expo with shared code

### Complexity vs. Control Matrix

**High Abstraction (Maximum Velocity):**
- Laravel Wave, Next.js Boilerplate (ixartz), Open SaaS, Meteor

**Medium Abstraction (Balanced):**
- Full Stack FastAPI Template, SupaNuxt, hackathon-starter, MEAN Stack

**Low Abstraction (Maximum Control):**
- Go React Template, Loco (Rust), create-t3-turbo

### Trends & Insights (2024-2025)

1. **Meta-Framework Dominance**: Next.js, Nuxt, SvelteKit increasingly preferred over decoupled architectures
2. **Systems Languages for Web**: Rust (Loco) bringing Rails-like DX with memory safety
3. **Auth/Payments as Infrastructure**: Clerk, Supabase Auth, Stripe considered table stakes
4. **Type Safety End-to-End**: TRPC, automatic OpenAPI client generation becoming standard
5. **TypeScript as Default**: TypeScript is now the norm for new starters, both frontend and backend
6. **Monorepo Architectures**: Nx and Turborepo increasingly popular for unified dev/deploy pipelines
7. **SaaS Features Standard**: RBAC, payments, multi-tenancy now expected in top-tier starters
8. **Cloud-Native Deployment**: Vercel, Railway, Docker expected out-of-the-box
9. **Declarative Frameworks Rising**: Wasp, OpenSaaS gaining traction for rapid prototyping
10. **AI/LLM Integration Emerging**: Some new starters include OpenAI API integration patterns
11. **Open-Source Over Paid**: Developers increasingly favor robust open-source starters over expensive premium kits
12. **Community Quality Signal**: Discord, docs, and changelogs strongly indicate starter quality

---

## Quick Reference

### Top Picks by Star Count

1. **meteor/meteor** - ~44.8k stars (Real-time JavaScript)
2. **fastapi/full-stack-fastapi-template** - ~40k stars
3. **sahat/hackathon-starter** - ~35.2k stars (Node.js/Express)
4. **remix-run/remix** - ~32k stars (Full-stack React)
5. **t3-oss/create-t3-app** - ~28.3k stars
6. **DioxusLabs/dioxus** - ~24.5k stars
7. **kriasoft/react-starter-kit** - ~23.4k stars
8. **wasp-lang/wasp** - ~18k stars
9. **redwoodjs/redwood** - ~17.6k stars
10. **nextjs/saas-starter** - ~15.1k stars
11. **blitz-js/blitz** - ~14.1k stars
12. **cookiecutter/cookiecutter-django** - ~13.3k stars
13. **wasp-lang/open-saas** - ~13.1k stars
14. **ixartz/Next-js-Boilerplate** - ~12.4k stars
15. **linnovate/mean** - ~12.1k stars (MEAN Stack)
16. **loco-rs/loco** - ~8.4k stars
17. **vercel/platforms** - ~6.6k stars
18. **thedevdojo/wave** - ~6.4k stars
19. **t3-oss/create-t3-turbo** - ~5.9k stars
20. **epicweb-dev/epic-stack** - ~5.4k stars
21. **boxyhq/saas-starter-kit** - ~4.6k stars

### Most Active Communities

- **Meteor** — Discord ([discord.gg/hZkTCaVjmT](https://discord.gg/hZkTCaVjmT)), 776+ contributors
- **T3 Community** (create-t3-app) — Active Discord (~30k members), created by Theo (t3dotgg)
- **Wasp Discord** — 16,000+ members, YC-backed
- **RedwoodJS** — Founded by Tom Preston-Werner, active forums and Discord, 250+ contributors
- **FastAPI** — Large Python community with comprehensive docs, 75+ contributors
- **Blitz.js** — Discord ([discord.blitzjs.com](https://discord.blitzjs.com)), 66+ contributors

### Recently Updated (2025)
- wasp-lang/wasp (December 18, 2025)
- meteor/meteor (December 16, 2025)
- fastapi/full-stack-fastapi-template (December 15, 2025)
- sahat/hackathon-starter (December 14, 2025)
- boxyhq/saas-starter-kit (December 14, 2025)
- t3-oss/create-t3-app (December 13, 2025)
- ixartz/Next-js-Boilerplate (December 12, 2025)
- ixartz/SaaS-Boilerplate (December 12, 2025)
- wasp-lang/open-saas (December 2025)
- blitz-js/blitz (December 2025)
- scosman/CMSaasStarter (November 2025)
- vercel/platforms (October 2025)
- nextjs/saas-starter (October 2025)
- redwoodjs/redwood (October 21, 2025)
- thedevdojo/wave (September 2025, v3.1.1)
- loco-rs/loco (July 2025, v0.16.3)

---

## Appendix

### Glossary of Terms

### Contributing & Updates

### Sources & Citations

**Awesome Lists:**
- [GitHub - kevindeasis/awesome-fullstack](https://github.com/kevindeasis/awesome-fullstack)
- [GitHub - stackshareio/awesome-stacks](https://github.com/stackshareio/awesome-stacks)
- [GitHub - devpose/awesome-starters](https://github.com/devpose/awesome-starters)
- [GitHub - lyqht/awesome-supabase](https://github.com/lyqht/awesome-supabase)

**Community Discussions:**
- [Ask HN: Ideal stack for solo dev (2025)](https://news.ycombinator.com/item?id=43486496)
- [Ask HN: Tech stack 2025](https://news.ycombinator.com/item?id=45166228)
- [Reddit r/webdev](https://www.reddit.com/r/webdev/)
- [Reddit r/nextjs: Best SaaS Boilerplate](https://www.reddit.com/r/nextjs/comments/1i093om/whats_the_best_saas_boilerplate_for_nextjs/)

**Curated Articles & Blogs:**
- [8 Best NextJS Boilerplates (Snappify)](https://snappify.com/blog/nextjs-boilerplates)
- [Best SaaS Stack in 2025 (Supastarter)](https://supastarter.dev/blog/best-saas-stack-2025)
- [Top 7 Next.js Boilerplates (AnotherWrapper)](https://anotherwrapper.com/blog/next-js-boilerplate)
- [6 Best SaaS Boilerplates (Pacgie)](https://www.pacgie.com/guides/6-best-saas-boilerplates-2025)
- [21+ Best Next.js SaaS Boilerplates (UIDeck)](https://uideck.com/blog/saas-boilerplates)
- [20 GitHub Full-Stack Projects (Medium)](https://medium.com/@baheer224/20-github-full-stack-projects-you-can-learn-from-f347aa006299)

**Repository Sources:**
- [GitHub - t3-oss/create-t3-app](https://github.com/t3-oss/create-t3-app)
- [GitHub - t3-oss/create-t3-turbo](https://github.com/t3-oss/create-t3-turbo)
- [GitHub - kriasoft/react-starter-kit](https://github.com/kriasoft/react-starter-kit)
- [GitHub - sahat/hackathon-starter](https://github.com/sahat/hackathon-starter)
- [GitHub - linnovate/mean](https://github.com/linnovate/mean)
- [GitHub - meteor/meteor](https://github.com/meteor/meteor)
- [GitHub - wasp-lang/wasp](https://github.com/wasp-lang/wasp)
- [GitHub - blitz-js/blitz](https://github.com/blitz-js/blitz)
- [GitHub - redwoodjs/redwood](https://github.com/redwoodjs/redwood)
- [GitHub - fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- [GitHub - vintasoftware/django-react-boilerplate](https://github.com/vintasoftware/django-react-boilerplate)
- [GitHub - ixartz/SaaS-Boilerplate](https://github.com/ixartz/SaaS-Boilerplate)
- [GitHub - ixartz/Next-js-Boilerplate](https://github.com/ixartz/Next-js-Boilerplate)
- [GitHub - boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit)
