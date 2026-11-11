---
id: M-ux-heuristics
lang: en
title: Heuristic UI evaluation — visible-evidence-only findings, V/I/H confidence levels, 0–4 severity scale
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation, after-decision]
tags: [heuristics, nielsen, shneiderman, norman, expert-review, severity, screenshot, ux-audit]
related: [M-usability-testing, M-cjm, M-ux-backlog, M-design-thinking, M-solution-design, M-competitors, M-source-criticism]
---

# Heuristic evaluation of an interface (visible evidence only)

## When to apply
When you have a screenshot, a mockup, a prototype, or a described flow, but no users and no time to recruit: to quickly remove the "low-hanging" problems before a test, to screen out weak options, or to audit a competitor. The method yields **hypotheses about problems with a severity estimate**, not proof of impact on metrics or on people's behavior — that boundary is fundamental.

## Core idea
Heuristics are universal usability principles against which an expert checks an interface without users. The course names three sets: Nielsen's 10 heuristics, Shneiderman's 8 golden rules, Norman's 7 principles; Nielsen's is the main working set.

| # | Nielsen heuristic | Essence | What to look for on a visible screen |
|---|---|---|---|
| 1 | Visibility of system status | The system says what is going on: loading, saving, success, error | Step/progress indicators, statuses ("Draft", "Not published"), confirmation of an action; **is it visible that the action was performed** |
| 2 | Match between the system and the real world | The user's language and metaphors | Jargon ("invoice", "entities", "ticket"), unclear icons without labels |
| 3 | User control and freedom | Easy to undo, go back, exit | "Back / Cancel / Close" buttons, the ability to undo a deletion (if a snackbar/button is visible) |
| 4 | Consistency and standards | Internal (within the product), external (in other services), metaphorical | Different labels for the same action ("Pay"/"Buy"), different colors of primary buttons, non-standard patterns |
| 5 | Error prevention | Better to prevent than to explain | Invalid actions disabled, input masks/hints, confirmation of destructive actions |
| 6 | Recognition rather than recall | Options and hints in plain view | Format examples in a field, hints, visible options instead of typing from memory |
| 7 | Flexibility and efficiency of use | Accelerators for the experienced while staying clear for novices | Quick actions, autofill, saved data (if visible) |
| 8 | Aesthetic and minimalist design | Every element serves a purpose | Several competing CTAs, visual noise, excess text |
| 9 | Help with errors | In plain language: what happened and what to do | The error message text; whether a path to fix it is stated |
| 10 | Help and documentation | Short, contextual | A hint next to the action, a link to the FAQ |

Shneiderman (reminder): consistency; accelerators; informative feedback; dialogs with a logical closure; simple error handling; easy reversal; internal locus of control; a reduced load on short-term memory. Norman: knowledge in the world and knowledge in the head; simplifying tasks; visibility; correct mappings; constraints; designing for error; standardization when all else fails.

**What the course says about effectiveness:** one or two experts find roughly 80% of "basic" errors in an hour. This is the lecturer's guideline, not a guarantee; outside practitioners recommend 3–5 independent evaluators (knowledge beyond the course). Drawbacks of the method per the course: subjectivity; real expectations and the "why" are invisible. Apply it **before** a UX test, so you don't spend respondents on the obvious.

## Procedure

### The evidence principle (mandatory)
Every finding rests on **what is actually visible in the material**: a specific screen/step, a specific element, the verbatim text, the position, the state. Confidence levels:
- **V — visible:** the problem can be read directly from the screenshot (the text, the position, the absence of an element where it is expected given the screen's context).
- **I — inferred from the visible:** follows from several visible signs but requires an assumption (state the assumption).
- **H — hypothesis:** depends on what is not visible (behavior after the click, other states, real users, metrics).
  Mark it explicitly and phrase it as a testable assumption.

Forbidden: attributing emotions and behavior to users as fact; naming a conversion effect; asserting the "absence" of a feature when the screen may simply not have shown it; evaluating inaccessible states (loading, error, empty), animations, sound.

### Steps
1. **Frame:** which flow/scenario, which presumed user and goal (recorded as an assumption), on which devices.
2. **Inventory of the visible:** for each screen, list the headings, the button and field texts, the statuses, the icons, the position of the CTAs,
   the colors/accents (in words). No judgments. All subsequent findings refer back to this inventory.
3. **Pass 1 — by screen:** for each screen, go through the 10 heuristics and answer, for each one, "is it violated in a visible way?"; a violation → a record.
4. **Pass 2 — by flow:** consistency between screens (terms, buttons, colors), the logic of the steps, the way back, the outcome/confirmation.
5. **Separate fact from assumption:** assign V/I/H; for I state the assumption, for H — how to check it.
6. **Severity:** the scale below; frequency cannot be known from a single frame — judge by impact and "through-flow" (whether it shows up on every pass).
7. **Merge duplicates**, pick the top-5, and propose a "one-line" fix for each.
8. **Verification plan:** for every I/H finding, specify the method ([[M-usability-testing]]): findability → first click; the meaning
   of a term → interpretation; first impression → 5-second; understanding of a status/flow → moderated.
9. **Hand over to the backlog** ([[M-ux-backlog]]): tag Heuristic-Review + the heuristic number; severity ≥3 goes into UX debt.

### Severity scale (unified)
Severity = Impact on the task × Frequency × Business risk, normalized to 0–4.

| Score | Name | Meaning | Action |
|---|---|---|---|
| 0 | Not a problem / cosmetics | Does not affect the task (a margin, a font) | When there is a chance |
| 1 | Insignificant | Slightly slows the user down, does not break anything | Backlog, "nice-to-have" |
| 2 | Friction (minor) | A noticeable share of people gets distracted or takes a wrong path | The nearest sprint |
| 3 | Serious (major) | A share of users will not finish the task or will err badly | Urgently, in the current sprint |
| 4 | Blocking | The task/money/release are blocked | A release blocker |

Mapping to the course's scale from session 6 (there the order is reversed: 1 Critical, 2 Major, 3 Minor, 4 Cosmetic): Critical → 4, Major → 3, Minor → 1–2,
Cosmetic → 0. **A limitation for static material:** a score of 4 is allowed only if the blocking is proven by a flow, a test recording,
or a metric; from a single screenshot the maximum is 3, with a confidence mark attached.

## Template / checklist

**Finding record:**
`ID | Screen/step | Visible element (verbatim/position) | Heuristic # | What is wrong (fact) | Consequence for the user (as a hypothesis) | Severity 0–4 | Confidence V/I/H | Assumption / what is not visible | Proposal | How to check`

**Example of a good finding:** "Payment screen, the button at the bottom 'Download invoice' (heuristic 2). The word 'invoice' is an anglicism on a Russian-language
screen; the neighboring elements are in Russian. V. Severity 2. Proposal: 'Download receipt'. Check: an interpretation test".
**Example of a bad finding:** "Users will be annoyed, conversion will fall" — no element, no source, no check → reject it or convert it into an H.

**Typical findings and quick fixes:** no loading/status indicator → a spinner or a skeleton, an explicit status; different labels for the same
action → a single verb; no undo after a deletion → a snackbar "Deleted — Undo"; two primary CTAs on a screen → keep one primary;
a button active while a required form is empty → inactive until the data are valid; a field without a format example → a placeholder and a mask; an error
reading "code 500" → "We couldn't upload the photo. Try again, or choose another file".

**Report checklist:** the frame and the assumptions; the inventory of the visible; findings with V/I/H; the scale applied according to the rules; the top-5; the list of "what is not visible";
recommendations on how to verify; no statements about metrics or about people presented as fact.

## Typical mistakes
| Mistake | Consequence | Fix |
|---|---|---|
| A finding with no reference to an element/screen | It cannot be verified | Always: screen + element + verbatim text |
| Presenting a hypothesis as fact ("users won't understand") | False confidence | An H mark and a verification plan |
| Evaluating the invisible (errors, loading, empty states) | Invention | Write it into "not visible", request the material |
| Everything is marked critical | No priority | Apply the scale; a maximum of 3 from static material |
| One evaluator, one pass | Subjectivity and misses | A second "diagonal" pass; a second evaluator where possible |
| Heuristics instead of a test where meaning/motivation is needed | No "why" | Hand it over to [[M-usability-testing]] |
| Substitution: "this is ugly" | Taste, not principle | Tie it to a heuristic and to a consequence |
| Comparing someone else's screen with yours "by feel" | Not comparable | The same inventory and scenario for both |

## Questions that can change the decision
- Which scenario and which user are the targets? Without them, assumptions about what is "superfluous" and "understandable" are arbitrary.
- Which screen states are not shown (error, empty, loading, the mobile/desktop version)?
- Is this an internal product for experts (many accelerators are appropriate) or a mass-market one (clarity is the priority)?
- Is there data (metrics, support tickets) that confirms or refutes the problem you found?
- Is an evaluation of a competitor ([[M-competitors]]) needed in the same format?

## Related maps
[[M-usability-testing]], [[M-cjm]], [[M-ux-backlog]], [[M-design-thinking]], [[M-solution-design]], [[M-competitors]], [[M-source-criticism]]
