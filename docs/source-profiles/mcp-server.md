# Source Profile: MCP Server

## Use When

Use this profile when evaluating an MCP server, agent connector, plugin, or
tool integration before adopting, wrapping, or building one.

## Required Sources

| Source | Required? | Reason |
| --- | --- | --- |
| GitHub | yes | Finds server implementations, activity, and issue patterns. |
| Package registries | optional | Useful for install surfaces and version maturity. |
| Web/docs pages | yes | Captures protocol support, auth requirements, and setup flow. |
| Skills/plugins registry | optional | Finds adjacent agent-facing wrappers. |
| Community sources | optional | Useful for operational failure modes. |

## Query Seeds

- capability + "mcp server"
- capability + "modelcontextprotocol"
- service name + "mcp"
- service name + "agent connector"
- service name + "plugin"

## Stop Criteria

- The report includes at least one implementation and one docs/setup source.
- Permission, credential, and remote-mutation boundaries are explicitly noted.
- Local validation commands are present or named as missing.

## Blind Spots To Name

- Hosted service APIs and auth scopes may change.
- Tool schemas can diverge from protocol examples.
- Security posture is difficult to judge from metadata alone.
