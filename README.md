# Aspose.Words for Java — GitHub Copilot Client Agent

Use GitHub Copilot Chat to explore Aspose.Words for Java with answers and Java examples grounded in your deployed MCP server's documentation and API tools.

This repository provides the **Aspose.Words for Java MCP** custom agent and VS Code client configuration. Deploy the MCP server separately, then connect this client to its HTTP endpoint.

[Setup and troubleshooting](docs/setup.md) · [Build verification](examples/README.md) · [Showcase generation](showcase/README.md)

## Project family

These repositories work together to provide documentation-backed MCP services and a GitHub Copilot client for Aspose.Words for Java. The shared engine is maintained under **aspose-core-mcp**; the Words/Java components are maintained under **aspose-words-mcp**.

| Repository | Responsibility |
| --- | --- |
| [context-engine](https://github.com/aspose-core-mcp/context-engine) | Shared documentation ingestion, indexing, retrieval, and MCP infrastructure |
| [java-plugin](https://github.com/aspose-words-mcp/java-plugin) | Aspose.Words for Java documentation/API extraction and retrieval profile |
| [java-server](https://github.com/aspose-words-mcp/java-server) | Deployment helpers that combine pinned engine and plugin versions |
| [java-client-copilot-agent](https://github.com/aspose-words-mcp/java-client-copilot-agent) **(this repository)** | GitHub Copilot agent, Java compilation checks, and example-answer showcase |

## Quick start

1. Install and deploy the MCP server using its repository instructions (link above). Obtain its full HTTP MCP endpoint URL (it ends in `/words/java/mcp/v1/streamable-http`) and any authentication requirements.
2. Install VS Code with GitHub Copilot Chat access, and open `java-client-copilot-agent.code-workspace` from this repository.
3. Replace `https://YOUR_MCP_HOST/YOUR_MCP_ENDPOINT` in `.vscode/mcp.json` with the full HTTP endpoint URL supplied by your deployment. Run **MCP: List Servers**, select **words-java**, and start it.
4. If your server requires authentication, complete the configuration described in [setup](docs/setup.md#authentication) before connecting.
5. Start a new Copilot chat and choose **Aspose.Words for Java MCP** from the agent picker.
6. Ask, for example: **How to convert DOC/DOCX to PDF using Aspose.Words for Java?**

The agent queries the server for evidence, checks relevant APIs, and cites documentation returned by the tools. It can read saved tool responses in bounded chunks when a response is too large to display directly.

## What is included

- `.github/agents/aspose-words-java-mcp.agent.md`: custom agent scope, retrieval, and response-reading workflow.
- `.github/copilot-instructions.md`: shared evidence and answer guidance, including Java-specific API conventions.
- `examples/`: pinned Maven compilation project, Java build rules, and error-correction examples.
- `.vscode/mcp.json`: HTTP connection configuration with an endpoint placeholder.
- `showcase/`: question runner with optional compilation/repair and concise showcase and metrics reports, plus the 99 input questions. See [generation instructions](showcase/README.md).

## Showcase

The [showcase runner](showcase/README.md) answers 99 saved questions in fresh Copilot CLI sessions. The questions cover document conversion, reporting, mail merge, comparison, splitting and merging, find and replace, signatures, watermarks, and AI features. It can compile each Java answer and request up to two repairs. A published run will be added under `showcase/runs/published-01/` after the first full run against a deployed server.

## Contributing

Include your VS Code version, selected model, and a minimal prompt when reporting a client issue. Remove credentials and private endpoint details from logs. Report server deployment or tool issues in the [MCP server repository](https://github.com/aspose-words-mcp/java-server).

## Compile generated examples

Install a JDK 17 or newer and Maven 3.9 or newer to enable Copilot compilation checks. The custom agent reads the rules under `examples/`, writes each Java block into a separate scratch Maven project, and compiles it against Aspose.Words for Java 26.10 (`jdk17` classifier) with `--release 17` and lint warnings as errors. It can attempt two repairs after an initial compiler failure and reports the actual result. Allow the required edit/terminal permissions when prompted. See [build verification](examples/README.md) for manual commands and requirements.

## License

[MIT](LICENSE), copyright (c) 2001–2026 Aspose Pty Ltd.
