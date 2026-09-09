# Reference-driven redesign

Read for a supplied design reference or a complaint that a deck is too simple, monotonous or lacks logic.

## Decode the reference

Inspect representative pages at full size, not just their extracted text. A deck may hold nearly its entire explanation inside image assets; a text-only read can miss the central design.

Record a brief contract in the task workspace:

| Dimension | Capture from the reference |
| --- | --- |
| Page hierarchy | Title, thesis, mechanism/evidence area, visual, takeaway |
| Density | Approximate copy length, number of groups, readable body size |
| Visual weight | Relative area of text, diagrams and evidence |
| Diagram grammar | Panels, branches, shared bases, arrows and feedback paths |
| Color roles | Primary structure, supporting elements, highlighted conclusions |
| Asset style | Real photos, screenshots, diagrams or illustrated equipment |
| Continuity | Title position, margins, logos, page numbers, repeated motifs |

For a short task, a few sentences suffice. Inspect enough source pages to see the pattern and its exceptions. When adapting the whole deck, inspect every page.

## Redesign the explanation

Translate source bullets into relationships before choosing graphics:

- “Quality control” becomes entry requirements, responsible checks, accepted output and a correction path.
- “Three databases” becomes what each stores, how records associate, and which services use the result.
- “A high-quality dataset” becomes selected inputs, expert processing, review, versioning and controlled use.
- “Remote consultation” becomes requester, authorization, data access, expert response and audit trail.

Not all items belong in one diagram. A payment rule can be a parallel governance condition rather than an automatic consequence of every quality failure. A legal authority boundary belongs in copy or notes if drawing it as a technical gate would overstate what software guarantees.

Use a short relationship review:

1. Can the audience name the input and output?
2. Does each connector express sequence, association, control or feedback consistently?
3. Are shared dependencies and parallel applications shown correctly?
4. Does the bottom statement name an actual deliverable or use rather than repeat the title?

## Example production brief

> Produce four replacement slides for a public-service data platform. Keep the source numbering. The selected reference uses a blue subject heading, a concise mechanism sentence, a compact gray explanation area, a dominant engineering illustration and a red output statement. Reuse that hierarchy without importing unrelated partner logos. Show quality intake with a correction loop; associated records with a common index; expert dataset processing; authorized service access with a response loop. The final two uses branch from the common database. Keep policy statements separate from technical safeguards. Titles and body remain editable; raster diagrams are acceptable only when the editing requirement allows them.

The portable method is reference analysis plus argument mapping and visual production. The colors and composition above are only an example of one reference style.

## Asset and prompt design

Choose the diagram's intended frame before generating it. For a wide mechanism band, request a wide illustration rather than cropping a square image until labels disappear. Specify all essential actors, labels and connector directions. Use the actual reference image as a style input when supported; inspect it first.

A useful prompt skeleton:

```text
Asset role: [diagram / illustration / evidence]
Reference role: [visual style only / exact edit target]
Frame: [aspect ratio and intended slide area]
Actors and structure: [ordered or branching groups]
Exact labels: [short, verified text]
Connectors: [direction and meaning; correction/response loop if needed]
Visual language: [from the selected reference]
Factual limits: no invented prices, performance figures, credentials,
patient records, institutional logos or claims of completed deployment
```

Inspect the image as content. Generators can add plausible-looking invoices, totals, chart labels, certificates and UI data that the prompt never supplied. Replace those with labeled schematic fields or source-backed evidence before assembly. Check small Chinese labels too. Make a targeted edit when one region is wrong instead of regenerating the entire style unnecessarily.

For multiple alternatives, vary the visual explanation intentionally: a process-centered page, an evidence-centered page and an architecture-centered page can each cover the same subject. Their quality still depends on the user's reference and presentation purpose, not the labels assigned to the variants.
