# Marketing team

An organic-first marketing team for Nerativ, Frameworks, GEO Radar and
Servayor, packaged as a Claude Code plugin. One CMO agent, twelve specialists
and a QA gate. They share house rules that strip out the way assistants
usually write, keep client names out of public copy, and put paid last.

## Install

**On any machine with Claude Code (recommended):**

```
/plugin marketplace add Jk-hub24/gstack
/plugin install marketing-team@jk-hub24
```

Then start a new session. Agents and skills show up as `marketing-team:*`.
`/plugin marketplace update jk-hub24` pulls new versions.

**Without the plugin system:** clone the repo and run
`bash marketing-team/install.sh` (copies into `~/.claude`) or
`bash marketing-team/install.sh --link` (symlinks, so edits here go live).

## Use it

| Command | What happens |
|---|---|
| `/campaign <company> <goal>` | The CMO plans it organic-first, shows you the plan, then the team produces and voice-qa gates every piece |
| `/content-sprint <company>` | A week of Reddit, LinkedIn, one article and outreach lines, built from this week's real material |
| `/de-ai` + pasted text | Rewrites it so it stops reading like a machine, with checker before/after |

You can also ask for any agent directly: "have the reddit-operator draft
replies for these three threads", "get geo-strategist to build a prompt set
for GEO Radar".

## The team

| Agent | Owns |
|---|---|
| cmo | Plans, assigns, gates. Starts here for anything multi-step |
| market-intel | Buyer language, where they talk, competitor sentiment |
| positioning-strategist | Wedge, message per buyer, the first-step offer |
| reddit-operator | Posts, replies, thread plans, retention |
| community-builder | Owned subs, AMAs, design-partner cohorts, event follow-up |
| geo-strategist | Prompt sets, citation source maps, AI visibility audits |
| search-writer | Articles and pages that rank and get cited |
| linkedin-ghostwriter | Josh, named experts, company pages, comments |
| outbound-writer | Cold sequences, follow-ups, newsletters |
| proof-builder | Anonymized case studies, the proof banks |
| conversion-writer | Landing pages, offer pages, CTAs |
| performance-analyst | What worked, monthly readouts |
| paid-advisor | Capped paid tests, only when you ask |
| voice-qa | Final PASS / REWRITE on everything public |

## The rules every agent loads

- `authentic-voice`: the writing rules. Start from a real detail, no
  setup-then-reversal sentences, no dashes, no connector words, no tidy
  endings, uneven rhythm, a register per channel.
- `proof-policy`: value first, real numbers only with their scope, no client,
  partner or competitor names without your OK for that piece.
- `organic-first`: the channel ladder, communities down to paid, and what
  organic never means (bots, fake reviews, vote rings).
- `company-context`: one brief per company with the proof bank, the
  never-say list and open questions.

`skills/authentic-voice/scripts/voice-check.py` enforces the mechanical part.
Any draft with a FAIL goes back. It also blocks every name in
`skills/proof-policy/blocked-names.txt`. Add new clients and competitors there.

```
python3 skills/authentic-voice/scripts/voice-check.py --channel linkedin post.md
python3 skills/authentic-voice/scripts/voice-check.py --allow-name "Acme" approved-case-study.md
```

## Keeping it current

- New result or fact about a company: edit its brief in
  `skills/company-context/references/`.
- Changed the shared rules in `shared/house-rules.md`: run
  `python3 scripts/sync-house-rules.py` to copy them into every agent.
- Before committing: `python3 tests/test_voice_check.py` and
  `python3 scripts/sync-house-rules.py --check`.
- Needs only `python3`. No other dependencies.
