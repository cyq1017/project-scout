# Source Profiles

Source profiles are lightweight presets for choosing where to look before a
build/adopt decision. They are not crawler instructions. Each profile should
turn into explicit fixture files, manual URL lists, or bounded query strings
before `project-scout report` runs.

Use these profiles to decide which sources are required, which are optional,
and which blind spots must be named in the final report.

## Profiles

- [market-opportunity](market-opportunity.md): evaluate demand, workflow pain,
  and existing solution categories before building a market-facing capability.
- [product](product.md): compare products, SaaS tools, and commercial
  alternatives before building or buying.
- [paper](paper.md): compare research papers, reference implementations, and
  benchmark claims before adopting an approach.
- [mcp-server](mcp-server.md): evaluate MCP servers, agent connectors, and
  plugin-like integrations before adopting or wrapping one.
