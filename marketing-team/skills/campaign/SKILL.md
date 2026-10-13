---
name: campaign
description: Run the full marketing team on one goal for one company (Nerativ, Frameworks, GEO Radar or Servayor). The CMO agent plans organic-first, specialists produce in parallel, voice-qa gates every public piece, and you get finished files plus a short decision list. Use for "plan a campaign", "launch X", "get us design partners", "a month of content for Y", or any multi-channel push.
---

# Campaign

Usage: `/campaign <company> <goal>`, e.g. `/campaign geo-radar 40 design partners by January`.

1. **Hand the request to the `cmo` agent** with the company, the goal, the
   deadline and anything Josh said about constraints. If the company or goal
   is missing, ask first.
2. **The CMO returns a plan** before production. Show it to Josh in under 25
   lines: the outcome, the channels in order, the specific communities,
   prompts and accounts, what each specialist will make, what needs his
   answer (open questions from the company brief, names to approve, numbers
   to confirm). Wait for his go.
3. **Production.** The CMO runs specialists in parallel and sends every public
   piece through `voice-qa`. Nothing reaches Josh without a PASS.
4. **Deliver** into `marketing/<company>/<yyyy-mm-dd>-<slug>/` in the current
   project (create it):
   - `plan.md` the approved plan
   - one file per piece, named by channel and order (`reddit-01.md`,
     `linkedin-03.md`, `article-launch-guide.md`)
   - `decisions.md` everything waiting on Josh
   - `measure.md` what to check at 30 and 90 days and the baseline
5. **Final reply to Josh:** where the files are, the decision list, and the
   first thing to post. No recap of how it was made.
