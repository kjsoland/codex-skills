# Codex Skills

Reusable skills and workflow bundles for Codex.

## Repository status

This public repository is initialized and ready for skill releases. Existing local
skills are being reviewed before publication so company-specific procedures,
internal links, personal information, credentials, and proprietary templates are
not exposed.

## Layout

Each published skill belongs in its own folder under `skills/`:

```text
skills/
  example-skill/
    SKILL.md
    agents/       # Optional agent metadata
    assets/       # Optional reusable assets
    references/   # Optional supporting guidance
    scripts/      # Optional automation
```

Every skill must include a complete `SKILL.md` with YAML front matter containing
at least its `name` and `description`.

## Publication checklist

Before publishing a skill:

- Remove secrets, credentials, tokens, private URLs, and personal information.
- Replace company-specific names, templates, and procedures with reusable examples.
- Confirm that included code, documents, and assets may be distributed publicly.
- Add setup requirements and a small usage example.
- Test the skill from a clean installation.

## License

No license has been selected yet. Until one is added, the repository is publicly
viewable but no permission is granted to reuse or redistribute its contents.
