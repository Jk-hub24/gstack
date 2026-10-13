# Servayor

## What it is
Takeoff automation for construction. It measures drawings (ceilings, walls with
heights and areas, skim, tape and jointing, fire check), checks against the
estimator's method, and produces a reviewed, annotated takeoff pack in the
estimator's own layout. Every line carries its source, basis and a confidence
level. A named human always releases it. Nothing goes to a customer
automatically. The owner's goal: a takeoff that surveyors can share with their
clients, accurate on every measurement.

How it works (from the plan): enquiry arrives by email, sheets get classified,
gaps become RFI drafts, each package is measured, a second method and a blind
second model cross-check it, a deterministic governor blocks anything that fails,
an estimator reviews it, and the estimator's final numbers feed back as proposed
lessons that only they can approve.

Status (Oct 2026): training phase on one historical project. In-sample only.
No email intake built. Next: 2-4 more historical jobs run blind, then build,
then shadow mode on live enquiries, then review packs.

## Who buys (working assumption, confirm with Josh)
UK estimators and quantity surveyors at drylining, ceilings and interior
finishing subcontractors, plus the surveyors who send takeoffs on to their own
clients. Pain: hours of manual takeoff per enquiry, tender volume they can't
keep up with, and the risk of one wrong height wiping out a margin.

## The wedge
Doesn't guess. Most takeoff tools silently assume a default height when a
drawing doesn't give one. Servayor refuses: no height means no area and an RFI
instead. Every number shows where it came from, and a human signs it off. It
works the way the estimator already works, in their layout, instead of making
them learn a new tool.

## Proof bank
Nothing public yet. The current accuracy figures are fitted to one project and
are NOT blind. They must not appear in any public copy.

Allowed now:
- How it works: the refusal rules, the human release, the second-method check,
  the estimator-approved learning loop.
- Honest status: "we're running it against past jobs before anyone sees a live
  pack".

Allowed after Phase 1 (blind jobs) and Josh's OK: accuracy bands with n, blind
vs in-sample labelled, per package.

## Organic plan shape
- Very early. The job right now is finding 4+ estimators with historical jobs
  and finished takeoffs who'll run blind comparisons. Marketing = recruiting
  design partners.
- Where estimators talk: r/QuantitySurveying, r/estimators, r/Construction,
  UK construction LinkedIn, trade association groups, drylining and ceilings
  forums.
- Content that earns trust with this crowd: the failure modes of takeoff
  software (silent default heights, double-counted bulkheads, fire curtains
  measured into totals), written by someone who's clearly done takeoffs.

## Never say
- "Validated", "accurate to X%", "AI does your takeoff". Not true yet, and
  estimators will test it.
- Project, architect or client names. The training project and its architect
  are on the deny list.
- That anything is sent automatically. It never is.
- Pricing, turnaround promises.

## Open questions
- Confirm the ICP above (subcontractor estimators vs QS firms vs both).
- Brand stage: stealth, or OK to build in public?
- Who is the public voice: Josh, or the estimator partner?
- Pricing model (per job, per seat, per month).
