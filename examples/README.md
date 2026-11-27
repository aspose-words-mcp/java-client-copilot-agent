# Java build verification

This project compiles examples against **Java release 17 and Aspose.Words for Java 26.10 (`jdk17` classifier)**. Lint warnings for deprecation, removal, unchecked and raw-type use are enabled and treated as errors. Any JDK 17 or newer can build it, because `--release 17` fixes the language level and JDK API.

Install a JDK 17+ and Maven 3.9+ separately. From the repository root:

```sh
cd examples
mvn -B -q compile
```

The first build downloads `com.aspose:aspose-words:26.10:jdk17` from the Aspose Maven repository (`https://releases.aspose.com/java/repo/`) and the pinned compiler plugin from Maven Central into your local Maven repository (`~/.m2/repository`). If your environment restricts repositories, configure an approved mirror in your Maven `settings.xml` or populate the local repository. The exact Aspose.Words version is pinned; it is the only declared dependency.

The checked-in `src/Example.java` is a DOCX-to-PDF compilation fixture. Building it does not read `input.docx` or create `output.pdf`; running it would. The agent must not run generated programs unless the user separately requests it.

## Copilot workflow

The custom agent and shared workspace guidance explicitly reference [Java rules](java-build-rules.instructions.md) and [error-correction examples](error-correction.md). These files are outside `.github/instructions/`, so they are loaded by explicit reads, not automatic directory discovery.

For each answer, Copilot creates a new `examples/.scratch/<unique-request>/block-N/` directory. It copies `pom.xml` there and writes each complete Java block as `src/<PublicClassName>.java`; the file name must match the block's public class. Each block is compiled independently with `mvn -B -q compile` from its own directory.

The agent may make at most two compiler-driven repairs per block after the initial attempt. It must build the exact final code shown in the answer, retain citations, and state the result. A missing JDK or Maven, dependency-resolution failures, denied tool access, and timeouts are reported as unavailable verification rather than successful builds. Compilation does not check runtime behavior or document output.

Each request uses a fresh scratch directory; existing user files and the checked-in fixture are not overwritten. Scratch files and build outputs (`target/`) are ignored by Git. File edits and commands remain subject to normal client permissions. This is an agent workflow, not an automatic CI gate or a guarantee that every response follows the instructions.

## Showcase controller

The [showcase runner](../showcase/README.md) compiles answers itself with `javac` (no Maven per block) using the same `--release`, lint and `-Werror` settings, and the `aspose-words` jar from your local Maven repository. Run `mvn -B -q compile` here once so that the jar is present; the controller never downloads dependencies.

## Rule provenance

Adapted from the Aspose.Words for .NET client's C# rules (R0–R8). Rules J0–J8 keep the same intent and numbering where it carries over, and J9 adds LINQ Reporting templates, which only fail at run time; the Java build contract replaces the C# one (single public class per file, explicit imports, checked exceptions, lint warnings as errors). Every wrong/right pair in `error-correction.md` was compiled with `javac --release 17` and these lint settings to confirm that the right block passes and the wrong one fails with the diagnostic named. The J1 and J9 examples, which use `ReportingEngine`, are also run against Aspose.Words for Java 26.10 by `showcase/scripts/check_linq_runtime.py`: the J9 WRONG example compiles but fails at run time, and the RIGHT ones produce the expected document.
