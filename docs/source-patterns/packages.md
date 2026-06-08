# Package Registry Source Pattern

## Use When

Use package registries when the target may already exist as an installable
library, CLI, SDK, plugin, or adapter.

## Routes

| Need | Preferred Route |
| --- | --- |
| Python packages | PyPI project page or package search |
| JavaScript packages | npm package page or package search |
| Rust packages | crates.io |
| Package source | linked repository and release tags |
| Maintenance check | release history, download trend, issue tracker |

## Metadata To Capture

- package name and registry URL
- current version and release date
- linked source repository
- license
- install command
- public API or CLI entrypoint
- compatibility constraints

## Pitfalls

- Download counts can be inflated by CI or dependency chains.
- A popular package can still be abandoned.
- Registry metadata may differ from repository metadata.
- Transitive dependency risk is outside the current MVP unless captured
  manually.

## Last Verified

2026-06-08
