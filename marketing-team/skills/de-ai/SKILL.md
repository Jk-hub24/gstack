---
name: de-ai
description: Rewrite any pasted text (post, email, article, page, reply) so it stops reading like an AI or a marketer, keeping the meaning. Runs the voice checker before and after and shows what changed. Use when Josh says "de-AI this", "make this sound human", "this reads like ChatGPT", "fix the voice", or pastes a draft with a channel.
---

# De-AI

1. **Get three things:** the text, the channel (reddit, linkedin, email,
   article, landing, generic), and who it's from. If the channel or speaker is
   missing, infer it from the text and say what you assumed.
2. **Load** `authentic-voice` and `proof-policy`. For Reddit or community
   posts, also load `reddit-native-voice` if available, and it wins.
3. **Save the original** to a scratch file and run the checker on it:
   `python3 <authentic-voice dir>/scripts/voice-check.py --channel <channel> original.txt`
4. **Find the real detail.** If the text has one, build the rewrite around it
   and move it to the top. If it has none, say so plainly and ask for one.
   Don't polish an empty draft.
5. **Rewrite, don't edit.** Patching banned words one by one leaves the
   skeleton intact, and the skeleton is what readers notice. Rewrite from the
   detail, keep the author's meaning and opinions, change the structure.
6. **Run the checker on the rewrite** until it shows `RESULT: PASS`. Then read
   it once for rhythm (three similar sentences in a row means break one).
7. **Return:** the rewrite, the checker's before/after fail count, and up to
   three short notes on what was structurally wrong in the original. Nothing
   else.
