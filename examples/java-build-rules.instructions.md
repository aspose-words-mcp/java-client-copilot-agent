# Java build rules

**Before writing any Java, read `examples/error-correction.md` in this workspace and follow its rules
J0–J8.** That file has the worked wrong/right example for each rule. The mandatory parts are repeated
here so they apply even if you do not open it.

**These rules tell you _how_ to write code, not _whether_ to include it.** If a question asks how to
perform a task, answer it with a working example. Never fall back to a prose-only answer, a fragment or
a list of type names in order to avoid the risk of a compiler error — an answer with no code where code
was asked for does not answer the task. Prose alone is right only for genuinely conceptual
questions ("what is X", "what is the difference between X and Y"), where an example would not be the
natural response.

For build verification, copy every fenced `java` block and compile it **on its own**, as the only source
file of a fresh project, saved as `<PublicClassName>.java`. Nothing carries over from another block or
from your prose.

| Setting | Value |
| --- | --- |
| JDK | 17 or newer |
| `--release` | `17` (Java 17 language and API) |
| Lint | `-Xlint:deprecation,removal,unchecked,rawtypes` |
| Warnings | treated as errors (`-Werror`) |
| Dependencies | only `com.aspose:aspose-words:26.10:jdk17` and the JDK |

Every block must therefore:

- **J0** — exist. A "how do I…" question is answered with a compiling example, not a description of
  which types to use. Omitting code to stay safe is a failed answer, not a cautious one.
- **J1** — be a complete, runnable program: exactly one top-level `public class` that declares
  `public static void main(String[] args) throws Exception`. Helper types go after it without
  `public`, or inside it as `static` nested types. No `package` declaration.
- **J2** — import every type it uses with explicit single-type imports. Never combine
  `import com.aspose.words.*;` with `java.util.*` or `java.awt.*`: `List`, `Shape` and `Font` exist in
  both, and the simple name becomes ambiguous.
- **J3** — stand alone: declare every identifier it references, and repeat its own imports and setup
  even when an earlier block already showed them.
- **J4** — handle checked exceptions: `main` and every helper method that calls Aspose.Words declares
  `throws Exception`.
- **J5** — not reuse an Aspose.Words type name for its own class (`Document`, `Range`, `Watermark`…).
  Name the public class after the task, for example `ConvertToPdf`.
- **J6** — compile without warnings: no deprecated or for-removal APIs, no raw generic types, no
  unchecked conversions. Target Java 17: no unnamed classes, instance `main`, or pattern-matching
  `switch`.
- **J7** — use only Aspose.Words for Java and the JDK. No other Maven dependency, and no API-reference
  test helpers (`getMyDir()`, `getArtifactsDir()`, `Assert`); use plain file paths.
- **J8** — when revising an answer, return it complete and reproduce **every** documentation URL the
  original cited. Preserve the original documentation URLs when repairing code; compare them before presenting the revision. Add a URL only from `words-java` evidence retrieved in this session.

Check once more before answering: does a "how do I" question have a code example at all, and does each
block have one public class with `main`, explicit imports with no ambiguous wildcards, every identifier
declared, `throws Exception` where needed, and nothing deprecated or raw? A compiler error is a failed
answer even when the Aspose.Words API usage is correct — and so is no code at all.
