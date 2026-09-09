---
name: deck-builder
description: Use when creating or improving PPT, PowerPoint, slide decks, HTML presentations, or reusable presentation prompts, especially when the user supplies a reference deck or says the slides are too simple, monotonous, or lack logic.
---

# Deck Builder

Turn source material into a finished presentation. Build the argument and the visual explanation together; a tidy arrangement of bullets is not enough when the audience needs to understand a mechanism, dependency, or decision.

This skill works in Claude Code and Codex. Use the current host's available tools and installed skills. An authorized creation or revision request is enough to begin reversible production; ask only for missing information that would materially change the result.

## 1. Lock the assignment

Identify audience, purpose, output format, page scope, reference materials, and editing needs from the request and files. State consequential assumptions briefly.

- A fixed N-page request means N slides total. Preserve requested page numbering when supplying replacement pages. Distinguish Word physical pages from numbered slide headings in an outline.
- Deliver PPTX when the user asks for PPT/PowerPoint. Use HTML when requested or when the intended presentation is web-native. Prompt-only requests end with the reusable prompt.
- Determine whether an existing deck is an **edit target**, an **exact template**, a **style reference**, or a **content/asset source**. These require different degrees of preservation.
- Keep user sources intact and place outputs in a new task directory. Reuse an existing working brief rather than creating parallel plans.

## 2. Inspect references visually

When a reference deck is supplied, or a redesign is requested because the result is simple, monotonous, or illogical, read [reference-driven.md](references/reference-driven.md).

Extract text for content discovery, then render the relevant source pages. Inspect a contact sheet for rhythm and individual pages for composition. Record a short visual contract: title treatment, text density, image/diagram proportion, color roles, typography, repeated elements, and how relationships are explained.

Reference fidelity includes **information structure**, not just palette and fonts. If the reference uses substantive diagrams and explanatory illustrations, plan visuals with comparable explanatory depth. Apply that direction to this task; do not make its colors, illustration style, or panel layout universal defaults.

For an exact template or edit target, follow the host's presentation skill to preserve masters, layout and existing objects. For inspiration, adapt the visual grammar and rebuild content around the new subject. Preserve original logos only when they belong in the new deliverable.

## 3. Build the argument before the layout

Use `humanize-ppt` when installed and useful for turning raw materials into a brief and slide plan. Follow its actual contract. Otherwise create a compact manual brief.

For each page, identify:

| Field | Decision it forces |
| --- | --- |
| Audience question | What must this page make understandable? |
| Main point | The claim or subject the page establishes |
| Inputs / actors | What enters, and who acts? |
| Mechanism | What transforms, connects, controls, or compares? |
| Output / use | What becomes possible, and for whom? |
| Feedback / boundary | What returns for correction; what is only planned? |
| Visual relation | Sequence, parallel branches, shared foundation, hierarchy, comparison, or loop |

Use the fields that fit the subject. Do not invent an operational loop for a portrait or a simple factual slide.

Map relationships across pages too. Page order does not imply dependency: if a shared database supports both research datasets and clinical access, depict two branches, not a chain that requires research processing before clinical access.

Review logic in a separate pass before expensive asset generation. Confirm that arrows mean something specific, responsibilities are clear, and the outcome follows from the mechanism. Distinguish facts, proposals, targets, hypotheses and measured results.

## 4. Compose one explanation per page

For a new deck without a controlling template, read [composition-playbook.md](references/composition-playbook.md) to choose a content-led page system. When reference and editability needs conflict, resolve the asset mode with [pptx-production.md](references/pptx-production.md).

Choose the layout from the argument and the reference. Useful options include process diagrams, system maps, annotated screenshots, comparison tables, evidence charts, timelines and editorial photography.

For a construction or solution briefing whose reference uses engineering diagrams, a useful composition is:

1. Subject title and a short sentence stating the mechanism.
2. A compact explanation of responsibilities, controls or implementation choices.
3. A dominant diagram showing the actual relationships.
4. A concrete output or value statement at the bottom.

This is a mode, not a mandatory slide template. Let the reference and content determine density and proportions. A minimal reference calls for restraint. A visually rich reference calls for substantive visual work, not cosmetic icons added to empty columns.

When asked for multiple versions, vary composition, diagram strategy or narrative emphasis while retaining the same factual coverage. Color swaps alone are not meaningful alternatives. Produce the requested complete versions, not only title-slide previews, unless the user asks to select a direction first.

## 5. Produce with available tools

For PPT/PPTX, read [pptx-production.md](references/pptx-production.md). Read [runtime-and-qa.md](references/runtime-and-qa.md) before producing assets or exporting a deck. The read-only `scripts/preflight.py` can inventory local authoring packages and renderers; it never installs them or selects a host policy.

| Need | Route when available |
| --- | --- |
| Argument / AST / page plan | `humanize-ppt` |
| PowerPoint creation, editing and rendering | Current host's presentation/PPTX skill and its prescribed runtime |
| Chinese magazine or Swiss HTML presentation | `guizang-ppt-skill` |
| Other self-contained HTML presentation | `frontend-slides` |
| Chinese copy refinement | `humanizer-zh`, only for writing |
| Custom raster illustrations and rich infographics | Current host's image-generation skill/tool |

Resolve the skill names and tools actually installed. Read their instructions; do not invent APIs or assume another host's tool is callable. If an optional tool is missing, continue with a suitable installed route and disclose material limitations. If a specifically requested essential tool is unavailable, explain the gap.

Write a task-specific production brief before authoring: audience, scope, message, reference contract, slide plan, asset roles, renderer, editability and QA. Show the full prompt only when requested; keep routine build artifacts private.

For each generated asset, specify subject, placement, aspect ratio, style reference, exact labels, meaningful connectors and forbidden factual inventions. Use local/official assets for real institutions, products or evidence. A generated illustration is a schematic, not proof of an existing system.

Keep titles, explanations and conclusions native and editable. Required editable charts, tables or diagrams must use the host's supported native route. A mixed deck may use raster infographics when allowed by the request; disclose that boundary rather than calling it fully editable. Do not silently substitute a flat image for a requested editable diagram.

## 6. Verify the actual deliverable

Conduct separate content and visual passes, using independent review when useful and authorized.

**Content:** exact page count and scope, source coverage, mechanism and branch correctness, factual status, image-caption match, policy scope, generated labels, invented numbers and unsupported claims. Keep source provenance in the relevant notes or visible citations where necessary.

**Visual:** render every final slide and inspect it individually. Check Chinese glyphs, wrapping, clipping, overlaps, connectors, crops, legibility, contrast and consistency. Use a contact sheet for flow, not as a substitute for page inspection. Compare against the selected reference contract.

**File:** verify package integrity and declared editability using available tools. Inspect reported findings as well as exit codes; a script that prints errors can still exit zero. A successful export or XML parse does not prove rendering or usability. Use fresh filenames/receipts for revisions where the exporter requires them, then keep superseded drafts outside the delivery folder.

Fix material findings and repeat the affected checks. Never claim PowerPoint verification unless inspected there; name the actual renderer when a limitation matters.

Deliver the finished file and, when comparison would help, a concise preview. Explain the main improvement and any material editability limitation. Do not deliver prompts or instructions in place of the requested presentation.

## Research provenance

See [source-review.md](references/source-review.md) for the inspected upstream skills, their actual output modes, licensing boundaries and the methods selected for this workflow. This is an independently authored integration; upstream code, templates and runtime gates are not installed or vendored by invoking this skill.
