# Runtime adaptation and final-file QA

Use the tools exposed by the active host. Shared skill instructions do not make one host's tools available in another.

## Claude Code and Codex

- Discover the installed presentation and image skills in the current session. Follow the selected skill's implementation and validation instructions.
- On Codex Desktop, when `load_workspace_dependencies` and the presentation skill are available, resolve the supplied runtime and use its prescribed authoring library. Treat paths returned by the loader as authoritative; do not hard-code a versioned cache path into this shared skill.
- On Claude Code, use its installed PPTX/image skills and supported tools. Do not call Codex-only namespaces, assume its dependency loader exists, or start another agent's CLI merely to render a presentation.
- If the preferred renderer is unavailable, choose an installed alternative that preserves the requested output and editability. Explain a material downgrade before presenting the artifact as complete.
- Use the host's image-generation policy. A built-in tool needs no user API key unless that tool says otherwise. Do not silently move to a paid CLI/provider fallback or request credentials just for convenience.

## Portable assets and bounded logs

Save chosen images in the task workspace, retain source paths/URLs, and record their source slide numbers or exact generation prompts. Keep reference content, factual sources and generated schematics distinguishable.

Image-generation responses may contain large base64 data URLs. Save/forward the media using the documented media API; log only small metadata such as asset key, saved path and status. Never JSON-print the entire media result. Parallelize independent assets only if supported, and wait for each requested result before assembly.

Use targeted image edits for wrong labels or invented figures. Preserve the accepted layout and style, verify the edit, and keep the original until the replacement is chosen.

## Export checks

- Use absolute, resolved workspace paths when locating output and parent directories. `Path('.') .parent` is not a reliable way to reach the current directory's parent; resolve the path first.
- When the installed finalizer uses `RUNTIME_NODE_MODULES`, export that environment value for its child import check as well as for the builder.
- Where outputs or receipts are exclusive-create, give both the final file and receipt a new revision name. Reusing a receipt can invalidate an otherwise successful revised export.
- Verify the exact final PPTX, not only in-memory authoring previews. Render every final page and inspect it at reading size.

These are conditional implementation notes, not required APIs on every host.

## Chinese font failures

A valid PPTX can render as empty boxes if the renderer cannot discover Chinese fonts. Diagnose the renderer's actual font inventory before replacing text or changing the design.

If the host's bundled LibreOffice lacks access to installed fonts, use a task-local fontconfig file pointing at verified font directories and pass it to that render process. Avoid global font configuration changes. When the presentation skill mandates bundled LibreOffice, use that binary, not a desktop installation. Re-render after the fix and inspect the Chinese text, including captions and notes where relevant.

## Two independent QA passes

**Argument and evidence pass**

- Check each requested topic against both native copy and diagrams.
- Check the source of each visual and whether its caption describes what it actually shows.
- Inspect generation additions: amounts, percentages, version labels, signatures, seals and status claims. Illustrative version labels may be suitable; fabricated financial or performance evidence is not.
- Keep planned capability, existing capability and measured performance distinct.
- Validate branches and feedback without assuming slide order equals execution order.

**Rendering and packaging pass**

- Inspect every final slide, then check deck-level rhythm with a contact sheet.
- Check actual font rendering, alignment, text density, image resolution, cropping, connecting lines and safe margins.
- Compare with the user's selected reference. More whitespace is not automatically an improvement if it removes the explanation the reference is designed to carry.
- Confirm requested editability. A deck with native text and raster diagrams is partly editable; disclose this specifically.
- Keep build logs, initial drafts and QA reports outside the final delivery folder. Provide a preview when it helps the user assess the result.
