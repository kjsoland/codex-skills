# Codex Skills

Reusable skills and workflow bundles for Codex.

## Included skills

- [`harness-drawing`](skills/harness-drawing/): create professional cable harness
  and cable assembly drawing packages.
- [`sol-cable-routing`](skills/sol-cable-routing/): maintain the Sol cable-routing
  workbook, route-length audit, and training material.
- [`sol-integration-plan`](skills/sol-integration-plan/): maintain, audit, and
  regenerate the Sol Integration Plan from its authoritative project sources.
- [`sol-change-management`](skills/sol-change-management/): prepare Sol controlled-
  document change packages and Smartsheet ECR artifacts.
- [`verify-beam-delivery-tests`](skills/verify-beam-delivery-tests/): map Sol Beam
  Delivery test results into verification records and waiver drafts.

The Sol bundles intentionally retain their project terminology, workflow rules,
and supporting assets so the published versions match the working skills.

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

## Publishing policy

New custom skills and material updates to existing skills are published to this
repository as part of completing the skill-development work. Repository copies
should stay synchronized with the working bundles after validation and credential
scanning.

## Publication checklist

Before publishing another skill:

- Remove secrets, credentials, and tokens.
- Confirm that any project-specific references and personal information are
  authorized for public distribution.
- Confirm that included code, documents, and assets may be distributed publicly.
- Add setup requirements and a small usage example.
- Test the skill from a clean installation.

## License

No license has been selected yet. Until one is added, the repository is publicly
viewable but no permission is granted to reuse or redistribute its contents.
