---
name: lab-safety-graphic
description: Create or update one-page lab hazard and emergency-reference graphics using an actual floor plan, numbered location callouts, supporting photos, and supplied response steps. Use for laser-hazard maps, shutoff-valve maps, and similar lab safety one-pagers; not for writing a complete safety program or certifying regulatory signage.
---

# Lab Safety Graphic

Create a location-based reference that a person can scan quickly during lab work. Reuse the user's approved composition and source images. When a workspace contains `Lab Safety Graphics/project_sources.json`, use it to locate the private reference graphic, builder, and source documents; the catalog and its contents do not belong in the public skill bundle.

## Preferred composition

- Default to one landscape US Letter sheet: 11 x 8.5 inches, 792 x 612 PDF points. An explicit user size or orientation takes precedence.
- Make the real floor plan or system layout the dominant central graphic. Put smaller location photos around it; do not turn it into a small inset beside a photo grid.
- Use conspicuous numbered markers and matching numbered photo headers. Point to the physical feature the user means, including the correct rack face, not just the nearest roof or cabinet.
- Embed front-door and back-wall labels near their actual positions within the graphic. A perspective image should remain upright unless a rotation is requested.
- Keep one compact response/contact box below the central graphic when response content is supplied. Preserve action order and label contacts by building or role. Distinguish building-specific alternatives from a sequential call list.
- A single useful detail crop can replace a redundant overview photo. Crop to improve label readability while retaining the important fittings, handles, or hazard features.
- Retain the established typography and colors for revisions. For a new hazard type, select the title/accent treatment without claiming compliance with a warning-sign standard.

Read [production.md](references/production.md) for placement guidance, faithful source extraction, and output checks.

## Evidence and scope

Locate local synced project files before fetching SharePoint URLs. Prefer the user's identified sources and record their revision. Inspect the source figure and its surrounding text before attaching a label to a location.

Keep a private source table for each callout: identifier, component, physical location, rack face or rack units when provided, photo/figure, source revision and locator, and unresolved facts. Distinguish an equipment location from an exposure area or hazard boundary.

Copy response steps and phone numbers from the user's instructions or current supplied safety material. Do not carry a water-shutoff response into a laser-hazard graphic merely because it is the visual template. Leave missing operational content out of the finished graphic or clearly label a working draft; ask only for the missing facts that affect the result.

For laser hazards, read [laser-inputs.md](references/laser-inputs.md). Assembly ICDs are useful for laser identities and rack placement. Hazard classifications, exposure boundaries, eyewear requirements, and emergency actions need explicit support in the relevant source material.

## Live status boards

When the user wants movable magnets, put a compact status table beside each location. Use the user's state labels, for example **Laser off**, **On contained**, and **On active hazard**. Give independently tracked lasers their own rows, with wavelength and a short identifier to distinguish equal-wavelength sources. Leave every state cell blank for setup; the document must not imply a live operating state. Keep the map dominant and use small ICD detail views where they help identify the sources.

Size cells for the stated magnet dimensions. If none are provided, choose practical cells for the requested sheet and report their printed dimensions. Preserve units in the table header or every row. Do not add response instructions when the user excludes them. Record source disagreements privately and apply the user's explicit resolution without silently rewriting the source document.

## Build and deliver

1. Preserve the current accepted files before a material edit. Adapt the existing project builder when it produces editable shapes and correct exports; keep a new hazard's outputs in a separate project folder.
2. Reuse original image bytes and native document crops. Transfer source annotations as well as the photo. Do not use generative reconstruction to recover labels, change equipment, or infer hidden features in documentary safety images.
3. Maintain an editable PowerPoint, a one-page PDF, and a PNG preview with matching content. Keep labels, numbered markers, contact text, and source annotation rectangles editable where practical.
4. Check the actual PDF page size and page count; compare the rendered PowerPoint with the PDF; inspect callout endpoints and source-image annotations. Verify every phone number and unit against its source.
5. Deliver links to the PDF and PowerPoint. Mention any material unresolved source facts rather than claiming a location-only draft is a complete hazard assessment.

Use `scripts/extract_slide_graphic.py` when a supplied PowerPoint graphic consists of a photo plus separate rectangular annotations. It lists named shapes or extracts the original image and photo-relative annotation geometry without modifying the deck. The script uses Python's standard library; render/inspect the selected source slide as well, especially when it contains several graphics.

Example request: "Use $lab-safety-graphic to make a landscape lab laser-hazard map from the assembly ICDs, with the floor plan centered and supporting rack figures around it."

## Public bundle boundary

Publish reusable instructions and tooling, not private floor plans, lab photographs, internal ICD excerpts, contacts, or generated project posters. Keep those in the user's workspace or authorized project location. This skill does not itself authorize publication or messaging.
