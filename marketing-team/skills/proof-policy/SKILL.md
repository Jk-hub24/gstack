---
name: proof-policy
description: Rules for proof points in every public piece across Nerativ, Frameworks, GEO Radar and Servayor. Value first, real numbers only, no client, prospect, partner or competitor names unless Josh gives an explicit per-piece instruction. Use whenever a draft contains a number, a result, a case study, a testimonial, a "we helped X" claim, a comparison, or any company name. Also use when building or updating a proof bank.
---

# Proof Policy

Proof is what separates us from the feed. It's also where most marketing lies.
These rules keep the proof real and keep client trust intact.

## 1. Value comes before proof

Lead with something the reader can use today: a mechanism, a test they can run,
a failure mode they can check for. Proof comes after, as the reason to believe
it. A post that is only proof ("we got 29M views!") is a brag, and brags get
scrolled.

Order inside any proof point: **number, then mechanism, then the caveat.**
Never the number alone.

> 85 to 90% of what we post stays up. That's mostly because every account is
> warmed for weeks and writes like the people in the sub, not like a vendor.
> It drops fast when a client pushes for brand mentions in the first month.

## 2. No names. Ever. Unless told.

Default: no client, prospect, partner or competitor appears by name. Not in
posts, articles, emails, decks, landing pages, alt text or file names that go
public. This holds even when a client is listed on our own website.

Describe instead of naming. Use the vertical, size, stage and situation:

| Don't | Do |
|---|---|
| "We helped Checkmarx..." | "an AppSec vendor with a big incumbent problem" |
| "Lili's accountant program" | "a small-business banking app going after bookkeepers" |
| "Unlike Foundation..." | "agencies that sell a strategy deck and a dashboard" |
| "Profound's data shows" | "a citation tracker with a few hundred thousand prompts" |

The description has to stay true. Don't stretch a 200-person company into
"enterprise".

**The only exception:** Josh explicitly names the company and says it's approved
for this specific piece. Then pass it to the checker with
`--allow-name "Name"`. Approval doesn't carry over to the next piece.

The deny list lives in `blocked-names.txt` next to this file. When a new client,
partner or competitor comes up, add it.

## 3. Third-party research

Outside studies are useful, and they also carry someone else's brand. Default:
describe the study by what it measured ("a 238,000-prompt study, Oct to Jan"),
not by who published it. Always state what the number is a percentage **of**.
Reddit citation stats run from about 1% to 40% depending on the denominator,
and quoting one without its denominator is how you get caught out by the exact
people we want to impress.

Long-form articles may link the source where an engine or editor expects a
citation. A link is fine. Naming the publisher in the body copy needs the same
explicit OK as a client name.

## 4. Numbers must be real and traceable

- Every number comes from the company's proof bank (in `company-context`) or a
  named internal source: a monthly report, a dashboard export, a CRM view, a
  call. Note the source next to the draft.
- Never invent, round up or "illustrate" a number. If you need one and don't
  have it, write `[NUMBER NEEDED: what, from where]` and flag it.
- Keep the scope honest. "45M views across 35+ clients since April 2025" is
  true. "45M views" alone suggests one client.
- Ranges beat point figures when results vary. Timelines beat promises.

## 5. Testimonials and quotes

Only real words from a real person, with their written OK. Attribute by role
and company type ("VP Marketing, Series B security company") unless they've
agreed to a name. Never write a quote and then go looking for someone to
approve it.

## 6. The checks before anything ships

1. `voice-check.py` passes with no name failures.
2. Every number has a source written next to it in the working notes.
3. Every company description is true and couldn't be used to identify a client
   who hasn't agreed to be identifiable. (Very small niches: be vaguer.)
4. The piece leads with value, not with the proof.
