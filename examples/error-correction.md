# Code rules — read before writing any Java code

**Read this file before you write a single line of Java. Do not start from memory of how Java examples usually look.**

For build verification, copy every fenced `java` block and compile it on its own, as the only source file of a
fresh project, with no other block and no surrounding prose available to it. A block that would be fine pasted
into an existing project can still fail here. The rules below exist because each one breaks a real build.

> **These rules tell you _how_ to write code, not _whether_ to include it.** They are a style guide, not a
> reason to answer in prose. See J0.

## The build contract

Your code is compiled with exactly these settings. Nothing else is configured for you.

| Setting | Value | What it means for you |
| --- | --- | --- |
| JDK | 17 or newer | a current `javac` |
| `--release` | `17` | Java 17 language level and JDK 17 API only |
| Source file | `<PublicClassName>.java` | the block is the only file; its public class names the file |
| Lint | `-Xlint:deprecation,removal,unchecked,rawtypes` | these warnings are reported |
| `-Werror` | on | **every reported warning fails the build** |
| Dependencies | `com.aspose:aspose-words:26.10:jdk17` | nothing else is on the class path |

The code is compiled, never executed. Correct compilation is required but does not make the example right.

## Pre-flight checklist

Before you emit a `java` block, confirm all eight:

- [ ] The question asked how to do something, and you are in fact giving a code example (J0).
- [ ] It has exactly one `public class`, with `public static void main(String[] args) throws Exception`, and no `package` line.
- [ ] Every type it uses is imported with an explicit single-type import at the top of **this** block.
- [ ] Every identifier it references is declared inside **this** block.
- [ ] Every method that calls Aspose.Words declares `throws Exception`.
- [ ] Its own classes do not reuse Aspose.Words type names.
- [ ] It uses no deprecated API and no raw generic type.
- [ ] It would compile if it were the only file in an empty project.

## Rules

### J0 — Still include the code

If the question asks how to perform a task, answer it with a working Java example. Do not drop to a
prose-only description to avoid the risk of a compiler error, and do not reduce an example to a
fragment, a single method signature or a bulleted list of type names for the same reason.

An answer with no code where code was asked for is a worse answer than one with a compiler error, and
it does not answer the task. The rules that follow exist to make your example compile — they
are never a reason to withhold one.

Prose alone is the right answer in one case only: when the question is genuinely conceptual — "what is
X", "what is the difference between X and Y", "what features are available" — and a code example would
not be the natural response. If you could reasonably open the answer with "here's how", include the
code.

WRONG shape of answer for *"How do I convert a document to an image?"*:

> Load the document as a `Document` and save it with `ImageSaveOptions`, choosing PNG or JPEG.
> See the conversion guide.

Correct, cited, and useless to someone who wanted the call. Give them the call:

```java
// RIGHT — the explanation plus a block that actually compiles
import com.aspose.words.Document;
import com.aspose.words.ImageSaveOptions;
import com.aspose.words.SaveFormat;

public class ConvertToImage {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("input.docx");
        ImageSaveOptions options = new ImageSaveOptions(SaveFormat.PNG);
        options.setResolution(300);
        doc.save("output.png", options);
    }
}
```

### J1 — Every block is a complete, runnable program

The block is the only source file. It needs one top-level `public class` with a `main` method; the file
is named after that class. A second `public` top-level class, a bare method, or loose statements do not
compile. Do not add a `package` line.

*Prevents `compiler.err.class.public.should.be.in.file`, `compiler.err.expected4`, and the controller's `missing-main`.*

```java
// WRONG — loose statements and a method with no class around them
Document doc = new Document("input.docx");
doc.save("output.pdf");
```

```java
// WRONG — a library class; nothing runs it
public class ReportGenerator {
    public static void generate() { /* ... */ }
}
```

```java
// RIGHT — one public class with main; the data class is a public static nested type (see J9)
import com.aspose.words.Document;
import com.aspose.words.ReportingEngine;

public class GenerateReport {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("template.docx");
        Sender sender = new Sender("Aspose", "Hello");
        new ReportingEngine().buildReport(doc, sender, "sender");
        doc.save("report.docx");
    }

    public static class Sender {
        private final String name;
        private final String message;

        public Sender(String name, String message) {
            this.name = name;
            this.message = message;
        }

        public String getName() { return name; }
        public String getMessage() { return message; }
    }
}
```

Other helper types may come after the public class without `public`; data classes read by
`ReportingEngine` may not (J9).

### J2 — Explicit single-type imports; no ambiguous wildcards

Nothing outside `java.lang` is imported for you. Import each type you use. Aspose.Words declares
`com.aspose.words.List`, `com.aspose.words.Shape` and `com.aspose.words.Font`; the JDK also has
`java.util.List`, `java.awt.Shape` and `java.awt.Font`. With two wildcard imports the simple name is
ambiguous and the build fails even though each import is valid.

*Prevents `compiler.err.ref.ambiguous` and `compiler.err.cant.resolve.location`.*

```java
// WRONG — List is in both packages; ArrayList is fine, List is not
import com.aspose.words.*;
import java.util.*;

public class Names {
    public static void main(String[] args) throws Exception {
        List<String> names = new ArrayList<>();
        names.add("James");
        new Document().save("names.docx");
    }
}
```

```java
// RIGHT — import exactly what is used
import com.aspose.words.Document;
import java.util.ArrayList;
import java.util.List;

public class Names {
    public static void main(String[] args) throws Exception {
        List<String> names = new ArrayList<>();
        names.add("James");
        new Document().save("names.docx");
    }
}
```

Aspose.Words for Java keeps its public API in `com.aspose.words`: `Document`, `SaveFormat`,
`PdfSaveOptions`, `ReportingEngine` and `FindReplaceOptions` are all imported from there. Colours are
`java.awt.Color`. Do not invent .NET-style sub-packages such as `com.aspose.words.saving`.

### J3 — Each block stands alone

Blocks do not share state. A variable declared in your first block does not exist in your second.
If you show two examples, each repeats its own imports, class and setup.

*Prevents `compiler.err.cant.resolve.location` — "cannot find symbol: variable doc".*

```java
// WRONG — `doc` came from an earlier block or from prose
doc.getRange().replace("a", "b", new FindReplaceOptions());
```

```java
// RIGHT — everything this block needs, it declares
import com.aspose.words.Document;
import com.aspose.words.FindReplaceOptions;

public class ReplaceText {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("input.docx");
        doc.getRange().replace("a", "b", new FindReplaceOptions());
        doc.save("output.docx");
    }
}
```

### J4 — Declare checked exceptions

Aspose.Words for Java methods declare `throws Exception`. Every method that calls them must declare it
too, or catch it. A helper without `throws Exception` fails even when `main` declares it.

*Prevents `compiler.err.unreported.exception.need.to.catch.or.throw`.*

```java
// WRONG — the helper does not declare the checked exception
import com.aspose.words.Document;

public class Convert {
    public static void main(String[] args) throws Exception {
        toPdf("input.docx");
    }

    static void toPdf(String path) {
        new Document(path).save("output.pdf");
    }
}
```

```java
// RIGHT
import com.aspose.words.Document;

public class Convert {
    public static void main(String[] args) throws Exception {
        toPdf("input.docx");
    }

    static void toPdf(String path) throws Exception {
        new Document(path).save("output.pdf");
    }
}
```

### J5 — Do not reuse Aspose.Words type names

A class named `Document`, `Range` or `Watermark` collides with the imported Aspose.Words type or
silently shadows it. Name your class after the task.

*Prevents `compiler.err.already.defined.this.unit` and confusing `cant.apply.symbol` errors.*

```java
// WRONG — the class name collides with the imported type
import com.aspose.words.Document;

public class Document {
    public static void main(String[] args) throws Exception {
        new Document("input.docx").save("output.pdf");
    }
}
```

```java
// RIGHT
import com.aspose.words.Document;

public class ConvertToPdf {
    public static void main(String[] args) throws Exception {
        new Document("input.docx").save("output.pdf");
    }
}
```

### J6 — No warnings: nothing deprecated, nothing raw, Java 17 only

`-Werror` turns lint warnings into build failures. Deprecated and for-removal APIs (in the JDK and in
Aspose.Words), raw generic types and unchecked conversions all fail the build. The language level is
Java 17: no unnamed classes, no instance `main`, no pattern matching for `switch`. `var`, text blocks
and records are fine.

*Prevents `compiler.err.warnings.and.werror` with `compiler.warn.has.been.deprecated`, `compiler.warn.has.been.deprecated.for.removal`, `compiler.warn.raw.class.use` and `compiler.warn.unchecked.call.mbr.of.raw.type`.*

```java
// WRONG — raw List, and a constructor deprecated for removal
import java.util.ArrayList;
import java.util.List;

public class Values {
    public static void main(String[] args) throws Exception {
        List values = new ArrayList();
        values.add(new Integer(5));
        System.out.println(values);
    }
}
```

```java
// RIGHT
import java.util.ArrayList;
import java.util.List;

public class Values {
    public static void main(String[] args) throws Exception {
        List<Integer> values = new ArrayList<>();
        values.add(Integer.valueOf(5));
        System.out.println(values);
    }
}
```

If the evidence shows an Aspose.Words member as deprecated, use the replacement it names.

### J7 — Use only Aspose.Words and the JDK

The class path holds `aspose-words` and nothing else. Do not reach for helper libraries, JSON packages,
logging frameworks or test frameworks. API-reference examples call test-suite helpers
(`getMyDir()`, `getArtifactsDir()`, `Assert.assertEquals`); these do not exist outside the Aspose test
suite. Replace them with plain paths and ordinary checks.

*Prevents `compiler.err.doesnt.exist` (missing package) and `compiler.err.cant.resolve.location.args` (missing helper).*

```java
// WRONG — test-suite helpers copied from the API reference
import com.aspose.words.Document;

public class Save {
    public static void main(String[] args) throws Exception {
        Document doc = new Document(getMyDir() + "Document.docx");
        doc.save(getArtifactsDir() + "Document.pdf");
    }
}
```

```java
// RIGHT
import com.aspose.words.Document;

public class Save {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("Document.docx");
        doc.save("Document.pdf");
    }
}
```

### J8 — Preserve every citation when you revise

When you are asked to repair or revise an answer, return the **complete** answer, and reproduce **every**
documentation URL the original contained. Before presenting a repair, compare its citations with the original and restore any missing documentation URLs. Add a new URL only if it came from
`words-java` evidence retrieved in this same session.

*Preserves the evidence accompanying the corrected answer.*

### J9 — LINQ Reporting templates must also work at run time

A LINQ Reporting template is text inside the document. `javac` never sees it; `ReportingEngine.buildReport`
parses it when the program runs, so a template mistake compiles cleanly and then throws. Each failure below
was observed with Aspose.Words for Java 26.10.

- The data source and every object the template reaches through it must be of a **public** type. A
  package-private class, or a nested class without `public`, fails with
  `IllegalArgumentException: A data source object must be of a visible type`.
- Close blocks with `<</if>>` and `<</foreach>>`. `<<end>>` fails with `IllegalStateException: Token 'end' is unexpected`.
- Over Java objects, call the getters and use the lowercase extension methods. .NET-style member names
  (`data.Orders`, `x.Total`) and `Where` fail with `IllegalStateException: An error has been encountered at the end of expression`.
- JSON and XML data sources (`JsonDataSource`, `XmlDataSource`) use the field names exactly as they appear in the data.

WRONG — template and data class as .NET would write them:

```text
<<foreach [o in data.Orders.Where(x => x.Total > 100)]>>
<<[o.Name]>> — <<[o.Total]>>
<<end>>
```

```java
// WRONG — compiles, but ReportData and Order are not visible to the engine
import com.aspose.words.Document;
import com.aspose.words.ReportingEngine;
import java.util.List;

public class CreateReport {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("template.docx");
        new ReportingEngine().buildReport(doc, new ReportData(List.of(new Order("Notebook", 150))), "data");
        doc.save("report.docx");
    }
}

class ReportData {
    private final List<Order> orders;
    ReportData(List<Order> orders) { this.orders = orders; }
    public List<Order> getOrders() { return orders; }
}

class Order {
    private final String name;
    private final int total;
    Order(String name, int total) { this.name = name; this.total = total; }
    public String getName() { return name; }
    public int getTotal() { return total; }
}
```

RIGHT — getters, lowercase `where`, proper closing tag, public nested data classes:

```text
<<foreach [o in data.getOrders().where(x => x.getTotal() > 100)]>>
<<[o.getName()]>> — <<[o.getTotal()]>>
<</foreach>>
```

```java
// RIGHT
import com.aspose.words.Document;
import com.aspose.words.ReportingEngine;
import java.util.List;

public class CreateReport {
    public static void main(String[] args) throws Exception {
        Document doc = new Document("template.docx");
        new ReportingEngine().buildReport(doc, new ReportData(List.of(new Order("Notebook", 150))), "data");
        doc.save("report.docx");
    }

    public static class ReportData {
        private final List<Order> orders;
        public ReportData(List<Order> orders) { this.orders = orders; }
        public List<Order> getOrders() { return orders; }
    }

    public static class Order {
        private final String name;
        private final int total;
        public Order(String name, int total) { this.name = name; this.total = total; }
        public String getName() { return name; }
        public int getTotal() { return total; }
    }
}
```

## Before you answer

First: if the question asked how to do something and your answer contains no `java` block, that is a
failed answer — add the example (J0).

Then re-read each `java` block once, as if it were the only file in an empty project:

1. Is there exactly one `public class`, with `public static void main(String[] args) throws Exception`, and no `package`?
2. Is every type it uses imported explicitly at the top of that same block, with no ambiguous wildcards?
3. Is every identifier it uses declared in that same block?
4. Does every method that calls Aspose.Words declare `throws Exception`?
5. Do its own class names avoid Aspose.Words type names?
6. Is everything free of deprecated APIs, raw types and post-Java-17 syntax?
7. If it uses `ReportingEngine`: are the data classes public, and does the template follow J9?

If any answer is no, fix the block before you send it. A compiler error is a failed answer even when the
Aspose.Words API usage is perfectly correct.
