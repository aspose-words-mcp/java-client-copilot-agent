# Generate a Copilot showcase

Run saved questions in fresh Copilot CLI sessions and produce three files under `showcase/runs/<run-name>/`:

- `showcase.md`: the title, introduction, question list grouped by topic, anchored answers, attempt wording, and model identities.
- `checkpoint.json`: compact answers, outcomes, and configuration for resuming. No raw traces or compiler logs.
- `metrics.md`: coverage, first-attempt outcomes, compilation results, generation/repair model counts, repair requests, duration, and concise failure reasons.

To publish a run, name it (or copy its reports to) `published-01`: only `showcase/runs/published-01/showcase.md` and `metrics.md` are included in Git; checkpoints stay local. Use a different run name for new generations. To publish a replacement, select its reports and update the documentation links and Git ignore exceptions together.

## Prerequisites

Use Python 3, an authenticated `copilot` CLI on PATH, and a working `words-java` endpoint in `.vscode/mcp.json` (see [client setup](../README.md#quick-start)). Compilation additionally requires `javac` from a JDK 17 or newer on PATH and the Aspose.Words for Java jar in your local Maven repository: run `mvn -B -q compile` in `examples/` once (see [build verification](../examples/README.md)), or point `--aspose-jar` or the `ASPOSE_WORDS_JAR` environment variable at the jar. Defaults are Aspose.Words for Java 26.10 (`jdk17` classifier) and `--release 17`; the compiler enables `-Xlint:deprecation,removal,unchecked,rawtypes` and `-Werror`. Automated compilation calls `javac` directly and never downloads dependencies. A missing `javac` or jar, or a JDK too old for the selected release, is reported as unavailable verification and does not trigger model repairs.

## Commands

From the repository root (use `python` instead of `python3` on Windows):

```sh
# Preview selection and configuration without model requests or output files
python3 showcase/scripts/run_copilot.py --run preview --all --dry-run

# Generate one question (the default limit)
python3 showcase/scripts/run_copilot.py --run sample-01

# Generate all 99 questions, compile Java and allow up to two repairs per answer
python3 showcase/scripts/run_copilot.py --run full-01 --all --verify-code

# Select a group or one question
python3 showcase/scripts/run_copilot.py --run pdf-01 --group word-to-pdf --all --verify-code
python3 showcase/scripts/run_copilot.py --run pdf-02 --query-id word-to-pdf-01

# Verify a saved answer for a single question
python3 showcase/scripts/run_copilot.py --run replay-01 --query-id word-to-pdf-01 --verify-code --answer-file /path/to/answer.md
```

`--input` defaults to `showcase/inputs/questions.json`: the 99 questions of the Aspose.Words for .NET client showcase with the same `query_id` and `group` values, with C#-specific wording changed to Java. The JSON retains the `cases` array and each question's `query_id`, `group`, and `question` fields. Group/ID filters apply before `--limit` (default 1); `--all` removes the limit. Model selection defaults to `--model auto`; reports show resolved identities, or `unknown` when absent.

`--timeout` defaults to 300 seconds per model invocation; `--build-timeout` to 120 seconds per block. `--repair-attempts` accepts 0–5 (default 2). Package and language level can be selected with `--aspose-version` and `--java-release` (`17`, `21`, or `25`). These settings control the controller's compiler; the repository's authoring guidance describes its default Java 17 setup.

## Output and failures

Only the two Markdown reports and the checkpoint persist in the run folder. CLI events, compiler logs, workspaces, and intermediate answers are temporary and cleaned up on normal completion, handled errors, and Ctrl+C. The runner does not request session transcripts or usage exports. Copilot may maintain its own application-managed session history outside this runner. Abrupt process termination or a machine crash can prevent temporary cleanup.

Reports are refreshed after each question and on handled interruption. A failed generation stops further questions; compilation failures allow subsequent questions to proceed. Failures return a nonzero exit code. Resume with the same question-selection and verification options plus `--resume`:

```sh
python3 showcase/scripts/run_copilot.py --run full-01 --all --verify-code --resume
```

Completed questions are skipped (verification must be `passed` or `no_code` when enabled). Failed, timed-out, and interrupted questions restart from generation. Both reports are regenerated as one combined result. Checkpoints are atomically replaced before each question and after generation/verification; a crash can require repeating the current question but preserves previously checkpointed work. Two processes cannot write the same run concurrently (a directory lock on Linux/macOS; a `showcase/runs/.<run>.lock` file on Windows).

Selected questions, model, instruction hashes, MCP configuration, CLI/runner version, `javac` version, jar hash, and verification settings must match. You may increase `--timeout` and `--build-timeout` on resume. Missing or incompatible checkpoints produce an error without overwriting prior results. Existing runs require explicit `--resume`; use a new name for a fresh run. Model, compilation, and repair metrics describe the latest attempt per question; generation retries are counted separately, and duration accumulates across saved sessions (excluding downtime).

Generation completion is separate from compilation success. No-code and unchecked answers are never counted as compilation passes. Replayed answers are labeled and excluded from generation model counts. Model counts are distinct questions per role; multiple models can contribute to one question. Repair totals count requests, including unsuccessful requests.

Each `java` block is compiled on its own as `<PublicClassName>.java`. A block that compiles but declares no `public static void main(String[] args)` is recorded as failed with the diagnostic `missing-main`, because the rules require runnable programs. Compiler diagnostics are recorded by their javac keys (for example `compiler.err.cant.resolve.location`) and passed to the repair request.

The runner snapshots this repository's evidence and code-quality guidance into a temporary workspace, with a controller-specific instruction that compilation/repair is handled outside the model session. The model is denied file writing; generated Java is compiled but never executed. Repairs preserve original citation URLs and accept new URLs only from successful words-java repair evidence. Runtime behavior is recorded as `Not checked` in the metrics table. If repair fails, the original answer remains in the showcase and the metrics report records the failure.

## Local tests

```sh
python3 -B -m unittest discover -s showcase/scripts -p 'test_*.py'
```

The `javac` integration tests compile against a small generated stub of `com.aspose.words` and are skipped when no JDK is installed; no network or Aspose jar is needed.
