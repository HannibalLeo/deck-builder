# Quality gates that inspect the product

Read before the representative-page check and before final delivery. Looking at a PNG is an action, not a verdict. Record what passed, what failed and what changed in the private task workspace.

## 1. Source and reference gate

Record distinct authorities for content, design and user corrections. Include exact files/pages and the latest corrected facts. If the user said “this style” after showing a reference, preserve that reference across tools and revisions. An older branded deck may provide logos or product screenshots without controlling layout or price.

## 2. Parameter gate

Record task-specific canvas dimensions, body/title/caption sizes and image frames before authoring. Choose them from the actual reference or intended viewing conditions. A 16.5pt reference body does not become 7.7pt because the new builder uses another library.

Use `scripts/audit_pptx.py` to inspect the final package's native font sizes, text counts and image aspect ratios. Set font and density thresholds for this task, not every deck. Name legitimate small text `caption-...`, `footer-...` or `page-...` so the report can distinguish it from body copy. The helper does not inspect rendered glyphs, full grouping semantics, internal overlaps, or rasterized labels; inspect those separately. Unknown objects and unsupported cases require review, not a claim of complete coverage.

Example, after setting the task's actual limits:

```bash
python3 scripts/audit_pptx.py /absolute/path/final.pptx \
  --min-font-pt 16 --max-slide-chars 350 \
  --report /absolute/path/private/geometry-report.json
```

These limits are an example for a readable short briefing, not a rule for a dense reading deck. Do not lower a failing threshold merely to make the artifact pass.

## 3. Image and diagram gate

- Measure the returned asset, not just the requested size. Preserve its aspect ratio after any deliberate crop. If it does not fit, reframe or regenerate; do not stretch it.
- Check each asset against that page's `visual_job` and `must_show`. A graphic about model selection must identify the choices and selection rule. A financial allocation page must expose amounts/proportions, and a payment page must identify milestones.
- Imagine the explanatory paragraph hidden: does the main visual still communicate the required relationship through its own labels and connections? If not, the image is decoration or incomplete, and the page needs revision.
- Keep significant quantities and classifications native when they need exact values or editing. Illustrations can support them without replacing the evidence.

## 4. Reading and hierarchy gate

At equivalent viewing size, compare the source and candidate page side by side. Check body readability, title/body hierarchy, dominant visual, and required detail. Look specifically for unrelated modules sharing equal emphasis, fragmented sentences in widely separated boxes, and a large image that crowds the actual decision into tiny copy.

For a reduced page count, keep one main question per page. Put secondary scripts, caveats and specifications in notes when appropriate. Do not preserve every original module at half the text size.

Inspect rectangle and text-box boundaries where modules meet. A bottom conclusion strip must not mask content above it. Image aspect checks and package integrity checks do not detect all such overlaps.

## 5. Representative-page and regression gate

Render one content-heavy page before propagating a design. Fix actual problems, then complete and render the remaining pages. This is an internal quality step when the user has already authorized the direction.

For a skill revision prompted by poor output, use the poor artifact as a negative case and the rebuilt artifact as the positive case. Record objective findings and visual changes. A model describing the right procedure or successfully loading the skill is not an end-to-end production test. Do not publish customer material, private references or session logs with the reusable skill.

Final acceptance requires both measurable checks and a page-level judgment that the visual answers the right question. If the output still has an accepted failure pattern, change the artifact or report the limitation; do not declare it clean just because all pages were opened.
