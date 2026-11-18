# Aspose.Words for Java workspace guidance

Apply these rules to Aspose.Words for Java tasks:

- Prefer the configured `words-java` MCP server for documentation and API evidence. The **Aspose.Words for Java MCP** custom agent adds an MCP-only retrieval workflow in `.github/agents/aspose-words-java-mcp.agent.md`.
- Base API and capability claims on inspected evidence. Verify relevant types, members, overloads, and options before using them. A failed lookup does not prove a capability is absent; describe unresolved support as **not verified**.
- If a tool saves an oversized response to a file, read the relevant documentation in bounded chunks before answering; metadata and previews are not evidence. Follow the custom agent’s chunk-reading procedure when using that agent. If the file is inaccessible, request narrower results and report any remaining evidence gap.
- Write Java, never C#. Aspose.Words for Java uses `com.aspose.words` packages, `getX()`/`setX()` accessors instead of properties, lower-camel method names (`doc.save`, `doc.getMailMerge().execute`), and `int` constants on classes such as `SaveFormat` and `LoadFormat`. Do not translate .NET members (`Save`, `MailMerge.Execute`, `Aspose.Words.Saving`) into Java by guessing; verify the Java name.
- Some documentation pages contain snippets copied from .NET or labelled `csharp`. Do not present C# or .NET-only APIs as Java. If only a non-Java example is available, say so and verify each Java member separately.
- API reference examples use test-suite helpers such as `getMyDir()`, `getArtifactsDir()` and `Assert`. Replace them with plain file paths or remove them, and say that you did.
- When Java code is requested, include the required imports, inputs, and outputs, and declare `throws Exception` where the APIs throw checked exceptions. Give the Maven coordinates only as documented by the tools; do not invent versions or repository URLs. Clearly identify incomplete snippets and placeholders.
- Never claim code compiled, ran, or produced a valid document unless actually tested; state what was tested when relevant.
- Cite exact documentation URLs returned by tools (`docs.aspose.com/words/java/...`, `reference.aspose.com/words/java/...`, including member anchors). Do not construct or repair URLs, or claim HTTP verification without a check.
- Answer directly with the simplest verified solution, concise citations, and relevant limitations. State evidence gaps or conflicts clearly.

- Before generating Java examples, read `examples/java-build-rules.instructions.md` and `examples/error-correction.md`. Follow the isolated build workflow in `examples/README.md` and the custom agent. Verify each final block against the pinned configuration when tools are available; report unavailable or failed checks honestly.
