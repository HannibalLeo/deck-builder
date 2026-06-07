---
name: deck-builder
description: Build polished presentations from arbitrary material by turning notes, URLs, docs, code, product/management/research content, or rough ideas into a slide strategy, production prompt, visual direction, generated/selected images, speaker notes, and a finished deck. Use when the user asks to create, improve, abstract, or generate PPT, PowerPoint, slide decks, web-native presentations, frontend-slides, pitch decks, talk decks, teaching decks, strategy decks, product decks, technical/code walkthrough decks, or a reusable prompt for making presentations.
---

# Deck Builder

## Overview

Turn varied source material into a presentation-ready deck. Preserve the useful structure of high-quality one-off PPT prompts while adapting the narrative, visual system, tools, and output format to the user's actual domain.

Do not stop at a generic prompt unless the user explicitly asks for prompt-only output. Build the deck or the closest runnable artifact available in the current environment.

This skill is an orchestrator. When the real downstream skills below are installed, load and follow their `SKILL.md` files instead of recreating their behavior from memory:

- `humanize-ppt`: AST outline director and router for presentation workflows.
- `guizang-ppt-skill`: single-file horizontal HTML PPT, image assets, covers, Style A editorial magazine and Style B Swiss systems.
- `humanizer-zh`: Chinese text humanization and AI-writing-pattern cleanup.
- `frontend-slides`: general self-contained HTML slide production when the route is not covered by `guizang-ppt-skill`.

## Workflow

### 1. Ingest

Read the user's source material first. Accept pasted notes, files, folders, URLs, code, transcripts, PDFs, docs, or existing decks.

If key inputs are missing, ask only for the minimum needed:

- audience and purpose
- target length or presentation time
- desired output: PPTX, HTML slides, PDF, or prompt-only
- brand constraints, if any

When the user gives enough context, proceed with reasonable assumptions and state them briefly.

### 2. Route To Real Tools

Prefer this routing:

- Use `humanize-ppt` first when raw material needs to become a deck outline, AST, slide plan, speaker intent, router plan, or repeatable presentation workflow.
- Use `guizang-ppt-skill` for Chinese PPT production when the user wants magazine style, Swiss style, horizontal swipe HTML deck, PPT images, screenshot framing, or social covers.
- Use `humanizer-zh` only to rewrite Chinese copy, speaker notes, titles, or slide text to remove AI tone and improve human voice. Do not treat it as a slide renderer or outline engine.
- Use `frontend-slides` for general HTML decks, non-Chinese routes, or custom visual directions outside `guizang-ppt-skill`.
- Use presentation/PPTX tooling when the user specifically needs editable PowerPoint.

If a named downstream skill is missing, say it is missing and either install it when appropriate or fall back explicitly. Do not pretend the missing skill's behavior is known.

### 3. Extract The Deck Thesis

If `humanize-ppt` is available, use it for this step. Otherwise find the core conflict, decision, transformation, or teaching arc. Prefer a sharp spine over a complete summary.

Fallback domain arcs:

- Product: user pain -> insight -> solution -> proof -> adoption path
- Strategy/management: context shift -> operating tension -> choices -> tradeoffs -> next moves
- Technical/code: problem -> architecture -> critical flows -> implementation details -> risks -> rollout
- Research/learning: question -> prior model -> evidence -> new model -> implications
- Sales/pitch: market change -> urgent pain -> differentiated offer -> traction -> ask
- Personal/story: moment -> conflict -> turning point -> lesson -> audience action

### 4. Create A Task-Specific Production Prompt

Before building, create a concise task-specific production prompt that names the real route selected above. Show the full prompt when the user asks for a reusable prompt, asks to inspect the prompt, or when approval before production would reduce risk. Otherwise use it as the working brief and summarize the key choices.

```markdown
# Role
You are a senior presentation strategist, information architect, visual director, and frontend-slide/PPT production agent.

# Task
Transform the supplied material into a polished presentation for [audience] to achieve [purpose]. Output [format] with [length/time] constraints.

# Tool Route
- First use [humanize-ppt / manual AST fallback] to produce the deck AST and slide plan.
- Then use [guizang-ppt-skill / frontend-slides / PPTX tooling] for rendering.
- Use [humanizer-zh] only for Chinese copy cleanup where needed.
- Use image generation or asset search only after slide structure is stable.

# Workflow
1. Structural distillation
   - Identify the central tension, decision, or transformation.
   - Build a slide spine, not a linear summary.
   - Limit the deck to the smallest number of slides that can carry the argument.
   - Assign each slide a clear Slide Type.

2. Humanized copy
   - Remove machine-like phrasing, filler, and long abstract sentences.
   - Use short, spoken, high-signal copy suitable for a live presentation.
   - Preserve technical precision where needed.
   - Add speaker notes that sound like an expert, not a report.

3. Visual direction
   - Choose a visual system from the material, audience, and domain.
   - Define palette, typography, layout rhythm, image style, and motion posture.
   - Avoid generic startup gradients and decorative visuals that do not clarify the idea.

4. Image and diagram plan
   - For each slide, specify one visual role: evidence, metaphor, diagram, product state, architecture, data, portrait, or atmosphere.
   - Generate images when an image tool is available; otherwise write precise generation prompts or use suitable local/search assets.
   - Use diagrams for systems, flows, org models, timelines, and code architecture.

5. Production
   - Prefer the available frontend-slides workflow for self-contained HTML decks.
   - Use presentation/PPTX tooling when the user specifically needs PowerPoint.
   - Reserve clean DOM nodes and semantic sections for slides that may later be animated in Remotion.
   - Verify layout, navigation, overflow, assets, and speaker notes before delivery.

# Output
- Slide outline with Slide Type, title, short copy, visual plan, and speaker notes.
- Generated/selected image prompts or assets.
- Finished deck artifact and verification notes.
```

### 5. Build The Slide Outline

For each slide, include:

- Slide Type and layout
- Slide title
- Short copy: usually 1-5 bullets, or one strong sentence
- Visual plan: image, diagram, data, code, product screenshot, or typographic treatment
- Speaker notes: concise spoken script

- Use 5-8 slides for short explainers.
- Use 8-12 slides for most talks, pitches, and strategy decks.
- Use 12-20 slides only when the source material is dense or the user requests depth.
- Split dense code, tables, or architectures across multiple slides instead of shrinking text.

## Visual Direction

Choose visuals from the content rather than forcing a fixed aesthetic.

Useful patterns:

- Code/engineering: dark/light editor accents, architecture diagrams, sequence flows, terminal or API states, restrained technical typography.
- Product: product screenshots, user journeys, problem/solution contrast, launch narrative, clear interface crops.
- Management/strategy: operating models, decision matrices, market maps, timelines, scorecards, crisp editorial layouts.
- Research/education: concept maps, evidence ladders, historical contrast, annotated diagrams, data-first slides.
- Brand/story: photographic direction, material textures, object closeups, narrative pacing, emotional contrast.

If image generation is available, generate or request images slide-by-slide only after the outline is stable. Each image prompt must include subject, composition, style, palette, lighting, aspect ratio, and what idea the image clarifies.

## Tool Routing

- `humanize-ppt`: run or follow it for AST outline, audience-state-transfer thinking, router plan, slide plan, presenter/export route, and QA workflow.
- `guizang-ppt-skill`: run or follow it for Chinese magazine/Swiss HTML PPT generation, image prompts, screenshot framing, social covers, built-in templates, and its validation checklist.
- `humanizer-zh`: run or follow it for Chinese copy cleanup only: remove AI-writing traces, inflated wording, filler, and unnatural rhythm while preserving meaning.
- `frontend-slides`: invoke it for HTML slide production when it is the selected renderer, and follow its viewport, density, animation, and verification rules.
- If image generation is available, use it for custom slide images; otherwise provide exact prompts and use local/search assets when allowed.
- If the user asks for PPTX/PowerPoint, use available presentation tooling or libraries to create a `.pptx`. If only HTML is practical, explain the limitation and provide the HTML plus export path.
- If Remotion is relevant, create semantic slide DOM, stable class names, and animation-ready structure; do not add Remotion unless the user asks for video/animation production.
- If source content requires current web facts, browse or otherwise verify from primary/current sources before building the deck.

## Quality Bar

Before delivery:

- Check that every slide advances the thesis.
- Remove generic AI phrases, padded transitions, and duplicate points.
- Verify that text fits the intended slide dimensions.
- Verify image paths/URLs render.
- Verify navigation and basic responsiveness for HTML decks.
- Include file paths and a short verification summary in the final response.

## Prompt-Only Mode

When the user asks only for a reusable prompt, output the adapted production prompt and do not build the deck. Still make the prompt domain-agnostic and include tool routing for `frontend-slides`, image generation, PPTX tooling, and optional Remotion.
