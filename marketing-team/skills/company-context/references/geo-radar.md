# GEO Radar

## What it is
A visibility board for how AI recommends brands. The first focus: how coding
agents (Claude Code, OpenAI's agents, GitHub Copilot) recommend tools,
libraries and services to developers while they build. Shows overview, which
competitors get recommended instead, which sources the agents rely on, and fix
recommendations. Planned: a single health score up top with click-through
detail, a chat assistant on the first page, delivery through the client's
existing tools (the "harness", in Josh's words) instead of yet another dashboard.
Josh's analogy: like a cloud cost board, but for AI recommendations.

Data is collected by running real agent sessions in test environments.
Recommendations shift 2-3 times a month, so it doesn't need to be real time.

Status (Oct 2026): in build. Demo with 10 test brands across two agents.
Website in progress. Launch plan: invite-only, design partners first, a list of
40-50 companies ready before going to market. SOC 2-adjacent compliance work
planned before broad launch.

## Who buys
Developer tool and technical AI companies whose product gets picked (or not) by
an agent during a build: databases, infra, observability, auth, APIs, SDKs, dev
platforms. Buyers: Head of DevRel, Product Marketing, VP Marketing / Growth,
founders at smaller devtools. Also technical execs who want to see AI
recommendation share the way they see cloud spend.

## The wedge
Nobody watches the moment that matters for devtools now: a developer asks an
agent to "add auth" or "set up a queue" and the agent picks a vendor in the
terminal. No search page, no click, no attribution. GEO Radar shows who gets
picked, why (which sources the agent read), and what to fix. Built by the team
that already runs citation programs, so the fixes are things we've actually
done.

## Proof bank
None public yet. Allowed:
- Describe what the product does and how data is gathered (real agent runs).
- The mechanism-level observations Josh's team has seen in client work (from
  the Nerativ brief), framed as observations.
Not allowed until there's data from design partners: recommendation-share
numbers, "X% of agents pick...", customer counts, accuracy claims.

## Organic plan shape
- Pre-launch, build in public with mechanism posts: "we ran the same prompt
  through two agents 40 times, here's which sources they read".
- Developer communities (r/ExperiencedDevs, r/devops, r/programming adjacent,
  Hacker News, devtool Discords), DevRel LinkedIn.
- Waitlist / design-partner invite as the only CTA. Invite-only is the
  positioning, keep it scarce and real.

## Never say
- Client or test-brand names from the demo set.
- Live/real-time tracking. It isn't, on purpose.
- SOC 2 compliant (it's planned as "SOC 2-adjacent" work, not certified).
- Numbers we don't have.

## Open questions
- Public name spelling: "GEO Radar" or "GeoRadar".
- Pricing model and design-partner terms.
- Does it also track AI search engines (ChatGPT, Perplexity) for marketing
  teams, or only coding agents at launch?
- Domain and website URL.
