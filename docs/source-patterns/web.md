# Web Source Pattern

## Use When

Use web sources for products, SaaS tools, public docs, blog posts, comparison
pages, official announcements, and public community references.

## Routes

| Need | Preferred Route |
| --- | --- |
| Candidate discovery | web search |
| Known URL text extraction | WebFetch, Jina Reader, or curl |
| Dynamic rendering | browser automation |
| Logged-in content | explicit user approval and high-permission route |

## Notes

- Search results are discovery leads, not evidence by themselves.
- Prefer official pages, docs, source repositories, and primary publications.
- If using a reader service fails, try browser extraction before marking the
  source unavailable.
- Record paywalls, anti-bot blocks, login requirements, and dynamic-rendering
  failures in the search log.

## Last Verified

2026-05-27
