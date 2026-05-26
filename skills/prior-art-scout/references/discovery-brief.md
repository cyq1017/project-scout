# Discovery Brief

Use this schema for Formal Gate. Keep fields concise and evidence-oriented.

```json
{
  "name": "",
  "target_type": "project|skill|plugin|tool|mcp_server|product|paper|internal_asset",
  "intent": "build|adopt|replace|extend|research",
  "goal": "",
  "keywords": [],
  "users_or_consumers": [],
  "ecosystems": [],
  "must_have": [],
  "nice_to_have": [],
  "exclusions": [],
  "known_candidates": []
}
```

Map to the current `project-scout` MVP brief when needed:

- `name` -> `name`
- `goal` -> `goal`
- `keywords + must_have + nice_to_have` -> `keywords`
- `users_or_consumers` -> `target_users`
- `ecosystems + must_have` -> `tech_stack`
- `exclusions` -> `exclusions`

Known candidates may be URLs, package names, skill names, repo names, product names, paper titles, or local paths. Include them in the candidate set even if they later score as `Avoid` or `Ignore`.
