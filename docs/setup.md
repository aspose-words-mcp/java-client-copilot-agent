# Client setup

## Prerequisites

- VS Code with GitHub Copilot Chat access.
- A deployed Aspose.Words for Java MCP server exposing an HTTP MCP endpoint.
- Network access to that endpoint and any credentials required by your deployment.

To execute generated Java examples, separately install a JDK and add Aspose.Words for Java to your application's build. Follow Aspose.Words licensing requirements for your usage. Neither is needed just to open the client configuration.

## Connect the server

Open `java-client-copilot-agent.code-workspace`. The server is named `words-java`; the custom agent's tool configuration refers to that name, so keep it consistent.

Replace `https://YOUR_MCP_HOST/YOUR_MCP_ENDPOINT` in `.vscode/mcp.json` with your full endpoint URL. The Words/Java server serves it at `/words/java/mcp/v1/streamable-http`, for example `http://127.0.0.1:8080/words/java/mcp/v1/streamable-http` for a local launch. Use the actual URL reported by your deployment; a repository URL or server homepage is not an MCP endpoint. No private address is bundled here.

Start the server connection through **MCP: List Servers**. Review VS Code's trust and tool-access prompts, then open a new chat with **Aspose.Words for Java MCP** selected.

## Authentication

See the [server setup guide](https://github.com/aspose-words-mcp/java-server/blob/main/docs/setup.md) and [client guide](https://github.com/aspose-words-mcp/java-server/blob/main/docs/clients.md) for deployment and authentication configuration.

Follow your server's authentication instructions. Configure authentication through VS Code's **MCP Servers → Add Server** flow for your selected session environment, or use the server's documented credential mechanism. Keep actual credentials out of committed files.

The supplied `.vscode/mcp.json` uses VS Code's `servers` format. Portable Copilot configurations use `mcpServers` instead. VS Code input variables are not supported in portable configurations, and servers requiring interactive inputs are not forwarded to Copilot sessions; the supplied endpoint is therefore an editable literal placeholder. See the [configuration guidance](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

## Verify the connection

Ask a simple question such as “How do I convert DOCX to PDF?” Inspect the chat's tool activity for `words-java` requests and `docs.aspose.com/words/java/` or `reference.aspose.com/words/java/` citations in the answer. A connected MCP server and a discovered custom agent are separate checks.

## Agent missing from the picker

1. Open the repository root or the supplied workspace file in the same VS Code window as the chat.
2. Confirm `.github/agents/aspose-words-java-mcp.agent.md` exists and has `user-invocable: true`.
3. Open **Configure Custom Agent…** and check the workspace agent list.
4. Run **Developer: Reload Window** and start a new chat. This refreshes discovery after the agent file changes.
5. If it remains missing, inspect **Developer: Open Agent Debug Panel** for discovery diagnostics.

## Server or tool errors

Check the endpoint, authentication, network access, and server logs. Use the [server repository's](https://github.com/aspose-words-mcp/java-server) setup guide. An unavailable tool or failed symbol lookup does not establish that an Aspose.Words feature is unsupported.

The server is fixed to Aspose.Words for Java. A request for another product or language is rejected by the server; the agent does not send one.

## Large responses

The agent can use read-only file and terminal tools to inspect saved MCP responses in small chunks, including the bundled `showcase/scripts/read_mcp_response.py` reader (Python 3) or PowerShell `ConvertFrom-Json` on Windows. Normal VS Code permissions apply. If access is declined or unavailable, the agent should request narrower evidence and explain any unresolved gap.

## References

- [VS Code MCP configuration](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)

## Java compilation checks

For generated Java examples, install a JDK 17+ and Maven 3.9+ and follow [build verification](../examples/README.md). The custom agent can edit isolated scratch projects and run Maven dependency resolution and compilation; these permissions extend its read-only MCP-response inspection workflow. Generated programs are not executed by default.
