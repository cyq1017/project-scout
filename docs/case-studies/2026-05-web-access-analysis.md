# Web Access Analysis

## Context

We inspected Web Access as a reference for search-related skill design. The
goal was not to copy its implementation, but to identify what should transfer
into `prior-art-scout` and future discovery skills.

Primary source:

- <https://github.com/eze-is/web-access>

Related write-up:

- <https://mp.weixin.qq.com/s/rps5YVB6TchT9npAaIWKCw>

## What It Is

Web Access is best understood as a web access strategy skill, not a single
search tool. Its useful design pieces are:

- tool selection across search, fetch, curl/Jina-style readers, and browser/CDP
- browser automation for dynamic pages and logged-in workflows
- site experience accumulation by domain
- explicit warnings around high-permission browser/session use

## Transferable Principles

1. **Separate strategy from tools.**
   A skill should teach when to use a route, not hard-code one route for every
   web task.

2. **Escalate permissions gradually.**
   Search and static readers should come before browser/CDP. Logged-in browser
   access should be explicit and rare.

3. **Preserve source-specific experience.**
   Site patterns, URL quirks, dynamic loading behavior, and failure modes should
   live in small reference files.

4. **Treat browser access as high-permission.**
   Logged-in state can expose private accounts and platform risk. Discovery
   skills should record such sources as optional or high-risk, not default.

5. **Keep the decision protocol independent.**
   `prior-art-scout` should own coverage, evidence, scoring, and recommendation.
   Web Access-like tools should remain adapters.

## What Not To Copy

- Do not make `prior-art-scout` take over every network task.
- Do not require CDP, a real browser, or logged-in state for ordinary discovery.
- Do not store cookies, tokens, or browser session data.
- Do not make social-platform automation part of the default path.

## Changes Suggested For This Repo

- Add a search adapter reference that names capabilities rather than fixed tools.
- Add source-pattern docs for GitHub, skills registry, web pages, social sources,
  and papers.
- Keep `SKILL.md` concise and route detailed source behavior through references.

## Last Verified

2026-05-27
