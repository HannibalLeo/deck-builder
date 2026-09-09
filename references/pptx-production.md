# Professional PPTX production

Use for PowerPoint requests. Default to a real PPTX and follow the active host's presentation skill. HTML is a distinct requested format, not an automatic replacement for PPTX.

## Select the content representation

| Mode | Use when | Preserve / disclose |
| --- | --- | --- |
| Native PowerPoint | User requires editable diagrams, tables, charts or frequent content updates | Text, evidence and required diagram elements remain native; inspect editability |
| Native text with illustrated diagrams | User wants a rich reference-led design and raster schematics are acceptable | Titles/body/conclusions remain editable; disclose that diagram internals are raster |
| Image-based deck | User explicitly accepts fixed visual slides or asks for image slides | Do not describe it as editable; preserve high-resolution source assets |
| Existing native template | User wants template fill or targeted editing | Preserve source geometry, theme and objects; change requested content only |

When editing needs are unspecified, keep text, data charts and tables native. Use raster illustrations for visual subjects that benefit from them. If a requested reference is entirely raster but the user needs every diagram label editable, rebuild the explanation with supported native objects or discuss a material limitation; visual similarity does not cancel the editing requirement.

## Host-aware authoring

1. Use the current host's installed PPTX skill if present; its package/API and validation rules control implementation.
2. Codex Desktop with the bundled presentation skill uses that skill's Artifact Tool route. Do not replace it with a library recommended by a downloaded skill.
3. On Claude Code without a dedicated PPTX skill, use an available PowerPoint library such as PptxGenJS after checking its local version and official API documentation. `scripts/preflight.py` reports resolvable packages and known renderer paths without installing or executing those libraries. It can discover the shared local dependency bundle when present, but that does not make Codex tool namespaces callable from Claude.
4. If a required dependency is missing, name the missing capability, use an installed suitable alternative, or ask for the genuinely necessary setup. Do not claim generation or editability from a plan alone.

For PptxGenJS, verify its current API at [the official repository](https://github.com/gitbrent/PptxGenJS). Do not transfer Artifact Tool units, color syntax or text styles into it: API conventions differ. Set the intended slide dimensions before authoring and set fonts explicitly. Keep evidence editable with supported native charts/tables. Retain the builder and selected assets in the private task workspace so revisions can be rebuilt from source.

## Illustration workflow

Compose the argument first, then produce illustrations at their intended aspect ratios. For a reference-led redesign, use representative reference images as style inputs when the tool supports them. Generate the mechanism graphic rather than an unrelated decorative scene.

Preserve original logos and real product/evidence images where identity matters. In generated schematics, replace plausible but unsupported invoice amounts, chart figures and certification claims with neutral field names. Inspect every generated image before it enters the final deck.

The mixed mode used in a successful reference-led construction briefing consists of native title and mechanism copy, a wide illustrated workflow, and a native outcome sentence. This mode is useful for explaining a system; it is not the default for a financial chart or a user request for fully editable diagrams.

## Final acceptance

Content correctness, visual resemblance, native editability and package validity are separate checks. None substitutes for another. Render the final exported file, inspect each page, review findings from validation scripts, and compare the result with the actual request. Fix source and rebuild when the source builder is available.

When the user requested a revision, deliver the completed revision rather than stopping at an improved outline or a template recommendation. Report partial capability honestly if a host can inspect the skill but cannot render the deck.
