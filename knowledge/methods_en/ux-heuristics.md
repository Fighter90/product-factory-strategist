---
id: M-ux-heuristics
lang: en
title: Heuristic evaluation of an interface — based only on what is visible, with a severity scale and evidence
course: ux
sources: ["EN mirror of the RU methodology card M-ux-heuristics (knowledge/methods/ux-heuristics.md); original sources are listed in the RU card"]
stages: [options, validation, after-decision]
tags: [heuristics, nielsen, shneiderman, norman, expert-review, severity, screenshot, ux-audit]
related: [M-usability-testing, M-cjm, M-ux-backlog, M-design-thinking, M-solution-design, M-competitors, M-source-criticism]
---

# Heuristic evaluation of an interface (based on what is visible)

## When to apply
When there is a screenshot, a mockup, a prototype or a described flow, but no users and no time for recruiting: you need to quickly remove the "low-hanging"
problems before the test, weed out weak variants or audit a competitor. The method yields **hypotheses about problems with a severity estimate**,
not proof of impact on metrics or on people's behavior — that is a fundamental boundary.

## Essence
Heuristics are universal usability principles against which an expert checks an interface without users. The course names three sets:
Nielsen's 10 heuristics, Shneiderman's 8 golden rules, Norman's 7 principles; the main working set is Nielsen's.

| # | Nielsen heuristic | Essence | What to look for on a visible screen |
|---|---|---|---|
| 1 | Visibility of system status | The system reports what is happening: loading, saving, success, error | Step/progress indicators, statuses ("Draft", "Not published"), confirmation of an action; **is it visible that the action was completed** |
| 2 | Match with the real world | The user's language and metaphors | Jargon ("invoice", "entities", "ticket"), unclear icons without labels |
| 3 | User control and freedom | Easy to cancel, go back, exit | "Back/Cancel/Close" buttons, the ability to undo a deletion (if a snackbar/button is visible) |
| 4 | Consistency and standards | Internal (within the product), external (other services), metaphorical | Different labels of one action ("Pay"/"Buy"), different colors of primary buttons, non-standard patterns |
| 5 | Error prevention | Better to prevent than to explain | Disabled invalid actions, input masks/hints, confirmation of destructive actions |
| 6 | Recognition rather than recall | Options and hints in plain sight | A format example in the field, hints, visible options instead of typing from memory |
| 7 | Flexibility and efficiency of use | Accelerators for the experienced while staying clear for novices | Quick actions, autocomplete, saved data (if visible) |
| 8 | Aesthetic and minimalist design | Every element serves a purpose | Several competing CTAs, visual noise, redundant text |
| 9 | Help with errors | In plain language: what happened and what to do | The text of the error message, whether the path to fix it is given |
| 10 | Help and documentation | Short, contextual | A hint next to the action, a link to the FAQ |

Shneiderman (a reminder): consistency; shortcuts; informative feedback; a dialog with a logical completion; simple error handling; easy reversal; internal locus of control; a reduced load on short-term memory. Norman: knowledge in the world and in the head; simplification of
tasks; visibility; the right mappings; constraints; accounting for errors; standardization when nothing else helps.

**What the course says about effectiveness:** one or two experts in an hour find on the order of 80% of the "basic" errors. This is the lecturer's guideline, not a
guarantee; third-party practice recommends 3–5 independent evaluators (knowledge outside the course). The downsides of the method per the course: subjectivity; real expectations and the "why" are not visible.
Apply it **before** the UX test, so as not to spend respondents on the obvious.

## Procedure

### The evidence principle (mandatory)
Every finding rests on **what is actually visible in the material**: a specific screen/step, a specific element, the verbatim text,
the position, the state. Confidence levels:
- **V — visible:** the problem reads directly off the screenshot (the text, the placement, the absence of an element where it is expected given the screen's context).
- **I — inference from the visible:** it follows from several visible signs but requires an assumption (state the assumption).
- **H — hypothesis:** it depends on what is not visible (behavior after the click, other states, real users, metrics).
  Flag it explicitly and word it as a testable assumption.

Forbidden: attributing emotions and behavior to users as a fact; naming a conversion effect; asserting the "absence" of a feature
when the screen may simply not have shown it; evaluating inaccessible states (loading, error, empty), animations, sound.

### Steps
1. **The frame:** which flow/scenario, which intended user and goal (written down as an assumption), on which devices.
2. **The inventory of the visible:** for each screen list the headings, the button and field texts, the statuses, the icons, the CTA placement,
   the colors/accents (in words). Without judgments. All subsequent findings reference this inventory.
3. **Pass 1 — by screen:** for each screen go through the 10 heuristics, answering for each "is it visibly violated?"; a violation → an entry.
4. **Pass 2 — by flow:** consistency across the screens (terms, buttons, colors), the logic of the steps, the place of return, the outcome/confirmation.
5. **Separate fact from assumption:** assign V/I/H; for I state the assumption, for H — how to check it.
6. **Severity:** the scale below; the frequency is not known from a single frame — estimate by impact and "flow-through" (does it show up on every pass).
7. **Merge the duplicates**, pick the top 5, propose a "one-line" fix for each.
8. **The verification plan:** for each finding of type I/H specify the method ([[M-usability-testing]]): findability → first click; the
   meaning of a term → interpretation; the first impression → 5-second; the understanding of a status/flow → moderated.
9. **Hand it over to the backlog** ([[M-ux-backlog]]): the tag Heuristic-Review + the heuristic number; severity ≥3 goes into UX debt.

### The severity scale (unified)
Severity = Impact on the task × Frequency × Business risk, normalized to 0–4.

| Score | Name | Meaning | Action |
|---|---|---|---|
| 0 | Not a problem / cosmetics | Does not affect the task (spacing, font) | As capacity allows |
| 1 | Minor | Slightly slows down, does not break | Into the backlog as "nice-to-have" |
| 2 | Friction (minor) | A noticeable share of people get distracted or take a wrong path | The nearest sprint |
| 3 | Serious (major) | Some users will not complete the task or will err badly | Urgently into the current sprint |
| 4 | Blocking | The task/money/release are blocked | A release blocker |

The mapping to the course scale from session 6 (there the order is reversed: 1 Critical, 2 Major, 3 Minor, 4 Cosmetic): Critical → 4, Major → 3, Minor → 1–2,
Cosmetic → 0. **A limitation for static material:** a score of 4 is allowed only if the blockage is proven by the flow, a test recording,
or a metric; from a single screenshot at most 3, with a confidence note.

## Template / checklist

**A finding entry:**
`ID | Screen/step | The visible element (verbatim/position) | Heuristic # | What is wrong (fact) | The consequence for the user (as a hypothesis) | Severity 0–4 | Confidence V/I/H | The assumption/what is not visible | The proposal | How to verify`

**An example of a good finding:** "Payment screen, the button at the bottom 'Download invoice' (heuristic 2). The word 'invoice' is an anglicism on a
Russian-language screen; the neighboring elements are in Russian. V. Severity 2. Proposal: 'Download receipt'. Verification: an interpretation test".
**An example of a bad finding:** "Users will be annoyed, conversion will drop" — no element, no source, no verification → reject or convert into H.

**Typical findings and quick fixes:** no loading/status indicator → a spinner or a skeleton, an explicit status; different labels of one
action → a single verb; no undo after a deletion → a snackbar "Deleted — Undo"; two primary CTAs on a screen → keep one primary;
a button active while a required form is empty → inactive until the data is valid; a field without a format example → a placeholder and a mask; an error
"code 500" → "Failed to upload the photo. Try again or choose a different file".

**The report checklist:** the frame and the assumptions; the inventory of the visible; the findings with V/I/H; the scale applied by the rules; the top 5; the list of "what is not visible";
the recommendations on verification; no statements about metrics or about people stated as fact.

## Typical mistakes
| Mistake | Consequence | Fix |
|---|---|---|
| A finding without a reference to an element/screen | Impossible to verify | Always: screen + element + verbatim text |
| Presenting a hypothesis as a fact ("users will not understand") | False confidence | The H flag and a verification plan |
| Evaluating the invisible (errors, loading, empty states) | Fabrication | Write it into "not visible", request the material |
| Everything is marked critical | No priority | Apply the scale, at most 3 for static material |
| One evaluator, one pass | Subjectivity and omissions | A second "diagonal" pass, a second evaluator where possible |
| Heuristics instead of a test where meaning/motivation is needed | No "why" | Hand it over to [[M-usability-testing]] |
| A substitution: "this is ugly" | Taste, not a principle | Tie it to a heuristic and a consequence |
| Comparing someone else's screen with yours "by feel" | Not comparable | The same inventory and scenario for both |

## Questions that can change the decision
- Which scenario and user are the target ones? Without them the assumptions about "excessive" and "understandable" are arbitrary.
- Which screen states are not shown (error, empty, loading, the mobile/desktop version)?
- Is this an internal product for experts (many accelerators are appropriate) or a mass-market one (clarity is the priority)?
- Is there data (metrics, support) that confirms or refutes the found problem?
- Is a competitor evaluation ([[M-competitors]]) needed in the same format?

## Related cards
[[M-usability-testing]], [[M-cjm]], [[M-ux-backlog]], [[M-design-thinking]], [[M-solution-design]], [[M-competitors]], [[M-source-criticism]]
